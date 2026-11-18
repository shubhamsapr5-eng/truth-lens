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
- Table text: 11 pt Times New Roman (or 10 pt for dense 6-column tables)
- References: 12 pt Times New Roman, 1.5 spacing, IEEE format
- Page numbering: Lower Roman numerals (i, ii, iii...) for front matter; Arabic numerals (1, 2, 3...) beginning with Chapter 1
Includes 12 embedded 300 DPI figures and 15 academic tables.
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

# Import content data
sys.path.append(str(Path(__file__).resolve().parent))
import report_data
import report_chapters

DOC_PATH = r"C:\Users\shubh\Desktop\TruthLens_Mini_Project_Report_CSS7102.docx"
PDF_PATH = r"C:\Users\shubh\Desktop\TruthLens_Mini_Project_Report_CSS7102.pdf"
DOCS_COPY = r"C:\Users\shubh\Desktop\truth-lens\docs\TruthLens_Mini_Project_Report_CSS7102.docx"
DOCS_PDF_COPY = r"C:\Users\shubh\Desktop\truth-lens\docs\TruthLens_Mini_Project_Report_CSS7102.pdf"
FIGURES_DIR = Path(r"C:\Users\shubh\Desktop\truth-lens\data\figures")


# ---------------------------------------------------------------------------
# CELL FORMATTING HELPERS
# ---------------------------------------------------------------------------

def set_cell_margins(cell, top=120, bottom=120, left=140, right=140):
    """Sets inner cell padding in twips."""
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)


def set_cell_shading(cell, color_hex):
    """Sets cell background fill color."""
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shd)


def format_table_header(row, col_widths, bg_hex="102C57", font_size=11.0):
    """Formats academic table header row with bold white text and navy fill."""
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


def format_table_row(row, col_widths, is_even=False, font_size=11.0):
    """Formats data row with zebra background shading and clean typography."""
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


# ---------------------------------------------------------------------------
# TYPOGRAPHY & HEADING HELPERS (STRICT INSTITUTIONAL FORMAT)
# ---------------------------------------------------------------------------

def add_frontmatter_heading(doc, title):
    """Front-matter major heading: 16 pt, bold, centered, uppercase."""
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
    """Chapter heading: 16 pt, bold, centered, uppercase."""
    p_num = doc.add_paragraph()
    p_num.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_num.paragraph_format.space_before = Pt(18)
    p_num.paragraph_format.space_after = Pt(4)
    r_num = p_num.add_run(f"CHAPTER {num}".upper())
    r_num.font.name = "Times New Roman"
    r_num.font.size = Pt(16)
    r_num.font.bold = True

    p_t = doc.add_paragraph()
    p_t.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_t.paragraph_format.space_after = Pt(20)
    r_t = p_t.add_run(title.upper())
    r_t.font.name = "Times New Roman"
    r_t.font.size = Pt(16)
    r_t.font.bold = True
    return p_t


def add_sec_heading(doc, sec_num, sec_title):
    """Section heading (e.g., 1.1): 14 pt, bold."""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(6)
    r = p.add_run(f"{sec_num}  {sec_title}")
    r.font.name = "Times New Roman"
    r.font.size = Pt(14)
    r.font.bold = True
    return p


def add_subsec_heading(doc, subsec_num, subsec_title):
    """Subsection heading (e.g., 1.1.1): 12 pt, bold."""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(4)
    r = p.add_run(f"{subsec_num}  {subsec_title}")
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)
    r.font.bold = True
    return p


def add_body_p(doc, text):
    """Body text: 12 pt, justified, 1.5 line spacing."""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.line_spacing = 1.5
    p.paragraph_format.space_after = Pt(6)
    r = p.add_run(text)
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)
    return p


def add_bullet_p(doc, text, bold_prefix=""):
    """Bulleted list paragraph with 12 pt Times New Roman and 1.5 line spacing."""
    p = doc.add_paragraph(style='List Bullet')
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.line_spacing = 1.5
    p.paragraph_format.space_after = Pt(4)
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = "Times New Roman"
        r_pre.font.size = Pt(12)
        r_pre.font.bold = True
    r = p.add_run(text)
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)
    return p


