#!/usr/bin/env python3
"""Build the Nyimbi strategy .potx template.

Creates a 16:9 PowerPoint template from python-pptx's default package, then
rewrites the theme, master, layouts and content type. Output:

    assets/nyimbi-strategy.potx
    assets/nyimbi-strategy-preview.pptx   (same package, presentation content type)

The preview file exists so the template can be rendered and inspected without
PowerPoint. Both files are generated; edit this script, not the binaries.
"""
from __future__ import annotations

import shutil
import tempfile
import uuid
import zipfile
from pathlib import Path

import lxml.etree as etree
from pptx import Presentation
from pptx.util import Inches

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
EMU = 914400
A_NS = "http://schemas.openxmlformats.org/drawingml/2006/main"
P_NS = "http://schemas.openxmlformats.org/presentationml/2006/main"
R_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
NS = {"a": A_NS, "p": P_NS, "r": R_NS}

INK = "111827"
INK_2 = "0B1220"
PAPER = "FBFAF7"
PAPER_2 = "F3F1EC"
TEAL = "0F766E"
TEAL_DARK = "115E59"
SLATE = "64748B"
SLATE_LIGHT = "94A3B8"
AMBER = "D97706"
RULE = "D1D5DB"
MUTED = "6B7280"
BODY = "374151"


def qn(prefix: str, tag: str) -> str:
    return f"{{{NS[prefix]}}}{tag}"


def emu(inches: float) -> str:
    return str(int(round(inches * EMU)))


def set_xfrm(sp, x: float, y: float, w: float, h: float) -> None:
    sp_pr = sp.find("p:spPr", NS)
    if sp_pr is None:
        sp_pr = etree.SubElement(sp, qn("p", "spPr"))
    xfrm = sp_pr.find("a:xfrm", NS)
    if xfrm is None:
        xfrm = etree.Element(qn("a", "xfrm"))
        sp_pr.insert(0, xfrm)
    off = xfrm.find("a:off", NS)
    if off is None:
        off = etree.SubElement(xfrm, qn("a", "off"))
    ext = xfrm.find("a:ext", NS)
    if ext is None:
        ext = etree.SubElement(xfrm, qn("a", "ext"))
    off.set("x", emu(x))
    off.set("y", emu(y))
    ext.set("cx", emu(w))
    ext.set("cy", emu(h))


def set_body_pr(sp, anchor: str = "t", insets: bool = True) -> None:
    body_pr = sp.find("p:txBody/a:bodyPr", NS)
    if body_pr is None:
        return
    body_pr.set("anchor", anchor)
    if insets:
        for attr in ("lIns", "tIns", "rIns", "bIns"):
            body_pr.set(attr, "0")
    for child in list(body_pr):
        if child.tag in {
            qn("a", "normAutofit"),
            qn("a", "spAutoFit"),
            qn("a", "noAutofit"),
        }:
            body_pr.remove(child)
    etree.SubElement(body_pr, qn("a", "noAutofit"))


def solid_fill(parent, color: str) -> None:
    fill = etree.SubElement(parent, qn("a", "solidFill"))
    etree.SubElement(fill, qn("a", "srgbClr")).set("val", color)


def set_bg(cSld, color: str) -> None:
    old = cSld.find("p:bg", NS)
    if old is not None:
        cSld.remove(old)
    bg = etree.Element(qn("p", "bg"))
    bg_pr = etree.SubElement(bg, qn("p", "bgPr"))
    solid_fill(bg_pr, color)
    etree.SubElement(bg_pr, qn("a", "effectLst"))
    cSld.insert(0, bg)


def shape_by_ph(sp_tree, ph_type: str | None = None, idx: int | None = None):
    for sp in sp_tree.findall("p:sp", NS):
        ph = sp.find("p:nvSpPr/p:nvPr/p:ph", NS)
        if ph is None:
            continue
        actual = ph.get("type")
        if ph_type == "obj":
            if actual not in (None, "obj"):
                continue
        elif ph_type is not None and actual != ph_type:
            continue
        if idx is not None and ph.get("idx") != str(idx):
            continue
        return sp
    return None


def remove_shape(sp_tree, sp) -> None:
    if sp is not None:
        sp_tree.remove(sp)


