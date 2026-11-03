"""Stub do motor v1: mesmo formato do motor real, números de mentira (determinísticos).

Duas camadas separadas (decisão `docs/decisoes/escopo-mvp.md`):
  1. verificações determinísticas (vedação): vêm prontas do pipeline na tabela `verificacoes`; o motor valida,
     audita (fonte, data_publicacao, hash) e calcula só a mecânica de bloqueio. Vedação NÃO entra em p.
  2. risco: p = sigmoid(intercepto + soma(coef * z)) + ruído determinístico por (unidade_id, semente).
     O intercepto é calibrado por `nivel_espacial` para média de p = taxa-base do nível.
Contrato: docs/produto/contrato-motor-v1.md.
"""
from __future__ import annotations

import hashlib
import json
import re
from datetime import date, datetime, timedelta
from typing import NamedTuple

import numpy as np
import pandas as pd

from . import fatores as ft
from .erros import ErroEntrada, ErroVazamentoTemporal
from .versao import versao_modelo

SEMENTE = 20261029
Y_PADRAO = "Y_total"
Y_DEFINICOES = (Y_PADRAO,)  # Y_ilegal e Y_agro são derivados reportados, não previstos (decisão 06, §2)
HORIZONTE_PADRAO = 12  # único horizonte aceito no v1; 24 meses é descritivo e fora do motor
TAXAS_BASE_PADRAO = {"poligono": 0.02, "imovel_inteiro": 0.04}  # stub: números de mentira, uma taxa por nível
FAIXAS = (("A", 0.5), ("B", 1.0), ("C", 2.0), ("D", 4.0))  # limite superior em múltiplos da taxa-base do nível
AVISO_IMOVEL_INTEIRO = (
    "Evento no imóvel: indicadores e p calculados sobre o imóvel inteiro (polígono financiado não informado). "
    "P(evento em qualquer parte do imóvel) cresce com a área; não comparar com resultados de nível polígono."
)
TIPOS_UNIDADE = ("car", "gleba")
NIVEIS = ("poligono", "imovel_inteiro")
TIPO_PARA_NIVEL = {"car": "imovel_inteiro", "gleba": "poligono"}
STATUS_JURIDICO = ("detectado", "autorizado", "sem_autorizacao_identificada", "indeterminado")
EFEITOS = ("bloqueia", "alerta")
COLUNAS_PROIBIDAS = {"cpf", "cnpj", "nome", "nome_produtor", "razao_social", "rg", "email", "telefone"}  # LGPD
RE_CAR = re.compile(r"^[A-Z]{2}-\d{7}-[0-9A-Fa-f]{32}$")
RE_HASH = re.compile(r"^[0-9a-f]{64}$")
RE_REGRA = re.compile(r"^[a-z][a-z0-9_]*$")

COLS_UNIDADES = ("unidade_id", "tipo_unidade", "nivel_espacial", "car_codigo", "porte_modulos_fiscais")
COLS_OPERACOES = ("operacao_id", "unidade_id", "car_codigo", "tipo_operacao", "programa", "valor_rs",
                  "data_contrato", "data_vencimento")
COLS_VERIFICACOES = ("unidade_id", "data_corte", "regra", "efeito", "status_juridico", "fonte", "data_referencia",
                     "data_publicacao", "hash_fonte", "texto")
COLS_ROTULOS = ("operacao_id", "data_corte", "y3_atraso_90d", "data_registro")


class Saida(NamedTuple):
    resultados: pd.DataFrame
    detalhes: pd.DataFrame
    verificacoes: pd.DataFrame


def calcular_score(p):
    """score = round(1000·(1−p)), arredondamento meio-para-cima (igual ao round() do Postgres para positivos)."""
    return np.floor(1000.0 * (1.0 - np.asarray(p, dtype=float)) + 0.5).astype(int)


def calcular_faixa(p, taxa_base=0.02):
    """A ≤0,5×; B ≤1×; C ≤2×; D ≤4×; E >4× a taxa-base (limites superiores inclusivos).

    `taxa_base` é escalar ou array (uma taxa por linha: a do `nivel_espacial` da unidade).
    """
    razao = np.asarray(p, dtype=float) / np.asarray(taxa_base, dtype=float)
    faixa = np.full(razao.shape, "E", dtype=object)
    for letra, lim in reversed(FAIXAS):
        faixa[razao <= lim + 1e-12] = letra
    return faixa


