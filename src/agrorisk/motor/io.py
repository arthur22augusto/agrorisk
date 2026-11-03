"""Leitura/gravação do motor: diretório (Parquet/CSV) ou banco via SQLAlchemy. Não depende do Django."""
from __future__ import annotations

import os
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

from .erros import ErroConexao, ErroEntrada

T_INDICADORES, T_UNIDADES, T_OPERACOES = "motor_indicadores", "motor_unidades", "motor_operacoes"
T_VERIFICACOES, T_ROTULOS = "motor_verificacoes", "motor_rotulos_piloto"  # entradas (verificações vêm do pipeline)
T_RESULTADOS, T_DETALHES = "motor_resultados", "motor_resultados_detalhes"
T_RES_VERIFICACOES = "motor_resultados_verificacoes"  # saída: verificações auditadas
CHAVE_RESULTADOS = ["unidade_id", "data_corte", "y_definicao", "versao_modelo"]
CHAVE_DETALHES = CHAVE_RESULTADOS + ["fator"]
CHAVE_RES_VERIFICACOES = ["unidade_id", "data_corte", "regra", "fonte", "hash_fonte"]
_ARQ = {T_INDICADORES: "indicadores", T_UNIDADES: "unidades", T_OPERACOES: "operacoes",
        T_VERIFICACOES: "verificacoes", T_ROTULOS: "rotulos_piloto",
        T_RESULTADOS: "resultados", T_DETALHES: "resultados_detalhes", T_RES_VERIFICACOES: "resultados_verificacoes"}
_TEXTO = {"unidade_id": str, "operacao_id": str, "municipio_ibge": str, "car_codigo": str}


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
    return pd.read_parquet(p) if p.suffix == ".parquet" else pd.read_csv(p, dtype=_TEXTO)


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


def _upsert_banco(con, tabela: str, novo: pd.DataFrame, chave: list[str]) -> None:
    if con.dialect.has_table(con, tabela):
        tmp = novo[chave].drop_duplicates()
        if len(tmp):
            cond = " AND ".join(f"{c} = :{c}" for c in chave)
            con.execute(text(f"DELETE FROM {tabela} WHERE {cond}"), tmp.to_dict("records"))
    novo.to_sql(tabela, con, if_exists="append", index=False)
    con.execute(text(f"CREATE UNIQUE INDEX IF NOT EXISTS ux_{tabela} ON {tabela} ({', '.join(chave)})"))


def gravar(saida: str, resultados: pd.DataFrame, detalhes: pd.DataFrame, verificacoes: pd.DataFrame) -> None:
    """Upsert idempotente das 3 tabelas de saída. No banco, UMA transação: ou grava tudo ou nada."""
    lote = ((T_RESULTADOS, resultados, CHAVE_RESULTADOS), (T_DETALHES, detalhes, CHAVE_DETALHES),
            (T_RES_VERIFICACOES, verificacoes, CHAVE_RES_VERIFICACOES))
    if _eh_banco(saida):
        try:
            with _engine(saida).begin() as con:
                for tabela, df, chave in lote:
                    _upsert_banco(con, tabela, df, chave)
        except SQLAlchemyError as e:
            raise ErroConexao(f"erro gravando saída: {e}") from e
    else:
        for tabela, df, chave in lote:
            _upsert_arquivo(Path(saida), tabela, df, chave)
