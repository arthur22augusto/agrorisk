#!/usr/bin/env python3
"""Renderiza uma única prévia consolidada de um PPTX, sem editar o original.

Requer PyMuPDF e Pillow. PDF via LibreOffice; ou PowerPoint + pywin32 no Windows.
Uso: python render_preview.py projeto/output/apresentacao.pptx --outdir projeto/qa
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
from pathlib import Path


def export_with_libreoffice(pptx: Path, pdf: Path) -> bool:
    command = shutil.which("libreoffice") or shutil.which("soffice")
    if not command:
        return False
    # Isola o perfil LO para evitar travar uma instância existente.
    profile = pdf.parent / "_lo_profile_pptx_skill"
    profile.mkdir(exist_ok=True)
    options = [command, f"-env:UserInstallation={profile.as_uri()}", "--headless", "--convert-to", "pdf", "--outdir", str(pdf.parent), str(pptx)]
    completed = subprocess.run(options, capture_output=True, text=True, timeout=150)
    generated = pdf.parent / (pptx.stem + ".pdf")
    if completed.returncode != 0 or not generated.exists():
        return False
    if generated != pdf:
        generated.replace(pdf)
    return True


def export_with_powerpoint(pptx: Path, pdf: Path) -> bool:
    if os.name != "nt":
        return False
    try:
        import win32com.client  # pip install pywin32; requer MS PowerPoint
    except ImportError:
        return False
    app, pres = None, None
    try:
        app = win32com.client.DispatchEx("PowerPoint.Application")
        pres = app.Presentations.Open(str(pptx), ReadOnly=True, WithWindow=False)
        pres.SaveAs(str(pdf), 32)  # ppSaveAsPDF
        return pdf.exists()
    except Exception:
        return False
    finally:
        if pres is not None:
            pres.Close()
        if app is not None:
            app.Quit()


def generate_contact_sheet(pdf: Path, outdir: Path, max_cols: int = 3) -> tuple[Path, int]:
    try:
        import fitz  # PyMuPDF
        from PIL import Image, ImageDraw, ImageFont
    except ImportError as exc:
        raise RuntimeError("Instale PyMuPDF e Pillow: pip install pymupdf pillow") from exc

    pages_dir = outdir / "slides"
    pages_dir.mkdir(exist_ok=True)
    tiles = []
    with fitz.open(str(pdf)) as doc:
        if len(doc) == 0:
            raise ValueError("PDF exportado não tem páginas")
        for index, page in enumerate(doc):
            pix = page.get_pixmap(matrix=fitz.Matrix(1.0, 1.0), alpha=False)
            img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
            img.thumbnail((460, 260))
            img.save(pages_dir / f"slide_{index+1:03d}.png")
            tiles.append(img.copy())

    width, height, gap, label_height = 460, 260, 22, 22
    cols = min(max_cols, len(tiles))
    rows = (len(tiles) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * (width + gap) + gap, rows * (height + label_height + gap) + gap), "#F2F2F2")
    draw = ImageDraw.Draw(sheet)
    for index, tile in enumerate(tiles):
        col, row = index % cols, index // cols
        x = gap + col * (width + gap)
        y = gap + row * (height + label_height + gap)
        draw.rectangle((x - 1, y - 1, x + width + 1, y + height + 1), outline="#C9C9C9", width=1)
        sheet.paste(tile, (x + (width - tile.width) // 2, y + (height - tile.height) // 2))
        draw.text((x + 2, y + height + 3), f"Slide {index + 1}", fill="#333333")
    outpath = outdir / "contact_sheet.png"
    sheet.save(outpath, optimize=True)
    return outpath, len(tiles)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pptx", type=Path)
    parser.add_argument("--outdir", type=Path, default=None)
    args = parser.parse_args()
    pptx = args.pptx.resolve()
    if not pptx.exists():
        print(f"PPTX não encontrado: {pptx}")
        return 2
    outdir = (args.outdir or pptx.parent / "qa").resolve()
    outdir.mkdir(parents=True, exist_ok=True)
    pdf = outdir / "preview.pdf"
    if not (export_with_libreoffice(pptx, pdf) or export_with_powerpoint(pptx, pdf)):
        print("Sem renderizador: instale LibreOffice ou, no Windows, MS PowerPoint + pywin32.")
        return 2
    try:
        png, count = generate_contact_sheet(pdf, outdir)
    except Exception as exc:
        print(f"Erro na geração da prévia: {exc}")
        return 2
    print(f"Prévia: {png} | {count} slides | PDF: {pdf}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