def porte_classe(modulos_fiscais):
    """≤ 4 MF, (4, 15], > 15 (recortes de reporte da decisão 06)."""
    mf = np.asarray(modulos_fiscais, dtype=float)
    return np.where(mf <= 4, "ate_4_mf", np.where(mf <= 15, "4_a_15_mf", "acima_15_mf"))


def _ruido(ids: pd.Series, semente: int) -> np.ndarray:
    def u(i):
        h = hashlib.sha256(f"{semente}:{i}".encode()).digest()
        return int.from_bytes(h[:8], "big") / 2**64
    return np.array([(u(i) - 0.5) * 0.6 for i in ids])  # ruído uniforme ±0,3 log-odds


def _datas(df: pd.DataFrame, cols) -> pd.DataFrame:
    df = df.copy()
    for c in cols:
        df[c] = pd.to_datetime(df[c]).dt.date
    return df


def hash_snapshot(**tabelas: pd.DataFrame | None) -> str:
    """SHA-256 do conteúdo lógico das tabelas de entrada (colunas e linhas ordenadas, tudo como texto)."""
    h = hashlib.sha256()
    for nome in sorted(tabelas):
        h.update(f"#{nome}\n".encode())
        df = tabelas[nome]
        if df is None:
            h.update(b"<ausente>\n")
            continue
        d = df[sorted(df.columns)].astype(str)
        d = d.sort_values(list(d.columns), kind="stable").reset_index(drop=True)
        h.update(d.to_csv(index=False).encode())
    return h.hexdigest()


def _sem_dados_pessoais(**tabelas) -> None:
    for nome, df in tabelas.items():
        if df is not None:
            ruins = sorted(c for c in df.columns if str(c).lower() in COLUNAS_PROIBIDAS)
            if ruins:
                raise ErroEntrada(f"{nome}: colunas com dado pessoal não são aceitas (LGPD): {ruins}")


def _exigir(df: pd.DataFrame, nome: str, cols) -> None:
    falt = set(cols) - set(df.columns)
    if falt:
        raise ErroEntrada(f"{nome}: colunas ausentes {sorted(falt)}")


def _validar(indicadores: pd.DataFrame, unidades: pd.DataFrame) -> None:
    _exigir(indicadores, "indicadores", {"unidade_id", "data_corte", *ft.COLUNAS_INDICADORES})
    _exigir(unidades, "unidades", COLS_UNIDADES)
    if unidades["unidade_id"].duplicated().any():
        raise ErroEntrada("unidades: unidade_id duplicado")
    if indicadores.duplicated(["unidade_id", "data_corte"]).any():
        raise ErroEntrada("indicadores: (unidade_id, data_corte) duplicado")
    if not set(unidades["tipo_unidade"]) <= set(TIPOS_UNIDADE):
        raise ErroEntrada(f"tipo_unidade deve estar em {TIPOS_UNIDADE}")
    if not set(unidades["nivel_espacial"]) <= set(NIVEIS):
        raise ErroEntrada(f"nivel_espacial deve estar em {NIVEIS}")
    if (unidades["nivel_espacial"] != unidades["tipo_unidade"].map(TIPO_PARA_NIVEL)).any():
        raise ErroEntrada("unidades: tipo_unidade 'car' exige nivel_espacial 'imovel_inteiro' e 'gleba' exige 'poligono'")
    if unidades["car_codigo"].isna().any() or not unidades["car_codigo"].astype(str).str.match(RE_CAR).all():
        raise ErroEntrada("unidades: car_codigo obrigatório no formato UF-IBGE7-32hex")
    mf = pd.to_numeric(unidades["porte_modulos_fiscais"], errors="coerce")
    if mf.isna().any() or (mf < 0).any():
        raise ErroEntrada("unidades: porte_modulos_fiscais obrigatório e ≥ 0")
    nulos = indicadores[list(ft.COLUNAS_INDICADORES)].isna().any(axis=1)
    if nulos.any():
        raise ErroEntrada(f"indicadores: {int(nulos.sum())} linha(s) com valor nulo")


