import json
from pathlib import Path

import jsonschema
import numpy as np
import pandas as pd
import pytest

from agrorisk.motor import (ErroEntrada, ErroVazamentoTemporal, calcular_faixa, calcular_score, hash_snapshot,
                            pontuar, porte_classe, saldo_na_data, validar_rotulos_piloto)
from agrorisk.motor.__main__ import main

RAIZ = Path(__file__).resolve().parents[1]
FIX = RAIZ / "tests" / "fixtures" / "sinteticos"
SCH = RAIZ / "docs/produto/schemas"
CORTE = "2023-07-31"


def _schema(nome):
    return json.loads((SCH / f"{nome}.schema.json").read_text())


def _csv(nome):
    return pd.read_csv(FIX / f"{nome}.csv", dtype={"unidade_id": str, "operacao_id": str, "municipio_ibge": str})


@pytest.fixture(scope="module")
def dados():
    return {n: _csv(n) for n in ("indicadores", "unidades", "operacoes", "verificacoes", "rotulos_piloto")}


@pytest.fixture(scope="module")
def saida(dados):
    return pontuar(dados["indicadores"], dados["unidades"], CORTE, verificacoes=dados["verificacoes"],
                   operacoes=dados["operacoes"])


def _pontuar(dados, **kw):
    return pontuar(dados["indicadores"], dados["unidades"], kw.pop("corte", CORTE),
                   verificacoes=kw.pop("verificacoes", dados["verificacoes"]),
                   operacoes=kw.pop("operacoes", dados["operacoes"]), **kw)


def test_resultados_coerentes(saida, dados):
    res = saida.resultados
    assert len(res) == len(dados["unidades"]) and res["unidade_id"].is_unique
    assert res["p"].between(0, 1).all() and res["score"].between(0, 1000).all()
    assert (res["score"] == np.floor(1000 * (1 - res["p"]) + 0.5)).all()
    assert (res["y_definicao"] == "Y_total").all() and (res["horizonte_meses"] == 12).all()
    assert (res["data_corte"].astype(str) == CORTE).all()
    assert (res["faixa"] == calcular_faixa(res["p"], res["taxa_base"])).all()
    for nivel, taxa in (("poligono", 0.02), ("imovel_inteiro", 0.04)):  # calibrado por nível
        r = res[res["nivel_espacial"] == nivel]
        assert len(r) > 0 and abs(r["p"].mean() - taxa) < 1e-4 and (r["taxa_base"] == taxa).all()
        o = r.sort_values("p")["faixa"].tolist()
        assert o == sorted(o)  # monotonia: maior p => faixa não melhor


def test_faixas_limites():
    p = np.array([0.01, 0.0100001, 0.02, 0.04, 0.0400001, 0.08, 0.0800001])
    assert list(calcular_faixa(p, 0.02)) == ["A", "B", "B", "C", "D", "D", "E"]
    assert list(calcular_faixa(p, np.full(7, 0.02))) == ["A", "B", "B", "C", "D", "D", "E"]
    assert list(calcular_faixa([0.04, 0.04], [0.02, 0.04])) == ["C", "B"]  # mesmo p, taxa-base do nível diferente
    assert list(calcular_score([0, 1, 0.0004, 0.0005])) == [1000, 0, 1000, 1000]
    assert list(porte_classe([0, 4, 4.01, 15, 15.01])) == ["ate_4_mf", "ate_4_mf", "4_a_15_mf", "4_a_15_mf", "acima_15_mf"]


def test_resultados_seguem_schema(saida):
    sch = _schema("resultado")
    res = saida.resultados.copy()
    res["data_corte"] = res["data_corte"].astype(str)
    for rec in json.loads(res.to_json(orient="records")):
        rec["calculado_em"] = rec["calculado_em"]
        jsonschema.validate(rec, sch, format_checker=jsonschema.FormatChecker())


def test_detalhes_seguem_schema(saida):
    sch = _schema("detalhes")
    campos = list(sch["items"]["required"])
    det = saida.detalhes
    for uid, g in list(det.groupby("unidade_id"))[:60]:
        itens = json.loads(g.sort_values("ordem")[campos].astype({"data_referencia": str, "data_publicacao": str}).to_json(orient="records"))
        jsonschema.validate(itens, sch, format_checker=jsonschema.FormatChecker())
        c = [abs(i["contribuicao"]) for i in itens]
        assert c == sorted(c, reverse=True)
    assert det["status_juridico"].isna().all()  # fatores de risco do stub não descrevem supressão


