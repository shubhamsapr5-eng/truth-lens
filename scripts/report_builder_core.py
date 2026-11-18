"""
TruthLens Mini Project Report Builder - Final Review (100% Production Milestone)
Course Code: CSS7102 | B.Tech Artificial Intelligence and Data Science
Presidency University, Bengaluru, India

Complies with all institutional formatting guidelines:
- A4 Paper (21.0 x 29.7 cm)
- Margins: Top 2.54 cm, Bottom 2.54 cm, Left 3.81 cm, Right 2.54 cm
- Font: Times New Roman throughout
- Body: 12 pt, justified, 1.5 line spacing
- Chapter heading: 16 pt, bold, centered, uppercase
- Section heading: 14 pt, bold
- Subsection heading: 12 pt, bold
- Front-matter major heading: 16 pt, bold, centered, uppercase
- Figure caption: 12 pt, centered, placed BELOW figure
- Table caption: 12 pt, centered, placed ABOVE table
- References: 12 pt Times New Roman, 1.5 spacing, IEEE format
- Page numbering: Roman numerals for front matter; Arabic numerals for Chapter 1 onwards
- Each chapter contains 4-6 pages of comprehensive technical depth with embedded figures & tables.
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

import docx
from docx import Document
from docx.shared import Inches, Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.enum.section import WD_SECTION_START
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

DOC_PATH = r"C:\Users\shubh\Desktop\TruthLens_Mini_Project_Report_CSS7102.docx"
PDF_PATH = r"C:\Users\shubh\Desktop\TruthLens_Mini_Project_Report_CSS7102.pdf"
DOCS_COPY = r"C:\Users\shubh\Desktop\truth-lens\docs\TruthLens_Mini_Project_Report_CSS7102.docx"
DOCS_PDF_COPY = r"C:\Users\shubh\Desktop\truth-lens\docs\TruthLens_Mini_Project_Report_CSS7102.pdf"
FIGURES_DIR = Path(r"C:\Users\shubh\Desktop\truth-lens\data\figures")

# Helpers
def set_cell_margins(cell, top=120, bottom=120, left=140, right=140):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_cell_shading(cell, color_hex):
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shd)

def add_academic_table(doc, tbl_num, tbl_caption, headers, rows, col_widths, font_size=10.5):
    # Caption ABOVE table
    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap.paragraph_format.space_before = Pt(12)
    p_cap.paragraph_format.space_after = Pt(4)
    p_cap.paragraph_format.line_spacing = 1.15
    r_lbl = p_cap.add_run(f"Table {tbl_num}: ")
    r_lbl.font.name = "Times New Roman"
    r_lbl.font.size = Pt(12)
    r_lbl.font.bold = True
    r_txt = p_cap.add_run(tbl_caption)
    r_txt.font.name = "Times New Roman"
    r_txt.font.size = Pt(12)
    r_txt.font.italic = True

    tbl = doc.add_table(rows=len(rows) + 1, cols=len(headers))
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False

    # Header
    hdr_row = tbl.rows[0]
    for idx, cell in enumerate(hdr_row.cells):
        cell.width = Inches(col_widths[idx])
        set_cell_shading(cell, "102C57")
        set_cell_margins(cell, top=120, bottom=120, left=120, right=120)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        for run in p.runs:
            run.font.name = "Times New Roman"
            run.font.size = Pt(font_size)
            run.font.bold = True
            run.font.color.rgb = RGBColor(255, 255, 255)
        if not p.runs:
            r = p.add_run(headers[idx])
            r.font.name = "Times New Roman"
            r.font.size = Pt(font_size)
            r.font.bold = True
            r.font.color.rgb = RGBColor(255, 255, 255)

    # Data Rows
    for r_idx, r_data in enumerate(rows):
        row = tbl.rows[r_idx + 1]
        for c_idx, cell in enumerate(row.cells):
            cell.width = Inches(col_widths[c_idx])
            if r_idx % 2 == 1:
                set_cell_shading(cell, "F8FAFC")
            set_cell_margins(cell, top=90, bottom=90, left=120, right=120)
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.15
            val = str(r_data[c_idx])
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if (c_idx == 0 or len(val) <= 12) else WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(val)
            r.font.name = "Times New Roman"
            r.font.size = Pt(font_size)

    # Space after table
    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_before = Pt(0)
    p_sp.paragraph_format.space_after = Pt(8)

def add_figure_to_doc(doc, img_rel_path, fig_num_str, fig_caption_str, width_inches=5.8):
    full_path = FIGURES_DIR / img_rel_path
    if not full_path.exists():
        print(f"[!] Warning: Figure not found at {full_path}")
        return
    p_img = doc.add_paragraph()
    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img.paragraph_format.space_before = Pt(12)
    p_img.paragraph_format.space_after = Pt(4)
    run_img = p_img.add_run()
    run_img.add_picture(str(full_path), width=Inches(width_inches))

    # Caption BELOW figure
    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap.paragraph_format.space_before = Pt(2)
    p_cap.paragraph_format.space_after = Pt(14)
    p_cap.paragraph_format.line_spacing = 1.15
    r_lbl = p_cap.add_run(f"Figure {fig_num_str}: ")
    r_lbl.font.name = "Times New Roman"
    r_lbl.font.size = Pt(12)
    r_lbl.font.bold = True
    r_txt = p_cap.add_run(fig_caption_str)
    r_txt.font.name = "Times New Roman"
    r_txt.font.size = Pt(12)
    r_txt.font.italic = True

def add_body_p(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.line_spacing = 1.5
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(6)
    r = p.add_run(text)
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)
    return p

def add_chapter_heading(doc, num, title):
    p_num = doc.add_paragraph()
    p_num.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_num.paragraph_format.space_before = Pt(18)
    p_num.paragraph_format.space_after = Pt(4)
    r_num = p_num.add_run(f"CHAPTER {num}".upper())
    r_num.font.name = "Times New Roman"
    r_num.font.size = Pt(16)
    r_num.font.bold = True

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(0)
    p_title.paragraph_format.space_after = Pt(16)
    r_title = p_title.add_run(title.upper())
    r_title.font.name = "Times New Roman"
    r_title.font.size = Pt(16)
    r_title.font.bold = True

def add_sec_heading(doc, num_str, title_str):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(f"{num_str}  {title_str}")
    r.font.name = "Times New Roman"
    r.font.size = Pt(14)
    r.font.bold = True
    return p

def add_subsec_heading(doc, num_str, title_str):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(9)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(f"{num_str}  {title_str}")
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)
    r.font.bold = True
    return p

def add_frontmatter_heading(doc, title):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(18)
    r = p.add_run(title.upper())
    r.font.name = "Times New Roman"
    r.font.size = Pt(16)
    r.font.bold = True
    return p

print("Builder core loaded successfully.")