def next_shape_id(sp_tree) -> int:
    ids = []
    for el in sp_tree.iter():
        if el.tag in {qn("p", "cNvPr"), qn("a", "cNvPr")}:
            try:
                ids.append(int(el.get("id", "0")))
            except ValueError:
                pass
    return max(ids, default=1) + 1


def add_rect(sp_tree, x, y, w, h, color: str, name: str):
    sp = etree.SubElement(sp_tree, qn("p", "sp"))
    nv = etree.SubElement(sp, qn("p", "nvSpPr"))
    etree.SubElement(nv, qn("p", "cNvPr")).attrib.update(
        {"id": str(next_shape_id(sp_tree)), "name": name}
    )
    etree.SubElement(nv, qn("p", "cNvSpPr"))
    etree.SubElement(nv, qn("p", "nvPr"))
    sp_pr = etree.SubElement(sp, qn("p", "spPr"))
    xfrm = etree.SubElement(sp_pr, qn("a", "xfrm"))
    etree.SubElement(xfrm, qn("a", "off")).attrib.update({"x": emu(x), "y": emu(y)})
    etree.SubElement(xfrm, qn("a", "ext")).attrib.update({"cx": emu(w), "cy": emu(h)})
    geom = etree.SubElement(sp_pr, qn("a", "prstGeom"))
    geom.set("prst", "rect")
    etree.SubElement(geom, qn("a", "avLst"))
    solid_fill(sp_pr, color)
    ln = etree.SubElement(sp_pr, qn("a", "ln"))
    etree.SubElement(ln, qn("a", "noFill"))
    tx = etree.SubElement(sp, qn("p", "txBody"))
    etree.SubElement(tx, qn("a", "bodyPr"))
    etree.SubElement(tx, qn("a", "lstStyle"))
    etree.SubElement(tx, qn("a", "p"))
    return sp


def add_text(
    sp_tree,
    x,
    y,
    w,
    h,
    text: str,
    *,
    font="Arial",
    size=9,
    color=MUTED,
    bold=False,
    align="l",
    spacing=0,
    caps=False,
    name="Label",
):
    sp = etree.SubElement(sp_tree, qn("p", "sp"))
    nv = etree.SubElement(sp, qn("p", "nvSpPr"))
    etree.SubElement(nv, qn("p", "cNvPr")).attrib.update(
        {"id": str(next_shape_id(sp_tree)), "name": name}
    )
    etree.SubElement(nv, qn("p", "cNvSpPr"))
    etree.SubElement(nv, qn("p", "nvPr"))
    sp_pr = etree.SubElement(sp, qn("p", "spPr"))
    xfrm = etree.SubElement(sp_pr, qn("a", "xfrm"))
    etree.SubElement(xfrm, qn("a", "off")).attrib.update({"x": emu(x), "y": emu(y)})
    etree.SubElement(xfrm, qn("a", "ext")).attrib.update({"cx": emu(w), "cy": emu(h)})
    geom = etree.SubElement(sp_pr, qn("a", "prstGeom"))
    geom.set("prst", "rect")
    etree.SubElement(geom, qn("a", "avLst"))
    etree.SubElement(sp_pr, qn("a", "noFill"))
    ln = etree.SubElement(sp_pr, qn("a", "ln"))
    etree.SubElement(ln, qn("a", "noFill"))
    tx = etree.SubElement(sp, qn("p", "txBody"))
    body_pr = etree.SubElement(tx, qn("a", "bodyPr"))
    body_pr.set("anchor", "ctr")
    for attr in ("lIns", "tIns", "rIns", "bIns"):
        body_pr.set(attr, "0")
    etree.SubElement(body_pr, qn("a", "noAutofit"))
    etree.SubElement(tx, qn("a", "lstStyle"))
    p = etree.SubElement(tx, qn("a", "p"))
    p_pr = etree.SubElement(p, qn("a", "pPr"))
    p_pr.set("algn", align)
    r = etree.SubElement(p, qn("a", "r"))
    r_pr = etree.SubElement(r, qn("a", "rPr"))
    r_pr.set("lang", "en-US")
    r_pr.set("sz", str(int(size * 100)))
    r_pr.set("b", "1" if bold else "0")
    r_pr.set("spc", str(spacing))
    r_pr.set("cap", "all" if caps else "none")
    solid_fill(r_pr, color)
    etree.SubElement(r_pr, qn("a", "latin")).set("typeface", font)
    etree.SubElement(r, qn("a", "t")).text = text
    etree.SubElement(p, qn("a", "endParaRPr")).set("lang", "en-US")
    return sp


