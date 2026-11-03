"""Catálogo de fatores do stub: coluna de entrada, transformação, padronização, coeficiente e proveniência.

⚠️ Depende da sessão 06: o conjunto de fatores e os coeficientes mudam com o Y e a unidade finais.
Os coeficientes do stub NÃO são estimados: são arbitrários, com os sinais esperados.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

import numpy as np


@dataclass(frozen=True)
class Fator:
    nome: str
    coluna: str
    unidade: str
    transformacao: Callable[[np.ndarray], np.ndarray]
    media: float  # da variável transformada
    dp: float
    coef_stub: float  # log-odds por desvio-padrão
    fonte: str
    defasagem_publicacao_dias: int  # dias entre o fim do ano de referência e a publicação
    texto_alto: str
    texto_baixo: str


def _id(x):
    return x


def _log1p(x):
    return np.log1p(x)


def _log(x):
    return np.log(np.maximum(x, 0.05))


FATORES: tuple[Fator, ...] = (
    Fator("supressao_vizinhanca", "supressao_viz_ha_3a", "ha", _log1p, 0.9, 0.9, 0.9,
          "MapBiomas Desmatamento (sintético)", 270,
          "Supressão recente na vizinhança do imóvel acima do típico.",
          "Pouca supressão recente na vizinhança."),
    Fator("vegetacao_nativa", "pct_veg_nativa", "%", _id, 35.0, 20.0, 0.5,
          "MapBiomas Cobertura (sintético)", 270,
          "Muita vegetação nativa remanescente (mais área passível de supressão).",
          "Pouca vegetação nativa remanescente."),
    Fator("distancia_urbano", "dist_urbano_km", "km", _log, 1.6, 0.9, -0.4,
          "MapBiomas Cobertura, classe urbana (sintético)", 270,
          "Distante de área urbana.", "Próximo de área urbana (pressão de expansão)."),
    Fator("distancia_mineracao", "dist_mineracao_km", "km", _log, 2.0, 0.9, -0.2,
          "MapBiomas Cobertura, classe mineração (sintético)", 270,
          "Distante de mineração.", "Próximo de mineração."),
    Fator("sobreposicao_uc", "sobreposicao_uc_pct", "%", _id, 15.0, 30.0, -0.6,
          "CNUC/IDE-Sisema (sintético)", 180,
          "Grande sobreposição com unidade de conservação (fiscalização mais intensa).",
          "Sem sobreposição relevante com unidade de conservação."),
    Fator("chuva_anual", "chuva_anual_mm", "mm", _id, 1400.0, 200.0, -0.15,
          "CHIRPS (sintético)", 30,
          "Ano chuvoso.", "Ano seco."),
)

COLUNAS_INDICADORES = tuple(f.coluna for f in FATORES)


def padronizar(f: Fator, x: np.ndarray) -> np.ndarray:
    return (f.transformacao(np.asarray(x, dtype=float)) - f.media) / f.dp
