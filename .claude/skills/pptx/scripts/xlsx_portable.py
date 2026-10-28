"""Minimalistic, dependency-free XLSX writer for tabular text/inventory workbooks.

Uses Python's built-in ZIP/XML standards (OOXML); does not interpret formulas,
import existing workbooks or calculate data. For the PPTX results *inventory* only.
"""
from __future__ import annotations

import re
from pathlib import Path
from xml.etree import ElementTree as ET
from zipfile import ZipFile, ZIP_DEFLATED

NS = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
REL = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
P_REL = "http://schemas.openxmlformats.org/package/2006/relationships"
CT = "http://schemas.openxmlformats.org/package/2006/content-types"
ET.register_namespace("", NS)
ET.register_namespace("r", REL)


def letter(n: int) -> str:
    s = ""
    while n:
        n, rem = divmod(n-1, 26)
        s = chr(65+rem) + s
    return s


def make_xml(root: ET.Element) -> bytes:
    # OOXML readers differ in tolerance of namespace prefixes for package metadata.
    root_ns = root.tag.partition("}")[0].removeprefix("{")
    ET.register_namespace("", root_ns)
    ET.register_namespace("r", REL)
    return ET.tostring(root, encoding="utf-8", xml_declaration=True)


def clean_string(obj) -> str:
    s = str(obj) if obj is not None else ""
    # Office Open XML forbids almost all ASCII C0 control chars.
    return re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", "", s)


def sheet_xml(headers: list, rows: list[list], widths: list[int]) -> bytes:
    ws = ET.Element(f"{{{NS}}}worksheet")
    views = ET.SubElement(ws, f"{{{NS}}}sheetViews")
    view = ET.SubElement(views, f"{{{NS}}}sheetView", workbookViewId="0")
    ET.SubElement(view, f"{{{NS}}}pane", ySplit="1", topLeftCell="A2", activePane="bottomLeft", state="frozen")
    ET.SubElement(view, f"{{{NS}}}selection", pane="bottomLeft", activeCell="A2", sqref="A2")
    ET.SubElement(ws, f"{{{NS}}}sheetFormatPr", defaultRowHeight="20")
    cols = ET.SubElement(ws, f"{{{NS}}}cols")
    for i, w in enumerate(widths, 1):
        ET.SubElement(cols, f"{{{NS}}}col", min=str(i), max=str(i), width=str(min(w, 100)), customWidth="1")
    body = ET.SubElement(ws, f"{{{NS}}}sheetData")
    for rownum, values in enumerate([headers]+rows, 1):
        row = ET.SubElement(body, f"{{{NS}}}row", r=str(rownum), ht=("29" if rownum == 1 else "34"), customHeight="1")
        for colnum, v in enumerate(values, 1):
            if v is None or v == "":
                continue
            coord = f"{letter(colnum)}{rownum}"
            style = "1" if rownum == 1 else "2"
            if isinstance(v, (int, float)) and not isinstance(v, bool):
                cell = ET.SubElement(row, f"{{{NS}}}c", r=coord, s=style)
                ET.SubElement(cell, f"{{{NS}}}v").text = str(v)
            else:
                cell = ET.SubElement(row, f"{{{NS}}}c", r=coord, s=style, t="inlineStr")
                inline = ET.SubElement(cell, f"{{{NS}}}is")
                text = ET.SubElement(inline, f"{{{NS}}}t")
                text.text = clean_string(v)
                if text.text and (text.text.startswith(" ") or text.text.endswith(" ")):
                    text.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
    end = f"{letter(len(headers))}{len(rows)+1}"
    ET.SubElement(ws, f"{{{NS}}}autoFilter", ref=f"A1:{end}")
    return make_xml(ws)


