"""Gerador de dados sintéticos do contrato v1 (frente A-reformulada: crédito rural pós-concessão). Reprodutível por semente.

TUDO AQUI É FICTÍCIO: nenhum dado real de pessoa, CPF ou nome. Códigos de CAR seguem o formato real
(`MG-<IBGE7>-<32 hex>`), mas os 8 primeiros hex são `00000000` (marca de fictício; coluna `car_ficticio`).
Geometrias: cada município vira uma caixa de lado √área numa grade FICTÍCIA (não é a posição real); imóveis
são caixas dentro da caixa do município. Servem só para testar o pipeline, não para análise espacial.

Eventos: y ~ Bernoulli(p), p = sigmoid(INTERCEPTO + Σ COEF_VERDADE[f]·z_f), com z padronizado como em
`agrorisk.motor.fatores`. O intercepto é calibrado (bisseção) por `nivel_espacial` para a taxa-base do nível
(TAXAS_BASE). Os coeficientes abaixo são a "verdade" que um backtest/modelo deve recuperar.
Cortes sempre em 31/jul (ciclo PRODES ago–jul). Frente B (fornecedor) não tem dado: é só discovery.
Verificações (vedação) são sorteadas independentemente de p: o sintético não afirma relação entre vedação e risco.
"""
from __future__ import annotations

import hashlib

import numpy as np
import pandas as pd

from .motor import fatores as ft

SEMENTE = 20261029
TAXAS_BASE = {"poligono": 0.02, "imovel_inteiro": 0.04}  # fictícias; imóvel inteiro tem taxa maior (cresce com a área)
DATAS_CORTE = ("2020-07-31", "2021-07-31", "2022-07-31", "2023-07-31")  # ciclos PRODES 2021–2024
HORIZONTE_MESES = 12
Y_DEFINICAO = "Y_total"

# Verdade do gerador (log-odds por desvio-padrão). Sinais iguais aos do stub, magnitudes diferentes.
COEF_VERDADE = {
    "supressao_vizinhanca": 1.1,
    "vegetacao_nativa": 0.6,
    "distancia_urbano": -0.5,
    "distancia_mineracao": -0.25,
    "sobreposicao_uc": -0.8,
    "chuva_anual": -0.2,
}

# (cod_ibge, municipio, grupo, area_km2) — docs/pesquisa/01-diagnostico-territorial.md, Tabela 1
MUNICIPIOS = (
("3105400", "Barão de Cocais", "Colar", 340.1),
("3106408", "Belo Vale", "Colar", 365.9),
("3107703", "Bom Jesus do Amparo", "Colar", 195.6),
("3108107", "Bonfim", "Colar", 301.9),
("3126406", "Fortuna de Minas", "Colar", 198.7),
("3127206", "Funilândia", "Colar", 199.8),
("3131000", "Inhaúma", "Colar", 245.0),
("3131901", "Itabirito", "Colar", 544.0),
("3133808", "Itaúna", "Colar", 495.8),
("3142304", "Moeda", "Colar", 155.1),
("3147105", "Pará de Minas", "Colar", 551.2),
("3153608", "Prudente de Morais", "Colar", 124.2),
("3157203", "Santa Bárbara", "Colar", 684.5),
("3167202", "Sete Lagoas", "Colar", 536.9),
("3161908", "São Gonçalo do Rio Abaixo", "Colar", 363.8),
("3163102", "São José da Varginha", "Colar", 205.5),
("3105004", "Baldim", "RMBH", 556.3),
("3106200", "Belo Horizonte", "RMBH", 331.4),
("3106705", "Betim", "RMBH", 344.1),
("3109006", "Brumadinho", "RMBH", 639.4),
("3110004", "Caeté", "RMBH", 542.5),
("3112505", "Capim Branco", "RMBH", 95.3),
("3117876", "Confins", "RMBH", 42.4),
("3118601", "Contagem", "RMBH", 194.7),
("3124104", "Esmeraldas", "RMBH", 909.7),
("3126000", "Florestal", "RMBH", 194.2),
("3129806", "Ibirité", "RMBH", 72.4),
("3130101", "Igarapé", "RMBH", 110.9),
("3132206", "Itaguara", "RMBH", 410.5),
("3133709", "Itatiaiuçu", "RMBH", 295.1),
("3134608", "Jaboticatubas", "RMBH", 1115.0),
("3136652", "Juatuba", "RMBH", 97.0),
("3137601", "Lagoa Santa", "RMBH", 229.4),
("3140704", "Mateus Leme", "RMBH", 301.4),
("3141108", "Matozinhos", "RMBH", 252.5),
("3140159", "Mário Campos", "RMBH", 35.2),
("3144805", "Nova Lima", "RMBH", 429.3),
("3136603", "Nova União", "RMBH", 172.1),
("3149309", "Pedro Leopoldo", "RMBH", 292.8),
("3153905", "Raposos", "RMBH", 72.2),
("3154606", "Ribeirão das Neves", "RMBH", 155.1),
("3154804", "Rio Acima", "RMBH", 228.4),
("3155306", "Rio Manso", "RMBH", 231.5),
("3156700", "Sabará", "RMBH", 302.5),
("3157807", "Santa Luzia", "RMBH", 235.2),
("3165537", "Sarzedo", "RMBH", 62.1),
("3162922", "São Joaquim de Bicas", "RMBH", 71.8),
("3162955", "São José da Lapa", "RMBH", 47.9),
("3168309", "Taquaraçu de Minas", "RMBH", 329.3),
("3171204", "Vespasiano", "RMBH", 71.0),
)

