import json
from pathlib import Path

import jsonschema
import numpy as np
import pandas as pd
import pytest

from agrorisk import sinteticos
from agrorisk.motor import ErroEntrada, calcular_faixa, calcular_score, pontuar
from agrorisk.motor.__main__ import main

RAIZ = Path(__file__).resolve().parents[1]
FIX = RAIZ / "tests" / "fixtures" / "sinteticos"
SCHEMA = json.loads((RAIZ / "docs/produto/schemas/detalhes.schema.json").read_text())


@pytest.fixture(scope="module")
def dados():
    return {n: pd.read_csv(FIX / f"{n}.csv", dtype={"unidade_id": str}) for n in ("indicadores", "unidades", "operacoes")}


@pytest.fixture(scope="module")
def saida(dados):
    return pontuar(dados["indicadores"], dados["unidades"], "2023-01-01")


def test_resultados_coerentes(saida, dados):
    res, _ = saida
    assert len(res) == len(dados["unidades"]) and res["unidade_id"].is_unique
    assert res["p"].between(0, 1).all() and res["score"].between(0, 1000).all()
    assert (res["score"] == np.floor(1000 * (1 - res["p"]) + 0.5)).all()
    assert (res["faixa"] == calcular_faixa(res["p"], res["taxa_base"].iloc[0])).all()
    assert abs(res["p"].mean() - 0.02) < 1e-4
    # monotonia: maior p => faixa não melhor
    ordem = res.sort_values("p")["faixa"].tolist()
    assert ordem == sorted(ordem)


def test_faixas_limites():
    p = np.array([0.01, 0.0100001, 0.02, 0.04, 0.0400001, 0.08, 0.0800001])
    assert list(calcular_faixa(p, 0.02)) == ["A", "B", "B", "C", "D", "D", "E"]
    assert list(calcular_score([0, 1, 0.0004, 0.0005])) == [1000, 0, 1000, 1000]


def test_detalhes_seguem_schema(saida):
    _, det = saida
    campos = list(SCHEMA["items"]["required"])
    for uid, g in list(det.groupby("unidade_id"))[:60]:
        itens = json.loads(g.sort_values("ordem")[campos].astype({"data_referencia": str, "data_publicacao": str}).to_json(orient="records"))
        jsonschema.validate(itens, SCHEMA, format_checker=jsonschema.FormatChecker())
        c = [abs(i["contribuicao"]) for i in itens]
        assert c == sorted(c, reverse=True)


def test_sem_vazamento_temporal(saida):
    res, det = saida
    corte = pd.Timestamp("2023-01-01").date()
    assert (pd.to_datetime(det["data_publicacao"]).dt.date <= corte).all()
    assert (pd.to_datetime(det["data_referencia"]) <= pd.to_datetime(det["data_publicacao"])).all()


def test_determinismo(dados, saida):
    res2, det2 = pontuar(dados["indicadores"], dados["unidades"], "2023-01-01")
    pd.testing.assert_series_equal(saida[0]["p"], res2["p"])
    pd.testing.assert_frame_equal(saida[1], det2)


def test_aviso_imovel_inteiro(saida):
    res, _ = saida
    assert res.loc[res["nivel_espacial"] == "imovel_inteiro", "aviso"].notna().all()
    assert res.loc[res["nivel_espacial"] == "gleba", "aviso"].isna().all()


def test_entrada_invalida(dados):
    with pytest.raises(ErroEntrada):
        pontuar(dados["indicadores"].drop(columns="chuva_anual_mm"), dados["unidades"], "2023-01-01")
    with pytest.raises(ErroEntrada):
        pontuar(dados["indicadores"], dados["unidades"], "1999-01-01")


def _cli(entrada, saida, *extra):
    return main(["--entrada", str(entrada), "--saida", str(saida), "--data-corte", "2023-01-01", *extra])


def test_cli_idempotente_arquivos(tmp_path):
    assert _cli(FIX, tmp_path) == 0
    n = len(pd.read_parquet(tmp_path / "resultados.parquet"))
    nd = len(pd.read_parquet(tmp_path / "resultados_detalhes.parquet"))
    assert _cli(FIX, tmp_path) == 0
    assert len(pd.read_parquet(tmp_path / "resultados.parquet")) == n
    assert len(pd.read_parquet(tmp_path / "resultados_detalhes.parquet")) == nd


def test_cli_idempotente_banco(tmp_path):
    url = f"sqlite:///{tmp_path / 'm.db'}"
    for _ in range(2):
        assert _cli(FIX, url) == 0
    from sqlalchemy import create_engine, text
    with create_engine(url).connect() as con:
        n = con.execute(text("select count(*) from motor_resultados")).scalar()
        d = con.execute(text("select count(*) from motor_resultados_detalhes")).scalar()
    assert n == len(pd.read_csv(FIX / "unidades.csv")) and d == 6 * n


def test_cli_entrada_banco(tmp_path, monkeypatch):
    from sqlalchemy import create_engine
    url = f"sqlite:///{tmp_path / 'e.db'}"
    eng = create_engine(url)
    for tab, arq in (("motor_indicadores", "indicadores"), ("motor_unidades", "unidades")):
        pd.read_csv(FIX / f"{arq}.csv").to_sql(tab, eng, index=False)
    monkeypatch.setenv("AGRORISK_DB_URL", url)
    assert main(["--entrada", "db", "--saida", str(tmp_path / "o"), "--data-corte", "2023-01-01"]) == 0


def test_codigos_de_saida(tmp_path, monkeypatch):
    assert _cli(tmp_path / "vazio", tmp_path / "o") == 2
    monkeypatch.delenv("AGRORISK_DB_URL", raising=False)
    assert main(["--entrada", "db", "--saida", str(tmp_path)]) == 3