def add_page_number(sp_tree, x=11.95, y=6.98, w=0.78, h=0.24):
    remove_shape(sp_tree, shape_by_ph(sp_tree, "sldNum"))
    sp = etree.SubElement(sp_tree, qn("p", "sp"))
    nv = etree.SubElement(sp, qn("p", "nvSpPr"))
    etree.SubElement(nv, qn("p", "cNvPr")).attrib.update(
        {"id": str(next_shape_id(sp_tree)), "name": "Slide Number"}
    )
    etree.SubElement(nv, qn("p", "cNvSpPr")).append(
        etree.Element(qn("a", "spLocks"), noGrp="1")
    )
    nv_pr = etree.SubElement(nv, qn("p", "nvPr"))
    ph = etree.SubElement(nv_pr, qn("p", "ph"))
    ph.attrib.update({"type": "sldNum", "sz": "quarter", "idx": "12"})
    sp_pr = etree.SubElement(sp, qn("p", "spPr"))
    xfrm = etree.SubElement(sp_pr, qn("a", "xfrm"))
    etree.SubElement(xfrm, qn("a", "off")).attrib.update({"x": emu(x), "y": emu(y)})
    etree.SubElement(xfrm, qn("a", "ext")).attrib.update({"cx": emu(w), "cy": emu(h)})
    geom = etree.SubElement(sp_pr, qn("a", "prstGeom"))
    geom.set("prst", "rect")
    etree.SubElement(geom, qn("a", "avLst"))
    tx = etree.SubElement(sp, qn("p", "txBody"))
    body_pr = etree.SubElement(tx, qn("a", "bodyPr"))
    body_pr.set("anchor", "ctr")
    for attr in ("lIns", "tIns", "rIns", "bIns"):
        body_pr.set(attr, "0")
    lst = etree.SubElement(tx, qn("a", "lstStyle"))
    lvl = etree.SubElement(lst, qn("a", "lvl1pPr"))
    lvl.set("algn", "r")
    d = etree.SubElement(lvl, qn("a", "defRPr"))
    d.set("sz", "900")
    solid_fill(d, MUTED)
    p = etree.SubElement(tx, qn("a", "p"))
    fld = etree.SubElement(p, qn("a", "fld"))
    fld.set("id", "{" + str(uuid.uuid4()).upper() + "}")
    fld.set("type", "slidenum")
    r = etree.SubElement(fld, qn("a", "rPr"))
    r.set("lang", "en-US")
    r.set("sz", "900")
    solid_fill(r, MUTED)
    etree.SubElement(fld, qn("a", "t")).text = "1"
    etree.SubElement(p, qn("a", "endParaRPr")).set("lang", "en-US")


def add_hf(root, sld_num: bool = True) -> None:
    for old in root.findall("p:hf", NS):
        root.remove(old)
    hf = etree.SubElement(root, qn("p", "hf"))
    hf.set("sldNum", "1" if sld_num else "0")


def add_layout_footer(sp_tree, dark: bool = False):
    color = SLATE_LIGHT if dark else MUTED
    add_rect(sp_tree, 0.6, 6.92, 12.13, 0.008, "334155" if dark else RULE, "Footer Rule")
    add_text(
        sp_tree, 0.6, 6.98, 6.0, 0.24, "Nyimbi Odero", size=9, color=color,
        name="Footer",
    )
    add_text(
        sp_tree, 11.55, 0.34, 1.18, 0.22, "NYIMBI", size=8, color=color,
        bold=True, align="r", spacing=240, name="Wordmark",
    )


