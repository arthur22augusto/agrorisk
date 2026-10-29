"""Exceções tipadas do motor e seus códigos de saída (ver docs/produto/contrato-motor-v0.md)."""


class MotorErro(Exception):
    """Base de todos os erros do motor. `codigo_saida` é usado pela CLI."""

    codigo_saida = 1


class ErroEntrada(MotorErro):
    """Tabela/coluna ausente, tipo inválido, chave duplicada ou valor fora de faixa."""

    codigo_saida = 2


class ErroConexao(MotorErro):
    """Falha ao conectar, ler ou gravar no banco (AGRORISK_DB_URL)."""

    codigo_saida = 3


class ErroVazamentoTemporal(MotorErro):
    """Indicador com data de publicação posterior à data de corte."""

    codigo_saida = 4


class ErroModelo(MotorErro):
    """Modelo treinado ausente ou incompatível (AGRORISK_MODELO_DIR). O stub não usa modelo."""

    codigo_saida = 5
