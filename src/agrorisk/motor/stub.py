"""Stub do motor: mesmo formato do motor real, números de mentira (determinísticos).

p = sigmoid(intercepto + soma(coef * z)) + ruído determinístico por (unidade_id, semente).
O intercepto é calibrado para a média de p no lote ≈ taxa_base (o lote inteiro tem a mesma taxa).
"""
from __future__ import annotations

import hashlib
import json
from datetime import date, datetime, timedelta

import numpy as np
import pandas as pd

from . import fatores as ft
from .erros import ErroEntrada, ErroVazamentoTemporal
from .versao import versao_modelo

SEMENTE = 20261029
TAXA_BASE_PADRAO = 0.02
EVENTO_PADRAO = "supressao_vegetacao"  # ⚠️ 06 define o Y
HORIZONTE_PADRAO = 12  # ⚠️ 06
FAIXAS = (("A", 0.5), ("B", 1.0), ("C", 2.0), ("D", 4.0))  # limite superior em múltiplos da taxa-base
AVISO_IMOVEL_INTEIRO = (
    "Indicadores calculados sobre o imóvel inteiro (gleba não informada): "
    "o risco da área financiada pode estar sobre/subestimado."
)
TIPOS_UNIDADE = ("gleba", "imovel", "fornecedor")
NIVEIS = ("gleba", "imovel_inteiro")


def calcular_score(p):
    """score = round(1000·(1−p)), arredondamento meio-para-cima (igual ao round() do Postgres para positivos)."""
    return np.floor(1000.0 * (1.0 - np.asarray(p, dtype=float)) + 0.5).astype(int)


def calcular_faixa(p, taxa_base: float = TAXA_BASE_PADRAO):
    """A ≤0,5×; B ≤1×; C ≤2×; D ≤4×; E >4× a taxa-base (limites superiores inclusivos)."""
    razao = np.asarray(p, dtype=float) / taxa_base
    faixa = np.full(razao.shape, "E", dtype=object)
    for letra, lim in reversed(FAIXAS):
        faixa[razao <= lim + 1e-12] = letra
    return faixa


def _ruido(ids: pd.Series, semente: int) -> np.ndarray:
    def u(i):
        h = hashlib.sha256(f"{semente}:{i}".encode()).digest()
        return int.from_bytes(h[:8], "big") / 2**64
    return np.array([(u(i) - 0.5) * 0.6 for i in ids])  # ruído uniforme ±0,3 log-odds


def _validar(indicadores: pd.DataFrame, unidades: pd.DataFrame) -> None:
    falt = {"unidade_id", "data_corte", *ft.COLUNAS_INDICADORES} - set(indicadores.columns)
    if falt:
        raise ErroEntrada(f"indicadores: colunas ausentes {sorted(falt)}")
    falt = {"unidade_id", "tipo_unidade", "nivel_espacial"} - set(unidades.columns)
    if falt:
        raise ErroEntrada(f"unidades: colunas ausentes {sorted(falt)}")
    if unidades["unidade_id"].duplicated().any():
        raise ErroEntrada("unidades: unidade_id duplicado")
    if indicadores.duplicated(["unidade_id", "data_corte"]).any():
        raise ErroEntrada("indicadores: (unidade_id, data_corte) duplicado")
    if not set(unidades["tipo_unidade"]) <= set(TIPOS_UNIDADE):
        raise ErroEntrada(f"tipo_unidade deve estar em {TIPOS_UNIDADE}")
    if not set(unidades["nivel_espacial"]) <= set(NIVEIS):
        raise ErroEntrada(f"nivel_espacial deve estar em {NIVEIS}")
    nulos = indicadores[list(ft.COLUNAS_INDICADORES)].isna().any(axis=1)
    if nulos.any():
        raise ErroEntrada(f"indicadores: {int(nulos.sum())} linha(s) com valor nulo")


def _referencias(f: ft.Fator, corte: date) -> tuple[date, date]:
    """Último ano de referência cuja publicação (fim do ano + defasagem) é ≤ corte."""
    ano = corte.year
    while True:
        pub = date(ano, 12, 31) + timedelta(days=f.defasagem_publicacao_dias)
        if pub <= corte:
            return date(ano, 12, 31), pub
        ano -= 1


