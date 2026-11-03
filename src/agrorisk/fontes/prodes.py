"""PRODES Cerrado e Mata Atlântica (INPE/TerraBrasilis WFS, camada yearly_deforestation) no bbox do recorte.

Produz data/raw/prodes/<data>/<camada>.geojson + manifest.json. Licença CC BY-SA 4.0 (licencas.md: incerto p/ derivados).
Atenção: `pub_date` do WFS é uniforme (data de recarga) — NÃO serve como data de publicação por ciclo.
"""
from __future__ import annotations

import argparse
import datetime as dt
from pathlib import Path

from agrorisk.fontes._comum import RAW, baixar_wfs, gravar_manifesto

URL = "https://terrabrasilis.dpi.inpe.br/geoserver/ows"
CAMADAS = ["prodes-cerrado-nb", "prodes-mata-atlantica-nb"]


def baixar(bbox: str, data: str, raiz: Path = RAW / "prodes") -> Path:
    pasta = raiz / data
    regs = [baixar_wfs(URL, f"{c}:yearly_deforestation", pasta / f"{c}.geojson", bbox=bbox, pagina=2000, ordenar="uuid")
            for c in CAMADAS]
    gravar_manifesto(pasta, regs, {"bbox": bbox})
    return pasta


if __name__ == "__main__":
    from agrorisk.fontes.snapshot import BBOX_VITRINE
    ap = argparse.ArgumentParser(); ap.add_argument("--bbox", default=BBOX_VITRINE); ap.add_argument("--data", default=dt.date.today().isoformat())
    a = ap.parse_args(); print(baixar(a.bbox, a.data))