def set_layout_text(sp, *, size=None, color=None, bold=None, align=None, caps=False,
                    spacing=None, no_bullet=True, font=None):
    lst = sp.find("p:txBody/a:lstStyle", NS)
    if lst is None:
        return
    lvl = lst.find("a:lvl1pPr", NS)
    if lvl is None:
        lvl = etree.SubElement(lst, qn("a", "lvl1pPr"))
    if align:
        lvl.set("algn", align)
    if no_bullet:
        for tag in ("buClr", "buFont", "buChar", "buAutoNum"):
            old = lvl.find(f"a:{tag}", NS)
            if old is not None:
                lvl.remove(old)
        etree.SubElement(lvl, qn("a", "buNone"))
    d = lvl.find("a:defRPr", NS)
    if d is None:
        d = etree.SubElement(lvl, qn("a", "defRPr"))
    if size:
        d.set("sz", str(int(size * 100)))
    if bold is not None:
        d.set("b", "1" if bold else "0")
    if caps:
        d.set("cap", "all")
    if spacing is not None:
        d.set("spc", str(spacing))
    if color:
        old = d.find("a:solidFill", NS)
        if old is not None:
            d.remove(old)
        solid_fill(d, color)
    if font:
        old = d.find("a:latin", NS)
        if old is not None:
            d.remove(old)
        etree.SubElement(d, qn("a", "latin")).set("typeface", font)


def build_theme(xml: bytes) -> bytes:
    root = etree.fromstring(xml)
    scheme = root.find("a:themeElements/a:clrScheme", NS)
    scheme.set("name", "Nyimbi")
    colors = {
        "dk1": INK, "lt1": PAPER, "dk2": INK_2, "lt2": PAPER_2,
        "accent1": TEAL, "accent2": INK_2, "accent3": SLATE,
        "accent4": AMBER, "accent5": SLATE_LIGHT, "accent6": RULE,
        "hlink": TEAL, "folHlink": TEAL_DARK,
    }
    for slot, color in colors.items():
        node = scheme.find(f"a:{slot}", NS)
        for child in list(node):
            node.remove(child)
        etree.SubElement(node, qn("a", "srgbClr")).set("val", color)
    fonts = root.find("a:themeElements/a:fontScheme", NS)
    fonts.set("name", "Nyimbi")
    for tag, face in (("majorFont", "Georgia"), ("minorFont", "Arial")):
        f = fonts.find(f"a:{tag}", NS)
        for child_tag in ("latin", "ea", "cs"):
            node = f.find(f"a:{child_tag}", NS)
            if node is not None:
                node.set("typeface", face)

    # Flat shapes by default: no drop shadows or 3-D bevels on inserted objects.
    effects = root.find("a:themeElements/a:fmtScheme/a:effectStyleLst", NS)
    for style in effects.findall("a:effectStyle", NS):
        effect_lst = style.find("a:effectLst", NS)
        if effect_lst is not None:
            for child in list(effect_lst):
                effect_lst.remove(child)
        for tag in ("scene3d", "sp3d"):
            node = style.find(f"a:{tag}", NS)
            if node is not None:
                style.remove(node)
    return etree.tostring(root, xml_declaration=True, encoding="UTF-8", standalone=True)