def pontuar(
    indicadores: pd.DataFrame,
    unidades: pd.DataFrame,
    data_corte,
    *,
    evento: str = EVENTO_PADRAO,
    horizonte_meses: int = HORIZONTE_PADRAO,
    taxa_base: float = TAXA_BASE_PADRAO,
    versoes_dados: dict | None = None,
    semente: int = SEMENTE,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Retorna (resultados, detalhes). Ver docs/produto/contrato-motor-v0.md."""
    corte = pd.Timestamp(data_corte).date()
    _validar(indicadores, unidades)
    ind = indicadores.copy()
    ind["data_corte"] = pd.to_datetime(ind["data_corte"]).dt.date
    ind = ind[ind["data_corte"] == corte].merge(unidades, on="unidade_id", how="inner", validate="one_to_one")
    if ind.empty:
        raise ErroEntrada(f"nenhum indicador para data_corte={corte} com unidade correspondente")

    refs = {f.nome: _referencias(f, corte) for f in ft.FATORES}
    for nome, (_, pub) in refs.items():  # defesa em profundidade: nunca deveria disparar
        if pub > corte:
            raise ErroVazamentoTemporal(f"{nome}: publicação {pub} > corte {corte}")

    ind = ind.sort_values("unidade_id").reset_index(drop=True)
    z = np.column_stack([ft.padronizar(f, ind[f.coluna].to_numpy()) for f in ft.FATORES])
    coef = np.array([f.coef_stub for f in ft.FATORES])
    eta = z @ coef + _ruido(ind["unidade_id"], semente)
    # calibra o intercepto (bisseção) para média de p = taxa_base
    lo, hi = -15.0, 5.0
    for _ in range(80):
        mid = (lo + hi) / 2
        if (1 / (1 + np.exp(-(eta + mid)))).mean() > taxa_base:
            hi = mid
        else:
            lo = mid
    p = 1 / (1 + np.exp(-(eta + (lo + hi) / 2)))
    contrib = z * coef  # log-odds

    valor = ind["valor_exposto"].astype(float) if "valor_exposto" in ind else pd.Series(np.nan, index=ind.index)
    versao = versao_modelo()
    vd = json.dumps(versoes_dados or {}, sort_keys=True, ensure_ascii=False)
    aviso = np.where(ind["nivel_espacial"] == "imovel_inteiro", AVISO_IMOVEL_INTEIRO, None)

    res = pd.DataFrame({
        "unidade_id": ind["unidade_id"], "tipo_unidade": ind["tipo_unidade"],
        "data_corte": corte, "evento": evento, "horizonte_meses": int(horizonte_meses),
        "versao_modelo": versao, "p": p, "score": calcular_score(p),
        "faixa": calcular_faixa(p, taxa_base), "taxa_base": taxa_base,
        "valor_exposto": valor, "exposicao_esperada": p * valor,
        "nivel_espacial": ind["nivel_espacial"], "aviso": aviso,
        "versoes_dados": vd, "calculado_em": datetime.now().replace(microsecond=0).isoformat(),
    })

    linhas = []
    for j, f in enumerate(ft.FATORES):
        ref, pub = refs[f.nome]
        direcao = np.where(contrib[:, j] > 0.05, "aumenta_risco", np.where(contrib[:, j] < -0.05, "reduz_risco", "neutro"))
        texto = np.where(contrib[:, j] >= 0, f.texto_alto if f.coef_stub > 0 else f.texto_baixo,
                         f.texto_baixo if f.coef_stub > 0 else f.texto_alto)
        linhas.append(pd.DataFrame({
            "unidade_id": ind["unidade_id"], "data_corte": corte, "evento": evento, "versao_modelo": versao,
            "fator": f.nome, "valor": ind[f.coluna].astype(float), "unidade": f.unidade,
            "contribuicao": contrib[:, j], "direcao": direcao, "fonte": f.fonte,
            "data_referencia": ref, "data_publicacao": pub, "texto": texto,
        }))
    det = pd.concat(linhas, ignore_index=True)
    det["_abs"] = det["contribuicao"].abs()
    det = det.sort_values(["unidade_id", "_abs"], ascending=[True, False]).drop(columns="_abs")
    det["ordem"] = det.groupby("unidade_id").cumcount() + 1
    return res.reset_index(drop=True), det.reset_index(drop=True)


def exposicao_na_data(operacoes: pd.DataFrame, data_corte) -> pd.Series:
    """Soma de valor_rs das operações vigentes em data_corte (data_inicio ≤ corte < data_fim), por unidade_id."""
    corte = pd.Timestamp(data_corte)
    o = operacoes.copy()
    ini, fim = pd.to_datetime(o["data_inicio"]), pd.to_datetime(o["data_fim"])
    return o[(ini <= corte) & (corte < fim)].groupby("unidade_id")["valor_rs"].sum().rename("valor_exposto")
