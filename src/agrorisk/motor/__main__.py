"""CLI: python -m agrorisk.motor --entrada <dir|db> --saida <dir|db>  (códigos de saída em erros.py)."""
from __future__ import annotations

import argparse
import sys

import pandas as pd

from . import io
from .erros import MotorErro
from .stub import EVENTO_PADRAO, HORIZONTE_PADRAO, TAXA_BASE_PADRAO, exposicao_na_data, pontuar


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="python -m agrorisk.motor", description=__doc__)
    ap.add_argument("--entrada", required=True, help="diretório com Parquet/CSV, URL SQLAlchemy ou 'db' (AGRORISK_DB_URL)")
    ap.add_argument("--saida", required=True, help="idem")
    ap.add_argument("--data-corte", help="AAAA-MM-DD (padrão: maior data_corte dos indicadores)")
    ap.add_argument("--evento", default=EVENTO_PADRAO)
    ap.add_argument("--horizonte-meses", type=int, default=HORIZONTE_PADRAO)
    ap.add_argument("--taxa-base", type=float, default=TAXA_BASE_PADRAO)
    a = ap.parse_args(argv)
    try:
        ind = io.ler(a.entrada, io.T_INDICADORES)
        uni = io.ler(a.entrada, io.T_UNIDADES)
        ops = io.ler(a.entrada, io.T_OPERACOES, obrigatoria=False)
        corte = a.data_corte or str(pd.to_datetime(ind["data_corte"]).max().date())
        if ops is not None and "valor_exposto" not in uni.columns:
            uni = uni.merge(exposicao_na_data(ops, corte), on="unidade_id", how="left")
        res, det = pontuar(ind, uni, corte, evento=a.evento, horizonte_meses=a.horizonte_meses,
                           taxa_base=a.taxa_base, versoes_dados={"origem": "cli"})
        io.gravar(a.saida, res, det)
    except MotorErro as e:
        print(f"{type(e).__name__}: {e}", file=sys.stderr)
        return e.codigo_saida
    print(f"ok: {len(res)} unidades pontuadas (data_corte={corte}, versao_modelo={res['versao_modelo'].iloc[0]})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