CULTURAS = ("soja", "milho", "cafe", "hortalicas", "pecuaria_corte", "leite", "eucalipto")
SAFRAS = ("2019/20", "2020/21", "2021/22", "2022/23")
PROGRAMAS = ("pronaf", "pronamp", "demais_programas")
FONTES_VERIFICACAO = {  # regra -> (fonte fictícia, efeito)
    "supressao_x_autorizacao": ("Supressão detectada × autorização IEF/FEAM (sintético)", "bloqueia"),
    "embargo": ("Embargos IBAMA/estadual (sintético)", "bloqueia"),
    "sobreposicao_uc": ("CNUC/IDE-Sisema (sintético)", "alerta"),
}


def _sigmoid(x):
    return 1 / (1 + np.exp(-x))


def _hex(rng, n):
    return "".join(rng.choice(list("0123456789abcdef"), n))


def _caixa_wkt(x0, y0, x1, y1):
    return f"POLYGON(({x0:.5f} {y0:.5f},{x1:.5f} {y0:.5f},{x1:.5f} {y1:.5f},{x0:.5f} {y1:.5f},{x0:.5f} {y0:.5f}))"


def _municipios_caixas():
    """Grade fictícia de caixas (graus ≈ km/111) em EPSG:4674."""
    caixas, x, y, alt_linha = {}, -44.6, -20.6, 0.0
    for cod, _, _, area in MUNICIPIOS:
        lado = np.sqrt(area) / 111.0
        if x + lado > -43.0:
            x, y, alt_linha = -44.6, y + alt_linha + 0.01, 0.0
        caixas[cod] = (x, y, x + lado, y + lado)
        x += lado + 0.01
        alt_linha = max(alt_linha, lado)
    return caixas


