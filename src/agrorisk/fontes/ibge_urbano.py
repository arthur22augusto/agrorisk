"""IBGE Áreas Urbanizadas do Brasil 2022 (shapefile nacional, ~54 MB) -> data/raw/ibge_urbano/<data>/. Idempotente, com hash.
Usado como proxy de destino urbano (MapBiomas bloqueado na nuvem). Produz manifest.json."""
from __future__ import annotations

import argparse
import datetime as dt
import subprocess
from pathlib import Path

from agrorisk.fontes._comum import RAW, gravar_manifesto, sha256_arquivo

URL = ("https://geoftp.ibge.gov.br/organizacao_do_territorio/tipologias_do_territorio/areas_urbanizadas_do_brasil/"
       "2022/Shapefile/AreasUrbanizadas2022_Brasil.zip")


def baixar(data: str, raiz: Path = RAW / "ibge_urbano") -> Path:
    pasta = raiz / data; pasta.mkdir(parents=True, exist_ok=True)
    z = pasta / "AreasUrbanizadas2022_Brasil.zip"
    if not z.exists():
        subprocess.run(["curl", "-s", "-f", "-m", "600", "-o", str(z), URL], check=True)
    gravar_manifesto(pasta, [{"arquivo": z.name, "camada": "ibge_urbanizadas_2022", "url": URL, "n_feicoes": -1, "sha256": sha256_arquivo(z)}])
    return pasta


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--data", default=dt.date.today().isoformat())
    print(baixar(ap.parse_args().data))
