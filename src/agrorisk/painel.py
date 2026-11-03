"""Painel de modelagem CAR x t0 (sessão 07, Etapa C).

Consome: snapshot do CAR e IDE-Sisema (data/raw/snapshots/<d>/<recorte>), PRODES (data/raw/prodes), pickles do gate
(`data/interim/gate_{car,prodes,pos}_<recorte>.pkl`, gerados por `agrorisk.gate`; fornecem Y_agro/Y_ilegal por evento).
Produz: data/processed/painel_car_t0[_treino].parquet (uma linha por CAR x t0; chave (cod_imovel, data_corte)).
CRS de cálculo: EPSG:31983. t0 = 31/jul/(y-1); ano_prodes y = ciclo ago/(y-1)–jul/y; h = 12 meses.

Regras anti-vazamento (CLAUDE.md regra 3):
- Preditores PRODES usam só anos <= y-2 (o ciclo y-1 termina em t0 e só é publicado ~3–4 meses depois).
  `prodes_ano_max_usado` registra o último ano usado; o teste exige ano + 4 meses <= t0.
- Colunas `vig_*` são estado VIGENTE (snapshot 2026-11-03), sem histórico: NÃO são preditores limpos e ficam fora do conjunto
  `PREDITORES_DATADOS`. Colunas `diag_*` usam informação posterior a t0 e servem só de diagnóstico.
- Não aplicado (limitação declarada): filtro de >= 1 ha de vegetação nativa em t0 (MapBiomas indisponível na nuvem).
"""
from __future__ import annotations

import argparse
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd

from agrorisk.gate import UTM

ANOS_PRODES = list(range(2018, 2026))  # t0 = 2017..2024
PREDITORES_DATADOS = [
    "porte_modulos_fiscais", "area_ha", "status_imovel", "idade_car_meses",
    "hist_imovel_ha_12m", "hist_imovel_ha_36m", "hist_imovel_n_anos_36m",
    "viz_1km_ha_12m", "viz_1km_ha_36m", "viz_3km_ha_12m", "viz_3km_ha_36m", "viz_5km_ha_12m", "viz_5km_ha_36m",
    "dist_evento_36m_m", "taxa_municipio_36m", "embargo_sisema_ate_t0",
]


