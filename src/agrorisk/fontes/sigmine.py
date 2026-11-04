"""ANM SIGMINE — processos minerários ativos (ArcGIS REST, camada 0 de SIGMINE/dados_anm). Snapshot ATUAL, sem histórico.

Produz data/raw/sigmine/<data>/processos.geojson. Licença não declarada (licencas.md: incerto). O campo NOME (titular) é removido.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path

from agrorisk.fontes._comum import RAW, curl_json, gravar_manifesto, sha256_arquivo

URL = "https://geo.anm.gov.br/arcgis/rest/services/SIGMINE/dados_anm/MapServer/0/query"


def baixar(bbox_xy: tuple[float, float, float, float], data: str, raiz: Path = RAW / "sigmine") -> Path:
    """bbox_xy = (xmin, ymin, xmax, ymax) em EPSG:4674/4326 (graus)."""
    pasta = raiz / data; pasta.mkdir(parents=True, exist_ok=True); saida = pasta / "processos.geojson"
    if not saida.exists():
        feats, ini = [], 0
        while True:
            d = curl_json(URL, {"f": "geojson", "where": "UF='MG'", "geometry": ",".join(map(str, bbox_xy)),
                                "geometryType": "esriGeometryEnvelope", "inSR": 4326, "spatialRel": "esriSpatialRelIntersects",
                                "outFields": "PROCESSO,ANO,FASE,SUBS,USO,AREA_HA,ULT_EVENTO", "outSR": 4674,
                                "resultOffset": ini, "resultRecordCount": 1000, "orderByFields": "OBJECTID"})
            feats += d["features"]
            if len(d["features"]) < 1000: break
            ini += 1000
        saida.write_text(json.dumps({"type": "FeatureCollection", "features": feats}), encoding="utf-8")
    n = len(json.loads(saida.read_text(encoding="utf-8"))["features"])
    gravar_manifesto(pasta, [{"arquivo": saida.name, "camada": "sigmine0", "url": URL, "n_feicoes": n, "sha256": sha256_arquivo(saida)}])
    return pasta


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--data", default=dt.date.today().isoformat())
    a = ap.parse_args(); print(baixar((-44.8, -20.52, -43.19, -19.05), a.data))
