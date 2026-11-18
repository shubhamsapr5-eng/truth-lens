"""
build_final_viva_report.py - Presidency University Official Final Viva Report Builder
Takes the official front-matter template document (with official Presidency University logos,
signatories, bonafide certificate, examiners table, and declaration) and properly merges it
with the complete 100% Final Review report (Chapters 1 to 9, References, and Appendices A, B, C).

Outputs:
- C:\\Users\\shubh\\Desktop\\final viva report.docx
- C:\\Users\\shubh\\Desktop\\final viva report.pdf
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
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.section import WD_SECTION_START
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

sys.path.append(str(Path(__file__).resolve().parent))
import report_data
import report_chapters

TEMPLATE_PATH = r"C:\Users\shubh\.gemini\antigravity\brain\eceef7e2-f5f0-4733-b30b-396e85084d3e\.user_uploaded\media_1794982388845_7fc6daca.docx"
OUT_DOCX = r"C:\Users\shubh\Desktop\final viva report.docx"
OUT_PDF = r"C:\Users\shubh\Desktop\final viva report.pdf"
DOCS_DOCX = r"C:\Users\shubh\Desktop\truth-lens\docs\final viva report.docx"
DOCS_PDF = r"C:\Users\shubh\Desktop\truth-lens\docs\final viva report.pdf"
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


def generate_final_viva_report():
    print(f"[*] Loading official front-matter template from: {TEMPLATE_PATH}...")
    doc = Document(TEMPLATE_PATH)

    # 1. Update Title Page
    for p in doc.paragraphs[:10]:
        if "PROJECT TITLE" in p.text:
            p.text = "TRUTHLENS: AI-POWERED REAL-TIME NEWS CREDIBILITY AND MISINFORMATION VERIFICATION ENGINE"
            for r in p.runs:
                r.font.name = "Times New Roman"
                r.font.size = Pt(16)
                r.font.bold = True
                r.font.color.rgb = RGBColor(16, 44, 87)

    # 2. Update Bonafide Certificate
    for p in doc.paragraphs[25:40]:
        if "Certified that this report" in p.text:
            p.text = (
                'Certified that this report "TRUTHLENS: AI-POWERED REAL-TIME NEWS CREDIBILITY AND MISINFORMATION '
                'VERIFICATION ENGINE" is a bonafide work of "Shubham Pandey (20231CAI0046), Karanam Radha Pranathi (20231CAI0003), '
                'Ikram Inayathulla Khan (20231CAI0006), Bhagyesh (20231CAI0068)", who have successfully carried out the project work '
                'and submitted the report for partial fulfilment of the requirements for the award of the degree of BACHELOR OF '
                'TECHNOLOGY in COMPUTER SCIENCE AND ENGINEERING (Artificial Intelligence and Machine Learning) during 2026-27.'
            )
            for r in p.runs:
                r.font.name = "Times New Roman"
                r.font.size = Pt(12)

    # 3. Update Examiners Table (Table 2 in template)
    t_exam = doc.tables[2]
    if len(t_exam.rows) >= 3:
        t_exam.rows[1].cells[0].paragraphs[0].text = "1."
        t_exam.rows[2].cells[0].paragraphs[0].text = "2."
        for row in t_exam.rows[1:]:
            for cell in row.cells:
                for p in cell.paragraphs:
                    for r in p.runs:
                        r.font.name = "Times New Roman"
                        r.font.size = Pt(11)

    # 4. Update Declaration Page
    for p in doc.paragraphs[45:55]:
        if "We the students of final year B.Tech" in p.text:
            p.text = (
                "We the students of final year B.Tech in COMPUTER SCIENCE AND ENGINEERING (Artificial Intelligence and "
                "Machine Learning) at Presidency University, Bengaluru, named Shubham Pandey, Karanam Radha Pranathi, "
                "Ikram Inayathulla Khan, Bhagyesh, hereby declare that the project work titled \"TRUTHLENS: AI-POWERED "
                "REAL-TIME NEWS CREDIBILITY AND MISINFORMATION VERIFICATION ENGINE\" has been independently carried out "
                "by us and submitted in partial fulfillment for the award of the degree of B.Tech in COMPUTER SCIENCE AND "
                "ENGINEERING (Artificial Intelligence and Machine Learning) during the academic year of 2026-27. Further, "
                "the matter embodied in the project has not been submitted previously by anybody for the award of any "
                "Degree or Diploma to any other institution."
            )
            for r in p.runs:
                r.font.name = "Times New Roman"
                r.font.size = Pt(12)

    # Update Student Signatures Table (Table 3 in template)
    t_stud = doc.tables[3]
    # Ensure all 4 rows exist
    while len(t_stud.rows) < 4:
        t_stud.add_row()

    students_sig = [
        ("Shubham Pandey", "20231CAI0046", "Signature: ____________________"),
        ("Karanam Radha Pranathi", "20231CAI0003", "Signature: ____________________"),
        ("Ikram Inayathulla Khan", "20231CAI0006", "Signature: ____________________"),
        ("Bhagyesh", "20231CAI0068", "Signature: ____________________")
    ]
    for idx, (name, roll, sig) in enumerate(students_sig):
        row = t_stud.rows[idx]
        row.cells[0].paragraphs[0].text = name
        row.cells[1].paragraphs[0].text = roll
        row.cells[2].paragraphs[0].text = sig
        for c in row.cells:
            for p in c.paragraphs:
                for r in p.runs:
                    r.font.name = "Times New Roman"
                    r.font.size = Pt(11)

    # Clean loose text after declaration table
    for p in doc.paragraphs[50:57]:
        if "Bhagyesh" in p.text and "20231CAI0068" in p.text:
            p.text = ""
        if "PLACE: BENGALURU" in p.text:
            p.text = "PLACE: BENGALURU\nDATE: 18th November 2026"
            for r in p.runs:
                r.font.name = "Times New Roman"
                r.font.size = Pt(11)

    # 5. Update Abstract
    for p in doc.paragraphs[70:75]:
        if "[Maximum about one page" in p.text:
            p.text = report_data.ABSTRACT_TEXT[0] + "\n\n" + report_data.ABSTRACT_TEXT[1] + "\n\n" + report_data.ABSTRACT_TEXT[2] + "\n\nKeywords: " + report_data.KEYWORDS_TEXT
            for r in p.runs:
                r.font.name = "Times New Roman"
                r.font.size = Pt(11.5)

    # 6. Populate Table of Content (Table 4 in template)
    t_toc = doc.tables[4]
    # Clear existing data rows except header
    # Let's rebuild Table 4 cleanly
    toc_data = [
        ("", "Declaration", "iii"),
        ("", "Acknowledgement", "iv"),
        ("", "Abstract", "v"),
        ("", "List of Figures", "vi"),
        ("", "List of Tables", "vii"),
        ("", "Abbreviations", "viii"),
        ("1.", "Introduction", "1"),
        ("", "1.1  Background", "1"),
        ("", "1.2  Statistics & Empirical Evidence", "2"),
        ("", "1.3  Prior existing technologies & Limitations", "3"),
        ("", "1.4  Proposed approach & Architecture", "4"),
        ("", "1.5  Objectives (Demonstrable Engineering Goals)", "5"),
        ("", "1.6  SDGs (UN Sustainable Development Goals)", "6"),
        ("", "1.7  Overview of project report", "7"),
        ("2.", "Literature Review", "8"),
        ("", "2.1  Theoretical Framework and Misinformation Taxonomy", "8"),
        ("", "2.2  Survey of Foundational Studies (7 Core Papers)", "9"),
        ("", "2.3  Stance Detection and Natural Language Inference", "11"),
        ("", "2.4  Critical Gaps in Prior Research", "12"),
        ("", "2.5  TruthLens Architectural Positioning", "13"),
        ("3.", "Methodology", "14"),
        ("", "3.1  Five-Pillar Mathematical Framework", "14"),
        ("", "3.2  Canonical Domain Extraction & B-Tree Indexing", "15"),
        ("", "3.3  Lexical Manipulation Metric (M_index, 109 Triggers)", "16"),
        ("", "3.4  Automated Factual Claim Extraction (spaCy NER)", "17"),
        ("", "3.5  Live News Corroboration Engine (NewsAPI)", "18"),
        ("", "3.6  Directional Stance Classification via RoBERTa-MNLI", "19"),
        ("", "3.7  Unified Credibility Score Aggregation (C_final)", "20"),
        ("", "3.8  Production REST API Specification", "21"),
        ("4.", "Project Management", "22"),
        ("", "4.1  Development Methodology & Sprint Lifecycle", "22"),
        ("", "4.2  Five-Phase Roadmap Execution (100% Completed)", "23"),
        ("", "4.3  12-Week Gantt Timeline", "24"),
        ("", "4.4  Resource Allocation and RACI Matrix", "25"),
        ("", "4.5  Risk Assessment and Mitigation Protocols", "26"),
        ("", "4.6  Continuous Integration & Quality Assurance", "27"),
        ("5.", "Analysis And Design", "28"),
        ("", "5.1  System Requirements Specification (SRS Matrix)", "28"),
        ("", "5.2  Hardware and Cloud Environment Specifications", "29"),
        ("", "5.3  Architectural Data Flow Models (DFD Level 0 & 1)", "30"),
        ("", "5.4  Relational Database Design & B-Tree Indexing", "31"),
        ("", "5.5  Detailed Use Case Specifications (UC-01 to UC-04)", "33"),
        ("6.", "Implementation And Development", "34"),
        ("", "6.1  System Architecture & Module Inventory", "34"),
        ("", "6.2  SQLite B-Tree Knowledge Base Implementation", "35"),
        ("", "6.3  Lexical Manipulation Detection Engine", "35"),
        ("", "6.4  spaCy Factual Claim Extraction Module", "36"),
        ("", "6.5  Live News Corroboration Engine", "36"),
        ("", "6.6  RoBERTa-MNLI Directional Stance Classifier", "37"),
        ("", "6.7  Unified Mathematical Score Aggregator", "37"),
        ("", "6.8  FastAPI Production REST Microservice", "38"),
        ("", "6.9  GCP Cloud Infrastructure, Docker & localsort.in", "38"),
        ("", "6.10 Interactive Web Dashboard & Sequence Flow", "40"),
        ("7.", "Evaluation And Results", "42"),
        ("", "7.1  Quantitative Latency Benchmarks (1,000 Iterations)", "42"),
        ("", "7.2  Automated Pytest Suite Validation (38/38 Passed)", "44"),
        ("", "7.3  Real-World Journalistic Case Studies", "45"),
        ("", "7.4  Comparative Architectural Matrix (TruthLens vs LLMs)", "46"),
        ("", "7.5  Error Analysis & Edge Case Robustness", "47"),
        ("", "7.6  100% Roadmap Milestone Verification Matrix", "48"),
        ("8.", "Social, Legal, Ethical, Sustainability And Safety Aspects", "49"),
        ("", "8.1  Ideological Decoupling and Free Speech Protection", "49"),
        ("", "8.2  Data Privacy and Regulatory Compliance (DPDP Act)", "50"),
        ("", "8.3  Green AI and Environmental Sustainability", "51"),
        ("", "8.4  Dual-Use Risk Analysis & System Safety Protocols", "51"),
        ("9.", "Conclusion", "52"),
        ("", "9.1  Summary of 100% System Accomplishments", "52"),
        ("", "9.2  Key Epistemic Contributions", "53"),
        ("", "9.3  Limitations of Current System", "53"),
        ("", "9.4  Future Work & Long-Term Roadmap", "54"),
        ("", "9.5  Concluding Remarks", "54"),
        ("", "References (IEEE Format)", "55"),
        ("", "Appendix A: Production REST API Endpoint Schemas", "57"),
        ("", "Appendix B: Complete Pytest 38-Test Execution Log", "58"),
        ("", "Appendix C: GCP Cloud VM & Docker Configurations", "59")
    ]

    while len(t_toc.rows) < len(toc_data) + 1:
        t_toc.add_row()
    while len(t_toc.rows) > len(toc_data) + 1:
        # remove excess row
        tr = t_toc.rows[-1]._tr
        tr.getparent().remove(tr)

    for idx, (sl, tit, pg) in enumerate(toc_data):
        row = t_toc.rows[idx + 1]
        row.cells[0].paragraphs[0].text = sl
        row.cells[1].paragraphs[0].text = tit
        row.cells[2].paragraphs[0].text = pg
        is_ch = (sl != "")
        for c_i, c in enumerate(row.cells):
            p = c.paragraphs[0]
            p.paragraph_format.line_spacing = 1.15
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            if c_i == 0 or c_i == 2:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            for r in p.runs:
                r.font.name = "Times New Roman"
                r.font.size = Pt(10.5)
                r.font.bold = is_ch

    # 7. Populate List of Figures (Table 5 in template)
    t_figs = doc.tables[5]
    figs_data = [
        ("Figure 2.1", "Taxonomy of Digital Media Information Disorders and Countermeasures", "9"),
        ("Figure 3.1", "TruthLens High-Level Five-Pillar Verification Architecture", "15"),
        ("Figure 3.2", "Mathematical Scoring Pipeline and Multi-Factor Decision Flowchart", "20"),
        ("Figure 4.1", "TruthLens 12-Week Development Gantt Chart (100% Target Met)", "24"),
        ("Figure 5.2", "TruthLens Data Flow Diagrams: DFD Level 0 and DFD Level 1", "30"),
        ("Figure 5.1", "Statistical Distributions of MBFC Factual Reporting Ratings and Bias", "31"),
        ("Figure 5.3", "Relational ER Schema and Clustered B-Tree Indexing Architecture", "32"),
        ("Figure 6.3", "Live News Corroboration Pool Architecture and Authority Weighting", "37"),
        ("Figure 6.5", "Cloud Production Architecture: GCP VM, Docker, Nginx, localsort.in", "39"),
        ("Figure 6.2", "Interactive Streamlit Web Dashboard: Score Dial and Stance Badges", "40"),
        ("Figure 6.4", "UML Sequence Diagram Illustrating End-to-End Execution Flow", "41"),
        ("Figure 7.1", "Pipeline Latency Benchmarks (Log Scale) and Pytest Suite (38/38)", "43"),
        ("Figure 7.2", "Comparative Verification Performance Across Four Real-World Cases", "46")
    ]
    while len(t_figs.rows) < len(figs_data) + 1:
        t_figs.add_row()
    while len(t_figs.rows) > len(figs_data) + 1:
        tr = t_figs.rows[-1]._tr
        tr.getparent().remove(tr)

    for idx, (f_num, f_cap, f_pg) in enumerate(figs_data):
        row = t_figs.rows[idx + 1]
        row.cells[0].paragraphs[0].text = f_num
        row.cells[1].paragraphs[0].text = f_cap
        row.cells[2].paragraphs[0].text = f_pg
        for c_i, c in enumerate(row.cells):
            p = c.paragraphs[0]
            p.paragraph_format.line_spacing = 1.15
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if (c_i == 0 or c_i == 2) else WD_ALIGN_PARAGRAPH.LEFT
            for r in p.runs:
                r.font.name = "Times New Roman"
                r.font.size = Pt(10.5)

    # 8. Populate List of Tables (Table 6 in template)
    t_tbls = doc.tables[6]
    tbls_data = [
        ("Table 1.1", "Mapping of Project Objectives to UN Sustainable Development Goals", "6"),
        ("Table 2.1", "Critical Appraisal of Foundational Studies in News Verification", "10"),
        ("Table 4.1", "RACI Responsibility Assignment Matrix for TruthLens Team", "25"),
        ("Table 4.2", "Risk Assessment and Mitigation Protocols Executed in TruthLens", "26"),
        ("Table 5.1", "TruthLens System Requirements Specification (SRS Matrix)", "28"),
        ("Table 5.2", "Hardware, Operating System, and Production Cloud Environment Specs", "29"),
        ("Table 5.3", "Physical Data Dictionary and Relational Schema for mbfc_sources", "32"),
        ("Table 6.1", "TruthLens Production Software Module Inventory and Codebase Metrics", "34"),
        ("Table 7.1", "Empirical Latency Benchmarks Across Core Modules (1,000 Runs)", "43"),
        ("Table 7.2", "Automated Pytest Quality Assurance Breakdown Across 7 Modules", "44"),
        ("Table 7.3", "Experimental Results Across Four Real-World Case Studies", "45"),
        ("Table 7.4", "Comparative Architectural Matrix: TruthLens vs LLMs vs BERT", "47"),
        ("Table 7.5", "TruthLens 100% Roadmap Milestone Deliverables Verification Matrix", "48"),
        ("Table 8.1", "Demonstration of Ideological Orthogonality & Decoupled Bias Score", "50")
    ]
    while len(t_tbls.rows) < len(tbls_data) + 1:
        t_tbls.add_row()
    while len(t_tbls.rows) > len(tbls_data) + 1:
        tr = t_tbls.rows[-1]._tr
        tr.getparent().remove(tr)

    for idx, (t_num, t_cap, t_pg) in enumerate(tbls_data):
        row = t_tbls.rows[idx + 1]
        row.cells[0].paragraphs[0].text = t_num
        row.cells[1].paragraphs[0].text = t_cap
        row.cells[2].paragraphs[0].text = t_pg
        for c_i, c in enumerate(row.cells):
            p = c.paragraphs[0]
            p.paragraph_format.line_spacing = 1.15
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if (c_i == 0 or c_i == 2) else WD_ALIGN_PARAGRAPH.LEFT
            for r in p.runs:
                r.font.name = "Times New Roman"
                r.font.size = Pt(10.5)

    # 9. Populate List of Abbreviations (Table 7 in template)
    t_abbr = doc.tables[7]
    while len(t_abbr.rows) < len(report_data.ABBREVIATIONS) + 1:
        t_abbr.add_row()

    for idx, (abbr, full_text) in enumerate(report_data.ABBREVIATIONS):
        row = t_abbr.rows[idx + 1]
        row.cells[0].paragraphs[0].text = abbr
        row.cells[1].paragraphs[0].text = full_text
        for c_i, c in enumerate(row.cells):
            p = c.paragraphs[0]
            p.paragraph_format.line_spacing = 1.15
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            for r in p.runs:
                r.font.name = "Times New Roman"
                r.font.size = Pt(10.5)
                r.font.bold = (c_i == 0)

    # -------------------------------------------------------------
    # 10. ADD MAIN BODY SECTION FOR CHAPTERS 1 TO 9
    # -------------------------------------------------------------
    print("[*] Attaching complete 63-page academic report chapters...")
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
    fld_xml = r'<w:fldSimple %s w:instr="PAGE"/>' % nsdecls('w')
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

    # Build Chapters 1 to 9
    for ch_idx, ch in enumerate(report_chapters.CHAPTERS):
        print(f"[*] Attaching Chapter {ch['num']}: {ch['title']}...")
        add_chapter_heading(doc, ch["num"], ch["title"])

        if "intro_summary" in ch:
            add_body_p(doc, ch["intro_summary"])

        for sec in ch["sections"]:
            add_sec_heading(doc, sec["num"], sec["title"])

            for p_text in sec.get("paras", []):
                add_body_p(doc, p_text)

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

            if "figure" in sec:
                f_info = sec["figure"]
                add_figure_to_doc(
                    doc,
                    img_rel_path=f_info["path"],
                    fig_num_str=f_info["num"],
                    fig_caption_str=f_info["caption"],
                    width_inches=5.65
                )

            if "figure2" in sec:
                f2_info = sec["figure2"]
                add_figure_to_doc(
                    doc,
                    img_rel_path=f2_info["path"],
                    fig_num_str=f2_info["num"],
                    fig_caption_str=f2_info["caption"],
                    width_inches=5.65
                )

            for key in ["paras_cont", "paras_cont2", "paras_cont3", "paras_cont4", "paras_cont5", "paras_cont6"]:
                for p_text in sec.get(key, []):
                    add_body_p(doc, p_text)

        if ch_idx < len(report_chapters.CHAPTERS) - 1:
            doc.add_page_break()

    # REFERENCES
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

    # APPENDICES
    doc.add_page_break()
    p_app_main = doc.add_paragraph()
    p_app_main.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_app_main.paragraph_format.space_before = Pt(16)
    p_app_main.paragraph_format.space_after = Pt(18)
    r_ap = p_app_main.add_run("APPENDIX")
    r_ap.font.name = "Times New Roman"
    r_ap.font.size = Pt(16)
    r_ap.font.bold = True

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

    # Save to Desktop as final viva report.docx
    print(f"[*] Saving final viva report to: {OUT_DOCX}...")
    doc.save(OUT_DOCX)
    doc.save(DOCS_DOCX)
    print(f"[+] Successfully saved Word document to: {OUT_DOCX}")

    # Convert to PDF
    convert_to_pdf(OUT_DOCX, OUT_PDF, DOCS_PDF)


def convert_to_pdf(docx_path, pdf_path, docs_pdf):
    print(f"[*] Converting {docx_path} to PDF via Microsoft Word COM...")
    subprocess.run("taskkill /F /IM WINWORD.EXE /T", shell=True, capture_output=True)

    try:
        import comtypes.client
        word = comtypes.client.CreateObject('Word.Application')
        word.Visible = False

        doc = word.Documents.Open(os.path.abspath(docx_path))
        try:
            doc.Fields.Update()
        except Exception:
            pass

        doc.SaveAs(os.path.abspath(pdf_path), FileFormat=17)
        page_count = doc.ComputeStatistics(2)
        doc.Close()
        word.Quit()

        shutil.copyfile(pdf_path, docs_pdf)
        print(f"[+] Successfully exported PDF report ({page_count} pages) to:")
        print(f"    - {pdf_path}")
        print(f"    - {docs_pdf}")
    except Exception as e:
        print(f"[!] PDF export warning: {e}")


if __name__ == "__main__":
    generate_final_viva_report()