def test_verificacoes_seguem_schema(saida):
    sch = _schema("verificacoes")
    campos = list(sch["items"]["required"])
    v = saida.verificacoes
    assert len(v) > 0
    itens = json.loads(v[campos].astype({"data_corte": str, "data_referencia": str, "data_publicacao": str}).to_json(orient="records"))
    jsonschema.validate(itens, sch, format_checker=jsonschema.FormatChecker())
    assert set(v["status_juridico"]) <= {"detectado", "autorizado", "sem_autorizacao_identificada", "indeterminado"}


def test_sem_vazamento_temporal(saida):
    corte = pd.Timestamp(CORTE).date()
    assert (pd.to_datetime(saida.detalhes["data_publicacao"]).dt.date <= corte).all()
    assert (pd.to_datetime(saida.detalhes["data_referencia"]) <= pd.to_datetime(saida.detalhes["data_publicacao"])).all()
    assert (pd.to_datetime(saida.verificacoes["data_publicacao"]).dt.date <= corte).all()


def test_verificacao_publicada_depois_do_corte_falha(dados):
    v = dados["verificacoes"].copy()
    v.loc[v["data_corte"] == CORTE, "data_publicacao"] = "2023-08-15"
    with pytest.raises(ErroVazamentoTemporal):
        _pontuar(dados, verificacoes=v)


def test_vedacao_nao_e_feature_de_p(dados, saida):
    """p e faixa são idênticos com e sem a camada determinística."""
    sem = _pontuar(dados, verificacoes=None, operacoes=None)
    pd.testing.assert_series_equal(saida.resultados["p"], sem.resultados["p"])
    pd.testing.assert_frame_equal(saida.detalhes, sem.detalhes)


def test_sem_verificacoes_nao_vira_sem_vedacao(dados):
    res = _pontuar(dados, verificacoes=None).resultados
    assert not res["verificacoes_avaliadas"].any()
    assert res["bloqueio_provavel"].isna().all() and res["n_vedacoes"].isna().all() and res["exposicao_bloqueavel"].isna().all()


def test_bloqueio_e_exposicao_bloqueavel(dados):
    uni = dados["unidades"].head(4).copy()
    ind = dados["indicadores"][dados["indicadores"]["unidade_id"].isin(uni["unidade_id"])]
    u0, u1, u2, u3 = uni["unidade_id"]
    hx = "a" * 64

    def v(uid, status, efeito="bloqueia", regra="supressao_x_autorizacao"):
        return {"unidade_id": uid, "data_corte": CORTE, "regra": regra, "efeito": efeito, "status_juridico": status,
                "fonte": "F", "data_referencia": "2023-03-01", "data_publicacao": "2023-06-01", "hash_fonte": hx, "texto": "t"}
    ver = pd.DataFrame([v(u0, "sem_autorizacao_identificada"), v(u1, "autorizado"), v(u2, "indeterminado"),
                        v(u3, "detectado", efeito="alerta", regra="sobreposicao_uc")])
    ops = dados["operacoes"][dados["operacoes"]["unidade_id"].isin(uni["unidade_id"])].copy()
    ops["data_contrato"], ops["data_vencimento"] = "2023-01-01", "2024-01-01"
    ops = ops.drop_duplicates("unidade_id")
    ops["valor_rs"] = 100.0
    res = pontuar(ind, uni, CORTE, verificacoes=ver, operacoes=ops, peso_indeterminado=0.5).resultados.set_index("unidade_id")
    assert list(res.loc[[u0, u1, u2, u3], "bloqueio_provavel"]) == [1.0, 0.0, 0.5, 0.0]
    assert list(res.loc[[u0, u1, u2, u3], "exposicao_bloqueavel"]) == [100.0, 0.0, 50.0, 0.0]
    assert list(res.loc[[u0, u1, u2, u3], "n_vedacoes"]) == [1, 0, 0, 0]
    assert list(res.loc[[u0, u1, u2, u3], "n_vedacoes_indeterminadas"]) == [0, 0, 1, 0]
    assert "exposicao_esperada" not in res.columns  # só depois de desfecho validado no piloto


