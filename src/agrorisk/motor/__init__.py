"""Motor estatístico do AgroRisk (v0: stub). Contrato: docs/produto/contrato-motor-v0.md."""
from .erros import (ErroConexao, ErroEntrada, ErroModelo, ErroVazamentoTemporal, MotorErro)
from .stub import calcular_faixa, calcular_score, exposicao_na_data, pontuar
from .versao import versao_modelo

__all__ = ["pontuar", "calcular_score", "calcular_faixa", "exposicao_na_data", "versao_modelo",
           "MotorErro", "ErroEntrada", "ErroConexao", "ErroVazamentoTemporal", "ErroModelo"]
