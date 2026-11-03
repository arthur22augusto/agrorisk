"""CLI: python -m agrorisk.motor --entrada <dir|db> --saida <dir|db>  (códigos de saída em erros.py)."""
from __future__ import annotations

import argparse
import sys

import pandas as pd

from . import io
from .erros import MotorErro
from .erros import ErroEntrada
from .stub import HORIZONTE_PADRAO, TAXAS_BASE_PADRAO, Y_PADRAO, pontuar, validar_rotulos_piloto


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="python -m agrorisk.motor", description=__doc__)
    ap.add_argument("--entrada", required=True, help="diretório com Parquet/CSV, URL SQLAlchemy ou 'db' (AGRORISK_DB_URL)")
    ap.add_argument("--saida", required=True, help="idem")
    ap.add_argument("--data-corte", help="AAAA-MM-DD, sempre 31/jul (padrão: maior data_corte dos indicadores)")
    ap.add_argument("--y-definicao", default=Y_PADRAO)
    ap.add_argument("--horizonte-meses", type=int, default=HORIZONTE_PADRAO)
    ap.add_argument("--taxas-base", default=",".join(f"{k}={v}" for k, v in TAXAS_BASE_PADRAO.items()),
                    help="taxa-base por nível, ex.: poligono=0.02,imovel_inteiro=0.04")
    ap.add_argument("--peso-indeterminado", type=float, default=1.0,
                    help="peso de bloqueio de verificação com status 'indeterminado' (0–1; 1 = limite superior)")
    a = ap.parse_args(argv)
    try:
        ind = io.ler(a.entrada, io.T_INDICADORES)
        uni = io.ler(a.entrada, io.T_UNIDADES)
        ops = io.ler(a.entrada, io.T_OPERACOES, obrigatoria=False)
        ver = io.ler(a.entrada, io.T_VERIFICACOES, obrigatoria=False)
        rot = io.ler(a.entrada, io.T_ROTULOS, obrigatoria=False)
        if rot is not None:
            validar_rotulos_piloto(rot)  # opcional; o motor não usa o rótulo para pontuar
        corte = a.data_corte or str(pd.to_datetime(ind["data_corte"]).max().date())
        try:
            taxas = {k: float(v) for k, v in (kv.split("=") for kv in a.taxas_base.split(","))}
        except ValueError as e:
            raise ErroEntrada(f"--taxas-base inválido: {a.taxas_base!r}") from e
        res, det, ver_out = pontuar(ind, uni, corte, verificacoes=ver, operacoes=ops, y_definicao=a.y_definicao,
                                    horizonte_meses=a.horizonte_meses, taxas_base=taxas,
                                    peso_indeterminado=a.peso_indeterminado)
        io.gravar(a.saida, res, det, ver_out)
    except MotorErro as e:
        print(f"{type(e).__name__}: {e}", file=sys.stderr)
        return e.codigo_saida
    aviso = "" if ver is not None else " [ATENÇÃO: sem tabela de verificações; vedações não avaliadas]"
    print(f"ok: {len(res)} unidades pontuadas (data_corte={corte}, versao_modelo={res['versao_modelo'].iloc[0]}){aviso}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
