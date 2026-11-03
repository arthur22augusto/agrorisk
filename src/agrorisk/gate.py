"""Gate do Y (sessão 07, Etapa 0; escopo-mvp §3). Mede, ANTES do painel/modelo, se o Y sustenta o escopo.

Consome: snapshot CAR (data/raw/snapshots/<d>/<recorte>/car), PRODES (data/raw/prodes/<d>), IDE-Sisema IEF/FEAM (snapshot),
SIGMINE (data/raw/sigmine/<d>), IBGE Áreas Urbanizadas 2022 (data/raw/ibge_urbano/<d>).
Produz: reports/07-gate/*.csv e reports/07-gate/resumo.json. CRS de cálculo: EPSG:31983 (UTM 23S), declarado aqui.
Convenção: ano-PRODES y = ciclo ago/(y-1)–jul/y; t0 = 31/jul/(y-1). Teste = anos-PRODES 2021–2024 (t0 2020–2023).
Geometria do CAR = vigente (exploratório/otimista, ver escopo-mvp §4). Sem MapBiomas (bloqueio de rede): urbano via IBGE 2022.
Uso: python -m agrorisk.gate --recorte vitrine --data 2026-11-03
"""
from __future__ import annotations

import argparse
import json
import zipfile
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd

UTM = 31983
ANOS = [2021, 2022, 2023, 2024]
MIN_FRAC_AUT = 0.10  # autorização só conta se cobrir ≥10% da área do evento (revisão estatística)
FASES_MINERACAO = ("LAVRA", "LICENCIAMENTO", "REGISTRO DE EXTRAÇÃO")  # sem pesquisa (sensibilidade à parte)


def carrega_car(pasta: Path) -> gpd.GeoDataFrame:
    g = pd.concat([gpd.read_file(f) for f in sorted(pasta.glob("*.geojson"))], ignore_index=True)
    g = gpd.GeoDataFrame(g, geometry="geometry").set_crs(4674, allow_override=True).to_crs(UTM)
    g["geometry"] = g.geometry.make_valid()
    g["criacao"] = pd.to_datetime(g.dat_criacao, utc=True).dt.tz_localize(None)
    g["atualizacao"] = pd.to_datetime(g.data_atualizacao, utc=True).dt.tz_localize(None)
    g["porte"] = pd.cut(g.m_fiscal, [-1, 4, 15, 1e9], labels=["<=4MF", "4-15MF", ">15MF"])
    return g.sort_values("atualizacao").drop_duplicates("cod_imovel", keep="last").reset_index(drop=True)[
        ["cod_imovel", "cod_municipio_ibge", "status_imovel", "criacao", "atualizacao", "area", "m_fiscal", "porte", "geometry"]]


def carrega_prodes(pasta: Path) -> gpd.GeoDataFrame:
    """Cerrado + Mata Atlântica (esta sem a sobreposição com o Cerrado), só desmatamento, polígonos simples."""
    cer = None
    out = []
    for lay in ["prodes-cerrado-nb", "prodes-mata-atlantica-nb"]:
        g = gpd.read_file(pasta / f"{lay}.geojson").set_crs(4326, allow_override=True).to_crs(UTM)
        g = g[g.main_class.str.upper() == "DESMATAMENTO"][["year", "geometry"]].copy()
        g["geometry"] = g.geometry.make_valid(method="structure", keep_collapsed=False)  # "linework" falha com dimensões mistas no treino
        g = g.explode(index_parts=False)
        g = g[g.geom_type == "Polygon"]
        if cer is None:
            cer = g.geometry.reset_index(drop=True)  # polígonos do Cerrado (sem união global: inviável no treino)
        else:
            # remove da Mata Atlântica a parte sobreposta ao Cerrado, só nos polígonos que de fato se sobrepõem (índice espacial)
            g = g.reset_index(drop=True)
            cand = cer.sindex.query(g.geometry.values, predicate="intersects")
            novo = g.geometry.copy()
            for i in np.unique(cand[0]):
                viz = cer.iloc[cand[1][cand[0] == i]].union_all()
                novo.iloc[i] = g.geometry.iloc[i].difference(viz)
            g["geometry"] = novo
            g = g[~g.geometry.is_empty].explode(index_parts=False)
            g = g[g.geom_type == "Polygon"]
        g["bioma"] = "Cerrado" if cer is not None and lay.endswith("cerrado-nb") else "Mata Atlantica"
        out.append(g)
    p = pd.concat(out, ignore_index=True)
    return gpd.GeoDataFrame(p, geometry="geometry", crs=UTM).query("year >= 2014").reset_index(drop=True)


