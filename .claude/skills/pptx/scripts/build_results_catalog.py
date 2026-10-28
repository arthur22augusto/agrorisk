#!/usr/bin/env python3
"""Converte um inventário JSON de evidências planejadas em um Excel rastreável.

O Excel NÃO contém resultados calculados ou simulados. O script só escreve o
inventário de tabelas e as perguntas, sem alterar dados de pesquisa.

Uso: python build_results_catalog.py data/resultados_manifest.json --out output/resultados_necessarios.xlsx
Exportação portável XLSX usando somente biblioteca padrão Python por padrão.
"""
from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

PRIORIDADES = {"P0", "P1", "P2"}
STATUS = {"disponivel", "parcial", "ausente", "validar"}


def ler_manifest(path: Path) -> dict:
    doc = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(doc, dict):
        raise ValueError("Manifesto precisa ser um objeto JSON")
    if not isinstance(doc.get("resultados"), list):
        raise ValueError("Campo 'resultados' precisa ser lista (pode estar vazia)")
    if not isinstance(doc.get("perguntas", []), list):
        raise ValueError("Campo 'perguntas' precisa ser lista")
    ids = set()
    for pos, item in enumerate(doc["resultados"], 1):
        if not isinstance(item, dict):
            raise ValueError(f"Resultado {pos}: deve ser objeto")
        rid = str(item.get("id", "")).strip()
        if not rid or rid in ids:
            raise ValueError(f"Resultado {pos}: ID vazio ou duplicado: {rid!r}")
        ids.add(rid)
        if item.get("prioridade") not in PRIORIDADES:
            raise ValueError(f"Resultado {rid}: prioridade deve ser P0, P1 ou P2")
        if item.get("status") not in STATUS:
            raise ValueError(f"Resultado {rid}: status inválido {item.get('status')!r}")
        if not str(item.get("titulo", "")).strip() or not str(item.get("pergunta", "")).strip():
            raise ValueError(f"Resultado {rid}: titulo e pergunta são obrigatórios")
        for field in ("comparadores", "dimensoes", "colunas_esperadas", "dependencias"):
            if field in item and not isinstance(item[field], list):
                raise ValueError(f"Resultado {rid}: {field} precisa ser uma lista")
    return doc


def txt(value) -> str:
    if value is None:
        return ""
    if isinstance(value, list):
        return " • ".join(str(x) for x in value)
    return str(value)


def largura_col(n: int) -> str:
    result = ""
    while n:
        n, r = divmod(n-1, 26)
        result = chr(65+r) + result
    return result


def criar_planilha(nome: str, headers: list[str], data: list[list], wb, widths=None) -> None:
    sheet = wb.worksheets.add(nome)
    count = len(headers)
    end = largura_col(count)
    sheet.get_range(f"A1:{end}1").values = [headers]
    sheet.get_range(f"A1:{end}1").format = {
        "fill": "#233546", "font": {"bold": True, "color": "#FFFFFF"},
        "row_height": 32, "wrap_text": True, "vertical_alignment": "center"
    }
    sheet.freeze_panes.freeze_rows(1)
    if data:
        sheet.get_range(f"A2:{end}{1+len(data)}").values = data
        sheet.get_range(f"A2:{end}{1+len(data)}").format.wrap_text = True
        sheet.get_range(f"A2:{end}{1+len(data)}").format.row_height = 44
    if widths:
        for i, width in enumerate(widths):
            col = largura_col(i + 1)
            sheet.get_range(f"{col}:{col}").format.column_width = width


