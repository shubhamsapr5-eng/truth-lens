"""
Generates the publication-grade Presidency University Mini Project Report (CSS7102)
for TruthLens strictly complying with all institutional format specifications:
- Page size: A4 (21.0 cm x 29.7 cm)
- Margins: Top 2.54 cm | Bottom 2.54 cm | Left 3.81 cm | Right 2.54 cm
- Font: Times New Roman throughout
- Body text: 12 pt, justified, 1.5 line spacing
- Chapter heading: 16 pt, bold, centered, uppercase
- Section heading (e.g., 1.1): 14 pt, bold
- Subsection heading (e.g., 1.1.1): 12 pt, bold
- Front-matter major heading: 16 pt, bold, centered, uppercase
- Figure caption: 12 pt, centered, placed BELOW the figure
- Table caption: 12 pt, centered, placed ABOVE the table
- Table text: 11 pt Times New Roman (or 10 pt for dense tables)
- References: 12 pt Times New Roman, 1.5 spacing, IEEE format
- Page numbering: Lower Roman numerals (i, ii, iii...) for front matter; Arabic numerals (1, 2, 3...) beginning with Chapter 1
Includes 13 embedded 300 DPI figures, 14 academic tables, and 3 technical appendices.
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

sys.path.append(str(Path(__file__).resolve().parent))
import report_data
import report_chapters

DOC_PATH = r"C:\Users\shubh\Desktop\TruthLens_Mini_Project_Report_CSS7102.docx"
PDF_PATH = r"C:\Users\shubh\Desktop\TruthLens_Mini_Project_Report_CSS7102.pdf"
DOCS_COPY = r"C:\Users\shubh\Desktop\truth-lens\docs\TruthLens_Mini_Project_Report_CSS7102.docx"
DOCS_PDF_COPY = r"C:\Users\shubh\Desktop\truth-lens\docs\TruthLens_Mini_Project_Report_CSS7102.pdf"
FIGURES_DIR = Path(r"C:\Users\shubh\Desktop\truth-lens\data\figures")


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


def format_table_header(row, col_widths, bg_hex="102C57", font_size=10.5):
    for idx, cell in enumerate(row.cells):
        cell.width = col_widths[idx]
        set_cell_shading(cell, bg_hex)
        set_cell_margins(cell, top=130, bottom=130, left=130, right=130)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        for run in p.runs:
            run.font.name = "Times New Roman"
            run.font.size = Pt(font_size)
            run.font.bold = True
            run.font.color.rgb = RGBColor(255, 255, 255)


def format_table_row(row, col_widths, is_even=False, font_size=10.5):
    for idx, cell in enumerate(row.cells):
        cell.width = col_widths[idx]
        if is_even:
            set_cell_shading(cell, "F8FAFC")
        set_cell_margins(cell, top=90, bottom=90, left=130, right=130)
        p = cell.paragraphs[0]
        p.paragraph_format.line_spacing = 1.2
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        for run in p.runs:
            run.font.name = "Times New Roman"
            run.font.size = Pt(font_size)


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


def add_chapter_heading(doc, num, title):
    p_num = doc.add_paragraph()
    p_num.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_num.paragraph_format.space_before = Pt(18)
    p_num.paragraph_format.space_after = Pt(4)
    p_num.paragraph_format.keep_with_next = True
    r_num = p_num.add_run(f"CHAPTER {num}".upper())
    r_num.font.name = "Times New Roman"
    r_num.font.size = Pt(16)
    r_num.font.bold = True

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(0)
    p_title.paragraph_format.space_after = Pt(16)
    p_title.paragraph_format.keep_with_next = True
    r_title = p_title.add_run(title.upper())
    r_title.font.name = "Times New Roman"
    r_title.font.size = Pt(16)
    r_title.font.bold = True
    return p_title


def add_sec_heading(doc, num_str, title_str):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(14)
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
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(f"{num_str}  {title_str}")
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)
    r.font.bold = True
    return p


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


def add_figure_to_doc(doc, img_rel_path, fig_num_str, fig_caption_str, width_inches=5.65):
    img_path = FIGURES_DIR / img_rel_path
    if not img_path.exists():
        print(f"[!] Warning: Figure not found at: {img_path}")
        return

    p_img = doc.add_paragraph()
    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img.paragraph_format.space_before = Pt(12)
    p_img.paragraph_format.space_after = Pt(4)
    r_img = p_img.add_run()
    r_img.add_picture(str(img_path), width=Inches(width_inches))

    # Caption BELOW figure
    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap.paragraph_format.space_before = Pt(2)
    p_cap.paragraph_format.space_after = Pt(14)
    p_cap.paragraph_format.line_spacing = 1.15
    r_num = p_cap.add_run(f"Figure {fig_num_str}: ")
    r_num.font.name = "Times New Roman"
    r_num.font.size = Pt(12)
    r_num.font.bold = True
    r_txt = p_cap.add_run(fig_caption_str)
    r_txt.font.name = "Times New Roman"
    r_txt.font.size = Pt(12)
    r_txt.font.italic = True


def add_academic_table(doc, tbl_num, tbl_caption, headers, rows, col_widths_inches, font_size=10.5):
    # Caption ABOVE table
    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap.paragraph_format.space_before = Pt(14)
    p_cap.paragraph_format.space_after = Pt(4)
    p_cap.paragraph_format.line_spacing = 1.15
    r_num = p_cap.add_run(f"Table {tbl_num}: ")
    r_num.font.name = "Times New Roman"
    r_num.font.size = Pt(12)
    r_num.font.bold = True
    r_txt = p_cap.add_run(tbl_caption)
    r_txt.font.name = "Times New Roman"
    r_txt.font.size = Pt(12)
    r_txt.font.italic = True

    table = doc.add_table(rows=len(rows) + 1, cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False

    col_widths = [Inches(w) for w in col_widths_inches]

    # Header Row
    hdr_row = table.rows[0]
    for idx, cell in enumerate(hdr_row.cells):
        cell.width = col_widths[idx]
        set_cell_shading(cell, "102C57")
        set_cell_margins(cell, top=120, bottom=120, left=120, right=120)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run(headers[idx])
        r.font.name = "Times New Roman"
        r.font.size = Pt(font_size)
        r.font.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)

    # Data Rows
    for r_idx, row_data in enumerate(rows):
        row = table.rows[r_idx + 1]
        is_even = (r_idx % 2 == 1)
        for c_idx, cell in enumerate(row.cells):
            cell.width = col_widths[c_idx]
            if is_even:
                set_cell_shading(cell, "F8FAFC")
            set_cell_margins(cell, top=90, bottom=90, left=120, right=120)
            p = cell.paragraphs[0]
            p.paragraph_format.line_spacing = 1.2
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            val = str(row_data[c_idx])
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if (c_idx == 0 or len(val) <= 12) else WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(val)
            r.font.name = "Times New Roman"
            r.font.size = Pt(font_size)

    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_before = Pt(0)
    p_sp.paragraph_format.space_after = Pt(8)


def build_report():
    print("[*] Initializing Presidency University Final Project Report document...")
    doc = Document()

    # -------------------------------------------------------------
    # SECTION 1: FRONT MATTER (ROMAN NUMERALS: i, ii, iii...)
    # -------------------------------------------------------------
    s_front = doc.sections[0]
    s_front.page_width = Cm(21.0)
    s_front.page_height = Cm(29.7)
    s_front.top_margin = Cm(2.54)
    s_front.bottom_margin = Cm(2.54)
    s_front.left_margin = Cm(3.81)
    s_front.right_margin = Cm(2.54)

    # Roman numeral page numbering for front matter
    sectPr = s_front._sectPr
    pgNumType = OxmlElement('w:pgNumType')
    pgNumType.set(qn('w:fmt'), 'lowerRoman')
    pgNumType.set(qn('w:start'), '1')
    sectPr.append(pgNumType)

    # Setup footer for front matter
    footer_front = s_front.footer
    f_p = footer_front.paragraphs[0]
    f_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    fld_xml = r'<w:fldSimple %s w:instr="PAGE"/>' % nsdecls('w')
    f_p_run = f_p.add_run()
    f_p_run.font.name = "Times New Roman"
    f_p_run.font.size = Pt(11)
    f_p._p.append(parse_xml(fld_xml))

    # -------------------------------------------------------------
    # 1. TITLE PAGE
    # -------------------------------------------------------------
    p_t1 = doc.add_paragraph()
    p_t1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_t1.paragraph_format.space_before = Pt(20)
    p_t1.paragraph_format.space_after = Pt(6)
    r = p_t1.add_run("TRUTHLENS: AI-POWERED REAL-TIME NEWS CREDIBILITY AND MISINFORMATION VERIFICATION ENGINE")
    r.font.name = "Times New Roman"
    r.font.size = Pt(18)
    r.font.bold = True
    r.font.color.rgb = RGBColor(16, 44, 87)

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_before = Pt(10)
    p_sub.paragraph_format.space_after = Pt(24)
    r = p_sub.add_run("A Mini Project Report Submitted in Partial Fulfilment of the Requirements for the Award of the Degree of")
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)
    r.font.italic = True

    p_deg = doc.add_paragraph()
    p_deg.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_deg.paragraph_format.space_after = Pt(4)
    r = p_deg.add_run("BACHELOR OF TECHNOLOGY")
    r.font.name = "Times New Roman"
    r.font.size = Pt(14)
    r.font.bold = True

    p_deg2 = doc.add_paragraph()
    p_deg2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_deg2.paragraph_format.space_after = Pt(24)
    r = p_deg2.add_run("IN\nCOMPUTER SCIENCE & ENGINEERING (ARTIFICIAL INTELLIGENCE)")
    r.font.name = "Times New Roman"
    r.font.size = Pt(13)
    r.font.bold = True

    p_by = doc.add_paragraph()
    p_by.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_by.paragraph_format.space_after = Pt(8)
    r = p_by.add_run("Submitted by")
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)
    r.font.italic = True

    t_stud = doc.add_table(rows=len(report_data.STUDENTS), cols=2)
    t_stud.alignment = WD_TABLE_ALIGNMENT.CENTER
    for idx, (name, roll) in enumerate(report_data.STUDENTS):
        row = t_stud.rows[idx]
        p_l = row.cells[0].paragraphs[0]
        p_l.alignment = WD_ALIGN_PARAGRAPH.LEFT
        r_l = p_l.add_run(name)
        r_l.font.name = "Times New Roman"
        r_l.font.size = Pt(11)
        r_l.font.bold = True

        p_r = row.cells[1].paragraphs[0]
        p_r.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        r_r = p_r.add_run(f"({roll})")
        r_r.font.name = "Times New Roman"
        r_r.font.size = Pt(11)

    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_before = Pt(36)

    p_dept = doc.add_paragraph()
    p_dept.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_dept.paragraph_format.space_after = Pt(4)
    r = p_dept.add_run("SCHOOL OF ARTIFICIAL INTELLIGENCE & ADVANCED COMPUTING")
    r.font.name = "Times New Roman"
    r.font.size = Pt(13)
    r.font.bold = True

    p_univ = doc.add_paragraph()
    p_univ.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_univ.paragraph_format.space_after = Pt(4)
    r = p_univ.add_run("PRESIDENCY UNIVERSITY, BENGALURU")
    r.font.name = "Times New Roman"
    r.font.size = Pt(14)
    r.font.bold = True
    r.font.color.rgb = RGBColor(16, 44, 87)

    p_date = doc.add_paragraph()
    p_date.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_date.paragraph_format.space_after = Pt(0)
    r = p_date.add_run("NOVEMBER 2026")
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)
    r.font.bold = True

    doc.add_page_break()

    # -------------------------------------------------------------
    # 2. BONAFIDE CERTIFICATE
    # -------------------------------------------------------------
    add_frontmatter_heading(doc, "BONAFIDE CERTIFICATE")
    add_body_p(doc, report_data.CERTIFICATE_TEXT)

    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_before = Pt(40)

    t_sig = doc.add_table(rows=1, cols=2)
    t_sig.alignment = WD_TABLE_ALIGNMENT.CENTER
    c1 = t_sig.rows[0].cells[0].paragraphs[0]
    c1.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r = c1.add_run("PROJECT SUPERVISOR\nDepartment of CSE (AI)\nPresidency University")
    r.font.name = "Times New Roman"
    r.font.size = Pt(11)
    r.font.bold = True

    c2 = t_sig.rows[0].cells[1].paragraphs[0]
    c2.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r = c2.add_run("HEAD OF DEPARTMENT\nSchool of AI & Advanced Computing\nPresidency University")
    r.font.name = "Times New Roman"
    r.font.size = Pt(11)
    r.font.bold = True

    doc.add_page_break()

    # -------------------------------------------------------------
    # 3. DECLARATION
    # -------------------------------------------------------------
    add_frontmatter_heading(doc, "DECLARATION")
    add_body_p(doc, report_data.DECLARATION_TEXT)

    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_before = Pt(36)

    p_dec_date = doc.add_paragraph()
    p_dec_date.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r = p_dec_date.add_run("Place: Bengaluru\nDate: 18th November 2026")
    r.font.name = "Times New Roman"
    r.font.size = Pt(11)

    t_dec_sig = doc.add_table(rows=4, cols=2)
    t_dec_sig.alignment = WD_TABLE_ALIGNMENT.CENTER
    for idx, (name, roll) in enumerate(report_data.STUDENTS):
        row = t_dec_sig.rows[idx]
        p_l = row.cells[0].paragraphs[0]
        p_l.alignment = WD_ALIGN_PARAGRAPH.LEFT
        r = p_l.add_run(name)
        r.font.name = "Times New Roman"
        r.font.size = Pt(11)

        p_r = row.cells[1].paragraphs[0]
        p_r.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        r = p_r.add_run("Signature: ____________________")
        r.font.name = "Times New Roman"
        r.font.size = Pt(11)

    doc.add_page_break()

    # -------------------------------------------------------------
    # 4. ACKNOWLEDGEMENT
    # -------------------------------------------------------------
    add_frontmatter_heading(doc, "ACKNOWLEDGEMENT")
    for para in report_data.ACKNOWLEDGEMENT_TEXT:
        add_body_p(doc, para)

    doc.add_page_break()

    # -------------------------------------------------------------
    # 5. ABSTRACT
    # -------------------------------------------------------------
    add_frontmatter_heading(doc, "ABSTRACT")
    for para in report_data.ABSTRACT_TEXT:
        add_body_p(doc, para)

    p_kw = doc.add_paragraph()
    p_kw.paragraph_format.space_before = Pt(12)
    p_kw.paragraph_format.line_spacing = 1.5
    r_kwh = p_kw.add_run("Keywords: ")
    r_kwh.font.name = "Times New Roman"
    r_kwh.font.size = Pt(11)
    r_kwh.font.bold = True
    r_kwt = p_kw.add_run(report_data.KEYWORDS_TEXT)
    r_kwt.font.name = "Times New Roman"
    r_kwt.font.size = Pt(11)
    r_kwt.font.italic = True

    doc.add_page_break()

    # -------------------------------------------------------------
    # 6. TABLE OF CONTENTS
    # -------------------------------------------------------------
    add_frontmatter_heading(doc, "TABLE OF CONTENTS")

    toc_entries = [
        ("CHAPTER 1  INTRODUCTION", "1", True),
        ("    1.1 Background", "1", False),
        ("    1.2 Statistics & Empirical Evidence", "2", False),
        ("    1.3 Prior Existing Technologies & Limitations", "3", False),
        ("    1.4 Proposed Approach & Architecture", "4", False),
        ("    1.5 Project Objectives", "5", False),
        ("    1.6 Alignment with UN Sustainable Development Goals (SDGs)", "6", False),
        ("    1.7 Overview of Project Report", "7", False),
        ("CHAPTER 2  LITERATURE REVIEW", "8", True),
        ("    2.1 Theoretical Framework and Misinformation Taxonomy", "8", False),
        ("    2.2 Survey of Foundational Studies", "9", False),
        ("    2.3 Stance Detection and Natural Language Inference in Verification", "11", False),
        ("    2.4 Critical Gaps in Prior Research", "12", False),
        ("    2.5 TruthLens Architectural Positioning", "13", False),
        ("CHAPTER 3  METHODOLOGY", "14", True),
        ("    3.1 Five-Pillar Mathematical Framework", "14", False),
        ("    3.2 Canonical Domain Extraction and Knowledge Base Indexing", "15", False),
        ("    3.3 Lexical Manipulation Metric (M_index)", "16", False),
        ("    3.4 Automated Factual Claim Extraction", "17", False),
        ("    3.5 Live News Corroboration Engine", "18", False),
        ("    3.6 Directional Stance Classification via RoBERTa-MNLI", "19", False),
        ("    3.7 Unified Credibility Score Aggregation (C_final)", "20", False),
        ("    3.8 Production REST API Specification", "21", False),
        ("CHAPTER 4  PROJECT MANAGEMENT", "22", True),
        ("    4.1 Development Methodology & Sprint Lifecycle", "22", False),
        ("    4.2 Five-Phase Roadmap Execution (100% Completed)", "23", False),
        ("    4.3 12-Week Gantt Timeline", "24", False),
        ("    4.4 Resource Allocation and RACI Matrix", "25", False),
        ("    4.5 Risk Assessment and Mitigation Protocols", "26", False),
        ("    4.6 Continuous Integration & Quality Assurance Standards", "27", False),
        ("CHAPTER 5  ANALYSIS AND DESIGN", "28", True),
        ("    5.1 System Requirements Specification (SRS)", "28", False),
        ("    5.2 Hardware and Cloud Environment Specifications", "29", False),
        ("    5.3 Architectural Data Flow Models (DFD Level 0 & Level 1)", "30", False),
        ("    5.4 Relational Database Design & B-Tree Indexing", "31", False),
        ("    5.5 Detailed Use Case Specifications", "33", False),
        ("CHAPTER 6  IMPLEMENTATION AND DEVELOPMENT", "34", True),
        ("    6.1 System Architecture & Module Inventory", "34", False),
        ("    6.2 SQLite B-Tree Knowledge Base Implementation", "35", False),
        ("    6.3 Lexical Manipulation Detection Engine", "35", False),
        ("    6.4 spaCy Factual Claim Extraction Module", "36", False),
        ("    6.5 Live News Corroboration Engine", "36", False),
        ("    6.6 RoBERTa-MNLI Directional Stance Classifier", "37", False),
        ("    6.7 Unified Mathematical Score Aggregator", "37", False),
        ("    6.8 FastAPI Production REST Microservice", "38", False),
        ("    6.9 GCP Cloud Infrastructure, Docker & Live Web Deployment", "38", False),
        ("    6.10 Interactive Web Dashboard & Sequence Flow", "40", False),
        ("CHAPTER 7  EVALUATION AND RESULTS", "42", True),
        ("    7.1 Quantitative Latency Benchmarks", "42", False),
        ("    7.2 Automated Pytest Suite Validation (38/38 Passing)", "44", False),
        ("    7.3 Real-World Journalistic Case Studies", "45", False),
        ("    7.4 Comparative Architectural Matrix", "46", False),
        ("    7.5 Error Analysis & Edge Case Robustness", "47", False),
        ("    7.6 100% Roadmap Milestone Verification Matrix", "48", False),
        ("CHAPTER 8  SOCIAL, LEGAL, ETHICAL, SUSTAINABILITY AND SAFETY ASPECTS", "49", True),
        ("    8.1 Ideological Decoupling and Free Speech Protection", "49", False),
        ("    8.2 Data Privacy and Regulatory Compliance", "50", False),
        ("    8.3 Green AI and Environmental Sustainability", "51", False),
        ("    8.4 Dual-Use Risk Analysis & System Safety Protocols", "51", False),
        ("CHAPTER 9  CONCLUSION", "52", True),
        ("    9.1 Summary of 100% System Accomplishments", "52", False),
        ("    9.2 Key Epistemic Contributions", "53", False),
        ("    9.3 Limitations of Current System", "53", False),
        ("    9.4 Future Work & Long-Term Roadmap", "54", False),
        ("    9.5 Concluding Remarks", "54", False),
        ("REFERENCES (IEEE FORMAT)", "55", True),
        ("APPENDIX", "57", True),
        ("    Appendix A: Production REST API Endpoint Schemas & FastAPI Specifications", "57", False),
        ("    Appendix B: Complete Pytest Automated Test Suite Execution Log (38/38 Passing)", "58", False),
        ("    Appendix C: GCP Cloud VM & Docker Deployment Configurations (systemd & Nginx)", "59", False)
    ]

    for title, pg, is_bold in toc_entries:
        p_row = doc.add_paragraph()
        p_row.paragraph_format.line_spacing = 1.15
        p_row.paragraph_format.space_after = Pt(2.5)
        r_t = p_row.add_run(title)
        r_t.font.name = "Times New Roman"
        r_t.font.size = Pt(10.5)
        r_t.font.bold = is_bold

        dots_count = max(4, 76 - len(title))
        r_d = p_row.add_run(" " + "." * dots_count + " ")
        r_d.font.name = "Times New Roman"
        r_d.font.size = Pt(10)
        r_d.font.color.rgb = RGBColor(160, 160, 160)

        r_p = p_row.add_run(pg)
        r_p.font.name = "Times New Roman"
        r_p.font.size = Pt(10.5)
        r_p.font.bold = is_bold

    doc.add_page_break()

    # -------------------------------------------------------------
    # 7. LIST OF FIGURES
    # -------------------------------------------------------------
    add_frontmatter_heading(doc, "LIST OF FIGURES")

    figures_list = [
        ("Figure 2.1: Taxonomy of Digital Media Information Disorders, Verification Signals, and TruthLens Architectural Countermeasures", "9"),
        ("Figure 3.1: TruthLens High-Level Five-Pillar Verification Architecture and Data Processing Pipeline", "15"),
        ("Figure 3.2: Mathematical Flow Diagram of Unified Credibility Score Aggregation (C_final) with Boundary Overrides", "20"),
        ("Figure 4.1: TruthLens 12-Week Development Gantt Chart Illustrating All Five Phases Completed (100% Target Met)", "24"),
        ("Figure 5.2: TruthLens Data Flow Diagrams: DFD Level 0 (Context Level) and DFD Level 1 (Functional Decomposition)", "30"),
        ("Figure 5.1: Statistical Distributions of Media Bias / Fact Check (MBFC) Factual Reporting Ratings and Ideological Coordinates", "31"),
        ("Figure 5.3: Relational Entity-Relationship (ER) Schema and Clustered B-Tree Indexing Architecture for Source Reputation Knowledge Base", "32"),
        ("Figure 6.3: Live News Corroboration Pool Architecture Illustrating Multi-Publisher Evidence Retrieval and Authority Weighting", "37"),
        ("Figure 6.5: Cloud Production Architecture: GCP Compute Engine VM, Docker, Nginx Reverse Proxy, and Firebase Hosting (https://localsort.in)", "39"),
        ("Figure 6.2: Interactive Streamlit Web Dashboard: Executive Credibility Dial, Stance Badges, and Corroboration Breakdown", "40"),
        ("Figure 6.4: UML Sequence Diagram Illustrating End-to-End Execution Flow Across TruthLens Verification Modules", "41"),
        ("Figure 7.1: Quantitative Latency Micro-Benchmarks (Log Scale) and Automated Pytest Validation Suite (38/38 Passed - 100%)", "43"),
        ("Figure 7.2: Comparative Verification Performance Across Four Real-World Journalistic Case Studies", "46")
    ]

    for f_title, f_pg in figures_list:
        p_fig = doc.add_paragraph()
        p_fig.paragraph_format.line_spacing = 1.15
        p_fig.paragraph_format.space_after = Pt(3)
        r1 = p_fig.add_run(f_title)
        r1.font.name = "Times New Roman"
        r1.font.size = Pt(10.5)
        dots = " " + "." * max(4, 78 - len(f_title)) + " "
        r2 = p_fig.add_run(dots)
        r2.font.name = "Times New Roman"
        r2.font.color.rgb = RGBColor(160, 160, 160)
        r3 = p_fig.add_run(f_pg)
        r3.font.name = "Times New Roman"
        r3.font.size = Pt(10.5)
        r3.font.bold = True

    doc.add_page_break()

    # -------------------------------------------------------------
    # 8. LIST OF TABLES
    # -------------------------------------------------------------
    add_frontmatter_heading(doc, "LIST OF TABLES")

    tables_list = [
        ("Table 1.1: Mapping of Project Engineering Objectives to UN Sustainable Development Goals (SDGs)", "6"),
        ("Table 2.1: Critical Appraisal of Foundational Research Studies in Automated News Verification and Stance Detection", "10"),
        ("Table 4.1: RACI Project Responsibility Assignment Matrix for TruthLens Engineering Team", "25"),
        ("Table 4.2: Risk Assessment and Engineering Mitigation Protocols Executed in TruthLens", "26"),
        ("Table 5.1: TruthLens System Requirements Specification (SRS) Functional and Non-Functional Matrix", "28"),
        ("Table 5.2: Hardware, Operating System, and Production Cloud Environment Specifications", "29"),
        ("Table 5.3: Physical Data Dictionary and Relational Schema for mbfc_sources Knowledge Base", "32"),
        ("Table 6.1: TruthLens Production Software Module Inventory and Codebase Metrics", "34"),
        ("Table 7.1: Empirical Latency Benchmarks Across TruthLens Core Modules (1,000 Automated Iterations)", "43"),
        ("Table 7.2: Complete Automated Pytest Verification Suite Breakdown Across 7 Software Modules (100% Pass Rate)", "44"),
        ("Table 7.3: Experimental Results Across Four Real-World Case Studies Validating Multi-Signal Discrimination", "45"),
        ("Table 7.4: Comparative Architectural Matrix: TruthLens vs. Monolithic LLMs vs. Traditional Stylistic Classifiers", "47"),
        ("Table 7.5: TruthLens 100% Roadmap Milestone Deliverables Verification Matrix", "48"),
        ("Table 8.1: Demonstration of Ideological Orthogonality: Decoupling Political Bias from Factual Credibility Score", "50")
    ]

    for t_title, t_pg in tables_list:
        p_tbl = doc.add_paragraph()
        p_tbl.paragraph_format.line_spacing = 1.15
        p_tbl.paragraph_format.space_after = Pt(3)
        r1 = p_tbl.add_run(t_title)
        r1.font.name = "Times New Roman"
        r1.font.size = Pt(10.5)
        dots = " " + "." * max(4, 78 - len(t_title)) + " "
        r2 = p_tbl.add_run(dots)
        r2.font.name = "Times New Roman"
        r2.font.color.rgb = RGBColor(160, 160, 160)
        r3 = p_tbl.add_run(t_pg)
        r3.font.name = "Times New Roman"
        r3.font.size = Pt(10.5)
        r3.font.bold = True

    doc.add_page_break()

    # -------------------------------------------------------------
    # 9. LIST OF ABBREVIATIONS
    # -------------------------------------------------------------
    add_frontmatter_heading(doc, "LIST OF ABBREVIATIONS")

    abbr_table = doc.add_table(rows=len(report_data.ABBREVIATIONS) + 1, cols=2)
    abbr_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    abbr_w = [Inches(1.5), Inches(4.25)]
    format_table_header(abbr_table.rows[0], abbr_w, font_size=11.0)
    abbr_table.rows[0].cells[0].text = "Abbreviation"
    abbr_table.rows[0].cells[1].text = "Full Expanded Terminology"
    for cell in abbr_table.rows[0].cells:
        cell.paragraphs[0].runs[0].font.bold = True

    for idx, (abbr, full_text) in enumerate(report_data.ABBREVIATIONS):
        row = abbr_table.rows[idx + 1]
        is_even = (idx % 2 == 1)
        row.cells[0].text = abbr
        row.cells[1].text = full_text
        format_table_row(row, abbr_w, is_even=is_even, font_size=10.5)
        row.cells[0].paragraphs[0].runs[0].font.bold = True

    doc.add_page_break()

    # -------------------------------------------------------------
    # SECTION 2: MAIN REPORT CHAPTERS (ARABIC PAGE NUMBERING: 1, 2, 3...)
    # -------------------------------------------------------------
    s_body = doc.add_section(WD_SECTION_START.NEW_PAGE)
    s_body.page_width = Cm(21.0)
    s_body.page_height = Cm(29.7)
    s_body.top_margin = Cm(2.54)
    s_body.bottom_margin = Cm(2.54)
    s_body.left_margin = Cm(3.81)
    s_body.right_margin = Cm(2.54)

    # Unlink footer from previous section
    s_body.footer.is_linked_to_previous = False
    footer_body = s_body.footer
    fp = footer_body.paragraphs[0]
    fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    fp_run = fp.add_run()
    fp_run.font.name = "Times New Roman"
    fp_run.font.size = Pt(11)
    fp._p.append(parse_xml(fld_xml))

    # Reset page numbering to decimal 1
    sectPr2 = s_body._sectPr
    pgNumType2 = OxmlElement('w:pgNumType')
    pgNumType2.set(qn('w:fmt'), 'decimal')
    pgNumType2.set(qn('w:start'), '1')
    sectPr2.append(pgNumType2)

    # -------------------------------------------------------------
    # BUILD CHAPTERS 1 TO 9
    # -------------------------------------------------------------
    for ch_idx, ch in enumerate(report_chapters.CHAPTERS):
        print(f"[*] Compiling Chapter {ch['num']}: {ch['title']}...")
        add_chapter_heading(doc, ch["num"], ch["title"])

        # Chapter summary introduction paragraph (as required by template)
        if "intro_summary" in ch:
            add_body_p(doc, ch["intro_summary"])

        for sec in ch["sections"]:
            add_sec_heading(doc, sec["num"], sec["title"])

            # Primary paragraphs
            for p_text in sec.get("paras", []):
                add_body_p(doc, p_text)

            # Embedded Academic Table (if present)
            if "table" in sec:
                t_info = sec["table"]
                font_sz = 10.0 if len(t_info["headers"]) >= 5 else 10.5
                add_academic_table(
                    doc,
                    tbl_num=t_info["num"],
                    tbl_caption=t_info["caption"],
                    headers=t_info["headers"],
                    rows=t_info["rows"],
                    col_widths_inches=t_info["widths"],
                    font_size=font_sz
                )

            # Embedded Academic Figure (if present)
            if "figure" in sec:
                f_info = sec["figure"]
                add_figure_to_doc(
                    doc,
                    img_rel_path=f_info["path"],
                    fig_num_str=f_info["num"],
                    fig_caption_str=f_info["caption"],
                    width_inches=5.65
                )

            # Second embedded figure (if present, e.g., in Ch 5 and Ch 6)
            if "figure2" in sec:
                f2_info = sec["figure2"]
                add_figure_to_doc(
                    doc,
                    img_rel_path=f2_info["path"],
                    fig_num_str=f2_info["num"],
                    fig_caption_str=f2_info["caption"],
                    width_inches=5.65
                )

            # Additional continuation paragraphs
            for key in ["paras_cont", "paras_cont2", "paras_cont3", "paras_cont4", "paras_cont5", "paras_cont6"]:
                for p_text in sec.get(key, []):
                    add_body_p(doc, p_text)

        # Page break after every chapter except the last one
        if ch_idx < len(report_chapters.CHAPTERS) - 1:
            doc.add_page_break()

    # -------------------------------------------------------------
    # REFERENCES (IEEE NUMBERED FORMAT)
    # -------------------------------------------------------------
    doc.add_page_break()
    p_ref_head = doc.add_paragraph()
    p_ref_head.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_ref_head.paragraph_format.space_before = Pt(16)
    p_ref_head.paragraph_format.space_after = Pt(20)
    r_rf = p_ref_head.add_run("REFERENCES")
    r_rf.font.name = "Times New Roman"
    r_rf.font.size = Pt(16)
    r_rf.font.bold = True

    for ref in report_data.REFERENCES_LIST:
        p_ref = doc.add_paragraph()
        p_ref.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p_ref.paragraph_format.line_spacing = 1.5
        p_ref.paragraph_format.space_after = Pt(6)
        r = p_ref.add_run(ref)
        r.font.name = "Times New Roman"
        r.font.size = Pt(12)

    # -------------------------------------------------------------
    # APPENDICES (APPENDIX A, B, C)
    # -------------------------------------------------------------
    doc.add_page_break()
    add_frontmatter_heading(doc, "APPENDIX")

    for app in getattr(report_chapters, "APPENDICES", []):
        p_app_h = doc.add_paragraph()
        p_app_h.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p_app_h.paragraph_format.space_before = Pt(14)
        p_app_h.paragraph_format.space_after = Pt(4)
        p_app_h.paragraph_format.keep_with_next = True
        r_app = p_app_h.add_run(f"Appendix {app['letter']}:  {app['title']}")
        r_app.font.name = "Times New Roman"
        r_app.font.size = Pt(14)
        r_app.font.bold = True

        for p_text in app.get("paras", []):
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            p.paragraph_format.line_spacing = 1.5
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(6)
            r = p.add_run(p_text)
            r.font.name = "Times New Roman"
            r.font.size = Pt(11)

    # -------------------------------------------------------------
    # SAVE WORD DOCUMENTS (.DOCX)
    # -------------------------------------------------------------
    print("[*] Saving generated Word documents...")
    saved_paths = []
    try:
        doc.save(DOC_PATH)
        saved_paths.append(DOC_PATH)
    except PermissionError:
        alt_path = r"C:\Users\shubh\Desktop\TruthLens_Mini_Project_Report_CSS7102_Updated.docx"
        doc.save(alt_path)
        saved_paths.append(alt_path)
        print(f"[!] Warning: Target '{DOC_PATH}' was locked. Saved to '{alt_path}' instead.")

    doc.save(DOCS_COPY)
    saved_paths.append(DOCS_COPY)
    print("[+] Successfully generated Word (.docx) files:")
    for p in saved_paths:
        print(f"    - {p}")

    # -------------------------------------------------------------
    # CONVERT TO PDF VIA WORD COM
    # -------------------------------------------------------------
    convert_to_pdf(DOC_PATH, PDF_PATH, DOCS_PDF_COPY)


def convert_to_pdf(docx_path, pdf_path, pdf_docs_copy):
    """Converts the formatted Word report to publication-grade PDF via Word COM."""
    print("[*] Initiating PDF export via Microsoft Word COM automation...")
    
    # Pre-emptively kill lingering WINWORD instances to prevent COM locks
    subprocess.run("taskkill /F /IM WINWORD.EXE /T", shell=True, capture_output=True)

    try:
        import comtypes.client
        word = comtypes.client.CreateObject('Word.Application')
        word.Visible = False

        doc = word.Documents.Open(os.path.abspath(docx_path))
        # Update table of contents and fields
        try:
            doc.Fields.Update()
        except Exception:
            pass

        # 17 corresponds to wdFormatPDF
        doc.SaveAs(os.path.abspath(pdf_path), FileFormat=17)
        doc.Close()
        word.Quit()

        # Copy to repository docs folder
        shutil.copyfile(pdf_path, pdf_docs_copy)
        print(f"[+] Successfully exported PDF report to:")
        print(f"    - {pdf_path}")
        print(f"    - {pdf_docs_copy}")
    except Exception as e:
        print(f"[!] PDF conversion warning: {e}")
        print("[!] The Word .docx file is saved and intact.")


if __name__ == "__main__":
    build_report()
