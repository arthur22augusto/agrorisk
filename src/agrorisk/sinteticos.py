"""Gerador de dados sintéticos (frentes A — crédito — e B — fornecedor). Reprodutível por semente.

TUDO AQUI É FICTÍCIO: nenhum dado real de pessoa, CPF ou nome. Códigos de CAR seguem o formato real
(`MG-<IBGE7>-<32 hex>`), mas os 8 primeiros hex são `00000000` (marca de fictício; coluna `car_ficticio`).
Geometrias: cada município vira uma caixa de lado √área numa grade FICTÍCIA (não é a posição real); imóveis
são caixas dentro da caixa do município. Servem só para testar o pipeline, não para análise espacial.

Eventos: y ~ Bernoulli(p), p = sigmoid(INTERCEPTO + Σ COEF_VERDADE[f]·z_f), com z padronizado como em
`agrorisk.motor.fatores`. O intercepto é calibrado (bisseção) para a taxa-base média ≈ TAXA_BASE.
Os coeficientes abaixo são a "verdade" que um backtest/modelo deve recuperar.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from .motor import fatores as ft

SEMENTE = 20261029
TAXA_BASE = 0.02
DATAS_CORTE = ("2020-01-01", "2021-01-01", "2022-01-01", "2023-01-01")
HORIZONTE_MESES = 12
EVENTO = "supressao_vegetacao"  # sintético; o Y real é decidido na sessão 06

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


def gerar(semente: int = SEMENTE, n_imoveis: int = 300, n_fornecedores: int = 60) -> dict[str, pd.DataFrame]:
    """Retorna dict de DataFrames: municipios, imoveis, unidades, operacoes, indicadores, eventos."""
    rng = np.random.default_rng(semente)
    caixas = _municipios_caixas()
    mun = pd.DataFrame(MUNICIPIOS, columns=["cod_ibge", "municipio", "grupo", "area_km2"])
    mun["geometria_wkt"] = [_caixa_wkt(*caixas[c]) for c in mun["cod_ibge"]]
    mun["pressao"] = rng.normal(0, 1, len(mun))  # latente: correlaciona supressão na vizinhança

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
        inteiro = rng.random() < 0.25
        k = 1 if inteiro else int(rng.integers(1, 4))
        for g in range(k):
            gx0, gx1 = cx + lado * g / k, cx + lado * (g + 1) / k
            glebas.append({"unidade_id": f"GLB{i:04d}-{g + 1}", "tipo_unidade": "gleba", "imovel_id": f"IMV{i:04d}",
                           "car_codigo": car, "municipio_ibge": cod,
                           "area_ha": round(area_ha / k, 2), "nivel_espacial": "imovel_inteiro" if inteiro else "gleba",
                           "geometria_wkt": _caixa_wkt(gx0, cy, gx1, cy + lado), "mun_idx": m})
    imoveis = pd.DataFrame(imoveis)
    # fornecedores (frente B): cada um abastece a partir de um imóvel; sem CPF/CNPJ/nome
    forn_imv = rng.choice(n_imoveis, size=n_fornecedores, replace=False)
    forn = []
    for j, i in enumerate(forn_imv):
        r = imoveis.iloc[i]
        forn.append({"unidade_id": f"FRN{j:04d}", "tipo_unidade": "fornecedor", "imovel_id": r["imovel_id"],
                     "car_codigo": r["car_codigo"], "municipio_ibge": r["municipio_ibge"], "area_ha": r["area_ha"],
                     "nivel_espacial": "imovel_inteiro", "geometria_wkt": r["geometria_wkt"], "mun_idx": r["mun_idx"]})
    unidades = pd.concat([pd.DataFrame(glebas), pd.DataFrame(forn)], ignore_index=True)

    # --- operações ---
    ops = []
    for _, u in unidades.iterrows():
        n = rng.integers(1, 3) if u["tipo_unidade"] == "gleba" else rng.integers(1, 4)
        for _k in range(n):
            ano = int(rng.integers(2019, 2023))
            ini = pd.Timestamp(ano, int(rng.integers(1, 13)), 1)
            dur = int(rng.integers(8, 25))
            cultura = str(rng.choice(CULTURAS))
            if u["tipo_unidade"] == "gleba":
                valor = float(np.clip(rng.lognormal(np.log(120_000), 0.9), 15_000, 2_000_000))
                tipo = str(rng.choice(["custeio", "investimento"], p=[0.8, 0.2]))
            else:
                valor = float(np.clip(rng.lognormal(np.log(300_000), 0.8), 30_000, 5_000_000))
                tipo = "fornecimento"
            ops.append({"operacao_id": f"OP{len(ops):05d}", "unidade_id": u["unidade_id"], "tipo_operacao": tipo,
                        "produto_cultura": cultura, "safra": SAFRAS[ano - 2019], "valor_rs": round(valor, 2),
                        "data_inicio": ini.date().isoformat(),
                        "data_fim": (ini + pd.DateOffset(months=dur)).date().isoformat()})
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

    # --- eventos (modelo logístico conhecido) ---
    z = np.column_stack([ft.padronizar(f, ind[f.coluna].to_numpy()) for f in ft.FATORES])
    eta = z @ np.array([COEF_VERDADE[f.nome] for f in ft.FATORES])
    lo, hi = -15.0, 5.0
    for _ in range(80):
        mid = (lo + hi) / 2
        lo, hi = (lo, mid) if _sigmoid(eta + mid).mean() > TAXA_BASE else (mid, hi)
    intercepto = (lo + hi) / 2
    p_verdade = _sigmoid(eta + intercepto)
    y = (rng.random(len(ind)) < p_verdade).astype(int)
    dias = rng.integers(0, 365, len(ind))
    eventos = pd.DataFrame({
        "unidade_id": ind["unidade_id"], "data_corte": ind["data_corte"], "evento": EVENTO,
        "horizonte_meses": HORIZONTE_MESES, "y": y,
        "data_evento": [(pd.Timestamp(c) + pd.Timedelta(days=int(d))).date().isoformat() if yy else None
                        for c, d, yy in zip(ind["data_corte"], dias, y)],
        "p_verdade": np.round(p_verdade, 6),
    })
    unidades = unidades.drop(columns="mun_idx")
    imoveis = imoveis.drop(columns="mun_idx")
    return {"municipios": mun.drop(columns="pressao"), "imoveis": imoveis, "unidades": unidades,
            "operacoes": ops, "indicadores": ind, "eventos": eventos,
            "_meta": pd.DataFrame({"intercepto": [intercepto], "semente": [semente], "taxa_base_alvo": [TAXA_BASE]})}


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
