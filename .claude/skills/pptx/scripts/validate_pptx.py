#!/usr/bin/env python3
"""Inspeção técnica estrutural de um PPTX, sem renderizar nem modificar o arquivo.

Uso:
    python validate_pptx.py projeto/output/apresentacao.pptx --out projeto/qa/validation.json

Não substitui revisão editorial/visual: a biblioteca não mede o texto renderizado.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

try:
    from pptx import Presentation
    from pptx.util import Pt
except ImportError as exc:
    raise SystemExit("Dependência ausente: instale python-pptx com pip.") from exc


BOUND_TOLERANCE = 10000  # EMUs: evita alertas falsos por arredondamento.


def add_issue(issues: list, severity: str, code: str, slide: int | None, message: str):
    issues.append({"severity": severity, "code": code, "slide": slide, "message": message})


def all_text(shape) -> tuple[str, list[float]]:
    if not getattr(shape, "has_text_frame", False):
        return "", []
    text = "\n".join(p.text for p in shape.text_frame.paragraphs)
    font_sizes = []
    for paragraph in shape.text_frame.paragraphs:
        for run in paragraph.runs:
            if run.text.strip() and run.font.size is not None:
                font_sizes.append(round(run.font.size / Pt(1), 1))
    return text, font_sizes


def validate(path: Path) -> dict:
    if not path.is_file():
        raise FileNotFoundError(f"Arquivo não encontrado: {path}")

    deck = Presentation(str(path))
    issues: list[dict] = []
    slides_info: list[dict] = []
    total = len(deck.slides)
    if total == 0:
        add_issue(issues, "error", "empty_deck", None, "Apresentação sem slides")

    ratio = round(deck.slide_width / deck.slide_height, 4)
    if abs(ratio - 16 / 9) > 0.015:
        add_issue(issues, "warning", "non_widescreen", None, f"Formato de tela {ratio:.3f}: padrão sugerido 16:9")

    for slide_no, slide in enumerate(deck.slides, 1):
        words, text_shapes, table_count, chart_count, numbers = 0, 0, 0, 0, 0
        slide_strings = []
        for shape in slide.shapes:
            # Formas de fundo que coincidam com a página são válidas.
            if (
                shape.left < -BOUND_TOLERANCE
                or shape.top < -BOUND_TOLERANCE
                or shape.left + shape.width > deck.slide_width + BOUND_TOLERANCE
                or shape.top + shape.height > deck.slide_height + BOUND_TOLERANCE
            ):
                add_issue(
                    issues, "error", "off_slide", slide_no,
                    f"Elemento '{shape.name}' excede limites do slide",
                )

            text, sizes = all_text(shape)
            if text.strip():
                text_shapes += 1
                words += len(re.findall(r"\b[\wÀ-ÿ-]+\b", text))
                slide_strings.append(text.strip())
                # Créditos/fonte e identificadores técnicos podem ser pequenos.
                is_footnote = bool(re.match(r"(?i)^\s*(fonte|nota|source|elabora[cç][aã]o|cr[eé]dito):", text))
                if sizes and min(sizes) < 14 and not is_footnote:
                    add_issue(
                        issues, "warning", "small_text", slide_no,
                        f"'{shape.name}' tem fonte explícita de {min(sizes):.1f} pt; verifique a legibilidade",
                    )
                numbers += len(re.findall(r"(?<!\w)\d+(?:[.,]\d+)?\s*(?:%|p\.p\.|milh(?:ão|ões)|R\$)", text, flags=re.I))

            if getattr(shape, "has_table", False):
                table_count += 1
                if len(shape.table.rows) > 8 or len(shape.table.columns) > 6:
                    add_issue(
                        issues, "warning", "dense_table", slide_no,
                        f"Tabela {len(shape.table.rows)}×{len(shape.table.columns)}; verificar legibilidade",
                    )
            if getattr(shape, "has_chart", False):
                chart_count += 1

        if words > 55:
            add_issue(
                issues, "warning", "text_dense", slide_no,
                f"{words} palavras de texto (incluindo rótulos); verificar excesso de informação",
            )
        if not slide.shapes:
            add_issue(issues, "warning", "blank_slide", slide_no, "Slide sem elementos")
        if slide_no <= 5 and not any(s.strip() for s in slide_strings):
            add_issue(issues, "warning", "no_readable_text_intro", slide_no, "Sem texto extraível no início; confirmar narrativa")

        slides_info.append({
            "slide": slide_no, "text_words": words, "text_boxes": text_shapes,
            "tables": table_count, "charts": chart_count, "prominent_number_patterns": numbers,
            "text_excerpt": " | ".join(slide_strings)[:230],
        })

    errors = sum(i["severity"] == "error" for i in issues)
    warnings = sum(i["severity"] == "warning" for i in issues)
    return {
        "pptx": str(path.resolve()),
        "slides": total,
        "aspect_ratio": ratio,
        "status": "FAIL" if errors else "PASS_WITH_WARNINGS" if warnings else "PASS",
        "errors": errors,
        "warnings": warnings,
        "issues": issues,
        "slides_summary": slides_info,
        "limitations": [
            "Não detecta texto cortado pela renderização, contraste ruim nem sobreposição entre formas válidas.",
            "A tipografia herdada do tema pode não aparecer na inspeção de tamanho de fonte.",
            "Não avalia fidelidade científica, qualidade narrativa ou direitos de uso de imagens.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pptx", type=Path, help="Caminho do arquivo .pptx")
    parser.add_argument("--out", type=Path, default=None, help="Caminho do relatório JSON")
    args = parser.parse_args()

    try:
        report = validate(args.pptx)
    except Exception as exc:
        print(json.dumps({"status": "FAIL", "error": str(exc)}, ensure_ascii=False, indent=2))
        return 2

    output = json.dumps(report, ensure_ascii=False, indent=2)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(output, encoding="utf-8")
    print(f"{report['status']} | {report['slides']} slides | {report['errors']} erros | {report['warnings']} alertas")
    if args.out:
        print(f"Relatório: {args.out.resolve()}")
    return 1 if report["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