def gerar(semente: int = SEMENTE, n_imoveis: int = 300) -> dict[str, pd.DataFrame]:
    """Retorna dict de DataFrames: municipios, imoveis, unidades, operacoes, indicadores, verificacoes, rotulos_piloto, eventos."""
    rng = np.random.default_rng(semente)
    caixas = _municipios_caixas()
    mun = pd.DataFrame(MUNICIPIOS, columns=["cod_ibge", "municipio", "grupo", "area_km2"])
    mun["geometria_wkt"] = [_caixa_wkt(*caixas[c]) for c in mun["cod_ibge"]]
    mun["pressao"] = rng.normal(0, 1, len(mun))  # latente: correlaciona supressão na vizinhança
    mun["modulo_fiscal_ha"] = np.round(rng.uniform(8, 40, len(mun)), 1)  # FICTÍCIO (não é o módulo fiscal real)

    # --- imóveis ---
    peso = mun["area_km2"].to_numpy() ** 0.5
    idx = rng.choice(len(mun), size=n_imoveis, p=peso / peso.sum())
    imoveis, glebas = [], []
    for i, m in enumerate(idx):
        cod, area_km2 = mun.at[m, "cod_ibge"], mun.at[m, "area_km2"]
        area_ha = float(np.clip(rng.lognormal(np.log(40), 0.9), 5, min(800, area_km2 * 100 * 0.2)))
        lado = np.sqrt(area_ha) / 100.0 / 111.0  # graus
        x0, y0, x1, y1 = caixas[cod]
        cx = rng.uniform(x0 + lado, max(x0 + lado, x1 - 2 * lado) + 1e-9)
        cy = rng.uniform(y0, max(y0, y1 - lado) + 1e-9)
        car = f"MG-{cod}-00000000{_hex(rng, 24)}"
        imoveis.append({"imovel_id": f"IMV{i:04d}", "car_codigo": car, "car_ficticio": True, "municipio_ibge": cod,
                        "area_ha": round(area_ha, 2), "geometria_wkt": _caixa_wkt(cx, cy, cx + lado, cy + lado),
                        "mun_idx": m})
        mf = round(area_ha / mun.at[m, "modulo_fiscal_ha"], 3)
        imoveis[-1]["porte_modulos_fiscais"] = mf
        inteiro = rng.random() < 0.25
        k = 1 if inteiro else int(rng.integers(1, 4))
        for g in range(k):
            gx0, gx1 = cx + lado * g / k, cx + lado * (g + 1) / k
            glebas.append({"unidade_id": f"CAR{i:04d}" if inteiro else f"GLB{i:04d}-{g + 1}",
                           "tipo_unidade": "car" if inteiro else "gleba", "imovel_id": f"IMV{i:04d}",
                           "car_codigo": car, "municipio_ibge": cod, "porte_modulos_fiscais": mf,
                           "area_ha": round(area_ha / k, 2), "nivel_espacial": "imovel_inteiro" if inteiro else "poligono",
                           "geometria_wkt": _caixa_wkt(gx0, cy, gx1, cy + lado), "mun_idx": m})
    imoveis = pd.DataFrame(imoveis)
    unidades = pd.DataFrame(glebas)

    # --- operações (unidade comercial = operação + CAR [+ gleba]) ---
    ops = []
    for _, u in unidades.iterrows():
        for _k in range(int(rng.integers(1, 3))):
            ano = int(rng.integers(2019, 2023))
            ini = pd.Timestamp(ano, int(rng.integers(1, 13)), 1)
            dur = int(rng.integers(8, 25))
            valor = float(np.clip(rng.lognormal(np.log(120_000), 0.9), 15_000, 2_000_000))
            pequeno = u["porte_modulos_fiscais"] <= 4
            ops.append({"operacao_id": f"OP{len(ops):05d}", "unidade_id": u["unidade_id"], "car_codigo": u["car_codigo"],
                        "tipo_operacao": str(rng.choice(["custeio", "investimento"], p=[0.8, 0.2])),
                        "programa": str(rng.choice(PROGRAMAS, p=[0.7, 0.15, 0.15] if pequeno else [0.05, 0.45, 0.5])),
                        "produto_cultura": str(rng.choice(CULTURAS)), "safra": SAFRAS[ano - 2019],
                        "valor_rs": round(valor, 2), "data_contrato": ini.date().isoformat(),
                        "data_vencimento": (ini + pd.DateOffset(months=dur)).date().isoformat(),
                        "proagro_acionado": bool(rng.random() < 0.03)})  # coluna opcional, nunca usada pelo motor
    ops = pd.DataFrame(ops)

    # --- indicadores (painel unidade × corte) ---
    pressao = mun["pressao"].to_numpy()[unidades["mun_idx"].to_numpy()]
    base_veg = np.clip(rng.beta(2, 3, len(unidades)) * 100, 1, 99)
    base_urb = rng.lognormal(np.log(5), 0.8, len(unidades))
    base_min = rng.lognormal(np.log(8), 0.9, len(unidades))
    uc = np.where(rng.random(len(unidades)) < 0.7, 0.0, rng.uniform(5, 100, len(unidades)))
    linhas = []
    for t, corte in enumerate(DATAS_CORTE):
        supr = np.maximum(0, rng.lognormal(np.log(4), 0.9, len(unidades)) * np.exp(0.35 * pressao) - 2)
        linhas.append(pd.DataFrame({
            "unidade_id": unidades["unidade_id"], "data_corte": corte,
            "pct_veg_nativa": np.round(np.clip(base_veg - 0.6 * t + rng.normal(0, 0.4, len(unidades)), 0, 100), 2),
            "supressao_viz_ha_3a": np.round(supr, 2),
            "dist_urbano_km": np.round(base_urb, 3), "dist_mineracao_km": np.round(base_min, 3),
            "sobreposicao_uc_pct": np.round(uc, 1),
            "chuva_anual_mm": np.round(rng.normal(1400, 200, len(unidades))).clip(600, 2400),
        }))
    ind = pd.concat(linhas, ignore_index=True)

    # --- eventos (modelo logístico conhecido; intercepto calibrado por nível espacial) ---
    z = np.column_stack([ft.padronizar(f, ind[f.coluna].to_numpy()) for f in ft.FATORES])
    eta = z @ np.array([COEF_VERDADE[f.nome] for f in ft.FATORES])
    nivel = ind["unidade_id"].map(unidades.set_index("unidade_id")["nivel_espacial"]).to_numpy()
    interceptos, p_verdade = {}, np.empty(len(ind))
    for nv, taxa in TAXAS_BASE.items():
        m = nivel == nv
        lo, hi = -15.0, 5.0
        for _ in range(80):
            mid = (lo + hi) / 2
            lo, hi = (lo, mid) if _sigmoid(eta[m] + mid).mean() > taxa else (mid, hi)
        interceptos[nv] = (lo + hi) / 2
        p_verdade[m] = _sigmoid(eta[m] + interceptos[nv])
    y = (rng.random(len(ind)) < p_verdade).astype(int)
    dias = rng.integers(0, 365, len(ind))
    eventos = pd.DataFrame({
        "unidade_id": ind["unidade_id"], "data_corte": ind["data_corte"], "y_definicao": Y_DEFINICAO,
        "horizonte_meses": HORIZONTE_MESES, "nivel_espacial": nivel, "y": y,
        "data_evento": [(pd.Timestamp(c) + pd.Timedelta(days=int(d))).date().isoformat() if yy else None
                        for c, d, yy in zip(ind["data_corte"], dias, y)],
        "p_verdade": np.round(p_verdade, 6),
    })

    # --- verificações determinísticas (vedação); sorteadas independentemente de p ---
    ver = []
    sobre = ind["sobreposicao_uc_pct"].to_numpy()
    for i, r in enumerate(ind.itertuples()):
        c = pd.Timestamp(r.data_corte)
        for regra, (fonte, efeito) in FONTES_VERIFICACAO.items():
            if regra == "sobreposicao_uc":
                status = "detectado" if sobre[i] > 0 else None
            elif regra == "embargo":
                status = "detectado" if rng.random() < 0.01 else None
            else:
                status = str(rng.choice(["detectado", "autorizado", "sem_autorizacao_identificada", "indeterminado"],
                                        p=[0.2, 0.3, 0.35, 0.15])) if rng.random() < 0.05 else None
            if status is None:
                continue
            pub = (c - pd.Timedelta(days=45)).date()
            ver.append({"unidade_id": r.unidade_id, "data_corte": r.data_corte, "regra": regra, "efeito": efeito,
                        "status_juridico": status, "fonte": fonte,
                        "data_referencia": (pub - pd.Timedelta(days=60)).isoformat(), "data_publicacao": pub.isoformat(),
                        "hash_fonte": hashlib.sha256(f"{fonte}|{r.data_corte}|sintetico".encode()).hexdigest(),
                        "texto": f"{regra}: {status} (dado sintético)."})
    ver = pd.DataFrame(ver)

    # --- rótulo opcional de piloto (Y3): sorteio independente, só para exercitar o schema ---
    rot = []
    for o in ops.itertuples():
        for corte in DATAS_CORTE:
            c = pd.Timestamp(corte)
            if not pd.Timestamp(o.data_contrato) <= c < pd.Timestamp(o.data_vencimento):
                continue
            if rng.random() < 0.05:
                ev = c + pd.Timedelta(days=int(rng.integers(30, 330)))
                rot.append({"operacao_id": o.operacao_id, "data_corte": corte, "y3_atraso_90d": 1,
                            "data_evento": ev.date().isoformat(),
                            "data_registro": (ev + pd.Timedelta(days=int(rng.integers(0, 60)))).date().isoformat()})
            else:  # sem evento: o registro só fecha ao fim da janela de 12 meses
                rot.append({"operacao_id": o.operacao_id, "data_corte": corte, "y3_atraso_90d": 0, "data_evento": None,
                            "data_registro": (c + pd.DateOffset(months=12)).date().isoformat()})
    rot = pd.DataFrame(rot)

    unidades = unidades.drop(columns="mun_idx")
    imoveis = imoveis.drop(columns="mun_idx")
    return {"municipios": mun.drop(columns="pressao"), "imoveis": imoveis, "unidades": unidades,
            "operacoes": ops, "indicadores": ind, "verificacoes": ver, "rotulos_piloto": rot, "eventos": eventos,
            "_meta": pd.DataFrame({"nivel_espacial": list(interceptos), "intercepto": list(interceptos.values()),
                                   "taxa_base_alvo": [TAXAS_BASE[k] for k in interceptos], "semente": semente})}


def gravar(destino, **kw) -> None:
    """Grava as tabelas como CSV (nomes que a CLI do motor lê: indicadores, unidades, operacoes) em `destino`."""
    from pathlib import Path
    d = Path(destino)
    d.mkdir(parents=True, exist_ok=True)
    for nome, df in gerar(**kw).items():
        df.to_csv(d / f"{nome.lstrip('_')}.csv", index=False)


if __name__ == "__main__":
    import sys
    gravar(sys.argv[1] if len(sys.argv) > 1 else "tests/fixtures/sinteticos")