def build_master(xml: bytes) -> bytes:
    root = etree.fromstring(xml)
    c_sld = root.find("p:cSld", NS)
    set_bg(c_sld, PAPER)
    sp_tree = c_sld.find("p:spTree", NS)

    title = shape_by_ph(sp_tree, "title")
    body = shape_by_ph(sp_tree, "body", 1)
    set_xfrm(title, 0.6, 0.55, 10.95, 0.86)
    set_body_pr(title, "t")
    set_xfrm(body, 0.6, 1.60, 12.13, 5.03)
    set_body_pr(body, "t")

    for ph in ("dt", "ftr", "sldNum"):
        remove_shape(sp_tree, shape_by_ph(sp_tree, ph))

    add_rect(sp_tree, 0.6, 0.24, 0.55, 0.035, TEAL, "Accent Rule")
    add_layout_footer(sp_tree)

    tx_styles = root.find("p:txStyles", NS)
    old_title = tx_styles.find("p:titleStyle", NS)
    old_body = tx_styles.find("p:bodyStyle", NS)

    def lvl(level: int, size: int, mar_l: int, indent: int, bullet: str, color: str):
        ppr = etree.Element(qn("a", f"lvl{level}pPr"))
        ppr.attrib.update({
            "marL": str(mar_l), "indent": str(indent), "algn": "l",
            "defTabSz": "457200", "rtl": "0", "eaLnBrk": "1",
            "latinLnBrk": "0", "hangingPunct": "1",
        })
        ln = etree.SubElement(ppr, qn("a", "lnSpc"))
        etree.SubElement(ln, qn("a", "spcPct")).set("val", "115000")
        before = etree.SubElement(ppr, qn("a", "spcBef"))
        etree.SubElement(before, qn("a", "spcPts")).set("val", "0")
        after = etree.SubElement(ppr, qn("a", "spcAft"))
        etree.SubElement(after, qn("a", "spcPts")).set("val", "600")
        bu_clr = etree.SubElement(ppr, qn("a", "buClr"))
        etree.SubElement(bu_clr, qn("a", "srgbClr")).set("val", TEAL)
        etree.SubElement(ppr, qn("a", "buFont")).set("typeface", "Arial")
        etree.SubElement(ppr, qn("a", "buChar")).set("char", bullet)
        d = etree.SubElement(ppr, qn("a", "defRPr"))
        d.set("sz", str(size))
        d.set("kern", "1200")
        solid_fill(d, color)
        etree.SubElement(d, qn("a", "latin")).set("typeface", "+mn-lt")
        etree.SubElement(d, qn("a", "ea")).set("typeface", "+mn-ea")
        etree.SubElement(d, qn("a", "cs")).set("typeface", "+mn-cs")
        return ppr

    title_style = etree.Element(qn("p", "titleStyle"))
    t_ppr = etree.SubElement(title_style, qn("a", "lvl1pPr"))
    t_ppr.attrib.update({"algn": "l", "defTabSz": "457200", "rtl": "0",
                         "eaLnBrk": "1", "latinLnBrk": "0", "hangingPunct": "1"})
    before = etree.SubElement(t_ppr, qn("a", "spcBef"))
    etree.SubElement(before, qn("a", "spcPct")).set("val", "0")
    etree.SubElement(t_ppr, qn("a", "buNone"))
    d = etree.SubElement(t_ppr, qn("a", "defRPr"))
    d.set("sz", "2800")
    d.set("b", "1")
    d.set("kern", "1200")
    solid_fill(d, INK)
    etree.SubElement(d, qn("a", "latin")).set("typeface", "+mj-lt")
    etree.SubElement(d, qn("a", "ea")).set("typeface", "+mj-ea")
    etree.SubElement(d, qn("a", "cs")).set("typeface", "+mj-cs")

    body_style = etree.Element(qn("p", "bodyStyle"))
    levels = [
        (1, 1400, 228600, -228600, "•", BODY),
        (2, 1200, 457200, -228600, "–", BODY),
        (3, 1100, 685800, -228600, "•", BODY),
        (4, 1000, 914400, -228600, "–", BODY),
        (5, 1000, 1143000, -228600, "•", BODY),
    ]
    for args in levels:
        body_style.append(lvl(*args))

    tx_styles.replace(old_title, title_style)
    tx_styles.replace(old_body, body_style)
    return etree.tostring(root, xml_declaration=True, encoding="UTF-8", standalone=True)