def eventos(car: gpd.GeoDataFrame, prodes: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """CAR x ano-PRODES: área total e maior componente contíguo (ha) da supressão dentro do polígono."""
    i = gpd.overlay(prodes[["year", "geometry"]], car[["cod_imovel", "geometry"]], how="intersection", keep_geom_type=True)
    i = i[~i.geometry.is_empty]
    rows = []
    for (cod, y), d in i.groupby(["cod_imovel", "year"]):
        u = d.geometry.union_all()
        partes = list(u.geoms) if hasattr(u, "geoms") else [u]
        rows.append((cod, int(y), u.area / 1e4, max(p.area for p in partes) / 1e4, u))
    e = gpd.GeoDataFrame(rows, columns=["cod_imovel", "year", "ha_total", "ha_contiguo", "geometry"], crs=UTM)
    return e


def carrega_urbano(pasta: Path, bbox4674: tuple) -> gpd.GeoDataFrame:
    z = next(pasta.glob("AreasUrbanizadas2022_Brasil.zip"))
    shp = [n for n in zipfile.ZipFile(z).namelist() if n.endswith(".shp")][0]
    u = gpd.read_file(f"zip://{z}!{shp}", bbox=bbox4674)
    u = u.to_crs(UTM); u["geometry"] = u.geometry.make_valid()
    return u[["geometry"]]


def fracao_sobreposta(ev: gpd.GeoDataFrame, camada: gpd.GeoDataFrame) -> pd.Series:
    """Fração da área do evento coberta pela união da camada (por linha de `ev`)."""
    if camada.empty:
        return pd.Series(0.0, index=ev.index)
    uni = gpd.GeoSeries([camada.geometry.union_all()], crs=UTM)
    inter = ev.geometry.intersection(uni.iloc[0])
    return (inter.area / ev.geometry.area).fillna(0)


def _filtra_fracao(j: gpd.GeoDataFrame, camada: gpd.GeoDataFrame, ev: gpd.GeoDataFrame, area_ev: pd.Series) -> gpd.GeoDataFrame:
    """Mantém pares (evento, feição) cuja interseção cobre >= MIN_FRAC_AUT da área do evento (usa a geometria da camada: índice `index_right`)."""
    if len(j) == 0:
        return j
    inter = ev.geometry.loc[j.index].values.intersection(camada.geometry.loc[j.index_right].values)
    frac = pd.Series(inter.area, index=j.index).to_numpy() / area_ev.loc[j.index].to_numpy()
    return j[frac >= MIN_FRAC_AUT]


def autorizacao(ev: gpd.GeoDataFrame, ief: gpd.GeoDataFrame, feam: gpd.GeoDataFrame) -> pd.DataFrame:
    """Sobreposição com IEF (datado, janela ±12 meses do ciclo) e FEAM (sem data na camada)."""
    out = pd.DataFrame(index=ev.index, data={"aut_ief_janela": False, "aut_ief_qualquer_data": False, "aut_feam_sem_data": False})
    ief = ief.copy(); ief["dpub"] = pd.to_datetime(ief.data_publi, dayfirst=True, errors="coerce")
    j = gpd.sjoin(ev[["geometry"]], ief[["dpub", "geometry"]], predicate="intersects", how="inner")
    area_ev = ev.geometry.area
    j = _filtra_fracao(j, ief, ev, area_ev)
    for idx, d in j.groupby(level=0):
        out.loc[idx, "aut_ief_qualquer_data"] = True
        y = int(ev.loc[idx, "year"])
        ini, fim = pd.Timestamp(y - 2, 8, 1), pd.Timestamp(y + 1, 7, 31)  # ciclo (y-1/08–y/07) ±12 meses
        if d.dpub.between(ini, fim).any():
            out.loc[idx, "aut_ief_janela"] = True
    jf = gpd.sjoin(ev[["geometry"]], feam[["geometry"]], predicate="intersects", how="inner")
    jf = _filtra_fracao(jf, feam, ev, area_ev)
    out.loc[jf.index.unique(), "aut_feam_sem_data"] = True
    return out


def _ic_boot(d: pd.DataFrame, f, B: int = 2000, seed: int = 7) -> tuple[float, float, float]:
    """Proporção f(d) com IC95% bootstrap em blocos = município (cod_municipio_ibge)."""
    if len(d) == 0: return (np.nan,) * 3
    rng = np.random.default_rng(seed)
    g = {k: f(v) for k, v in d.groupby("cod_municipio_ibge")}  # vetores booleanos por município
    ks = list(g)
    est = []
    for _ in range(B):
        sel = rng.choice(len(ks), len(ks))
        v = np.concatenate([g[ks[i]] for i in sel]); est.append(v.mean())
    return round(100 * f(d).mean(), 1), round(100 * np.percentile(est, 2.5), 1), round(100 * np.percentile(est, 97.5), 1)


def sensibilidades(pos_t: pd.DataFrame) -> pd.DataFrame:
    """Métricas do gate sob recortes alternativos, com IC (bootstrap por município). Sem autorização como filtro (IEF só cobre 2021+)
    e com autorização apenas em 2023–24. Subconjunto `atualizacao <= t0` = geometria do CAR plausivelmente a de t0."""
    base = {"todos_positivos": pos_t, "elegiveis": pos_t[pos_t.elegivel],
            "elegiveis_geom_estavel_(atualizacao<=t0)": pos_t[pos_t.elegivel & ~pos_t.geom_alterada_pos_t0],
            "elegiveis_sem_historico": pos_t[pos_t.elegivel & ~pos_t.historico_explica]}
    defs = {"Yagro_<=4MF (sem filtro de autorizacao)": lambda d: (~d.nao_agro & (d.porte == "<=4MF")).to_numpy(),
            "Yagro_sem_aut_<=4MF (aut. só 2023-24)": lambda d: (~d.nao_agro & (d.porte == "<=4MF") & ~(d.autorizado & d.year.isin([2023, 2024]))).to_numpy(),
            "historico_explica": lambda d: d.historico_explica.to_numpy(),
            "prev_imovel_3a": lambda d: d.prev_imovel_3a.to_numpy()}
    linhas = []
    for sub, d in base.items():
        for nome, f in defs.items():
            m, lo, hi = _ic_boot(d, f)
            linhas.append(dict(subconjunto=sub, n=len(d), metrica=nome, pct=m, ic95_inf=lo, ic95_sup=hi))
    return pd.DataFrame(linhas)


def regra_historico(car: gpd.GeoDataFrame, prodes: gpd.GeoDataFrame, pos: pd.DataFrame) -> pd.DataFrame:
    """(e2) Baseline 'distância a evento recente': ranqueia CARs elegíveis em t0 pela distância ao PRODES dos 3 anos anteriores
    (empates por distância 0 desfeitos por área desmatada prévia no imóvel) e mede recall@10% / @5% e taxa-base por ano.
    Também no subconjunto SEM evento prévio no imóvel (o do critério primário). Exploratório: geometria atual do CAR."""
    linhas = []
    for y in ANOS:
        t0 = pd.Timestamp(y - 1, 7, 31)
        c = car[car.criacao <= t0 - pd.DateOffset(months=6)].reset_index(drop=True)
        hist = prodes[prodes.year.between(y - 3, y - 1)]
        j = gpd.sjoin_nearest(c[["cod_imovel", "geometry"]], hist[["geometry"]], how="left", distance_col="dist").drop_duplicates("cod_imovel")
        prev_ha = gpd.overlay(hist[["geometry"]], c[["cod_imovel", "geometry"]], how="intersection").assign(ha=lambda d: d.area / 1e4)
        prev_ha = prev_ha.groupby("cod_imovel").ha.sum()
        c = c.merge(j[["cod_imovel", "dist"]], on="cod_imovel"); c["prev_ha"] = c.cod_imovel.map(prev_ha).fillna(0)
        c["y"] = c.cod_imovel.isin(pos[pos.year == y].cod_imovel)
        for nome, d in [("todos_elegiveis", c), ("sem_evento_previo_no_imovel", c[c.prev_ha == 0])]:
            d = d.sort_values(["dist", "prev_ha"], ascending=[True, False])
            n, npos = len(d), int(d.y.sum())
            r = {"ano_prodes": y, "grupo": nome, "n_cars": n, "n_positivos": npos, "taxa_base_pct": round(100 * npos / n, 2)}
            for q in (5, 10):
                k = int(np.ceil(n * q / 100)); r[f"recall_at_{q}pct"] = round(100 * d.y.iloc[:k].sum() / max(npos, 1), 1)
            linhas.append(r)
    return pd.DataFrame(linhas)


def _ext(fonte: str, data: str, recorte: str) -> Path:
    """Pasta da fonte externa: vitrine em <data>; treino (bbox maior) em <data>-treino."""
    return Path("data/raw") / fonte / (data if recorte == "vitrine" else f"{data}-treino")


def rodar(recorte: str, data: str, saida: Path = Path("reports/07-gate")) -> dict:
    saida.mkdir(parents=True, exist_ok=True)
    snap = Path("data/raw/snapshots") / data / recorte
    car = carrega_car(snap / "car")
    prodes = carrega_prodes(_ext("prodes", data, recorte))
    print("CARs", len(car), "poligonos PRODES", len(prodes), flush=True)
    ev = eventos(car, prodes)
    ev = ev.merge(car.drop(columns="geometry"), on="cod_imovel", how="left")
    ev["pos"] = ev.ha_contiguo >= 1.0
    pos = ev[ev.pos].copy().reset_index(drop=True)
    pos.crs = UTM
    # (b) destino: mineração (SIGMINE, snapshot atual) e urbano (IBGE 2022)
    sig = gpd.read_file(_ext("sigmine", data, recorte) / "processos.geojson").set_crs(4674, allow_override=True).to_crs(UTM)
    sig["geometry"] = sig.geometry.make_valid()
    minera = sig[sig.FASE.str.upper().apply(lambda f: any(k in f for k in FASES_MINERACAO))]
    b = tuple(gpd.GeoSeries([car.union_all()], crs=UTM).to_crs(4674).total_bounds)
    urb = carrega_urbano(Path("data/raw/ibge_urbano") / data, b)
    pos["f_mineracao"] = fracao_sobreposta(pos, minera)
    pos["f_mineracao_c_pesquisa"] = fracao_sobreposta(pos, sig)
    pos["f_urbano"] = fracao_sobreposta(pos, urb)
    pos["mineracao"] = pos.f_mineracao >= 0.5
    pos["urbano"] = pos.f_urbano >= 0.5
    pos["nao_agro"] = pos.mineracao | pos.urbano
    # (c) autorização
    sis = snap / "sisema"
    ief = gpd.read_file(sis / "ide_2105_mg_area_autorizada_intervencao_ambiental_ief_pol.geojson").set_crs(4674, allow_override=True).to_crs(UTM)
    feam = gpd.read_file(sis / "ide_2105_mg_area_autoriz_interv_amb_feam_pol.geojson").set_crs(4674, allow_override=True).to_crs(UTM)
    for g in (ief, feam): g["geometry"] = g.geometry.make_valid()
    pos = pos.join(autorizacao(pos, ief, feam))
    pos["autorizado"] = pos.aut_ief_janela | pos.aut_feam_sem_data
    # (d) elegibilidade e estabilidade da geometria
    pos["t0"] = pd.to_datetime([f"{y - 1}-07-31" for y in pos.year])
    pos["elegivel"] = pos.criacao <= (pos.t0 - pd.DateOffset(months=6))
    pos["geom_alterada_pos_t0"] = pos.atualizacao > pos.t0
    # (e) histórico: evento prévio no imóvel (qualquer tamanho, 3 anos) e vizinhança (1 km, ano y-1)
    ev_all = ev[["cod_imovel", "year", "ha_total"]]
    prev = []
    for _, r in pos.iterrows():
        h = ev_all[(ev_all.cod_imovel == r.cod_imovel) & ev_all.year.between(r.year - 3, r.year - 1)]
        prev.append(len(h) > 0)
    pos["prev_imovel_3a"] = prev
    viz = []
    for y in ANOS:
        sel = pos[pos.year == y]
        if sel.empty: continue
        pol = prodes[prodes.year == y - 1]
        c = car.set_index("cod_imovel").loc[sel.cod_imovel]
        bg = gpd.GeoDataFrame(geometry=[g.buffer(1000).difference(g) for g in c.geometry.values], index=sel.index, crs=UTM)  # anel de 1 km, sem o próprio imóvel
        hit = gpd.sjoin(bg, pol[["geometry"]], predicate="intersects", how="inner").index.unique()
        viz.append(pd.Series(sel.index.isin(hit), index=sel.index))
    pos["prev_viz_1km_12m"] = pd.concat(viz) if viz else False
    pos["historico_explica"] = pos.prev_imovel_3a | pos.prev_viz_1km_12m
    # tabelas
    pos_t = pos[pos.year.isin(ANOS)]
    def fr(m, d): return round(100 * m.mean(), 1) if len(d) else np.nan
    linhas = []
    for y, d in list(pos_t.groupby("year")) + [("pooled", pos_t)]:
        el = d[d.elegivel]
        linhas.append(dict(ano_prodes=y, n_positivos=len(d), n_elegiveis=len(el),
                           pct_ate4MF=fr(d.porte == "<=4MF", d), pct_mineracao=fr(d.mineracao, d), pct_urbano=fr(d.urbano, d),
                           pct_nao_agro=fr(d.nao_agro, d), pct_autorizado=fr(d.autorizado, d), pct_aut_ief=fr(d.aut_ief_janela, d),
                           pct_geom_alterada_pos_t0=fr(d.geom_alterada_pos_t0, d),
                           pct_historico_explica=fr(el.historico_explica, el), pct_prev_imovel=fr(el.prev_imovel_3a, el), pct_prev_viz=fr(el.prev_viz_1km_12m, el),
                           n_Yagro_sem_aut=int((~d.nao_agro & ~d.autorizado).sum()),
                           n_Yagro_sem_aut_ate4MF=int((~d.nao_agro & ~d.autorizado & (d.porte == "<=4MF")).sum()),
                           pct_Yagro_sem_aut_ate4MF=fr(~d.nao_agro & ~d.autorizado & (d.porte == "<=4MF"), d),
                           pct_Yagro_sem_aut_ate4MF_elegiveis_sem_hist=fr(~el.nao_agro & ~el.autorizado & (el.porte == "<=4MF") & ~el.historico_explica, el)))
    tab = pd.DataFrame(linhas)
    tab.to_csv(saida / f"gate_{recorte}.csv", index=False)
    sens = sensibilidades(pos_t)
    sens.to_csv(saida / f"sensibilidades_{recorte}.csv", index=False); print(sens.to_string())
    por_porte = pos_t.groupby(["year", "porte"], observed=True).size().unstack(fill_value=0)
    por_porte.to_csv(saida / f"positivos_por_porte_{recorte}.csv")
    cols = [c for c in pos.columns if c != "geometry"]
    pos[cols].drop(columns=["cod_imovel"]).describe(include="all").to_csv(saida / f"diag_{recorte}.csv")
    ev_ano = ev.groupby("year").agg(imoveis_qualquer_ha=("cod_imovel", "size"), imoveis_ge_1ha=("pos", "sum"))
    ev_ano.to_csv(saida / f"eventos_por_ano_{recorte}.csv")
    pos[cols].to_csv(Path("data/interim") / f"gate_positivos_{recorte}.csv", index=False)
    res = dict(recorte=recorte, data=data, n_cars=len(car), n_cars_nao_cancelados=int((car.status_imovel != "CA").sum()),
               eventos_por_ano=ev_ano.to_dict(), tabela=tab.to_dict(orient="records"))
    (saida / f"resumo_{recorte}.json").write_text(json.dumps(res, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    rh = regra_historico(car, prodes, pos_t); rh.to_csv(saida / f"baseline_distancia_{recorte}.csv", index=False); print(rh.to_string())
    pos.to_pickle(Path("data/interim") / f"gate_pos_{recorte}.pkl")
    car.to_pickle(Path("data/interim") / f"gate_car_{recorte}.pkl"); prodes.to_pickle(Path("data/interim") / f"gate_prodes_{recorte}.pkl")
    print(tab.T.to_string()); print(ev_ano.to_string())
    return res


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--recorte", choices=["vitrine", "treino"], default="vitrine")
    ap.add_argument("--data", default="2026-11-03")
    a = ap.parse_args()
    rodar(a.recorte, a.data)
