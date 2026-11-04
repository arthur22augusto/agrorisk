"""Ponto de entrada do pipeline piloto (sessão 07).

python -m agrorisk.pipeline --etapa baixar|gate|painel|todas --recorte vitrine|treino [--data AAAA-MM-DD]
Ordem: baixar (snapshot CAR+Sisema, PRODES, SIGMINE, IBGE urbano) -> gate (Y e pickles intermediários) -> painel (parquet).
Cada etapa é idempotente nos downloads (pula o que já existe com manifesto). Dados ficam em data/ (fora do git).
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path


def baixar(recorte: str, data: str) -> None:
    from agrorisk.fontes import ibge_urbano, prodes, sigmine, snapshot
    snapshot.snapshot(recorte, data)
    man = json.loads((Path("data/raw/snapshots") / data / recorte / "manifest.json").read_text())
    bbox = man["bbox_sisema"]; y0, x0, y1, x1 = map(float, bbox.split(",")[:4])
    sufixo = data if recorte == "vitrine" else f"{data}-treino"  # o gate espera esta convenção (gate._ext)
    prodes.baixar(bbox, sufixo)
    sigmine.baixar((x0, y0, x1, y1), sufixo)
    ibge_urbano.baixar(data)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--etapa", choices=["baixar", "gate", "painel", "todas"], default="todas")
    ap.add_argument("--recorte", choices=["vitrine", "treino"], default="vitrine")
    ap.add_argument("--data", default=dt.date.today().isoformat(), help="data do snapshot/downloads (AAAA-MM-DD)")
    a = ap.parse_args()
    if a.etapa in ("baixar", "todas"): baixar(a.recorte, a.data)
    if a.etapa in ("gate", "todas"):
        from agrorisk import gate; gate.rodar(a.recorte, a.data)
    if a.etapa in ("painel", "todas"):
        from agrorisk import painel; painel.construir(a.recorte, a.data)


if __name__ == "__main__":
    main()