def test_saldo_usa_vigencia_e_saldo_rs():
    ops = pd.DataFrame({"operacao_id": ["a", "b", "c"], "unidade_id": ["u", "u", "u"], "valor_rs": [100., 200., 400.],
                        "data_contrato": ["2023-01-01", "2023-07-31", "2023-08-01"],
                        "data_vencimento": ["2023-07-31", "2024-01-01", "2024-01-01"]})
    s = saldo_na_data(ops, CORTE)  # a venceu no corte (fim exclusivo); c começa depois
    assert s.loc[0, "saldo_exposto"] == 200 and s.loc[0, "n_operacoes"] == 1
    ops["saldo_rs"] = [np.nan, 150., np.nan]
    assert saldo_na_data(ops, CORTE).loc[0, "saldo_exposto"] == 150


def test_auditoria(saida, dados):
    res = saida.resultados
    assert res["hash_snapshot"].str.fullmatch(r"[0-9a-f]{64}").all() and res["hash_snapshot"].nunique() == 1
    assert (saida.verificacoes["hash_snapshot"] == res["hash_snapshot"].iloc[0]).all()
    vd = json.loads(res["versoes_dados"].iloc[0])
    assert all({"data_referencia", "data_publicacao"} <= set(x) for x in vd.values())
    assert any("hashes" in x for x in vd.values())
    assert res["versao_modelo"].str.contains(r"-stub\+").all()
    # entrada diferente => hash diferente
    ind = dados["indicadores"].copy()
    base = pontuar(ind, dados["unidades"], CORTE).resultados["hash_snapshot"].iloc[0]
    ind.loc[ind.index[ind["data_corte"] == "2020-07-31"][0], "chuva_anual_mm"] += 1  # outro corte: hash igual
    assert pontuar(ind, dados["unidades"], CORTE).resultados["hash_snapshot"].iloc[0] == base
    ind.loc[ind.index[ind["data_corte"] == CORTE][0], "chuva_anual_mm"] += 1  # mesmo corte: hash muda
    assert pontuar(ind, dados["unidades"], CORTE).resultados["hash_snapshot"].iloc[0] != base


def test_hash_snapshot_independe_da_ordem():
    a = pd.DataFrame({"x": [1, 2], "y": ["a", "b"]})
    assert hash_snapshot(t=a) == hash_snapshot(t=a.iloc[::-1][["y", "x"]])
    assert hash_snapshot(t=a) != hash_snapshot(t=None)


def test_determinismo(dados, saida):
    out2 = _pontuar(dados)
    pd.testing.assert_series_equal(saida.resultados["p"], out2.resultados["p"])
    pd.testing.assert_frame_equal(saida.detalhes, out2.detalhes)
    assert saida.resultados["hash_snapshot"].iloc[0] == out2.resultados["hash_snapshot"].iloc[0]


def test_aviso_imovel_inteiro(saida):
    res = saida.resultados
    assert res.loc[res["nivel_espacial"] == "imovel_inteiro", "aviso"].str.contains("Evento no imóvel").all()
    assert res.loc[res["nivel_espacial"] == "poligono", "aviso"].isna().all()


def test_entrada_invalida(dados):
    ind, uni = dados["indicadores"], dados["unidades"]
    with pytest.raises(ErroEntrada):
        pontuar(ind.drop(columns="chuva_anual_mm"), uni, CORTE)
    with pytest.raises(ErroEntrada):
        pontuar(ind, uni, "1999-07-31")  # sem indicadores nessa data
    with pytest.raises(ErroEntrada):
        pontuar(ind, uni, "2023-01-01")  # data_corte não é 31/jul
    with pytest.raises(ErroEntrada):
        pontuar(ind, uni, CORTE, y_definicao="Y_ilegal")
    with pytest.raises(ErroEntrada):
        pontuar(ind, uni, CORTE, horizonte_meses=24)
    with pytest.raises(ErroEntrada):
        pontuar(ind, uni.drop(columns="nivel_espacial"), CORTE)  # nivel_espacial é obrigatório
    with pytest.raises(ErroEntrada):
        pontuar(ind, uni.assign(nivel_espacial="gleba"), CORTE)  # valor antigo do v0
    with pytest.raises(ErroEntrada):
        pontuar(ind, uni.assign(porte_modulos_fiscais=np.nan), CORTE)
    with pytest.raises(ErroEntrada):
        pontuar(ind, uni.assign(car_codigo=None), CORTE)