def produzir_portatil(doc: dict, out: Path) -> None:
    from xlsx_portable import write_xlsx
    results = doc["resultados"]
    questions = doc.get("perguntas", [])
    states = Counter(x["status"] for x in results)
    priorities = Counter(x["prioridade"] for x in results)
    resumo = [
        ["Projeto", txt(doc.get("projeto")), "Identificação do contexto"],
        ["Objetivo", txt(doc.get("objetivo")), "Pergunta que orienta o PPT"],
        ["Público", txt(doc.get("publico")), "Ajuste de linguagem"],
        ["Tese", txt(doc.get("tese")), "Afirmar apenas se sustentada"],
        ["Total de resultados necessários", len(results), "Inclui ausentes"],
        ["Disponíveis", states["disponivel"], "Com arquivo conferível"],
        ["Parciais", states["parcial"], "Requer complementação"],
        ["Ausentes", states["ausente"], "A produzir"],
        ["Validar", states["validar"], "Conferir existência e qualidade"],
        ["Prioridade P0", priorities["P0"], "Essenciais / bloqueantes"],
        ["Prioridade P1", priorities["P1"], "Alta relevância"],
        ["Prioridade P2", priorities["P2"], "Opcionais"],
        ["Nota", "SEM DADOS FABRICADOS", "Inventário de análises, não resultados calculados"],
    ]
    keys = [
        ("id", "ID"), ("prioridade", "Prioridade"), ("status", "Status"),
        ("titulo", "Resultado/tabela"), ("pergunta", "Pergunta"),
        ("claim", "Afirmação testada"), ("tipo", "Tipo"), ("metrica", "Métrica"),
        ("unidade", "Unidade"), ("comparadores", "Comparadores"),
        ("periodo", "Período"), ("populacao", "População"),
        ("denominador", "Denominador"), ("dimensoes", "Dimensões"),
        ("colunas_esperadas", "Colunas esperadas"), ("calculo", "Cálculo necessário"),
        ("metodo", "Método"), ("fonte", "Fonte"), ("arquivo_origem", "Arquivo real"),
        ("aba_origem", "Aba real"), ("slide", "Slide"), ("risco_se_faltar", "Risco"),
        ("proxima_acao", "Ação"), ("dependencias", "Dependências"),
        ("observacoes", "Observações")
    ]
    comparisons = [r for r in results if r.get("comparadores") or r.get("tipo") == "comparacao"]
    compare_keys = ["id", "prioridade", "status", "comparadores", "metrica", "unidade", "periodo", "populacao", "denominador", "colunas_esperadas", "slide"]
    question_keys = ["id", "prioridade", "pergunta", "porque_importa", "impacto_no_ppt", "status", "resposta"]
    tabs = [
        ("Resumo", ["Campo", "Valor", "Interpretação"], resumo, [33, 60, 64]),
        ("Resultados", [h for _, h in keys], [[txt(r.get(k, "")) for k, _ in keys] for r in results], [14, 13, 16, 34, 45, 40, 20, 30, 16, 36, 24, 35, 32, 26, 50, 48, 28, 30, 36, 18, 18, 45, 45, 20, 35]),
        ("Comparacoes", ["ID", "Prioridade", "Status", "Comparação desejada", "Métrica", "Unidade", "Período", "População", "Denominador", "Colunas esperadas", "Slide"], [[txt(r.get(k, "")) for k in compare_keys] for r in comparisons], [14, 13, 14, 46, 28, 16, 28, 35, 35, 49, 18]),
        ("Perguntas", ["ID", "Prioridade", "Pergunta", "Por que importa", "Impacto no PPT", "Status", "Resposta"], [[txt(q.get(k, "")) for k in question_keys] for q in questions], [14, 15, 60, 52, 46, 18, 52]),
        ("Instrucoes", ["Orientação", "Significado"], [
            ["Objeto", "Inventário de resultados tabulares NECESSÁRIOS, incluindo ausentes"],
            ["Disponível", "Existe e possui arquivo conferível"],
            ["Parcial", "Requer complementação"],
            ["Ausente", "Tabela ainda não foi gerada; não inventar valores"],
            ["Validar", "A existência ou qualidade da fonte não foi verificada"],
            ["Prioridade", "P0 essencial, P1 alta, P2 opcional"],
            ["Colunas esperadas", "Esquema desejado para saída FUTURA, não colunas existentes"],
            ["Atualizar", "Editar resultados_manifest.json e regenerar o Excel"],
        ], [31, 90]),
    ]
    write_xlsx(out, tabs)
    print(f"Excel: {out.resolve()} | {len(results)} resultados | {len(comparisons)} comparações | {len(questions)} perguntas | portável")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path, help="JSON de resultados necessários")
    parser.add_argument("--out", type=Path, required=True, help="Saída XLSX")
    args = parser.parse_args()
    try:
        manifest = ler_manifest(args.manifest)
        produzir_portatil(manifest, args.out)
    except (OSError, ValueError, json.JSONDecodeError, RuntimeError) as exc:
        parser.exit(2, f"ERRO: {exc}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
