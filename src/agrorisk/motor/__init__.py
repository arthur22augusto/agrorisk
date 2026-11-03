"""Motor estatístico do AgroRisk (v1: stub). Contrato: docs/produto/contrato-motor-v1.md."""
from .erros import (ErroConexao, ErroEntrada, ErroModelo, ErroVazamentoTemporal, MotorErro)
from .stub import (Saida, calcular_faixa, calcular_score, hash_snapshot, pontuar, porte_classe, saldo_na_data,
                   validar_rotulos_piloto)
from .versao import versao_modelo

__all__ = ["pontuar", "Saida", "calcular_score", "calcular_faixa", "porte_classe", "saldo_na_data", "hash_snapshot",
           "validar_rotulos_piloto", "versao_modelo",
           "MotorErro", "ErroEntrada", "ErroConexao", "ErroVazamentoTemporal", "ErroModelo"]