def test_sem_dados_pessoais(dados):
    for col in ("cpf", "nome", "CNPJ"):
        with pytest.raises(ErroEntrada, match="LGPD"):
            pontuar(dados["indicadores"], dados["unidades"].assign(**{col: "x"}), CORTE)
    with pytest.raises(ErroEntrada, match="LGPD"):
        _pontuar(dados, operacoes=dados["operacoes"].assign(cpf="x"))
    for t in ("unidades", "operacoes", "verificacoes", "indicadores", "rotulos_piloto"):
        assert not {"cpf", "cnpj", "nome"} & {c.lower() for c in dados[t].columns}


def test_operacoes_invalidas(dados):
    ops = dados["operacoes"]
    with pytest.raises(ErroEntrada):
        _pontuar(dados, operacoes=ops.drop(columns="programa"))
    with pytest.raises(ErroEntrada):
        _pontuar(dados, operacoes=ops.assign(car_codigo="MG-3106200-" + "0" * 32))
    assert {"programa", "data_contrato", "proagro_acionado"} <= set(ops.columns)


def test_proagro_e_opcional_e_nao_afeta(dados, saida):
    sem = _pontuar(dados, operacoes=dados["operacoes"].drop(columns="proagro_acionado"))
    pd.testing.assert_series_equal(saida.resultados["p"], sem.resultados["p"])
    pd.testing.assert_series_equal(saida.resultados["saldo_exposto"], sem.resultados["saldo_exposto"])


def test_rotulos_piloto(dados):
    validar_rotulos_piloto(dados["rotulos_piloto"])
    r = dados["rotulos_piloto"]
    with pytest.raises(ErroEntrada):  # registro antes do evento
        validar_rotulos_piloto(r.assign(data_registro="2000-01-01").query("y3_atraso_90d == 1"))
    with pytest.raises(ErroEntrada):
        validar_rotulos_piloto(r.drop(columns="data_registro"))


def _cli(entrada, saida, *extra):
    return main(["--entrada", str(entrada), "--saida", str(saida), "--data-corte", CORTE, *extra])


def test_cli_idempotente_arquivos(tmp_path):
    assert _cli(FIX, tmp_path) == 0
    tab = ("resultados", "resultados_detalhes", "resultados_verificacoes")
    n = [len(pd.read_parquet(tmp_path / f"{t}.parquet")) for t in tab]
    assert n[0] == len(_csv("unidades")) and n[1] == 6 * n[0] and n[2] > 0
    assert _cli(FIX, tmp_path) == 0
    assert [len(pd.read_parquet(tmp_path / f"{t}.parquet")) for t in tab] == n


def test_cli_idempotente_banco(tmp_path):
    url = f"sqlite:///{tmp_path / 'm.db'}"
    for _ in range(2):
        assert _cli(FIX, url) == 0
    from sqlalchemy import create_engine, text
    with create_engine(url).connect() as con:
        n = con.execute(text("select count(*) from motor_resultados")).scalar()
        d = con.execute(text("select count(*) from motor_resultados_detalhes")).scalar()
        v = con.execute(text("select count(*) from motor_resultados_verificacoes")).scalar()
    assert n == len(_csv("unidades")) and d == 6 * n and v > 0


def test_cli_entrada_banco(tmp_path, monkeypatch):
    from sqlalchemy import create_engine
    url = f"sqlite:///{tmp_path / 'e.db'}"
    eng = create_engine(url)
    for tab, arq in (("motor_indicadores", "indicadores"), ("motor_unidades", "unidades")):
        pd.read_csv(FIX / f"{arq}.csv").to_sql(tab, eng, index=False)
    monkeypatch.setenv("AGRORISK_DB_URL", url)
    assert main(["--entrada", "db", "--saida", str(tmp_path / "o"), "--data-corte", CORTE]) == 0
    res = pd.read_parquet(tmp_path / "o" / "resultados.parquet")
    assert not res["verificacoes_avaliadas"].any()  # sem tabela de verificações: não avaliado


def test_codigos_de_saida(tmp_path, monkeypatch):
    assert _cli(tmp_path / "vazio", tmp_path / "o") == 2
    assert _cli(FIX, tmp_path / "o", "--y-definicao", "Y_agro") == 2
    assert _cli(FIX, tmp_path / "o", "--taxas-base", "lixo") == 2
    monkeypatch.delenv("AGRORISK_DB_URL", raising=False)
    assert main(["--entrada", "db", "--saida", str(tmp_path)]) == 3