def add_figure_to_doc(doc, img_rel_path, fig_num_str, fig_caption_str, width_inches=5.65):
    """
    Figure caption: 12 pt, centered, placed BELOW the figure.
    Width fits within 5.75 inches printable width on A4 with 3.81cm left margin.
    """
    fig_path = FIGURES_DIR / img_rel_path
    if fig_path.exists():
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(12)
        p_img.paragraph_format.space_after = Pt(6)
        run = p_img.add_run()
        run.add_picture(str(fig_path), width=Inches(width_inches))

        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_before = Pt(4)
        p_cap.paragraph_format.space_after = Pt(14)
        r_num = p_cap.add_run(f"Figure {fig_num_str}: ")
        r_num.font.name = "Times New Roman"
        r_num.font.size = Pt(12)
        r_num.font.bold = True

        r_txt = p_cap.add_run(fig_caption_str)
        r_txt.font.name = "Times New Roman"
        r_txt.font.size = Pt(12)


def add_academic_table(doc, tbl_num, tbl_caption, headers, rows, col_widths_inches, font_size=11.0):
    """
    Table caption: 12 pt, centered, placed ABOVE the table.
    Table text: 11 pt Times New Roman (or specified font_size for dense tables).
    """
    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap.paragraph_format.space_before = Pt(14)
    p_cap.paragraph_format.space_after = Pt(6)
    r_num = p_cap.add_run(f"Table {tbl_num}: ")
    r_num.font.name = "Times New Roman"
    r_num.font.size = Pt(12)
    r_num.font.bold = True

    r_txt = p_cap.add_run(tbl_caption)
    r_txt.font.name = "Times New Roman"
    r_txt.font.size = Pt(12)

    col_widths = [Inches(w) for w in col_widths_inches]
    table = doc.add_table(rows=len(rows) + 1, cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER

    # Header Row
    format_table_header(table.rows[0], col_widths, font_size=font_size)
    for i, h in enumerate(headers):
        table.rows[0].cells[i].text = h
        table.rows[0].cells[i].paragraphs[0].runs[0].font.bold = True

    # Data Rows
    for r_idx, row_data in enumerate(rows):
        row = table.rows[r_idx + 1]
        for c_idx, val in enumerate(row_data):
            row.cells[c_idx].text = str(val)
        format_table_row(row, col_widths, is_even=(r_idx % 2 == 1), font_size=font_size)

    p_spacer = doc.add_paragraph()
    p_spacer.paragraph_format.space_before = Pt(4)
    p_spacer.paragraph_format.space_after = Pt(8)
    return table


# ---------------------------------------------------------------------------
# MAIN REPORT BUILDER
# ---------------------------------------------------------------------------

def build_report():
    print("[*] Initializing TruthLens Academic Mini Project Report (CSS7102)...")
    doc = Document()

    # -----------------------------------------------------------------------
    # SECTION 1: FRONT MATTER (ROMAN PAGE NUMBERING: i, ii, iii...)
    # -----------------------------------------------------------------------
    s_front = doc.sections[0]
    s_front.page_width = Cm(21.0)
    s_front.page_height = Cm(29.7)
    s_front.top_margin = Cm(2.54)
    s_front.bottom_margin = Cm(2.54)
    s_front.left_margin = Cm(3.81)    # 1.5 inches for binding margin
    s_front.right_margin = Cm(2.54)   # 1.0 inch
    s_front.different_first_page_header_footer = True

    # Front matter footer: Centered lower Roman page number
    f_p = s_front.footer.paragraphs[0]
    f_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    f_p_run = f_p.add_run()
    f_p_run.font.name = "Times New Roman"
    f_p_run.font.size = Pt(11)
    fld_xml = f'<w:fldSimple {nsdecls("w")} w:instr="PAGE"/>'
    f_p._p.append(parse_xml(fld_xml))

    # XML configuration for lowerRoman page numbers
    sectPr = s_front._sectPr
    pgNumType = OxmlElement('w:pgNumType')
    pgNumType.set(qn('w:fmt'), 'lowerRoman')
    pgNumType.set(qn('w:start'), '1')
    sectPr.append(pgNumType)

    # -------------------------------------------------------------
    # 1. TITLE PAGE (COVER)
    # -------------------------------------------------------------
    p_uni = doc.add_paragraph()
    p_uni.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_uni.paragraph_format.space_before = Pt(12)
    p_uni.paragraph_format.space_after = Pt(2)
    r = p_uni.add_run("PRESIDENCY UNIVERSITY\n")
    r.font.name = "Times New Roman"
    r.font.size = Pt(16)
    r.font.bold = True

    r = p_uni.add_run("Bengaluru, India\n\n")
    r.font.name = "Times New Roman"
    r.font.size = Pt(13)

    r = p_uni.add_run("MINI PROJECT REPORT (CSS7102)\n\n")
    r.font.name = "Times New Roman"
    r.font.size = Pt(14)
    r.font.bold = True

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_after = Pt(16)
    r_t = p_title.add_run("TRUTHLENS: AI-POWERED REAL-TIME NEWS CREDIBILITY\nAND MISINFORMATION VERIFICATION ENGINE\n")
    r_t.font.name = "Times New Roman"
    r_t.font.size = Pt(16)
    r_t.font.bold = True
    r_t.font.color.rgb = RGBColor(16, 44, 87)

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_after = Pt(14)
    r_s = p_sub.add_run("Submitted in partial fulfilment of the requirements for the award of the degree of\n")
    r_s.font.name = "Times New Roman"
    r_s.font.size = Pt(11)
    r_s.font.italic = True

    run_deg = p_sub.add_run("BACHELOR OF TECHNOLOGY\nin\nCOMPUTER SCIENCE & ENGINEERING (ARTIFICIAL INTELLIGENCE)\n\n")
    run_deg.font.name = "Times New Roman"
    run_deg.font.size = Pt(13)
    run_deg.font.bold = True

    run_by = p_sub.add_run("Submitted by\n")
    run_by.font.name = "Times New Roman"
    run_by.font.size = Pt(11)

    p_team = doc.add_paragraph()
    p_team.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_team.paragraph_format.space_after = Pt(18)
    p_team.paragraph_format.line_spacing = 1.3
    for name, roll in report_data.STUDENTS:
        r_name = p_team.add_run(f"{name}  -  {roll}\n")
        r_name.font.name = "Times New Roman"
        r_name.font.size = Pt(11.5)
        r_name.font.bold = True

    p_guide = doc.add_paragraph()
    p_guide.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_guide.paragraph_format.space_after = Pt(22)
    r_g1 = p_guide.add_run("Under the Guidance of\n")
    r_g1.font.name = "Times New Roman"
    r_g1.font.size = Pt(11)
    r_g1.font.italic = True

    r_g2 = p_guide.add_run("FACULTY GUIDE & EVALUATION COMMITTEE\n")
    r_g2.font.name = "Times New Roman"
    r_g2.font.size = Pt(12)
    r_g2.font.bold = True

    r_g3 = p_guide.add_run("Department of Computer Science & Engineering (Artificial Intelligence)\nPresidency University, Bengaluru\n\n")
    r_g3.font.name = "Times New Roman"
    r_g3.font.size = Pt(11)

    p_dept = doc.add_paragraph()
    p_dept.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_d = p_dept.add_run("SCHOOL OF ARTIFICIAL INTELLIGENCE & ADVANCED COMPUTING\nPRESIDENCY UNIVERSITY, BENGALURU - 560064\nOCTOBER 2026")
    r_d.font.name = "Times New Roman"
    r_d.font.size = Pt(11.5)
    r_d.font.bold = True

    doc.add_page_break()

    # -------------------------------------------------------------
    # 2. BONAFIDE CERTIFICATE (PAGE ii)
    # -------------------------------------------------------------
    add_frontmatter_heading(doc, "BONAFIDE CERTIFICATE")

    p_cert_body = doc.add_paragraph()
    p_cert_body.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_cert_body.paragraph_format.line_spacing = 1.5
    p_cert_body.paragraph_format.space_after = Pt(28)
    r_cb = p_cert_body.add_run(report_data.CERTIFICATE_TEXT)
    r_cb.font.name = "Times New Roman"
    r_cb.font.size = Pt(12)

    # Signature Table (fits within 5.75 inches printable width)
    sig_table = doc.add_table(rows=2, cols=3)
    sig_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    sig_widths = [Inches(1.9), Inches(1.95), Inches(1.9)]

    row0 = sig_table.rows[0]
    for idx, (title, name) in enumerate([("Faculty Guide", "Project Supervisor"), ("Course Coordinator", "CSS7102"), ("Head of Department", "School of AI & AC")]):
        row0.cells[idx].width = sig_widths[idx]
        p = row0.cells[idx].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(f"\n\n\n____________________\n{title}\n{name}")
        r.font.name = "Times New Roman"
        r.font.size = Pt(10.5)
        r.font.bold = True

    doc.add_page_break()

    # -------------------------------------------------------------
    # 3. DECLARATION (PAGE iii)
    # -------------------------------------------------------------
    add_frontmatter_heading(doc, "DECLARATION")

    p_dec_body = doc.add_paragraph()
    p_dec_body.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_dec_body.paragraph_format.line_spacing = 1.5
    p_dec_body.paragraph_format.space_after = Pt(24)
    r_db = p_dec_body.add_run(report_data.DECLARATION_TEXT)
    r_db.font.name = "Times New Roman"
    r_db.font.size = Pt(12)

    dec_tbl = doc.add_table(rows=5, cols=3)
    dec_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    dec_w = [Inches(1.4), Inches(2.65), Inches(1.7)]
    format_table_header(dec_tbl.rows[0], dec_w, font_size=11.0)
    dec_tbl.rows[0].cells[0].text = "Roll Number"
    dec_tbl.rows[0].cells[1].text = "Student Name"
    dec_tbl.rows[0].cells[2].text = "Signature"
    for cell in dec_tbl.rows[0].cells:
        cell.paragraphs[0].runs[0].font.bold = True

    for idx, (sname, sroll) in enumerate(report_data.STUDENTS):
        row = dec_tbl.rows[idx + 1]
        row.cells[0].text = sroll
        row.cells[1].text = sname
        row.cells[2].text = "_______________"
        format_table_row(row, dec_w, is_even=(idx % 2 == 1), font_size=11.0)

    doc.add_page_break()

    # -------------------------------------------------------------
    # 4. ACKNOWLEDGEMENT (PAGE iv)
    # -------------------------------------------------------------
    add_frontmatter_heading(doc, "ACKNOWLEDGEMENT")
    for para_text in report_data.ACKNOWLEDGEMENT_TEXT:
        add_body_p(doc, para_text)

    doc.add_page_break()

    # -------------------------------------------------------------
    # 5. ABSTRACT (PAGE v)
    # -------------------------------------------------------------
    add_frontmatter_heading(doc, "ABSTRACT")
    for para_text in report_data.ABSTRACT_TEXT:
        add_body_p(doc, para_text)

    p_kw = doc.add_paragraph()
    p_kw.paragraph_format.space_before = Pt(10)
    p_kw.paragraph_format.line_spacing = 1.5
    r_kw = p_kw.add_run("Keywords: ")
    r_kw.font.name = "Times New Roman"
    r_kw.font.size = Pt(11)
    r_kw.font.bold = True
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
        ("    1.1 Problem Context, Misinformation Epidemic & Information Cascades", "1", False),
        ("    1.2 Limitations of Conventional Text-Only & Blacklist Approaches", "2", False),
        ("    1.3 Theoretical Framework and Research Hypotheses", "2", False),
        ("    1.4 SMART Engineering Objectives", "3", False),
        ("    1.5 Scope and Delimitations of the 50% Milestone", "4", False),
        ("    1.6 Alignment with UN Sustainable Development Goals (SDGs)", "5", False),
        ("    1.7 Organisation of the Report", "6", False),
        ("CHAPTER 2  LITERATURE REVIEW", "7", True),
        ("    2.1 Empirical Diffusion & Cascading Dynamics of Online Falsehoods", "7", False),
        ("    2.2 Content-Only Classifiers & Topic Overfitting Vulnerabilities", "7", False),
        ("    2.3 Source-Level Journalistic Profiling & Media Bias / Fact Check", "8", False),
        ("    2.4 Multi-Document Corroboration & Natural Language Inference (FEVER)", "8", False),
        ("    2.5 Cross-Source Stance Detection Paradigms", "9", False),
        ("    2.6 Deep Transformer Architectures for Fact Verification (RoBERTa)", "9", False),
        ("    2.7 Literature Survey Comparison Matrix (12 IEEE/Scopus Studies)", "10", False),
        ("    2.8 Taxonomy and Evolution of Fact-Checking Paradigms", "12", False),
        ("    2.9 Summary of Research Gaps & TruthLens Value Proposition", "12", False),
        ("CHAPTER 3  METHODOLOGY", "14", True),
        ("    3.1 Proposed 3-Pillar Verification Architecture", "14", False),
        ("    3.2 MBFC Knowledge Base & Mathematical Weight Mapping", "15", False),
        ("    3.3 Multi-Tier Canonical Domain Resolution Algorithm", "16", False),
        ("    3.4 109-Trigger Linguistic Manipulation Risk Metric (M_index)", "16", False),
        ("    3.5 Multi-Source Evidence Retrieval Pipeline", "17", False),
        ("    3.6 Mathematical Credibility Scoring Formulation & Fusion Mechanics", "18", False),
        ("CHAPTER 4  PROJECT MANAGEMENT", "20", True),
        ("    4.1 5-Phase Project Schedule & Review Milestone Mapping", "20", False),
        ("    4.2 12-Week Development Gantt Chart", "20", False),
        ("    4.3 Team Roles & Work Breakdown Structure (WBS)", "21", False),
        ("    4.4 Risk Management, Technical Contingencies & Mitigation Protocols", "22", False),
        ("CHAPTER 5  ANALYSIS AND SYSTEM DESIGN", "24", True),
        ("    5.1 Comprehensive Functional & Non-Functional Requirements", "24", False),
        ("    5.2 Hardware, Software & Development Environment Specifications", "25", False),
        ("    5.3 Data Flow Modeling: Level 0 Context & Level 1 DFD", "26", False),
        ("    5.4 Database Architecture & Entity-Relationship (ER) Schema", "26", False),
        ("    5.5 Knowledge Base Distributions & Statistical Characterization", "28", False),
        ("    5.6 Detailed Use Case Modeling", "29", False),
        ("CHAPTER 6  IMPLEMENTATION (50% MILESTONE DELIVERABLES)", "30", True),
        ("    6.1 Modular Directory & Repository Architecture", "30", False),
        ("    6.2 Module 1: Sub-Millisecond SQLite Source Reputation Engine", "31", False),
        ("    6.3 Module 2: 109-Trigger Linguistic Manipulation Scanner", "31", False),
        ("    6.4 Module 3: NewsAPI Live Multi-Source Retrieval Engine", "32", False),
        ("    6.5 Module 4: Interactive Full-Stack Streamlit Web Portal", "32", False),
        ("    6.6 Component Runtime Interaction & UML Sequence Flow", "33", False),
        ("    6.7 Phase 4 / 65% Milestone Progress: Stance NLI Engine & Claim Extractor", "34", False),
        ("CHAPTER 7  RESULTS AND DISCUSSION", "35", True),
        ("    7.1 Empirical Sub-Millisecond Execution Latency Benchmarks", "35", False),
        ("    7.2 Automated Quality Assurance & Pytest Suite Validation", "36", False),
        ("    7.3 Real-World Case Study Verification Profiles Across 4 Scenarios", "37", False),
        ("    7.4 Comparative Matrix: 50% Completed vs. Remaining 50% Deliverables", "38", False),
        ("    7.5 Technical Discussion of 50% Milestone Observations & Challenges", "39", False),
        ("CHAPTER 8  ETHICAL, LEGAL AND SUSTAINABILITY ASPECTS", "40", True),
        ("    8.1 Algorithmic Fairness, Political Neutrality & Bias Decoupling", "40", False),
        ("    8.2 Data Privacy & Compliance with India's DPDP Act 2023", "41", False),
        ("    8.3 Green Computing, Energy Efficiency & Edge Hardware Viability", "41", False),
        ("CHAPTER 9  CONCLUSION AND FUTURE WORK", "42", True),
        ("    9.1 Conclusion on 50% Milestone Accomplishments", "42", False),
        ("    9.2 Upcoming Phase 4: RoBERTa-MNLI Transformer Integration", "42", False),
        ("    9.3 Upcoming Phase 5: Score Aggregator & Production REST API", "42", False),
        ("REFERENCES (IEEE FORMAT)", "44", True)
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
        ("Figure 2.1: Taxonomy and Evolution of Automated Misinformation Verification Approaches", "12"),
        ("Figure 3.1: Architecture of the proposed TruthLens credibility verification system", "14"),
        ("Figure 3.2: Mathematical Scoring Pipeline and Multi-Factor Decision Flowchart", "18"),
        ("Figure 4.1: TruthLens 5-Phase Project Timeline and Review Milestone Gantt Chart", "21"),
        ("Figure 5.2: Level 0 (Context Diagram) and Level 1 Detailed Data Flow Diagram (DFD)", "26"),
        ("Figure 5.3: Entity-Relationship (ER) and SQLite Database Schema Architecture", "28"),
        ("Figure 5.1: Distribution of 4,442 media outlets across factuality/bias tiers", "29"),
        ("Figure 6.1: Live NewsAPI evidence corroboration pool with attached source reputation metrics", "32"),
        ("Figure 6.2: Streamlit interactive web dashboard mockup with evaluator login and verification tabs", "33"),
        ("Figure 6.3: System Component Runtime Interaction and Execution Sequence Diagram", "34"),
        ("Figure 7.1: Pipeline latency performance benchmarks and automated pytest suite passing metrics", "36"),
        ("Figure 7.2: Empirical case study validation profiles across 4 distinct media scenarios", "37")
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
        ("Table 1.1: SMART Project Objectives, Quantitative Metrics, and Milestone Verification Criteria", "4"),
        ("Table 2.1: Comprehensive Literature Survey Matrix of 12 Foundational IEEE/Scopus Research Studies", "10"),
        ("Table 3.1: Media Bias / Fact Check (MBFC) Factual Reporting & Bias Tier Weights", "15"),
        ("Table 3.2: 109-Trigger Linguistic Manipulation Lexicon Breakdown by Category", "16"),
        ("Table 4.1: RACI Responsibility Assignment Matrix Across Team Members and Modules", "21"),
        ("Table 4.2: Technical Risk Assessment, Probability/Severity Rating, and Mitigation Protocols", "22"),
        ("Table 5.1: Comprehensive IEEE 830 Functional & Non-Functional System Requirements Matrix", "24"),
        ("Table 5.2: Functional Hardware and Software Specification Environment", "25"),
        ("Table 5.3: SQLite Relational Database Table Specification (sources table)", "26"),
        ("Table 6.1: TruthLens Component Modular Architecture, Source Files, LOC & Test Coverage", "30"),
        ("Table 7.1: Empirical Query Execution Latency Benchmarks across Pipeline Modules", "35"),
        ("Table 7.2: Comprehensive 27-Test Automated Pytest Quality Assurance Verification Matrix", "36"),
        ("Table 7.3: Real-World Case Study Verification Profiles and Decision Matrix", "37"),
        ("Table 7.4: Comparative Matrix: 50% Completed Deliverables vs. Remaining 50% Deliverables", "38"),
        ("Table 8.1: Ethical Decoupling and DPDP Act 2023 Compliance Governance Checklist", "40")
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
        row.cells[0].text = abbr
        row.cells[1].text = full_text
        format_table_row(row, abbr_w, is_even=(idx % 2 == 1), font_size=11.0)

    doc.add_page_break()

    # -----------------------------------------------------------------------
    # SECTION 2: MAIN REPORT CHAPTERS (ARABIC PAGE NUMBERING: 1, 2, 3...)
    # -----------------------------------------------------------------------
    s_body = doc.add_section(WD_SECTION_START.NEW_PAGE)
    s_body.page_width = Cm(21.0)
    s_body.page_height = Cm(29.7)
    s_body.top_margin = Cm(2.54)
    s_body.bottom_margin = Cm(2.54)
    s_body.left_margin = Cm(3.81)    # 1.5 inch binding margin
    s_body.right_margin = Cm(2.54)   # 1.0 inch
    s_body.different_first_page_header_footer = False

    s_body.header.is_linked_to_previous = False
    s_body.footer.is_linked_to_previous = False

    # Header for body: Right aligned italic Times New Roman 9pt
    hp = s_body.header.paragraphs[0]
    hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    hrun = hp.add_run("TruthLens: AI-Powered Real-Time News Credibility Verification Engine")
    hrun.font.name = "Times New Roman"
    hrun.font.size = Pt(9)
    hrun.font.italic = True
    hrun.font.color.rgb = RGBColor(110, 110, 110)

    # Footer for body: Center aligned decimal Arabic page number
    fp = s_body.footer.paragraphs[0]
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

        for sec in ch["sections"]:
            add_sec_heading(doc, sec["num"], sec["title"])

            # Primary paragraphs
            for p_text in sec.get("paras", []):
                add_body_p(doc, p_text)

            # Embedded Academic Table (if present)
            if "table" in sec:
                t_info = sec["table"]
                font_sz = 10.0 if len(t_info["headers"]) >= 6 else 11.0
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
