import numpy as np
import pandas as pd

from agrorisk import sinteticos
from agrorisk.motor import fatores as ft


def test_reprodutivel_com_semente():
    a, b = sinteticos.gerar(semente=7), sinteticos.gerar(semente=7)
    for k in a:
        pd.testing.assert_frame_equal(a[k], b[k])
    c = sinteticos.gerar(semente=8)
    assert not a["indicadores"].equals(c["indicadores"])


def test_formato_car_e_sem_dados_pessoais():
    d = sinteticos.gerar()
    assert d["imoveis"]["car_codigo"].str.fullmatch(r"MG-31\d{5}-[0-9a-f]{32}").all()
    assert d["imoveis"]["car_codigo"].str[11:19].eq("00000000").all() and d["imoveis"]["car_ficticio"].all()
    assert len(d["imoveis"]) == 300 and d["imoveis"]["car_codigo"].is_unique
    assert not {"cpf", "cnpj", "nome"} & {c.lower() for t in d.values() for c in t.columns}


def test_cobertura_do_painel_e_taxa_base():
    d = sinteticos.gerar()
    assert set(d["unidades"]["tipo_unidade"]) == {"car", "gleba"}  # frente B (fornecedor) não tem dado
    assert set(d["unidades"]["nivel_espacial"]) == {"poligono", "imovel_inteiro"}
    assert set(d["eventos"]["data_corte"]) == set(sinteticos.DATAS_CORTE)
    assert all(c.endswith("-07-31") for c in sinteticos.DATAS_CORTE)
    for nivel, taxa in sinteticos.TAXAS_BASE.items():
        assert abs(d["eventos"].query("nivel_espacial == @nivel")["p_verdade"].mean() - taxa) < 0.002


def test_imoveis_dentro_dos_municipios():
    d = sinteticos.gerar()
    def bbox(w):
        xy = np.array([[float(v) for v in p.split()] for p in w[len("POLYGON(("):-2].split(",")])
        return xy[:, 0].min(), xy[:, 1].min(), xy[:, 0].max(), xy[:, 1].max()
    mun = {r.cod_ibge: bbox(r.geometria_wkt) for r in d["municipios"].itertuples()}
    for r in d["imoveis"].itertuples():
        x0, y0, x1, y1 = bbox(r.geometria_wkt)
        m = mun[r.municipio_ibge]
        assert m[0] - 1e-5 <= x0 and x1 <= m[2] + 1e-5 and m[1] - 1e-5 <= y0 and y1 <= m[3] + 1e-5, r.imovel_id


def _logit_fit(X, y, it=30):
    X = np.column_stack([np.ones(len(X)), X])
    b = np.zeros(X.shape[1])
    for _ in range(it):
        p = 1 / (1 + np.exp(-X @ b))
        W = p * (1 - p)
        b += np.linalg.solve(X.T @ (X * W[:, None]) + 1e-6 * np.eye(len(b)), X.T @ (y - p))
    return b


def test_modelo_conhecido_e_recuperavel():
    d = sinteticos.gerar(n_imoveis=3000)
    df = d["indicadores"].merge(d["eventos"], on=["unidade_id", "data_corte"])
    X = np.column_stack([ft.padronizar(f, df[f.coluna].to_numpy()) for f in ft.FATORES])
    b = _logit_fit(X, df["y"].to_numpy(float))[1:]
    verdade = np.array([sinteticos.COEF_VERDADE[f.nome] for f in ft.FATORES])
    assert (np.sign(b) == np.sign(verdade)).all()
    assert abs(b[0] - verdade[0]) < 0.25  # fator mais forte, bem estimado


def test_camadas_v1_presentes():
    d = sinteticos.gerar()
    u, o, v = d["unidades"], d["operacoes"], d["verificacoes"]
    assert {"porte_modulos_fiscais", "car_codigo", "nivel_espacial"} <= set(u.columns) and u["porte_modulos_fiscais"].ge(0).all()
    assert {"programa", "data_contrato", "data_vencimento", "proagro_acionado"} <= set(o.columns)
    assert set(v["status_juridico"]) == {"detectado", "autorizado", "sem_autorizacao_identificada", "indeterminado"}
    assert (pd.to_datetime(v["data_publicacao"]) <= pd.to_datetime(v["data_corte"])).all()
    assert v["hash_fonte"].str.fullmatch(r"[0-9a-f]{64}").all()
    r = d["rotulos_piloto"]
    assert (pd.to_datetime(r["data_registro"]) >= pd.to_datetime(r["data_corte"])).all()