def build_layout(xml: bytes, number: int) -> bytes:
    root = etree.fromstring(xml)
    c_sld = root.find("p:cSld", NS)
    sp_tree = c_sld.find("p:spTree", NS)
    set_bg(c_sld, PAPER)

    # Drop date and footer placeholders everywhere; page numbers are added per layout.
    for ph in ("dt", "ftr"):
        remove_shape(sp_tree, shape_by_ph(sp_tree, ph))

    if number == 1:  # Title
        root.set("showMasterSp", "0")
        c_sld.set("name", "Title")
        title = shape_by_ph(sp_tree, "ctrTitle")
        sub = shape_by_ph(sp_tree, "subTitle", 1)
        remove_shape(sp_tree, shape_by_ph(sp_tree, "sldNum"))
        set_xfrm(title, 0.6, 2.10, 11.2, 1.75)
        set_body_pr(title, "t")
        set_layout_text(title, size=40, bold=True, align="l", font="Georgia", color=INK)
        set_xfrm(sub, 0.6, 3.95, 10.5, 0.95)
        set_body_pr(sub, "t")
        set_layout_text(sub, size=16, align="l", color=MUTED)
        add_rect(sp_tree, 0.6, 1.85, 1.20, 0.06, TEAL, "Title Rule")
        add_layout_footer(sp_tree)

    elif number == 2:  # Title and Content
        c_sld.set("name", "Title and Content")
        title = shape_by_ph(sp_tree, "title")
        set_xfrm(title, 0.6, 0.55, 10.95, 0.86)
        set_body_pr(title, "t")
        body = shape_by_ph(sp_tree, "obj", 1)
        set_xfrm(body, 0.6, 1.60, 12.13, 5.03)
        set_body_pr(body, "t")
        add_page_number(sp_tree)
        add_hf(root)

    elif number == 3:  # Section Header
        root.set("showMasterSp", "0")
        c_sld.set("name", "Section Divider")
        set_bg(c_sld, INK_2)
        title = shape_by_ph(sp_tree, "title")
        body = shape_by_ph(sp_tree, "body", 1)
        remove_shape(sp_tree, shape_by_ph(sp_tree, "sldNum"))
        set_xfrm(body, 0.6, 2.80, 8.0, 0.30)
        set_body_pr(body, "b")
        set_layout_text(body, size=11, color="5EEAD4", caps=True, spacing=240, align="l")
        set_xfrm(title, 0.6, 3.30, 11.5, 1.50)
        set_body_pr(title, "t")
        set_layout_text(title, size=40, bold=True, align="l", font="Georgia", color="FFFFFF")
        add_rect(sp_tree, 0.6, 3.18, 0.90, 0.05, "5EEAD4", "Divider Rule")
        add_text(sp_tree, 11.55, 0.34, 1.18, 0.22, "NYIMBI", size=8,
                 color=SLATE_LIGHT, bold=True, align="r", spacing=240, name="Wordmark")

    elif number == 4:  # Two Content
        c_sld.set("name", "Two Content")
        title = shape_by_ph(sp_tree, "title")
        set_xfrm(title, 0.6, 0.55, 10.95, 0.86)
        set_body_pr(title, "t")
        left = shape_by_ph(sp_tree, "obj", 1)
        right = shape_by_ph(sp_tree, "obj", 2)
        for sp, x in ((left, 0.6), (right, 6.85)):
            set_xfrm(sp, x, 1.60, 5.88, 5.03)
            set_body_pr(sp, "t")
        add_page_number(sp_tree)
        add_hf(root)

    elif number == 5:  # Comparison
        c_sld.set("name", "Comparison")
        title = shape_by_ph(sp_tree, "title")
        set_xfrm(title, 0.6, 0.55, 10.95, 0.86)
        set_body_pr(title, "t")
        left_h = shape_by_ph(sp_tree, "body", 1)
        left_c = shape_by_ph(sp_tree, "obj", 2)
        right_h = shape_by_ph(sp_tree, "body", 3)
        right_c = shape_by_ph(sp_tree, "obj", 4)
        for sp, x in ((left_h, 0.6), (right_h, 6.85)):
            set_xfrm(sp, x, 1.55, 5.88, 0.42)
            set_body_pr(sp, "b")
            set_layout_text(sp, size=13, bold=True, color=TEAL, align="l")
        for sp, x in ((left_c, 0.6), (right_c, 6.85)):
            set_xfrm(sp, x, 2.08, 5.88, 4.55)
            set_body_pr(sp, "t")
        add_page_number(sp_tree)
        add_hf(root)

    elif number == 6:  # Title Only
        c_sld.set("name", "Title Only")
        title = shape_by_ph(sp_tree, "title")
        set_xfrm(title, 0.6, 0.55, 10.95, 0.86)
        set_body_pr(title, "t")
        add_page_number(sp_tree)
        add_hf(root)

    elif number == 8:  # Content with Caption -> Chart or Table with Source
        c_sld.set("name", "Chart or Table with Source")
        title = shape_by_ph(sp_tree, "title")
        set_xfrm(title, 0.6, 0.55, 10.95, 0.86)
        set_body_pr(title, "t")
        body = shape_by_ph(sp_tree, "obj", 1)
        cap = shape_by_ph(sp_tree, "body", 2)
        set_xfrm(body, 0.6, 1.50, 12.13, 4.63)
        set_body_pr(body, "t")
        set_xfrm(cap, 0.6, 6.28, 12.13, 0.40)
        set_body_pr(cap, "t")
        set_layout_text(cap, size=9, color=MUTED, align="l")
        add_page_number(sp_tree)
        add_hf(root)

    elif number == 9:  # Picture with Caption -> Image with Caption
        c_sld.set("name", "Image with Caption")
        title = shape_by_ph(sp_tree, "title")
        set_xfrm(title, 0.6, 0.55, 10.95, 0.86)
        set_body_pr(title, "t")
        pic = shape_by_ph(sp_tree, "pic", 1)
        cap = shape_by_ph(sp_tree, "body", 2)
        set_xfrm(pic, 0.6, 1.50, 12.13, 4.58)
        set_xfrm(cap, 0.6, 6.22, 12.13, 0.40)
        set_body_pr(cap, "t")
        set_layout_text(cap, size=9, color=MUTED, align="l")
        add_page_number(sp_tree)
        add_hf(root)

    elif number == 7:  # Blank -> Full-bleed Image
        root.set("showMasterSp", "0")
        c_sld.set("name", "Full-bleed Image")
        for sp in list(sp_tree.findall("p:sp", NS)):
            sp_tree.remove(sp)
        pic = etree.SubElement(sp_tree, qn("p", "sp"))
        nv = etree.SubElement(pic, qn("p", "nvSpPr"))
        etree.SubElement(nv, qn("p", "cNvPr")).attrib.update(
            {"id": str(next_shape_id(sp_tree)), "name": "Picture Placeholder"}
        )
        etree.SubElement(nv, qn("p", "cNvSpPr"))
        nv_pr = etree.SubElement(nv, qn("p", "nvPr"))
        etree.SubElement(nv_pr, qn("p", "ph")).attrib.update({"type": "pic", "idx": "1"})
        sp_pr = etree.SubElement(pic, qn("p", "spPr"))
        xfrm = etree.SubElement(sp_pr, qn("a", "xfrm"))
        etree.SubElement(xfrm, qn("a", "off")).attrib.update({"x": "0", "y": "0"})
        etree.SubElement(xfrm, qn("a", "ext")).attrib.update(
            {"cx": emu(13.333), "cy": emu(7.5)}
        )
        geom = etree.SubElement(sp_pr, qn("a", "prstGeom"))
        geom.set("prst", "rect")
        etree.SubElement(geom, qn("a", "avLst"))
        tx = etree.SubElement(pic, qn("p", "txBody"))
        etree.SubElement(tx, qn("a", "bodyPr"))
        etree.SubElement(tx, qn("a", "lstStyle"))
        etree.SubElement(tx, qn("a", "p"))

    return etree.tostring(root, xml_declaration=True, encoding="UTF-8", standalone=True)