def _validar_operacoes(ops: pd.DataFrame, unidades: pd.DataFrame) -> pd.DataFrame:
    _exigir(ops, "operacoes", COLS_OPERACOES)
    if ops["operacao_id"].duplicated().any():
        raise ErroEntrada("operacoes: operacao_id duplicado")
    ops = _datas(ops, ["data_contrato", "data_vencimento"])
    if (ops["data_contrato"] > ops["data_vencimento"]).any():
        raise ErroEntrada("operacoes: data_contrato posterior a data_vencimento")
    car = unidades.set_index("unidade_id")["car_codigo"]
    if not ops["unidade_id"].isin(car.index).all():
        raise ErroEntrada("operacoes: unidade_id inexistente em unidades")
    if (ops["car_codigo"] != ops["unidade_id"].map(car)).any():
        raise ErroEntrada("operacoes: car_codigo diverge do CAR da unidade")
    if "proagro_acionado" in ops.columns and not ops["proagro_acionado"].dropna().isin([0, 1, True, False]).all():
        raise ErroEntrada("operacoes: proagro_acionado deve ser booleano (coluna opcional, não usada pelo motor)")
    return ops


def _validar_verificacoes(ver: pd.DataFrame, unidades: pd.DataFrame, corte: date) -> pd.DataFrame:
    """Valida e devolve as verificações da data de corte. Vazamento temporal → ErroVazamentoTemporal."""
    _exigir(ver, "verificacoes", COLS_VERIFICACOES)
    v = _datas(ver, ["data_corte", "data_referencia", "data_publicacao"])
    v = v[v["data_corte"] == corte].reset_index(drop=True)
    if not v["status_juridico"].isin(STATUS_JURIDICO).all():
        raise ErroEntrada(f"verificacoes: status_juridico deve estar em {STATUS_JURIDICO}")
    if not v["efeito"].isin(EFEITOS).all():
        raise ErroEntrada(f"verificacoes: efeito deve estar em {EFEITOS}")
    if not v["regra"].astype(str).str.match(RE_REGRA).all():
        raise ErroEntrada("verificacoes: regra deve ser snake_case")
    if not v["hash_fonte"].astype(str).str.match(RE_HASH).all():
        raise ErroEntrada("verificacoes: hash_fonte deve ser SHA-256 em hexadecimal minúsculo (64 caracteres)")
    if v[["fonte", "texto"]].isna().any().any():
        raise ErroEntrada("verificacoes: fonte e texto são obrigatórios")
    if not v["unidade_id"].isin(unidades["unidade_id"]).all():
        raise ErroEntrada("verificacoes: unidade_id inexistente em unidades")
    if v.duplicated(["unidade_id", "regra", "fonte", "hash_fonte"]).any():
        raise ErroEntrada("verificacoes: (unidade_id, regra, fonte, hash_fonte) duplicado")
    if (v["data_referencia"] > v["data_publicacao"]).any():
        raise ErroEntrada("verificacoes: data_referencia posterior a data_publicacao")
    if (v["data_publicacao"] > corte).any():
        raise ErroVazamentoTemporal(f"verificacoes: data_publicacao posterior à data de corte {corte}")
    return v


def validar_rotulos_piloto(rot: pd.DataFrame) -> None:
    """Rótulo opcional do piloto (Y3 = atraso > 90 dias ou renegociação). O motor NÃO o usa para pontuar.

    Data do registro e data do evento são separadas (anti-vazamento): data_registro ≥ data_evento.
    """
    _exigir(rot, "rotulos_piloto", COLS_ROTULOS)
    if not rot["y3_atraso_90d"].isin([0, 1, True, False]).all():
        raise ErroEntrada("rotulos_piloto: y3_atraso_90d deve ser 0/1")
    r = _datas(rot, ["data_corte", "data_registro"])
    pos = rot["y3_atraso_90d"].astype(bool)
    if "data_evento" not in rot.columns:
        if pos.any():
            raise ErroEntrada("rotulos_piloto: data_evento é obrigatória quando y3_atraso_90d = 1")
        return
    if rot.loc[pos, "data_evento"].isna().any():
        raise ErroEntrada("rotulos_piloto: data_evento é obrigatória quando y3_atraso_90d = 1")
    ev = pd.to_datetime(rot["data_evento"]).dt.date
    if (ev[pos] > r.loc[pos, "data_registro"]).any():
        raise ErroEntrada("rotulos_piloto: data_registro anterior a data_evento")
    if (ev[pos] <= r.loc[pos, "data_corte"]).any():
        raise ErroEntrada("rotulos_piloto: data_evento deve ser posterior à data de corte")


