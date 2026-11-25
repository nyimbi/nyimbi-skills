#!/usr/bin/env python3
"""Build a sample deck from the strategy template and render it for inspection.

    python3 scripts/build_template_preview.py

Writes assets/template-preview.pptx, assets/template-preview.pdf and
assets/template-preview/*.png. Run build_template.py first.
"""
from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Any

import lxml.etree as etree
from PIL import Image, ImageDraw
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
INK = RGBColor(0x11, 0x18, 0x27)
BODY = RGBColor(0x37, 0x41, 0x51)
MUTED = RGBColor(0x6B, 0x72, 0x80)
TEAL = RGBColor(0x0F, 0x76, 0x6E)
PAPER = RGBColor(0xFB, 0xFA, 0xF7)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)


def set_title(slide, text: str) -> None:
    title = slide.shapes.title
    assert title is not None
    title.text = text


def ph(slide, idx: int) -> Any:
    return slide.placeholders[idx]


def pic(slide, idx: int) -> Any:
    return slide.placeholders[idx]


def bullets(shape: Any, items: list[tuple[int, str]]) -> None:
    tf = shape.text_frame
    tf.clear()
    for i, (level, text) in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = text
        p.level = level


def gradient(path: Path, w=1600, h=900) -> None:
    img = Image.new("RGB", (w, h))
    px = img.load()
    assert px is not None
    for y in range(h):
        for x in range(w):
            u, v = x / w, y / h
            r = int(11 + 10 * u + 6 * v)
            g = int(30 + 90 * (1 - v) + 30 * u)
            b = int(45 + 85 * (1 - u) + 30 * (1 - v))
            px[x, y] = (r, g, b)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 660, w, h], fill=(11, 18, 32))
    d.rectangle([80, 80, 88, 300], fill=(15, 118, 110))
    img.save(path)


