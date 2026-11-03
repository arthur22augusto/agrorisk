"""Snapshots mensais com hash do CAR (SICAR WFS) e da IDE-Sisema (escopo-mvp §4, item iii).

Consome: SICAR `sicar:sicar_imoveis_mg` (filtro por município) e camadas WFS da IDE-Sisema (bbox do recorte).
Produz: data/raw/snapshots/<AAAA-MM-DD>/{car,sisema}/*.geojson + manifest.json (sha256 por arquivo e do conjunto).
O hash do conjunto também vai para docs/dados/snapshots_registro.csv (este SIM no git; os dados não).
Colunas com dados pessoais (nome, CPF/CNPJ) são removidas antes de gravar (LGPD; licencas.md).
Uso: python -m agrorisk.fontes.snapshot --recorte vitrine|treino [--data AAAA-MM-DD]
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
from pathlib import Path

from agrorisk.fontes._comum import RAW, baixar_wfs, gravar_manifesto
from agrorisk.recortes import municipios

SICAR = "https://geoserver.car.gov.br/geoserver/sicar/wfs"
SISEMA = "https://geoserver.meioambiente.mg.gov.br/wfs"
# bbox da vitrine (sessão 01, lat/lon EPSG:4326 na ordem do WFS 2.0); treino recebe margem pelo CAR baixado.
BBOX_VITRINE = "-20.52,-44.8,-19.05,-43.19,urn:ogc:def:crs:EPSG::4326"

CAMADAS_SISEMA = [
    "ide_2105_mg_area_autorizada_intervencao_ambiental_ief_pol",  # supressão autorizada IEF
    "ide_2105_mg_area_autoriz_interv_amb_feam_pol",               # supressão autorizada FEAM (mineração)
    "ide_2304_mg_areas_embargadas_sisema_pol",                    # embargos estaduais
    "ide_2010_mg_unidades_conservacao_estaduais_pol",
    "ide_2010_mg_unidades_conservacao_federais_pol",
    "ide_2010_mg_unidades_conservacao_municipais_pol",
]
PESSOAIS = ("cpf", "cnpj", "autuado", "embargado", "nome_emp", "nome_req", "requerente", "titular", "nome_pess", "razao",
            "autorizado", "fiscalizad", "doc_fiscal")  # IEF: `autorizado`=nome; embargos Sisema: `fiscalizad`=nome, `doc_fiscal`=CPF/CNPJ


def sem_pessoais(arq: Path) -> list[str]:
    """Remove no próprio arquivo as propriedades pessoais; retorna os nomes removidos."""
    d = json.loads(arq.read_text(encoding="utf-8"))
    removidas: set[str] = set()
    for f in d["features"]:
        for k in list(f.get("properties", {})):
            if any(p in k.lower() for p in PESSOAIS):
                removidas.add(k); del f["properties"][k]
    if removidas:
        arq.write_text(json.dumps(d), encoding="utf-8")
    return sorted(removidas)


def bbox_do_car(pasta_car: Path, margem: float = 0.05) -> str:
    import geopandas as gpd
    b = [gpd.read_file(p).total_bounds for p in pasta_car.glob("*.geojson")]
    x0, y0 = min(t[0] for t in b) - margem, min(t[1] for t in b) - margem
    x1, y1 = max(t[2] for t in b) + margem, max(t[3] for t in b) + margem
    return f"{y0:.4f},{x0:.4f},{y1:.4f},{x1:.4f},urn:ogc:def:crs:EPSG::4326"


def snapshot(recorte: str, data: str, raiz: Path = RAW / "snapshots") -> str:
    pasta = raiz / data / recorte
    if (pasta / "manifest.json").exists():
        h = json.loads((pasta / "manifest.json").read_text())["hash_snapshot"]
        print("snapshot já existe:", pasta, h); return h
    regs: list[dict] = []
    for cod, info in municipios(recorte).items():
        r = baixar_wfs(SICAR, "sicar:sicar_imoveis_mg", pasta / "car" / f"{cod}.geojson",
                       cql=f"cod_municipio_ibge={cod}", ordenar="cod_imovel")
        regs.append(r); print("car", cod, info["municipio"], r["n_feicoes"], flush=True)
    bbox = BBOX_VITRINE if recorte == "vitrine" else bbox_do_car(pasta / "car")
    removidas: dict[str, list[str]] = {}
    for lay in CAMADAS_SISEMA:
        arq = pasta / "sisema" / f"{lay}.geojson"
        try:
            r = baixar_wfs(SISEMA, "IDE:" + lay, arq, bbox=bbox, srs="EPSG:4674", pagina=5000)
        except RuntimeError as e:
            print("sisema ERRO", lay, e); continue
        rem = sem_pessoais(arq)
        if rem:
            removidas[lay] = rem
            from agrorisk.fontes._comum import sha256_arquivo
            r["sha256"] = sha256_arquivo(arq)  # hash do arquivo já sem pessoais
        regs.append(r); print("sisema", lay, r["n_feicoes"], flush=True)
    h = gravar_manifesto(pasta, regs, {"recorte": recorte, "data": data, "bbox_sisema": bbox,
                                       "colunas_pessoais_removidas": removidas})
    reg = Path("docs/dados/snapshots_registro.csv"); novo = not reg.exists()
    with open(reg, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if novo: w.writerow(["data", "recorte", "n_car", "n_arquivos", "sha256_snapshot"])
        w.writerow([data, recorte, sum(x["n_feicoes"] for x in regs if x["camada"].startswith("sicar")), len(regs), h])
    return h


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--recorte", choices=["vitrine", "treino"], default="vitrine")
    ap.add_argument("--data", default=dt.date.today().isoformat())
    a = ap.parse_args()
    print(snapshot(a.recorte, a.data))