def _referencias(f: ft.Fator, corte: date) -> tuple[date, date]:
    """Último ano de referência cuja publicação (fim do ano + defasagem) é ≤ corte."""
    ano = corte.year
    while True:
        pub = date(ano, 12, 31) + timedelta(days=f.defasagem_publicacao_dias)
        if pub <= corte:
            return date(ano, 12, 31), pub
        ano -= 1


def saldo_na_data(operacoes: pd.DataFrame, data_corte) -> pd.DataFrame:
    """Saldo exposto por unidade_id na data de corte: operações vigentes (data_contrato ≤ corte < data_vencimento).

    Usa `saldo_rs` quando existe (cai para `valor_rs` onde for nulo); `valor_rs` é só proxy do saldo.
    Retorna colunas unidade_id, saldo_exposto, n_operacoes.
    """
    corte = pd.Timestamp(data_corte)
    o = operacoes.copy()
    ini, fim = pd.to_datetime(o["data_contrato"]), pd.to_datetime(o["data_vencimento"])
    o["_saldo"] = o["saldo_rs"].fillna(o["valor_rs"]) if "saldo_rs" in o.columns else o["valor_rs"]
    vig = o[(ini <= corte) & (corte < fim)]
    return (vig.groupby("unidade_id").agg(saldo_exposto=("_saldo", "sum"), n_operacoes=("operacao_id", "count"))
            .reset_index())


def _bloqueio(v: pd.DataFrame, peso_indeterminado: float) -> pd.DataFrame:
    """Mecânica de bloqueio provável por unidade (NÃO é probabilidade estimada).

    peso por verificação com efeito=bloqueia: detectado/sem_autorizacao_identificada → 1; autorizado → 0;
    indeterminado → peso_indeterminado. bloqueio_provavel = máximo dos pesos da unidade (0 sem verificações).
    """
    bloq = v["efeito"] == "bloqueia"
    peso = np.where(v["status_juridico"].isin(["detectado", "sem_autorizacao_identificada"]), 1.0,
                    np.where(v["status_juridico"] == "indeterminado", peso_indeterminado, 0.0)) * bloq
    t = pd.DataFrame({
        "unidade_id": v["unidade_id"], "peso": peso,
        "vedacao": bloq & v["status_juridico"].isin(["detectado", "sem_autorizacao_identificada"]),
        "indet": bloq & (v["status_juridico"] == "indeterminado"),
    })
    return t.groupby("unidade_id").agg(bloqueio_provavel=("peso", "max"), n_vedacoes=("vedacao", "sum"),
                                       n_vedacoes_indeterminadas=("indet", "sum")).reset_index()


