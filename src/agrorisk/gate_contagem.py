"""Gate (g): nº de eventos PRODES >= 1 ha contíguo por CAR e ano no recorte de treino (versão enxuta de `gate.py`: só contagem).
Consome o snapshot do CAR e o PRODES do treino; produz reports/07-gate/eventos_por_ano_<recorte>.csv. Uso: python -m agrorisk.gate_contagem --recorte treino"""
from __future__ import annotations

import argparse
import time
from pathlib import Path

from agrorisk.gate import _ext, carrega_car, carrega_prodes, eventos


def contar(recorte: str, data: str) -> None:
    t = time.time()
    car = carrega_car(Path("data/raw/snapshots") / data / recorte / "car"); print("CAR", len(car), round(time.time() - t), "s", flush=True)
    prodes = carrega_prodes(_ext("prodes", data, recorte)); print("PRODES", len(prodes), round(time.time() - t), "s", flush=True)
    ev = eventos(car, prodes); print("eventos", len(ev), round(time.time() - t), "s", flush=True)
    ev["pos"] = ev.ha_contiguo >= 1.0
    out = ev.groupby("year").agg(imoveis_qualquer_ha=("cod_imovel", "size"), imoveis_ge_1ha=("pos", "sum"))
    out.to_csv(f"reports/07-gate/eventos_por_ano_{recorte}.csv"); print(out.to_string())


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--recorte", default="treino"); ap.add_argument("--data", default="2026-11-03")
    a = ap.parse_args(); contar(a.recorte, a.data)