def main() -> None:
    src = ASSETS / "nyimbi-strategy-preview.pptx"
    prs = Presentation(str(src))
    layouts = list(prs.slide_masters[0].slide_layouts)
    by_name = {l.name: l for l in layouts}

    # 1 Title
    s = prs.slides.add_slide(by_name["Title"])
    set_title(s, "Strategy that survives contact with the market")
    ph(s, 1).text = "A decision-first template for Nyimbi Odero · 2026"

    # 2 Title and Content
    s = prs.slides.add_slide(by_name["Title and Content"])
    set_title(s, "Two segments drive 80% of profit, so the growth plan should concentrate there")
    bullets(ph(s, 1), [
        (0, "Enterprise and mid-market account for four fifths of contribution margin."),
        (0, "The long tail consumes 60% of support and onboarding capacity."),
        (1, "Serve it through a product-led tier or a partner, not the direct team."),
        (0, "Concentrating spend adds an estimated 3.2 points of margin within 18 months."),
        (1, "Assumption: churn in the long tail stays flat; kill condition on slide 7."),
    ])

    # 3 Section divider
    s = prs.slides.add_slide(by_name["Section Divider"])
    ph(s, 1).text = "01 · DIAGNOSE"
    set_title(s, "What is true, and why")

    # 4 Two Content
    s = prs.slides.add_slide(by_name["Two Content"])
    set_title(s, "The value sits in two segments; the right to win sits in distribution")
    bullets(ph(s, 1), [
        (0, "Where the value sits"),
        (1, "Enterprise: 46% of margin, 12% of customers."),
        (1, "Mid-market: 34% of margin, 23% of customers."),
        (0, "Long tail: 20% of margin, 65% of customers."),
    ])
    bullets(ph(s, 2), [
        (0, "Where we can win"),
        (1, "Only national distribution reaches enterprise procurement."),
        (1, "Two incumbents lack mid-market onboarding."),
        (0, "Do not compete on price in the long tail."),
    ])

    # 5 Comparison
    s = prs.slides.add_slide(by_name["Comparison"])
    set_title(s, "Option A protects margin faster; Option B buys a larger market later")
    ph(s, 1).text = "Option A · Concentrate"
    bullets(ph(s, 2), [
        (0, "Reallocate 8 of 24 initiatives."),
        (0, "Margin +3.2 pts in 18 months."),
        (0, "Execution risk: low."),
        (0, "Reversible in one quarter."),
    ])
    ph(s, 3).text = "Option B · Expand"
    bullets(ph(s, 4), [
        (0, "Enter two adjacent markets."),
        (0, "Margin +1.1 pts in 24 months."),
        (0, "Execution risk: high."),
        (0, "Reversible only by exit."),
    ])

    # 6 Chart or table with source
    s = prs.slides.add_slide(by_name["Chart or Table with Source"])
    set_title(s, "Margin recovery is one quarter behind, driven by three stalled initiatives")
    rows, cols = 4, 4
    table = s.shapes.add_table(rows, cols, Inches(0.6), Inches(1.60), Inches(12.1), Inches(2.65)).table
    widths = (4.0, 2.7, 2.7, 2.7)
    for i, width in enumerate(widths):
        table.columns[i].width = Inches(width)
    for i in range(rows):
        table.rows[i].height = Inches(0.50 if i == 0 else 0.55)
    data = [
        ["Driver", "Plan", "Actual", "Gap"],
        ["Cost programme", "−2.4 pts", "−1.1 pts", "1.3 pts"],
        ["Procurement", "−0.8 pts", "−0.6 pts", "0.2 pts"],
        ["Service productivity", "−0.9 pts", "−0.4 pts", "0.5 pts"],
    ]
    for r, row in enumerate(data):
        for c, value in enumerate(row):
            cell = table.cell(r, c)
            cell.text = value
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            cell.margin_left = Inches(0.12)
            cell.margin_right = Inches(0.12)
            for p in cell.text_frame.paragraphs:
                p.font.size = Pt(12 if r else 11)
                p.font.name = "Arial"
                p.font.bold = r == 0
                p.font.color.rgb = WHITE if r == 0 else BODY
            cell.fill.solid()
            cell.fill.fore_color.rgb = TEAL if r == 0 else (PAPER if r % 2 else RGBColor(0xF3, 0xF1, 0xEC))
    ph(s, 2).text = "Source: finance review, Q2 2026. Gap to the board-approved recovery curve."

    # 7 Image with caption
    img = ASSETS / "template-cover.png"
    gradient(img)
    s = prs.slides.add_slide(by_name["Image with Caption"])
    set_title(s, "The market is moving faster than the operating model")
    pic(s, 1).insert_picture(str(img))
    ph(s, 2).text = "Illustrative image. Replace with approved photography or a client exhibit."

    # 8 Full-bleed image
    s = prs.slides.add_slide(by_name["Full-bleed Image"])
    pic(s, 1).insert_picture(str(img))

    # 9 Title only: 2x2
    s = prs.slides.add_slide(by_name["Title Only"])
    set_title(s, "Concentrate where the value and the right to win overlap")
    boxes = [
        ("Invest", "High growth, high profit", 0.6, 1.75, TEAL, WHITE),
        ("Nurture", "High growth, low profit", 6.85, 1.75, RGBColor(0xF3, 0xF1, 0xEC), INK),
        ("Harvest", "Low growth, high profit", 0.6, 4.15, RGBColor(0xF3, 0xF1, 0xEC), INK),
        ("Exit", "Low growth, low profit", 6.85, 4.15, RGBColor(0xE5, 0xE7, 0xEB), MUTED),
    ]
    for label, sub, x, y, fill, color in boxes:
        sh = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(5.85), Inches(2.05))
        sh.fill.solid(); sh.fill.fore_color.rgb = fill
        sh.line.color.rgb = RGBColor(0xD1, 0xD5, 0xDB)
        sh.shadow.inherit = False
        tf = sh.text_frame
        tf.clear()
        p = tf.paragraphs[0]; p.text = label
        p.font.size = Pt(20); p.font.name = "Georgia"; p.font.bold = True; p.font.color.rgb = color
        p.alignment = PP_ALIGN.LEFT
        p2 = tf.add_paragraph(); p2.text = sub
        p2.font.size = Pt(12); p2.font.name = "Arial"; p2.font.color.rgb = color
        p2.alignment = PP_ALIGN.LEFT

    # Enable slide numbers on every slide (the layout carries the field).
    p_ns = "http://schemas.openxmlformats.org/presentationml/2006/main"
    for slide in prs.slides:
        sld = slide._element
        for old in sld.findall(f"{{{p_ns}}}hf"):
            sld.remove(old)
        hf = etree.Element(f"{{{p_ns}}}hf")
        hf.set("sldNum", "1")
        sld.insert(1, hf)

    out = ASSETS / "template-preview.pptx"
    prs.save(str(out))

    pdf = ASSETS / "template-preview.pdf"
    subprocess.run(
        ["soffice", "--headless", "--convert-to", "pdf", "--outdir", str(ASSETS), str(out)],
        check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    png_dir = ASSETS / "template-preview"
    png_dir.mkdir(exist_ok=True)
    subprocess.run(
        ["pdftoppm", "-png", "-r", "110", str(pdf), str(png_dir / "slide")],
        check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    print(f"wrote {out}")
    print(f"wrote {pdf}")
    print(f"wrote {len(list(png_dir.glob('slide-*.png')))} pngs in {png_dir}")


if __name__ == "__main__":
    main()