def styles_xml() -> bytes:
    st = ET.Element(f"{{{NS}}}styleSheet")
    fonts = ET.SubElement(st, f"{{{NS}}}fonts", count="2")
    n = ET.SubElement(fonts, f"{{{NS}}}font")
    ET.SubElement(n, f"{{{NS}}}sz", val="11")
    ET.SubElement(n, f"{{{NS}}}name", val="Aptos")
    n = ET.SubElement(fonts, f"{{{NS}}}font")
    ET.SubElement(n, f"{{{NS}}}b")
    ET.SubElement(n, f"{{{NS}}}sz", val="11")
    ET.SubElement(n, f"{{{NS}}}name", val="Aptos")
    ET.SubElement(n, f"{{{NS}}}color", rgb="FFFFFFFF")
    fills = ET.SubElement(st, f"{{{NS}}}fills", count="3")
    for pattern in ("none", "gray125"):
        f = ET.SubElement(fills, f"{{{NS}}}fill")
        ET.SubElement(f, f"{{{NS}}}patternFill", patternType=pattern)
    f = ET.SubElement(fills, f"{{{NS}}}fill")
    pf = ET.SubElement(f, f"{{{NS}}}patternFill", patternType="solid")
    ET.SubElement(pf, f"{{{NS}}}fgColor", rgb="FF233546")
    ET.SubElement(pf, f"{{{NS}}}bgColor", indexed="64")
    borders = ET.SubElement(st, f"{{{NS}}}borders", count="1")
    b = ET.SubElement(borders, f"{{{NS}}}border")
    for tag in ("left", "right", "top", "bottom", "diagonal"):
        ET.SubElement(b, f"{{{NS}}}{tag}")
    cs = ET.SubElement(st, f"{{{NS}}}cellStyleXfs", count="1")
    ET.SubElement(cs, f"{{{NS}}}xf", numFmtId="0", fontId="0", fillId="0", borderId="0")
    xfs = ET.SubElement(st, f"{{{NS}}}cellXfs", count="3")
    ET.SubElement(xfs, f"{{{NS}}}xf", numFmtId="0", fontId="0", fillId="0", borderId="0", xfId="0")
    ET.SubElement(xfs, f"{{{NS}}}xf", numFmtId="0", fontId="1", fillId="2", borderId="0", xfId="0", applyFont="1", applyFill="1", applyAlignment="1").append(
        ET.Element(f"{{{NS}}}alignment", vertical="center", wrapText="1"))
    ET.SubElement(xfs, f"{{{NS}}}xf", numFmtId="0", fontId="0", fillId="0", borderId="0", xfId="0", applyAlignment="1").append(
        ET.Element(f"{{{NS}}}alignment", vertical="center", wrapText="1"))
    return make_xml(st)


def write_xlsx(path: Path, tabs: list[tuple[str, list[str], list[list], list[int]]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    wb = ET.Element(f"{{{NS}}}workbook")
    views = ET.SubElement(wb, f"{{{NS}}}bookViews")
    ET.SubElement(views, f"{{{NS}}}workbookView")
    sheets = ET.SubElement(wb, f"{{{NS}}}sheets")
    for i, (name, _, _, _) in enumerate(tabs, 1):
        ET.SubElement(sheets, f"{{{NS}}}sheet", name=name[:31], sheetId=str(i), attrib={f"{{{REL}}}id": f"rId{i}"})
    rels = ET.Element(f"{{{P_REL}}}Relationships")
    for i in range(1, len(tabs)+1):
        ET.SubElement(rels, f"{{{P_REL}}}Relationship", Id=f"rId{i}", Type=f"{REL}/worksheet", Target=f"worksheets/sheet{i}.xml")
    ET.SubElement(rels, f"{{{P_REL}}}Relationship", Id=f"rId{len(tabs)+1}", Type=f"{REL}/styles", Target="styles.xml")
    pkg = ET.Element(f"{{{P_REL}}}Relationships")
    ET.SubElement(pkg, f"{{{P_REL}}}Relationship", Id="rId1", Type=f"{REL}/officeDocument", Target="xl/workbook.xml")
    types = ET.Element(f"{{{CT}}}Types")
    ET.SubElement(types, f"{{{CT}}}Default", Extension="rels", ContentType="application/vnd.openxmlformats-package.relationships+xml")
    ET.SubElement(types, f"{{{CT}}}Default", Extension="xml", ContentType="application/xml")
    ET.SubElement(types, f"{{{CT}}}Override", PartName="/xl/workbook.xml", ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml")
    ET.SubElement(types, f"{{{CT}}}Override", PartName="/xl/styles.xml", ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml")
    for i in range(1, len(tabs)+1):
        ET.SubElement(types, f"{{{CT}}}Override", PartName=f"/xl/worksheets/sheet{i}.xml", ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml")
    with ZipFile(path, "w", ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", make_xml(types))
        z.writestr("_rels/.rels", make_xml(pkg))
        z.writestr("xl/workbook.xml", make_xml(wb))
        z.writestr("xl/_rels/workbook.xml.rels", make_xml(rels))
        z.writestr("xl/styles.xml", styles_xml())
        for i, (_, headers, rows, widths) in enumerate(tabs, 1):
            z.writestr(f"xl/worksheets/sheet{i}.xml", sheet_xml(headers, rows, widths))