def remove_vertical_layouts(files: dict[str, bytes]) -> None:
    """Drop layout parts 10 and 11 (the vertical-text layouts)."""
    removed = []
    for number in (10, 11):
        name = f"ppt/slideLayouts/slideLayout{number}.xml"
        if name in files:
            removed.append(f"slideLayout{number}.xml")
    if not removed:
        return

    master_name = "ppt/slideMasters/slideMaster1.xml"
    master = etree.fromstring(files[master_name])
    master_rels_name = "ppt/slideMasters/_rels/slideMaster1.xml.rels"
    master_rels = etree.fromstring(files[master_rels_name])
    rel_map = {
        rel.get("Id"): rel.get("Target", "").split("/")[-1]
        for rel in master_rels
    }
    layout_ids = master.find("p:sldLayoutIdLst", NS)
    for entry in list(layout_ids):
        if rel_map.get(entry.get(qn("r", "id"))) in removed:
            layout_ids.remove(entry)
    files[master_name] = etree.tostring(
        master, xml_declaration=True, encoding="UTF-8", standalone=True
    )
    for rel in list(master_rels):
        target = rel.get("Target", "")
        if target.split("/")[-1] in removed:
            master_rels.remove(rel)
    files[master_rels_name] = etree.tostring(
        master_rels, xml_declaration=True, encoding="UTF-8", standalone=True
    )

    ct = etree.fromstring(files["[Content_Types].xml"])
    for override in list(ct):
        name = override.get("PartName", "")
        if name.split("/")[-1] in removed:
            ct.remove(override)
    ct_ns = "http://schemas.openxmlformats.org/package/2006/content-types"
    etree.register_namespace("ct", ct_ns)
    files["[Content_Types].xml"] = etree.tostring(
        ct, xml_declaration=True, encoding="UTF-8", standalone=True
    )

    for number in (10, 11):
        for name in (
            f"ppt/slideLayouts/slideLayout{number}.xml",
            f"ppt/slideLayouts/_rels/slideLayout{number}.xml.rels",
        ):
            files.pop(name, None)