def pontuar(
    indicadores: pd.DataFrame,
    unidades: pd.DataFrame,
    data_corte,
    *,
    verificacoes: pd.DataFrame | None = None,
    operacoes: pd.DataFrame | None = None,
    y_definicao: str = Y_PADRAO,
    horizonte_meses: int = HORIZONTE_PADRAO,
    taxas_base: dict | None = None,
    peso_indeterminado: float = 1.0,
    versoes_dados: dict | None = None,
    semente: int = SEMENTE,
) -> Saida:
    """Retorna `Saida(resultados, detalhes, verificacoes)`. Ver docs/produto/contrato-motor-v1.md."""
    corte = pd.Timestamp(data_corte).date()
    if (corte.month, corte.day) != (7, 31):
        raise ErroEntrada(f"data_corte deve ser 31/jul (ciclo PRODES ago–jul); recebido {corte}")
    if y_definicao not in Y_DEFINICOES:
        raise ErroEntrada(f"y_definicao deve estar em {Y_DEFINICOES} (Y_ilegal e Y_agro são derivados, não previstos)")
    if horizonte_meses != HORIZONTE_PADRAO:
        raise ErroEntrada(f"horizonte_meses deve ser {HORIZONTE_PADRAO} no v1")
    if not 0 <= peso_indeterminado <= 1:
        raise ErroEntrada("peso_indeterminado deve estar em [0, 1]")
    taxas = {**TAXAS_BASE_PADRAO, **(taxas_base or {})}
    if set(taxas) - set(NIVEIS) or not all(0 < t < 1 for t in taxas.values()):
        raise ErroEntrada(f"taxas_base: chaves em {NIVEIS} e valores em (0, 1)")
    _sem_dados_pessoais(indicadores=indicadores, unidades=unidades, operacoes=operacoes, verificacoes=verificacoes)
    _validar(indicadores, unidades)

    ind = _datas(indicadores, ["data_corte"])
    ind = ind[ind["data_corte"] == corte].merge(unidades, on="unidade_id", how="inner", validate="one_to_one")
    if ind.empty:
        raise ErroEntrada(f"nenhum indicador para data_corte={corte} com unidade correspondente")

    ops = _validar_operacoes(operacoes, unidades) if operacoes is not None else None
    ver = _validar_verificacoes(verificacoes, unidades, corte) if verificacoes is not None else None

    refs = {f.nome: _referencias(f, corte) for f in ft.FATORES}
    for nome, (_, pub) in refs.items():  # defesa em profundidade: nunca deveria disparar
        if pub > corte:
            raise ErroVazamentoTemporal(f"{nome}: publicação {pub} > corte {corte}")

    ind = ind.sort_values("unidade_id").reset_index(drop=True)
    z = np.column_stack([ft.padronizar(f, ind[f.coluna].to_numpy()) for f in ft.FATORES])
    coef = np.array([f.coef_stub for f in ft.FATORES])
    eta = z @ coef + _ruido(ind["unidade_id"], semente)
    # calibra o intercepto (bisseção) por nível: média de p do nível = taxa-base do nível
    p = np.empty(len(ind))
    taxa_linha = ind["nivel_espacial"].map(taxas).to_numpy(dtype=float)
    for nivel in ind["nivel_espacial"].unique():
        m = (ind["nivel_espacial"] == nivel).to_numpy()
        lo, hi = -15.0, 5.0
        for _ in range(80):
            mid = (lo + hi) / 2
            if (1 / (1 + np.exp(-(eta[m] + mid)))).mean() > taxas[nivel]:
                hi = mid
            else:
                lo = mid
        p[m] = 1 / (1 + np.exp(-(eta[m] + (lo + hi) / 2)))
    contrib = z * coef  # log-odds

    versao = versao_modelo()
    calculado_em = datetime.now().replace(microsecond=0).isoformat()
    sal = ind[["unidade_id"]].copy()

    # --- camada 1: vedação (separada de p) e mecânica de exposição bloqueável ---
    if ver is not None:
        sal = sal.merge(_bloqueio(ver, peso_indeterminado), on="unidade_id", how="left")
        sal["bloqueio_provavel"] = sal["bloqueio_provavel"].fillna(0.0)
        for c in ("n_vedacoes", "n_vedacoes_indeterminadas"):
            sal[c] = sal[c].fillna(0).astype("Int64")
    else:
        sal["bloqueio_provavel"] = np.nan
        sal["n_vedacoes"] = pd.array([pd.NA] * len(sal), dtype="Int64")
        sal["n_vedacoes_indeterminadas"] = pd.array([pd.NA] * len(sal), dtype="Int64")
    if ops is not None:
        sal = sal.merge(saldo_na_data(ops, corte), on="unidade_id", how="left")
        sal["saldo_exposto"] = sal["saldo_exposto"].fillna(0.0)
        sal["n_operacoes"] = sal["n_operacoes"].fillna(0).astype("Int64")
    else:
        sal["saldo_exposto"] = np.nan
        sal["n_operacoes"] = pd.array([pd.NA] * len(sal), dtype="Int64")
    sal["exposicao_bloqueavel"] = sal["saldo_exposto"] * sal["bloqueio_provavel"]

    # --- trilha de auditoria ---
    vd = {f.fonte: {"data_referencia": refs[f.nome][0].isoformat(), "data_publicacao": refs[f.nome][1].isoformat()}
          for f in ft.FATORES}
    if ver is not None:
        for fonte, g in ver.groupby("fonte"):
            vd[fonte] = {"data_referencia": max(g["data_referencia"]).isoformat(),
                         "data_publicacao": max(g["data_publicacao"]).isoformat(),
                         "hashes": sorted(set(g["hash_fonte"]))}
    vd.update(versoes_dados or {})
    versoes_json = json.dumps(vd, sort_keys=True, ensure_ascii=False)
    hash_ent = hash_snapshot(
        indicadores=ind[["unidade_id", "data_corte", *ft.COLUNAS_INDICADORES]], unidades=unidades,
        operacoes=None if ops is None else ops[(ops["data_contrato"] <= corte) & (corte < ops["data_vencimento"])],
        verificacoes=ver)

    res = pd.DataFrame({
        "unidade_id": ind["unidade_id"], "tipo_unidade": ind["tipo_unidade"], "car_codigo": ind["car_codigo"],
        "data_corte": corte, "y_definicao": y_definicao, "horizonte_meses": int(horizonte_meses),
        "versao_modelo": versao, "p": p, "score": calcular_score(p),
        "faixa": calcular_faixa(p, taxa_linha), "taxa_base": taxa_linha,
        "nivel_espacial": ind["nivel_espacial"],
        "aviso": np.where(ind["nivel_espacial"] == "imovel_inteiro", AVISO_IMOVEL_INTEIRO, None),
        "porte_modulos_fiscais": ind["porte_modulos_fiscais"].astype(float),
        "porte_classe": porte_classe(ind["porte_modulos_fiscais"]),
        "verificacoes_avaliadas": ver is not None,
    })
    res = res.merge(sal, on="unidade_id", how="left", validate="one_to_one")
    res["hash_snapshot"], res["versoes_dados"], res["calculado_em"] = hash_ent, versoes_json, calculado_em

    linhas = []
    for j, f in enumerate(ft.FATORES):
        ref, pub = refs[f.nome]
        direcao = np.where(contrib[:, j] > 0.05, "aumenta_risco", np.where(contrib[:, j] < -0.05, "reduz_risco", "neutro"))
        texto = np.where(contrib[:, j] >= 0, f.texto_alto if f.coef_stub > 0 else f.texto_baixo,
                         f.texto_baixo if f.coef_stub > 0 else f.texto_alto)
        linhas.append(pd.DataFrame({
            "unidade_id": ind["unidade_id"], "data_corte": corte, "y_definicao": y_definicao, "versao_modelo": versao,
            "fator": f.nome, "valor": ind[f.coluna].astype(float), "unidade": f.unidade,
            "contribuicao": contrib[:, j], "direcao": direcao, "fonte": f.fonte,
            "data_referencia": ref, "data_publicacao": pub, "status_juridico": None, "texto": texto,
        }))
    det = pd.concat(linhas, ignore_index=True)
    det["_abs"] = det["contribuicao"].abs()
    det = det.sort_values(["unidade_id", "_abs"], ascending=[True, False], kind="stable").drop(columns="_abs")
    det["ordem"] = det.groupby("unidade_id").cumcount() + 1

    cols_ver = [*COLS_VERIFICACOES, "versao_modelo", "hash_snapshot", "calculado_em"]
    if ver is None:
        ver_out = pd.DataFrame(columns=cols_ver)
    else:
        ver_out = ver[list(COLS_VERIFICACOES)].assign(versao_modelo=versao, hash_snapshot=hash_ent,
                                                      calculado_em=calculado_em)
        ver_out = ver_out.sort_values(["unidade_id", "regra", "fonte"], kind="stable")
    return Saida(res.reset_index(drop=True), det.reset_index(drop=True), ver_out.reset_index(drop=True))
