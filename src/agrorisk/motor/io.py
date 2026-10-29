"""Leitura/gravação do motor: diretório (Parquet/CSV) ou banco via SQLAlchemy. Não depende do Django."""
from __future__ import annotations

import os
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

from .erros import ErroConexao, ErroEntrada

T_INDICADORES, T_UNIDADES, T_OPERACOES = "motor_indicadores", "motor_unidades", "motor_operacoes"
T_RESULTADOS, T_DETALHES = "motor_resultados", "motor_resultados_detalhes"
CHAVE_RESULTADOS = ["unidade_id", "data_corte", "evento", "versao_modelo"]
CHAVE_DETALHES = CHAVE_RESULTADOS + ["fator"]
_ARQ = {T_INDICADORES: "indicadores", T_UNIDADES: "unidades", T_OPERACOES: "operacoes",
        T_RESULTADOS: "resultados", T_DETALHES: "resultados_detalhes"}


def _eh_banco(destino: str) -> bool:
    return destino == "db" or "://" in destino


def _engine(destino: str):
    url = os.environ.get("AGRORISK_DB_URL") if destino == "db" else destino
    if not url:
        raise ErroConexao("AGRORISK_DB_URL não definida")
    try:
        return create_engine(url)
    except (SQLAlchemyError, ImportError, ValueError) as e:
        raise ErroConexao(f"URL de banco inválida: {e}") from e


def _arquivo(pasta: Path, tabela: str) -> Path | None:
    base = _ARQ[tabela]
    for ext in (".parquet", ".csv"):
        if (pasta / f"{base}{ext}").exists():
            return pasta / f"{base}{ext}"
    return None


def _ler_arq(p: Path) -> pd.DataFrame:
    return pd.read_parquet(p) if p.suffix == ".parquet" else pd.read_csv(p, dtype={"unidade_id": str})


def ler(entrada: str, tabela: str, obrigatoria: bool = True) -> pd.DataFrame | None:
    if _eh_banco(entrada):
        try:
            with _engine(entrada).connect() as con:
                return pd.read_sql_table(tabela, con)
        except ValueError as e:  # tabela inexistente
            if obrigatoria:
                raise ErroEntrada(f"tabela {tabela} não encontrada") from e
            return None
        except SQLAlchemyError as e:
            raise ErroConexao(f"erro lendo {tabela}: {e}") from e
    arq = _arquivo(Path(entrada), tabela)
    if arq is None:
        if obrigatoria:
            raise ErroEntrada(f"{_ARQ[tabela]}.parquet|csv não encontrado em {entrada}")
        return None
    return _ler_arq(arq)


def _norm_chave(df: pd.DataFrame, cols) -> pd.Series:
    return df[cols].astype(str).agg("|".join, axis=1)


def _upsert_arquivo(pasta: Path, tabela: str, novo: pd.DataFrame, chave: list[str]) -> None:
    pasta.mkdir(parents=True, exist_ok=True)
    arq = _arquivo(pasta, tabela) or pasta / f"{_ARQ[tabela]}.parquet"
    novo = novo.copy()
    for c in novo.columns:
        if novo[c].map(lambda v: hasattr(v, "isoformat")).any():
            novo[c] = novo[c].map(lambda v: v.isoformat() if hasattr(v, "isoformat") else v)
    if arq.exists():
        antigo = _ler_arq(arq)
        antigo = antigo[~_norm_chave(antigo, chave).isin(set(_norm_chave(novo, chave)))]
        novo = pd.concat([antigo, novo], ignore_index=True)
    if arq.suffix == ".parquet":
        novo.to_parquet(arq, index=False)
    else:
        novo.to_csv(arq, index=False)


def _upsert_banco(destino: str, tabela: str, novo: pd.DataFrame, chave: list[str]) -> None:
    eng = _engine(destino)
    try:
        with eng.begin() as con:  # transação única: ou grava tudo ou nada
            existe = con.dialect.has_table(con, tabela)
            if existe:
                tmp = novo[chave].drop_duplicates()
                cond = " AND ".join(f"{c} = :{c}" for c in chave)
                con.execute(text(f"DELETE FROM {tabela} WHERE {cond}"),
                            tmp.to_dict("records"))
            novo.to_sql(tabela, con, if_exists="append", index=False)
            cols = ", ".join(chave)
            con.execute(text(f"CREATE UNIQUE INDEX IF NOT EXISTS ux_{tabela} ON {tabela} ({cols})"))
    except SQLAlchemyError as e:
        raise ErroConexao(f"erro gravando {tabela}: {e}") from e


def gravar(saida: str, resultados: pd.DataFrame, detalhes: pd.DataFrame) -> None:
    """Upsert idempotente: chave (unidade_id, data_corte, evento, versao_modelo) [+ fator nos detalhes]."""
    for tabela, df, chave in ((T_RESULTADOS, resultados, CHAVE_RESULTADOS), (T_DETALHES, detalhes, CHAVE_DETALHES)):
        if _eh_banco(saida):
            _upsert_banco(saida, tabela, df, chave)
        else:
            _upsert_arquivo(Path(saida), tabela, df, chave)