def reorder_layouts(files: dict[str, bytes]) -> None:
    """Set the layout-gallery order explicitly."""
    order = [
        "slideLayout1.xml",   # Title
        "slideLayout2.xml",   # Title and Content
        "slideLayout3.xml",   # Section Divider
        "slideLayout4.xml",   # Two Content
        "slideLayout5.xml",   # Comparison
        "slideLayout8.xml",   # Chart or Table with Source
        "slideLayout9.xml",   # Image with Caption
        "slideLayout7.xml",   # Full-bleed Image
        "slideLayout6.xml",   # Title Only
    ]
    master_name = "ppt/slideMasters/slideMaster1.xml"
    master = etree.fromstring(files[master_name])
    master_rels = etree.fromstring(files["ppt/slideMasters/_rels/slideMaster1.xml.rels"])
    rel_map = {
        rel.get("Id"): rel.get("Target", "").split("/")[-1]
        for rel in master_rels
    }
    lst = master.find("p:sldLayoutIdLst", NS)
    entries = {rel_map.get(e.get(qn("r", "id"))): e for e in list(lst)}
    for e in list(lst):
        lst.remove(e)
    for name in order:
        if name in entries:
            lst.append(entries[name])
    for e in entries.values():
        if e.getparent() is None:
            lst.append(e)
    files[master_name] = etree.tostring(
        master, xml_declaration=True, encoding="UTF-8", standalone=True
    )


def write_package(files: dict[str, bytes], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for name, data in files.items():
            z.writestr(name, data)


def main() -> None:
    ASSETS.mkdir(parents=True, exist_ok=True)
    tmp = Path(tempfile.mkdtemp(prefix="nyimbi-potx-"))
    base = tmp / "base.pptx"
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    prs.save(str(base))

    with zipfile.ZipFile(base) as z:
        files = {info.filename: z.read(info.filename) for info in z.infolist() if not info.is_dir()}

    files["ppt/theme/theme1.xml"] = build_theme(files["ppt/theme/theme1.xml"])
    files["ppt/slideMasters/slideMaster1.xml"] = build_master(
        files["ppt/slideMasters/slideMaster1.xml"]
    )
    for number in range(1, 12):
        name = f"ppt/slideLayouts/slideLayout{number}.xml"
        if name in files:
            files[name] = build_layout(files[name], number)

    remove_vertical_layouts(files)
    reorder_layouts(files)

    # Presentation content type, both variants.
    pres = etree.fromstring(files["ppt/presentation.xml"])
    sz = pres.find("p:sldSz", NS)
    sz.set("cx", emu(13.333))
    sz.set("cy", emu(7.5))
    files["ppt/presentation.xml"] = etree.tostring(
        pres, xml_declaration=True, encoding="UTF-8", standalone=True
    )

    ct = etree.fromstring(files["[Content_Types].xml"])
    for override in ct:
        if override.get("PartName") == "/ppt/presentation.xml":
            override.set(
                "ContentType",
                "application/vnd.openxmlformats-officedocument.presentationml.template.main+xml",
            )
    files["[Content_Types].xml"] = etree.tostring(
        ct, xml_declaration=True, encoding="UTF-8", standalone=True
    )

    potx = ASSETS / "nyimbi-strategy.potx"
    write_package(files, potx)

    # Preview variant: presentation content type, so python-pptx and LibreOffice
    # can build and render sample slides without changing the .potx.
    for override in ct:
        if override.get("PartName") == "/ppt/presentation.xml":
            override.set(
                "ContentType",
                "application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml",
            )
    files["[Content_Types].xml"] = etree.tostring(
        ct, xml_declaration=True, encoding="UTF-8", standalone=True
    )
    preview = ASSETS / "nyimbi-strategy-preview.pptx"
    write_package(files, preview)

    shutil.rmtree(tmp, ignore_errors=True)
    print(f"wrote {potx} ({potx.stat().st_size} bytes)")
    print(f"wrote {preview} ({preview.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