def construir(recorte: str, data: str, saida: Path = Path("data/processed")) -> Path:
    car = pd.read_pickle(f"data/interim/gate_car_{recorte}.pkl")
    prodes = pd.read_pickle(f"data/interim/gate_prodes_{recorte}.pkl").reset_index(drop=True)
    pos = pd.read_pickle(f"data/interim/gate_pos_{recorte}.pkl")
    car = gpd.GeoDataFrame(car, geometry="geometry", crs=UTM).reset_index(drop=True)
    prodes = gpd.GeoDataFrame(prodes, geometry="geometry", crs=UTM)
    prodes["ha"] = prodes.area / 1e4
    anos_poly = prodes.year.to_numpy(); ha_poly = prodes.ha.to_numpy()

    # pares CAR–polígono: interseção (próprio imóvel) e anéis de 1/3/5 km (excluindo polígonos que tocam o próprio imóvel)
    own = gpd.sjoin(car[["geometry"]], prodes[["geometry"]], predicate="intersects", how="inner")
    own_pairs = set(zip(own.index.to_numpy(), own.index_right.to_numpy()))
    own_ha = gpd.overlay(prodes[["geometry"]].reset_index(names="poly"), car[["geometry"]].reset_index(names="car"),
                         how="intersection", keep_geom_type=True)
    own_ha["ha"] = own_ha.area / 1e4; own_ha["ano"] = anos_poly[own_ha.poly.to_numpy()]
    aneis = {}
    for km in (1, 3, 5):
        b = gpd.GeoDataFrame(geometry=car.geometry.buffer(km * 1000), crs=UTM)
        j = gpd.sjoin(b, prodes[["geometry"]], predicate="intersects", how="inner")
        d = pd.DataFrame({"car": j.index.to_numpy(), "poly": j.index_right.to_numpy()})
        d = d[[(c, p) not in own_pairs for c, p in zip(d.car, d.poly)]]
        d["ano"] = anos_poly[d.poly.to_numpy()]; d["ha"] = ha_poly[d.poly.to_numpy()]
        aneis[km] = d

    # camadas Sisema (embargo datado) e vigentes (UC, mineração)
    snap = Path("data/raw/snapshots") / data / recorte / "sisema"
    emb = gpd.read_file(snap / "ide_2304_mg_areas_embargadas_sisema_pol.geojson").set_crs(4674, allow_override=True).to_crs(UTM)
    emb["data_emb"] = pd.to_datetime(emb.data_fisca, format="%d/%m/%Y", errors="coerce")
    uc = pd.concat([gpd.read_file(p).set_crs(4674, allow_override=True).to_crs(UTM)[["geometry"]]
                    for p in snap.glob("ide_2010_*conservacao*.geojson")])
    uc["geometry"] = uc.geometry.make_valid(); uc_u = uc.geometry.union_all()
    car["vig_uc_frac"] = (car.geometry.intersection(uc_u).area / car.geometry.area).fillna(0).round(4)
    emb_j = gpd.sjoin(car[["geometry"]], emb[["data_emb", "geometry"]], predicate="intersects", how="inner")
    emb_min = emb_j.groupby(level=0).data_emb.min()

    # taxa de município: eventos >=1 ha por CAR no município, até y-2 (usa os próprios eventos do gate; ver ressalva no dicionário)
    ev_mun = pos[pos.cod_imovel.isin(car.cod_imovel)][["cod_imovel", "year", "cod_municipio_ibge"]]

    saida.mkdir(parents=True, exist_ok=True)
    linhas = []
    for y in ANOS_PRODES:
        t0 = pd.Timestamp(y - 1, 7, 31)
        el = car[(car.criacao <= t0 - pd.DateOffset(months=6))]
        idx = el.index.to_numpy()
        df = pd.DataFrame({"cod_imovel": el.cod_imovel.to_numpy(), "data_corte": t0, "ano_prodes": y,
                           "cod_municipio_ibge": el.cod_municipio_ibge.to_numpy(), "porte_modulos_fiscais": el.m_fiscal.to_numpy(),
                           "classe_porte": el.porte.astype(str).to_numpy(), "area_ha": (el.geometry.area / 1e4).round(3).to_numpy(),
                           "status_imovel": el.status_imovel.to_numpy(),
                           "idade_car_meses": ((t0 - el.criacao).dt.days / 30.44).round(1).to_numpy()}, index=idx)
        a12, a36 = range(y - 2, y - 1), range(y - 4, y - 1)
        for nome, anos in (("12m", a12), ("36m", a36)):
            o = own_ha[own_ha.ano.isin(list(anos))].groupby("car").ha.sum()
            df[f"hist_imovel_ha_{nome}"] = o.reindex(idx).fillna(0).round(3).to_numpy()
            for km, d in aneis.items():
                s = d[d.ano.isin(list(anos))].groupby("car").ha.sum()
                df[f"viz_{km}km_ha_{nome}"] = s.reindex(idx).fillna(0).round(3).to_numpy()
        df["hist_imovel_n_anos_36m"] = own_ha[own_ha.ano.isin(list(a36))].groupby("car").ano.nunique().reindex(idx).fillna(0).to_numpy()
        hist = prodes[prodes.year.isin(list(a36))]
        if len(hist):
            nn = gpd.sjoin_nearest(el[["geometry"]], hist[["geometry"]], how="left", distance_col="dist")
            df["dist_evento_36m_m"] = nn[~nn.index.duplicated()].dist.reindex(idx).round(1).to_numpy()
        else:
            df["dist_evento_36m_m"] = np.nan
        em = ev_mun[ev_mun.year.isin(list(a36))].groupby("cod_municipio_ibge").size()
        ncar = el.groupby("cod_municipio_ibge").size()
        df["taxa_municipio_36m"] = (df.cod_municipio_ibge.map(em).fillna(0) / df.cod_municipio_ibge.map(ncar)).round(5).to_numpy()
        e = emb_min.reindex(idx)
        df["embargo_sisema_ate_t0"] = (e <= t0).fillna(False).to_numpy()
        df["embargo_data_min"] = e.where(e <= t0).to_numpy()
        df["prodes_ano_max_usado"] = y - 2
        df["vig_uc_frac"] = el.vig_uc_frac.to_numpy()
        # rótulos
        evs = pos[pos.year == y].set_index("cod_imovel")
        df["Y_total"] = df.cod_imovel.isin(evs.index).astype(int)
        agro = evs[~evs.nao_agro].index; sem_aut = evs[~evs.autorizado].index
        df["Y_agro"] = df.cod_imovel.isin(agro).astype(int)
        df["Y_ilegal"] = df.cod_imovel.isin(sem_aut).astype(int)
        df["diag_geom_atualizada_pos_t0"] = (el.atualizacao > t0).to_numpy()
        linhas.append(df)
    p = pd.concat(linhas, ignore_index=True)
    arq = saida / ("painel_car_t0.parquet" if recorte == "vitrine" else f"painel_car_t0_{recorte}.parquet")
    p.to_parquet(arq, index=False)
    print(arq, p.shape); print(p.groupby("ano_prodes").agg(n=("Y_total", "size"), y_total=("Y_total", "sum"), y_agro=("Y_agro", "sum"), y_ilegal=("Y_ilegal", "sum")))
    return arq


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--recorte", choices=["vitrine", "treino"], default="vitrine")
    ap.add_argument("--data", default="2026-11-03"); a = ap.parse_args(); construir(a.recorte, a.data)
