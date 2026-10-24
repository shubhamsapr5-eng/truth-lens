"""
Builds the complete, publication-grade Review 4 (85% Milestone) PowerPoint presentation for TruthLens.
Mapped directly to the 85% project evaluation criteria for CSS7102, School of AI & AC, Presidency University.
"""

import os
import shutil
import pptx
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

SRC_PPT = r"C:\Users\shubh\Desktop\AI_News_Credibility_Scorer_Review3.pptx"
DST_PPT = r"C:\Users\shubh\Desktop\AI_News_Credibility_Scorer_Review4.pptx"
DOCS_PPT = r"C:\Users\shubh\Desktop\truth-lens\docs\AI_News_Credibility_Scorer_Review4.pptx"
FIGURES_DIR = r"C:\Users\shubh\Desktop\truth-lens\data\figures"

PRIMARY_COLOR = RGBColor(16, 44, 87)       # Navy Blue
ACCENT_COLOR = RGBColor(53, 101, 169)     # Medium Blue
TEXT_DARK = RGBColor(33, 37, 41)          # Dark Charcoal
BG_LIGHT = RGBColor(245, 247, 250)        # Soft Gray
SUCCESS_COLOR = RGBColor(40, 167, 69)     # Forest Green
WARNING_COLOR = RGBColor(217, 119, 6)     # Amber
DANGER_COLOR = RGBColor(220, 38, 38)      # Crimson


def create_review4_presentation():
    # Load Review 3 PPT as base to preserve Presidency University slide master, layouts, and institutional branding
    prs = Presentation(SRC_PPT)
    slide_layout_content = prs.slide_layouts[1] if len(prs.slide_layouts) > 1 else prs.slide_layouts[0]

    # 1. Update Slide 2 for Review 4 (85% Milestone)
    slide2 = prs.slides[1]
    for shape in slide2.shapes:
        if shape.has_text_frame:
            for p in shape.text_frame.paragraphs:
                if "Review-3" in p.text or "Review 3" in p.text or "50%" in p.text:
                    p.text = "CSS7102 - Mini Project Review-4 (85% Milestone)"
                    p.font.bold = True
                    p.font.color.rgb = PRIMARY_COLOR
                if "AI-Powered Real-Time News Credibility Scorer" in p.text or "TruthLens" in p.text:
                    p.text = "TruthLens: AI-Powered Real-Time News Credibility and Misinformation Verification Engine"

    # Helper: Clear shapes on a slide
    def clear_slide(slide):
        shapes_to_remove = [s for s in slide.shapes]
        for s in shapes_to_remove:
            sp = s._element
            sp.getparent().remove(sp)

    def add_slide_header(slide, title_text):
        """Adds a unified styled title header."""
        tx_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.8), Inches(0.85))
        tf = tx_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.text = title_text
        p.font.name = "Arial"
        p.font.size = Pt(25)
        p.font.bold = True
        p.font.color.rgb = PRIMARY_COLOR

    def format_cell(cell, text, font_size=10, bold=False, color=TEXT_DARK, bg_color=None, align=PP_ALIGN.LEFT):
        """Formats a table cell with text, padding, and optional background."""
        cell.text = text
        cell.margin_left = Inches(0.08)
        cell.margin_right = Inches(0.08)
        cell.margin_top = Inches(0.05)
        cell.margin_bottom = Inches(0.05)
        cell.vertical_anchor = MSO_ANCHOR.MIDDLE
        if bg_color:
            cell.fill.solid()
            cell.fill.fore_color.rgb = bg_color
        p = cell.text_frame.paragraphs[0]
        p.alignment = align
        p.font.name = "Arial"
        p.font.size = Pt(font_size)
        p.font.bold = bold
        p.font.color.rgb = color

    # Ensure 22 slides total for comprehensive Review 4 coverage
    total_needed = 22
    while len(prs.slides) < total_needed:
        prs.slides.add_slide(slide_layout_content)

    # Clear slides 3 to 22
    for i in range(2, total_needed):
        clear_slide(prs.slides[i])

    # ==========================================
    # SLIDE 3: Table of Contents (Review 4 - 85% Milestone)
    # ==========================================
    s3 = prs.slides[2]
    add_slide_header(s3, "Table of Contents (Review 4 - 85% Milestone Deliverables)")

    col1_items = [
        ("1. Problem Statement & Official GitHub Repository", "PSAIAC_61 Scope & CI Pipeline"),
        ("2. Abstract & Executive Summary", "Real-Time Multi-Source Corroboration Engine"),
        ("3. Literature Survey (7 Core IEEE Papers)", "Foundational Works & Research Gaps"),
        ("4. Project Objectives & 85% Realization", "SMART Technical Goals & Progress Audit"),
        ("5. Existing Methods vs. TruthLens Innovation", "Comparative Critique of Current Classifiers"),
        ("6. Mathematical Scoring Model (C_final)", "Three-Pillar Formula & Calibration Math"),
        ("7. System Architecture Diagram", "Review 4 Fused Pipeline Architecture"),
        ("8. Level-1 Data Flow Diagram (DFD)", "Submodule Interaction & Data Pipelines"),
        ("9. Database Entity-Relationship (ER) Architecture", "SQLite B-Tree Index (4,442 Media Outlets)")
    ]

    col2_items = [
        ("10. Automated Factual Claim Extraction", "spaCy NER & Linguistic Assertion Heuristics"),
        ("11. RoBERTa-MNLI Directional Stance Engine", "Pairwise Semantic NLI (+1, -1, 0) Classification"),
        ("12. Phase 4 Core Technical Achievements", "85% Operational Milestone Fused Engine"),
        ("13. Empirical Benchmarks & Performance", "Latency Profiling (<2.5s) & Model Accuracy"),
        ("14. Real-World Case Studies & Dial Outputs", "Reuters (96%) vs Bleach (14%) vs Onion (0%)"),
        ("15. Automated Test Suite Audit (27/27 Tests)", "100% Pytest Pass Rate Across 6 Submodules"),
        ("16. 85% vs Remaining 15% Engineering Division", "Completed Milestones vs Final Phase 5 Scope"),
        ("17. Project Timeline & 5-Phase Gantt Chart", "Review 4 Status with Phase 4 Completed"),
        ("18. Team Member Contribution Matrix", "Review 4 Engineering Deliverables & Roles"),
        ("19. References", "Standard IEEE Format Citations")
    ]

    t_box1 = s3.shapes.add_textbox(Inches(0.8), Inches(1.3), Inches(5.8), Inches(5.6))
    tf1 = t_box1.text_frame
    tf1.word_wrap = True
    for idx, (title, desc) in enumerate(col1_items):
        p = tf1.add_paragraph() if idx > 0 else tf1.paragraphs[0]
        p.text = f"{title} -- {desc}"
        p.font.name = "Arial"
        p.font.size = Pt(11)
        p.font.color.rgb = TEXT_DARK
        p.space_after = Pt(4)

    t_box2 = s3.shapes.add_textbox(Inches(6.8), Inches(1.3), Inches(5.8), Inches(5.6))
    tf2 = t_box2.text_frame
    tf2.word_wrap = True
    for idx, (title, desc) in enumerate(col2_items):
        p = tf2.add_paragraph() if idx > 0 else tf2.paragraphs[0]
        p.text = f"{title} -- {desc}"
        p.font.name = "Arial"
        p.font.size = Pt(11)
        p.font.color.rgb = TEXT_DARK
        p.space_after = Pt(4)

    # ==========================================
    # SLIDE 4: Problem Statement & GitHub
    # ==========================================
    s4 = prs.slides[3]
    add_slide_header(s4, "Problem Statement & Official GitHub Repository")

    s4_box = s4.shapes.add_textbox(Inches(0.8), Inches(1.3), Inches(11.8), Inches(5.6))
    s4_tf = s4_box.text_frame
    s4_tf.word_wrap = True

    p = s4_tf.paragraphs[0]
    p.text = "Problem Statement Number: PSAIAC_61"
    p.font.name = "Arial"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = PRIMARY_COLOR
    p.space_after = Pt(10)

    details = [
        ("Institution & School:", "School of Artificial Intelligence and Advanced Computing (AI&AC), Presidency University, Bengaluru"),
        ("Course & Review:", "CSS7102 - Mini Project | Review 4 Evaluation (Target: 85% System Completion)"),
        ("Domain / Category:", "Applied Natural Language Processing (NLP), Deep Learning & Information Retrieval"),
        ("The Misinformation Crisis:", "Peer-reviewed research (Vosoughi et al., Science 2018) proves false news spreads ~6x faster than verified journalism due to emotional shock and novelty. Traditional text classifiers fail because sophisticated misinformation is written in formal, professional journalistic syntax."),
        ("The TruthLens Innovation:", "Instead of assessing an article in isolation, TruthLens cross-examines factual claims against the living consensus of independent global news reporting using Natural Language Inference (NLI), source authority weighting, and lexical manipulation penalties."),
        ("Official GitHub Repository:", "https://github.com/shubhamsapr5-eng/truth-lens (Fully tracked, CI test suite passing 27/27)")
    ]

    for label, val in details:
        p = s4_tf.add_paragraph()
        run1 = p.add_run()
        run1.text = f"{label} "
        run1.font.bold = True
        run1.font.size = Pt(13)
        run1.font.color.rgb = ACCENT_COLOR if "GitHub" in label else PRIMARY_COLOR

        run2 = p.add_run()
        run2.text = val
        run2.font.bold = True if "GitHub" in label else False
        run2.font.size = Pt(13)
        run2.font.color.rgb = SUCCESS_COLOR if "GitHub" in label else TEXT_DARK
        p.space_after = Pt(7)

    # ==========================================
    # SLIDE 5: Abstract & Executive Summary (85% State)
    # ==========================================
    s5 = prs.slides[4]
    add_slide_header(s5, "Abstract & Executive Summary (85% Milestone State)")

    s5_box = s5.shapes.add_textbox(Inches(0.8), Inches(1.3), Inches(11.8), Inches(5.6))
    s5_tf = s5_box.text_frame
    s5_tf.word_wrap = True

    abstract_sections = [
        ("Problem Statement:", "Modern digital disinformation leverages emotional urgency and formal journalistic tone, rendering conventional single-document NLP classifiers ineffective. Misinformation cascades across digital networks 6x faster than truthful reporting."),
        ("Proposed TruthLens Engine:", "TruthLens presents a multi-modal, real-time news credibility verification engine. It isolates empirical assertions via NLP entity parsing, queries live independent global news pools via NewsAPI, computes directional NLI stance using RoBERTa-MNLI, and derives a calibrated mathematical credibility index."),
        ("85% Milestone Technical Realization:", "At Review 4, TruthLens has fully realized: (1) Sub-millisecond SQLite B-Tree domain database (4,442 outlets, 0.018ms), (2) 109-trigger lexical manipulation engine (0.24ms), (3) Automated claim extractor (spaCy NER), (4) RoBERTa-MNLI 3-way directional stance classifier (88.4% accuracy), and (5) Unified algebraic score dial with epistemic confidence calibration."),
        ("Verification & Verification Audit:", "100% automated pytest pass rate across 27 unit and integration tests (4.17s execution), a fully responsive interactive web portal, a 54-page institutionally compliant project report, and a 6-page IEEE conference paper.")
    ]

    for idx, (label, text) in enumerate(abstract_sections):
        p = s5_tf.add_paragraph() if idx > 0 else s5_tf.paragraphs[0]
        r1 = p.add_run()
        r1.text = f"{label} "
        r1.font.bold = True
        r1.font.size = Pt(13)
        r1.font.color.rgb = PRIMARY_COLOR

        r2 = p.add_run()
        r2.text = text
        r2.font.size = Pt(13)
        r2.font.color.rgb = TEXT_DARK
        p.space_after = Pt(8)

    # ==========================================
    # SLIDE 6: Literature Survey (7 Foundational Papers) + Taxonomy Diagram
    # ==========================================
    s6 = prs.slides[5]
    add_slide_header(s6, "Literature Survey (7 Foundational Papers & Research Gaps)")

    s6_box = s6.shapes.add_textbox(Inches(0.8), Inches(1.3), Inches(5.9), Inches(5.6))
    s6_tf = s6_box.text_frame
    s6_tf.word_wrap = True

    lit_summary = [
        ("1. Vosoughi et al. (Science 2018):", "Analyzed 126k Twitter rumor cascades; proved falsehoods diffuse 6x faster than truth due to novelty and emotional arousal. (Gap: Purely empirical; TruthLens builds the active verification system)."),
        ("2. Thorne et al. (NAACL 2018):", "FEVER benchmark formalizing 3-way fact checking (Supported, Refuted, NEI). (Gap: Limited to static Wikipedia; TruthLens operates over live streaming web news)."),
        ("3. Baly et al. (EMNLP 2018):", "Source-level profiling of 1,066 news outlets via MBFC. (Gap: Evaluates domains in isolation without verifying article claims; TruthLens unifies domain and claim stance)."),
        ("4. Liu et al. (arXiv 2019):", "RoBERTa transformer achieving 90.2% NLI accuracy. (Gap: High computational overhead; TruthLens optimizes top-sentence extraction for <2.5s inference)."),
        ("5. Baly et al. (ACL 2020):", "Proved single-text fake news classifiers learn topic shortcuts rather than truthfulness. (Directly validates TruthLens's cross-source corroboration requirement)."),
        ("6. Horne & Adali (AAAI ICWSM 2017):", "Linguistic manipulation profiling showing clickbait has higher emotional intensity. (TruthLens integrates this as an explicit penalty factor M_index)."),
        ("7. Norregaard et al. (AAAI 2019):", "NELA-GT corpus linking domain credibility with linguistic traits. (TruthLens operationalizes this into a sub-millisecond SQLite B-tree database).")
    ]

    for idx, (title, text) in enumerate(lit_summary):
        p = s6_tf.add_paragraph() if idx > 0 else s6_tf.paragraphs[0]
        r1 = p.add_run()
        r1.text = f"{title} "
        r1.font.bold = True
        r1.font.size = Pt(10)
        r1.font.color.rgb = PRIMARY_COLOR

        r2 = p.add_run()
        r2.text = text
        r2.font.size = Pt(9.5)
        r2.font.color.rgb = TEXT_DARK
        p.space_after = Pt(2.5)

    fig_lit = os.path.join(FIGURES_DIR, "fig2_1_literature_taxonomy.png")
    if os.path.exists(fig_lit):
        s6.shapes.add_picture(fig_lit, Inches(6.9), Inches(1.35), Inches(5.6), Inches(5.35))

    # ==========================================
    # SLIDE 7: Project Objectives & 85% Realization
    # ==========================================
    s7 = prs.slides[6]
    add_slide_header(s7, "Project Objectives & 85% Review 4 Realization")

    s7_box = s7.shapes.add_textbox(Inches(0.8), Inches(1.3), Inches(11.8), Inches(5.6))
    s7_tf = s7_box.text_frame
    s7_tf.word_wrap = True

    objs = [
        ("Objective 1 -- Automated Factual Claim Extraction [COMPLETED - 100%]:", "Engineered spaCy NER and syntactic assertion parsing heuristics to isolate checkable claims from news text in <2.5s. Ranks claims by empirical salience."),
        ("Objective 2 -- High-Speed Source Reputation Profiling [COMPLETED - 100%]:", "Constructed SQLite B-Tree indexed database of 4,442 media outlets cataloged via Media Bias/Fact Check (MBFC). Delivers sub-millisecond (0.018ms) query lookups, TLD fallbacks (.gov, .edu), and satire overrides."),
        ("Objective 3 -- Multi-Source Evidence Retrieval [COMPLETED - 100%]:", "Integrated live NewsAPI corroboration engine querying 80,000+ independent global publications to assemble a balanced corroboration pool of 5-8 independent sources per claim."),
        ("Objective 4 -- RoBERTa-MNLI Directional Stance Classification [COMPLETED - 100%]:", "Implemented directional NLI pipeline classifying pairwise claim-evidence alignment into Entailment (+1.0), Neutral (0.0), and Contradiction (-1.0) with Bayesian posterior confidence calibration."),
        ("Objective 5 -- Linguistic Manipulation & Sensationalism Scanner [COMPLETED - 100%]:", "Built a 109-trigger lexical scanner detecting sensationalism, emotional panic, and structural conspiracy triggers in 0.245ms."),
        ("Objective 6 -- Unified Mathematical Aggregator & Dashboard [COMPLETED - 100%]:", "Implemented the algebraic formula C_final = 0.70*S_evidence + 0.30*W_origin - 0.25*M_index in an interactive Streamlit web dashboard."),
        ("Objective 7 -- Production REST API & Containerization [SCHEDULED - PHASE 5]:", "Asynchronous FastAPI microservice endpoints and Docker Compose containerization for production deployment (Scheduled for Final Review 5).")
    ]

    for idx, (title, text) in enumerate(objs):
        p = s7_tf.add_paragraph() if idx > 0 else s7_tf.paragraphs[0]
        r1 = p.add_run()
        r1.text = f"{title} "
        r1.font.bold = True
        r1.font.size = Pt(11.5)
        r1.font.color.rgb = SUCCESS_COLOR if "[COMPLETED" in title else WARNING_COLOR

        r2 = p.add_run()
        r2.text = text
        r2.font.size = Pt(11)
        r2.font.color.rgb = TEXT_DARK
        p.space_after = Pt(4)

    # ==========================================
    # SLIDE 8: Existing Methods vs TruthLens
    # ==========================================
    s8 = prs.slides[7]
    add_slide_header(s8, "Existing Methods vs. TruthLens Innovation")

    rows_em = [
        ("Approach", "Working Principle", "Critical Drawbacks & Limitations", "TruthLens Innovation"),
        ("1. Single-Text NLP Classifiers\n(BERT / SVM / LSTM)", "Evaluates input text in isolation based on style, sentiment, and keywords.", "High False Positives: Fails when falsehoods are written in formal tone (Baly et al., ACL 2020).", "Cross-Source Corroboration: Verifies facts against independent global news consensus."),
        ("2. Static Domain Blacklisting", "Maintains static lists of flagged fake news and conspiracy domains.", "Zero-Day Vulnerability: Useless against newly registered domains, clone sites, or forums.", "Multi-Tier Resolver: Apex matching, wildcard subdomains, and authoritative TLD fallbacks."),
        ("3. Manual Human Fact-Checking\n(Snopes, PolitiFact)", "Human journalists manually research claims and write debunking articles.", "Severe Latency: Takes hours to days per claim. Ineffective against viral surges.", "Real-Time Automation: Executes full 5-stage verification pipeline in <2.5 seconds."),
        ("4. Shallow Keyword Search", "Searches web for shared keywords between articles.", "Semantic Blindness: Cannot tell if external reporting agrees, refutes, or is neutral.", "Directional NLI: RoBERTa computes directional entailment (+1.0) vs contradiction (-1.0).")
    ]

    t8 = s8.shapes.add_table(len(rows_em), 4, Inches(0.8), Inches(1.3), Inches(11.8), Inches(5.6)).table
    t8.columns[0].width = Inches(2.2)
    t8.columns[1].width = Inches(2.8)
    t8.columns[2].width = Inches(3.4)
    t8.columns[3].width = Inches(3.4)

    for r_idx, row in enumerate(rows_em):
        is_hdr = (r_idx == 0)
        bg = PRIMARY_COLOR if is_hdr else (BG_LIGHT if r_idx % 2 == 1 else None)
        fg = RGBColor(255, 255, 255) if is_hdr else TEXT_DARK
        for c_idx, val in enumerate(row):
            format_cell(t8.cell(r_idx, c_idx), val, font_size=9.5 if not is_hdr else 10.5, bold=is_hdr, color=fg, bg_color=bg)

    # ==========================================
    # SLIDE 9: Mathematical Credibility Scoring Model
    # ==========================================
    s9 = prs.slides[8]
    add_slide_header(s9, "Mathematical Credibility Scoring Model (C_final)")

    s9_box = s9.shapes.add_textbox(Inches(0.8), Inches(1.3), Inches(5.9), Inches(5.6))
    s9_tf = s9_box.text_frame
    s9_tf.word_wrap = True

    p = s9_tf.paragraphs[0]
    r = p.add_run()
    r.text = "Unified Mathematical Scoring Equation:\n"
    r.font.bold = True
    r.font.size = Pt(13)
    r.font.color.rgb = PRIMARY_COLOR
    p.space_after = Pt(2)

    p_eq = s9_tf.add_paragraph()
    r_eq = p_eq.add_run()
    r_eq.text = "C_final = 0.70 * S_evidence + 0.30 * W_origin - (0.25 * M_index)\n"
    r_eq.font.bold = True
    r_eq.font.size = Pt(12)
    r_eq.font.color.rgb = ACCENT_COLOR
    p_eq.space_after = Pt(4)

    math_points = [
        ("1. Multi-Source Evidence Consensus (S_evidence - 70%):", "Derived from directional NLI stances Phi_i in {+1.0, 0.0, -1.0} weighted by publisher authority W_rep,i and model confidence Conf_i:\nPhi_bar = sum(W_rep,i * Phi_i * Conf_i) / sum(W_rep,i)\nS_evidence = (Phi_bar + 1.0) * 50.0  -> Maps [-1, +1] to [0, 100]."),
        ("2. Origin Publisher Reputation (W_origin - 30%):", "Media Bias/Fact Check (MBFC) authority score mapped to [0, 100]. High-factuality wire outlets (Reuters, AP) contribute 100%; mixed outlets contribute 40-50%."),
        ("3. Manipulation Penalty Factor (M_index):", "Deducts up to 25 points based on 109 lexical trigger markers (sensationalism, panic urgency, conspiracy rhetoric)."),
        ("4. Epistemic Calibration & Overrides:", "• Satire Override: Domain cataloged as satire -> C_final clamped to 0.0%.\n• Conspiracy Override: Recorded conspiracy domain -> C_final capped at 15.0%.\n• Refutation Cap: Independent consensus refutes claim -> C_final capped at 25.0%.")
    ]

    for title, text in math_points:
        p = s9_tf.add_paragraph()
        r1 = p.add_run()
        r1.text = f"{title}\n"
        r1.font.bold = True
        r1.font.size = Pt(10)
        r1.font.color.rgb = PRIMARY_COLOR

        r2 = p.add_run()
        r2.text = f"{text}\n"
        r2.font.size = Pt(9)
        r2.font.color.rgb = TEXT_DARK
        p.space_after = Pt(2)

    fig_scoring = os.path.join(FIGURES_DIR, "fig3_2_scoring_pipeline.png")
    if os.path.exists(fig_scoring):
        s9.shapes.add_picture(fig_scoring, Inches(6.9), Inches(1.35), Inches(5.6), Inches(5.35))

    # ==========================================
    # SLIDE 10: System Architecture Diagram (Full Slide)
    # ==========================================
    s10 = prs.slides[9]
    add_slide_header(s10, "System Architecture Diagram (Review 4 Fused Pipeline)")

    fig_arch = os.path.join(FIGURES_DIR, "fig3_1_architecture.png")
    if os.path.exists(fig_arch):
        s10.shapes.add_picture(fig_arch, Inches(0.8), Inches(1.35), Inches(11.73), Inches(5.35))

    # ==========================================
    # SLIDE 11: Level-1 Data Flow Diagram (DFD)
    # ==========================================
    s11 = prs.slides[10]
    add_slide_header(s11, "Level-1 Data Flow Diagram (DFD) & Submodule Interaction")

    s11_box = s11.shapes.add_textbox(Inches(0.8), Inches(1.3), Inches(5.9), Inches(5.6))
    s11_tf = s11_box.text_frame
    s11_tf.word_wrap = True

    dfd_desc = [
        ("Process 1.0 -- Ingestion & Canonical Resolution:", "Incoming article URL or text is cleaned; URL helper isolates apex domain (e.g. edition.cnn.com -> cnn.com)."),
        ("Process 2.0 -- Source Reputation Query:", "SQLite B-Tree lookup queries 4,442 MBFC records; extracts factual rating, bias, and assigns authority weight W_origin in <0.02ms."),
        ("Process 3.0 -- Manipulation Scanning:", "Lexicon scanner matches 109 trigger regexes across 4 categories; calculates manipulation score M_index in 0.24ms."),
        ("Process 4.0 -- Factual Claim Extraction:", "spaCy NER and dependency parser isolate top empirical claims; filters out non-testable opinions."),
        ("Process 5.0 -- Multi-Source Retrieval:", "Queries NewsAPI for independent reporting pool; pulls top 5-8 corroborating articles."),
        ("Process 6.0 -- Semantic Stance Inference:", "RoBERTa-MNLI classifies claim-evidence pairs into Supports (+1), Refutes (-1), Neutral (0)."),
        ("Process 7.0 -- Score Aggregator & UI:", "Fuses S_evidence, W_origin, M_index into C_final dial; displays transparent audit breakdown.")
    ]

    for title, text in dfd_desc:
        p = s11_tf.add_paragraph()
        r1 = p.add_run()
        r1.text = f"{title}\n"
        r1.font.bold = True
        r1.font.size = Pt(10)
        r1.font.color.rgb = PRIMARY_COLOR

        r2 = p.add_run()
        r2.text = f"{text}\n"
        r2.font.size = Pt(9.2)
        r2.font.color.rgb = TEXT_DARK
        p.space_after = Pt(2)

    fig_dfd = os.path.join(FIGURES_DIR, "fig5_2_dfd.png")
    if os.path.exists(fig_dfd):
        s11.shapes.add_picture(fig_dfd, Inches(6.9), Inches(1.35), Inches(5.6), Inches(5.35))

    # ==========================================
    # SLIDE 12: Database Architecture & ER Diagram
    # ==========================================
    s12 = prs.slides[11]
    add_slide_header(s12, "Database Entity-Relationship (ER) Architecture (4,442 Sources)")

    s12_box = s12.shapes.add_textbox(Inches(0.8), Inches(1.3), Inches(5.9), Inches(5.6))
    s12_tf = s12_box.text_frame
    s12_tf.word_wrap = True

    db_points = [
        ("1. High-Performance SQLite B-Tree Index:", "Indexed SQLite database optimized for sub-millisecond query execution. Benchmarked at 0.018ms latency per domain lookup."),
        ("2. Comprehensive 4,442 Media Outlet Coverage:", "Cataloged via Media Bias/Fact Check (MBFC) dataset across global journalistic channels, regional press, satire, and conspiracy portals."),
        ("3. Relational Schema Attributes:", "• domain (PRIMARY KEY, indexed text)\n• source_name (VARCHAR)\n• factual_reporting (VERY HIGH / HIGH / MIXED / LOW)\n• bias (LEFT / LEAST BIASED / RIGHT)\n• credibility_score (REAL 0.0 to 1.0)\n• is_satire (BOOLEAN flag for automatic 0.0% override)\n• is_conspiracy (BOOLEAN flag for 15.0% cap)"),
        ("4. Resilient Multi-Tier Resolver:", "Direct Canonical -> Apex Domain -> Wildcard Subdomain -> Institutional TLD (.gov, .edu) -> Name Match -> Default Fallback.")
    ]

    for title, text in db_points:
        p = s12_tf.add_paragraph()
        r1 = p.add_run()
        r1.text = f"{title}\n"
        r1.font.bold = True
        r1.font.size = Pt(10.5)
        r1.font.color.rgb = PRIMARY_COLOR

        r2 = p.add_run()
        r2.text = f"{text}\n"
        r2.font.size = Pt(9.5)
        r2.font.color.rgb = TEXT_DARK
        p.space_after = Pt(3)

    fig_er = os.path.join(FIGURES_DIR, "fig5_3_er_diagram.png")
    if os.path.exists(fig_er):
        s12.shapes.add_picture(fig_er, Inches(6.9), Inches(1.35), Inches(5.6), Inches(5.35))

    # ==========================================
    # SLIDE 13: Automated Factual Claim Extraction
    # ==========================================
    s13 = prs.slides[12]
    add_slide_header(s13, "Automated Factual Claim Extraction & NLP Heuristics")

    s13_box = s13.shapes.add_textbox(Inches(0.8), Inches(1.3), Inches(11.8), Inches(5.6))
    s13_tf = s13_box.text_frame
    s13_tf.word_wrap = True

    p = s13_tf.paragraphs[0]
    p.text = "Review 4 Core Deliverable: spaCy NER & Assertion Verb Parser"
    p.font.name = "Arial"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = PRIMARY_COLOR
    p.space_after = Pt(8)

    claim_features = [
        ("1. The Need for Automated Claim Extraction:", "Users frequently input entire paragraphs or multi-thousand-word news articles. Verifying an entire article directly produces noise; extracting the core testable factual assertion is strictly necessary for precise NLI verification."),
        ("2. Named Entity Recognition (NER) & Numerical Parsing:", "Utilizes spaCy's `en_core_web_sm` pipeline to detect Named Entities (PERSON, ORG, GPE, DATE, CARDINAL, MONEY). Sentences containing concrete entities and quantitative numbers are prioritized as checkable empirical propositions."),
        ("3. Factual Assertion Heuristics:", "Scans for assertive declaration verbs (e.g., 'confirmed', 'announced', 'discovered', 'landed', 'approved', 'reported') while actively filtering out epistemic modals ('might', 'believes', 'feels', 'in my opinion') to eliminate non-testable subjective opinions."),
        ("4. Empirical Salience Scoring:", "Scores each extracted candidate claim on a [0.0, 1.0] salience scale based on entity density, assertion verbs, and sentence position. Selects the top 2-3 most salient factual claims for downstream cross-examination."),
        ("5. Benchmarked Execution Speed:", "Processes average news paragraphs (150-300 words) in <0.95 seconds with zero GPU dependency.")
    ]

    for title, text in claim_features:
        p = s13_tf.add_paragraph()
        r1 = p.add_run()
        r1.text = f"{title} "
        r1.font.bold = True
        r1.font.size = Pt(12)
        r1.font.color.rgb = PRIMARY_COLOR

        r2 = p.add_run()
        r2.text = text
        r2.font.size = Pt(11.5)
        r2.font.color.rgb = TEXT_DARK
        p.space_after = Pt(5)

    # ==========================================
    # SLIDE 14: RoBERTa-MNLI Stance Engine & Evidence Pool
    # ==========================================
    s14 = prs.slides[13]
    add_slide_header(s14, "RoBERTa-MNLI Directional Stance Classification Engine")

    s14_box = s14.shapes.add_textbox(Inches(0.8), Inches(1.3), Inches(5.9), Inches(5.6))
    s14_tf = s14_box.text_frame
    s14_tf.word_wrap = True

    stance_desc = [
        ("1. Natural Language Inference (NLI) Architecture:", "Uses cross-encoder RoBERTa pretrained on Multi-Genre NLI (392k sentence pairs) to model semantic entailment between a claim and retrieved evidence."),
        ("2. Three-Way Directional Mapping (Phi):", "• Entailment (Phi = +1.0): Evidence directly confirms, corroborates, or supports claim.\n• Contradiction (Phi = -1.0): Evidence refutes, contradicts, or debunks claim.\n• Neutral (Phi = 0.0): Contextual topic overlap without affirmation or denial."),
        ("3. Epistemic Bayesian Confidence Calibration:", "Stance impact is multiplied by the model's posterior probability Conf_i in [0.5, 1.0]. Dampens low-confidence inferences and eliminates borderline noise."),
        ("4. Multi-Source Consensus Convergence:", "Combines directional stance with publisher authority weights W_rep,i. Tabloids have minimal influence; authoritative news wire services (Reuters, AP, BBC) anchor the consensus direction."),
        ("5. Directional Stance Badges:", "Visualized in the dashboard as glowing 🟢 SUPPORTS (+1.0), 🔴 REFUTES (-1.0), and ⚪ NEUTRAL (0.0) pills with confidence ratings.")
    ]

    for title, text in stance_desc:
        p = s14_tf.add_paragraph()
        r1 = p.add_run()
        r1.text = f"{title}\n"
        r1.font.bold = True
        r1.font.size = Pt(10)
        r1.font.color.rgb = PRIMARY_COLOR

        r2 = p.add_run()
        r2.text = f"{text}\n"
        r2.font.size = Pt(9)
        r2.font.color.rgb = TEXT_DARK
        p.space_after = Pt(2)

    fig_pool = os.path.join(FIGURES_DIR, "fig6_3_evidence_pool.png")
    if os.path.exists(fig_pool):
        s14.shapes.add_picture(fig_pool, Inches(6.9), Inches(1.35), Inches(5.6), Inches(5.35))

    # ==========================================
    # SLIDE 15: End-to-End Sequence Diagram
    # ==========================================
    s15 = prs.slides[14]
    add_slide_header(s15, "End-to-End System Execution & Sequence Diagram")

    fig_seq = os.path.join(FIGURES_DIR, "fig6_4_sequence_diagram.png")
    if os.path.exists(fig_seq):
        s15.shapes.add_picture(fig_seq, Inches(0.8), Inches(1.35), Inches(11.73), Inches(5.35))

    # ==========================================
    # SLIDE 16: Phase 4 Core Achievements (85% Milestone)
    # ==========================================
    s16 = prs.slides[15]
    add_slide_header(s16, "Phase 4 Core Technical Achievements (85% Milestone Complete)")

    s16_box = s16.shapes.add_textbox(Inches(0.8), Inches(1.3), Inches(5.9), Inches(5.6))
    s16_tf = s16_box.text_frame
    s16_tf.word_wrap = True

    achieve_r4 = [
        ("1. RoBERTa-MNLI Directional Stance Engine:", "Fully integrated 3-way NLI inference pipeline delivering 88.4% stance accuracy across real-world news claim-evidence pairs."),
        ("2. Unified Algebraic Score Dial (C_final):", "Integrated mathematical aggregator fusing multi-source consensus S_evidence (70%), origin authority W_origin (30%), and manipulation penalty M_index (25%)."),
        ("3. Automated Claim Extractor:", "spaCy NER and assertion verb parser extracting checkable factual propositions in <0.95s."),
        ("4. Complete 27-Test Continuous Integration Suite:", "100% pytest pass rate covering all 6 submodules with continuous regression protection (4.17s execution)."),
        ("5. High-Tech Dark Cyberpunk UI:", "Sleek dark glassmorphism dashboard with 4 circular SVG score dials, transparent mathematical audit callout, and 1-click viva demo presets."),
        ("6. Publication-Grade Documentation:", "54-page institutionally compliant project report and 6-page IEEE conference paper.")
    ]

    for title, text in achieve_r4:
        p = s16_tf.add_paragraph()
        r1 = p.add_run()
        r1.text = f"{title}\n"
        r1.font.bold = True
        r1.font.size = Pt(10)
        r1.font.color.rgb = PRIMARY_COLOR

        r2 = p.add_run()
        r2.text = f"{text}\n"
        r2.font.size = Pt(9)
        r2.font.color.rgb = TEXT_DARK
        p.space_after = Pt(2)

    fig_ui = os.path.join(FIGURES_DIR, "fig6_2_streamlit_ui.png")
    if os.path.exists(fig_ui):
        s16.shapes.add_picture(fig_ui, Inches(6.9), Inches(1.35), Inches(5.6), Inches(5.35))

    # ==========================================
    # SLIDE 17: Empirical Benchmarks & Real-World Case Studies
    # ==========================================
    s17 = prs.slides[16]
    add_slide_header(s17, "Empirical Benchmarks & Real-World Case Studies")

    s17_box = s17.shapes.add_textbox(Inches(0.8), Inches(1.3), Inches(5.9), Inches(5.6))
    s17_tf = s17_box.text_frame
    s17_tf.word_wrap = True

    cases_desc = [
        ("Case Study 1 -- Verified Breaking Journalism (Chandrayaan-3):", "• Claim: 'ISRO soft-landed Chandrayaan-3 on the lunar south pole.'\n• Origin: Reuters (W_origin = 1.0)\n• Evidence Pool: 5/5 independent outlets confirm (Phi = +1.0)\n• Output: C_final = 96.0% -> HIGH CREDIBILITY (VERIFIED) 🟢"),
        ("Case Study 2 -- Viral Medical Disinformation (Bleach Cure):", "• Claim: 'Drinking bleach cures viral infections.'\n• Origin: Natural News (Low Factuality, W_origin = 0.15)\n• Evidence Pool: Medical fact-checkers refute (Phi = -1.0)\n• Output: C_final = 14.0% -> DEBUNKED / LOW CREDIBILITY 🔴"),
        ("Case Study 3 -- Satirical Parody (The Onion):", "• Claim: 'Scientists discover moon dust cures aging.'\n• Origin: The Onion (100% Satirical humor outlet)\n• Output: Categorical override -> C_final = 0.0% SATIRE 🎭"),
        ("Latency Benchmarking:", "SQLite lookup: 0.018ms | Manipulation: 0.24ms | Stance Inference: 48ms/pair | Total Pipeline: <2.3s.")
    ]

    for title, text in cases_desc:
        p = s17_tf.add_paragraph()
        r1 = p.add_run()
        r1.text = f"{title}\n"
        r1.font.bold = True
        r1.font.size = Pt(10)
        r1.font.color.rgb = PRIMARY_COLOR

        r2 = p.add_run()
        r2.text = f"{text}\n"
        r2.font.size = Pt(8.8)
        r2.font.color.rgb = TEXT_DARK
        p.space_after = Pt(2)

    fig_bench = os.path.join(FIGURES_DIR, "fig7_2_case_studies.png")
    if os.path.exists(fig_bench):
        s17.shapes.add_picture(fig_bench, Inches(6.9), Inches(1.35), Inches(5.6), Inches(5.35))

    # ==========================================
    # SLIDE 18: Automated Test Suite Audit (27/27 Tests Passed)
    # ==========================================
    s18 = prs.slides[17]
    add_slide_header(s18, "Automated Test Suite Audit (27/27 Tests Passed - 100% Pass Rate)")

    s18_box = s18.shapes.add_textbox(Inches(0.8), Inches(1.25), Inches(11.8), Inches(1.0))
    s18_tf = s18_box.text_frame
    s18_tf.word_wrap = True
    p = s18_tf.paragraphs[0]
    p.text = "TruthLens maintains continuous automated testing using pytest. Full 27-test suite executes in 4.17 seconds with zero failures and zero warnings."
    p.font.name = "Arial"
    p.font.size = Pt(12)
    p.font.color.rgb = TEXT_DARK

    rows_test = [
        ("Test Module", "Subsystem Scope & Test Criteria", "Test Count", "Pass Rate", "Execution Latency"),
        ("tests/test_source_reputation.py", "SQLite B-Tree lookups, apex domains, wildcards, TLD fallbacks, satire flags, batch query performance.", "9 Tests", "100% (9/9)", "0.18 s"),
        ("tests/test_manipulation.py", "109-trigger lexical scanner, sensationalism, emotional panic, conspiracy rhetoric, clean text control.", "4 Tests", "100% (4/4)", "0.08 s"),
        ("tests/test_claim_extractor.py", "spaCy NER parsing, assertion verb identification, empirical salience ranking, empty input handling.", "3 Tests", "100% (3/3)", "0.95 s"),
        ("tests/test_news_retriever.py", "Live NewsAPI queries, query parameter formulation, network fallback mocks, empty search protection.", "3 Tests", "100% (3/3)", "0.32 s"),
        ("tests/test_stance.py", "RoBERTa-MNLI directional stance (Supports +1, Refutes -1, Neutral 0), batch inference, neutral cases.", "4 Tests", "100% (4/4)", "2.14 s"),
        ("tests/test_score_aggregator.py", "Unified C_final formula, satire clamp (0%), refutation cap (25%), manipulation penalty deduction.", "4 Tests", "100% (4/4)", "0.12 s"),
        ("TOTAL VERIFIED SUITE", "Comprehensive End-to-End System Integrity Validation", "27 Tests", "100% PASSED", "4.17 s (PASS)")
    ]

    t18 = s18.shapes.add_table(len(rows_test), 5, Inches(0.8), Inches(2.2), Inches(11.8), Inches(4.8)).table
    t18.columns[0].width = Inches(2.5)
    t18.columns[1].width = Inches(4.7)
    t18.columns[2].width = Inches(1.3)
    t18.columns[3].width = Inches(1.7)
    t18.columns[4].width = Inches(1.6)

    for r_idx, row in enumerate(rows_test):
        is_hdr = (r_idx == 0)
        is_total = (r_idx == len(rows_test) - 1)
        bg = PRIMARY_COLOR if is_hdr else (RGBColor(230, 245, 230) if is_total else (BG_LIGHT if r_idx % 2 == 1 else None))
        fg = RGBColor(255, 255, 255) if is_hdr else (SUCCESS_COLOR if is_total else TEXT_DARK)
        for c_idx, val in enumerate(row):
            format_cell(t18.cell(r_idx, c_idx), val, font_size=9.5 if not is_hdr else 10.5, bold=(is_hdr or is_total), color=fg, bg_color=bg)

    # ==========================================
    # SLIDE 19: 85% Completed vs Remaining 15% Engineering Division
    # ==========================================
    s19 = prs.slides[18]
    add_slide_header(s19, "85% Completed vs. Remaining 15% Engineering Division")

    rows_div = [
        ("Engineering Dimension", "85% Completed (Phases 1, 2, 3 & 4) -- REVIEW 4", "Remaining 15% (Phase 5) -- FINAL REVIEW 5"),
        ("Core Engineering Scope", "Data Infrastructure, SQLite MBFC Database, NewsAPI Live Retrieval, spaCy Claim Extractor, RoBERTa Stance NLI & C_final Dial.", "FastAPI Asynchronous REST Microservice, Docker Compose Containerization & Chrome Web Extension."),
        ("Source Reputation Engine", "SQLite database of 4,442 media outlets cataloged via MBFC (<0.02ms query speed) with multi-tier domain resolution.", "Periodic automated MBFC database update crawler and automated caching."),
        ("Linguistic Manipulation", "109-trigger lexical and structural scanner detecting sensationalism, panic urgency, and conspiracy markers in 0.24ms.", "Transformer-based stylistic clickbait classifier (optional ensemble)."),
        ("Claim Extraction", "spaCy NER and factual assertion verb parser extracting top-3 testable empirical claims in <0.95s.", "Multi-sentence coreference resolution for long-form investigatory pieces."),
        ("AI Fact Verification", "RoBERTa-MNLI directional stance classification (Supports +1, Refutes -1, Neutral 0) with confidence calibration.", "Asynchronous Celery/Redis queue for high-concurrency batch processing."),
        ("Deployment & UI", "Full-featured interactive Streamlit web dashboard with 4 score dials, transparent formula audit, and viva presets.", "Containerized Docker deployment and lightweight Chrome browser extension.")
    ]

    t19 = s19.shapes.add_table(len(rows_div), 3, Inches(0.8), Inches(1.3), Inches(11.8), Inches(5.6)).table
    t19.columns[0].width = Inches(2.2)
    t19.columns[1].width = Inches(4.8)
    t19.columns[2].width = Inches(4.8)

    for r_idx, row in enumerate(rows_div):
        is_hdr = (r_idx == 0)
        bg = PRIMARY_COLOR if is_hdr else (BG_LIGHT if r_idx % 2 == 1 else None)
        fg = RGBColor(255, 255, 255) if is_hdr else TEXT_DARK
        for c_idx, val in enumerate(row):
            format_cell(t19.cell(r_idx, c_idx), val, font_size=9.5 if not is_hdr else 10.5, bold=is_hdr, color=fg, bg_color=bg)

    # ==========================================
    # SLIDE 20: Project Timeline & 5-Phase Gantt Chart
    # ==========================================
    s20 = prs.slides[19]
    add_slide_header(s20, "Project Timeline & 5-Phase Gantt Chart (Review 4 Status)")

    fig_gantt = os.path.join(FIGURES_DIR, "fig4_1_gantt.png")
    if os.path.exists(fig_gantt):
        s20.shapes.add_picture(fig_gantt, Inches(0.8), Inches(1.35), Inches(11.73), Inches(5.35))

    # ==========================================
    # SLIDE 21: Team Member Contribution Matrix
    # ==========================================
    s21 = prs.slides[20]
    add_slide_header(s21, "Team Member Contribution Matrix (Review 4 Deliverables)")

    rows_team = [
        ("Roll Number", "Team Member", "Review 4 (85% Milestone) Core Deliverables", "Final Review 5 Focus"),
        ("20231CAI0046", "Shubham Pandey\n(Team Leader)", "• Engineered Unified Mathematical Score Aggregator (C_final formula).\n• Implemented epistemic Bayesian confidence calibration.\n• Architected 27-suite automated pytest pipeline.\n• Designed system architecture and coordinated full-pipeline integration.", "FastAPI asynchronous microservice REST endpoints & final evaluation thesis."),
        ("20231CAI0006", "Ikram Inayathulla Khan", "• Engineered Automated Factual Claim Extraction module (spaCy NER).\n• Formulated syntactic assertion heuristics and empirical salience ranking.\n• Maintained 109-trigger linguistic manipulation detector.\n• Authored Chapter 3 & 4 documentation on claim parsing heuristics.", "Docker Compose containerization and multi-sentence coreference resolution."),
        ("20231CAI0003", "Karanam Radha Pranathi", "• Engineered RoBERTa-MNLI directional stance classification pipeline.\n• Tuned 3-way entailment, contradiction, and neutral threshold boundaries.\n• Maintained live NewsAPI independent evidence pool retrieval.\n• Authored Chapter 5 & 6 documentation on semantic NLI inference.", "Chrome Web Extension manifest development and user testing."),
        ("20231CAI0068", "Bhagyesh", "• Engineered interactive Streamlit web dashboard with high-contrast theme.\n• Built 4 circular SVG score dials and transparent mathematical audit box.\n• Created 1-click demonstration viva presets for instantaneous faculty testing.\n• Handled UI state persistence and domain inspection reactivity.", "Web UI production deployment, user guide, and final demo packaging.")
    ]

    t21 = s21.shapes.add_table(len(rows_team), 4, Inches(0.8), Inches(1.3), Inches(11.8), Inches(5.6)).table
    t21.columns[0].width = Inches(1.8)
    t21.columns[1].width = Inches(2.2)
    t21.columns[2].width = Inches(5.0)
    t21.columns[3].width = Inches(2.8)

    for r_idx, row in enumerate(rows_team):
        is_hdr = (r_idx == 0)
        bg = PRIMARY_COLOR if is_hdr else (BG_LIGHT if r_idx % 2 == 1 else None)
        fg = RGBColor(255, 255, 255) if is_hdr else TEXT_DARK
        for c_idx, val in enumerate(row):
            format_cell(t21.cell(r_idx, c_idx), val, font_size=9.5 if not is_hdr else 10.5, bold=is_hdr, color=fg, bg_color=bg)

    # ==========================================
    # SLIDE 22: References (IEEE Format)
    # ==========================================
    s22 = prs.slides[21]
    add_slide_header(s22, "References (IEEE Standard Citations)")

    s22_box = s22.shapes.add_textbox(Inches(0.8), Inches(1.3), Inches(11.8), Inches(5.6))
    s22_tf = s22_box.text_frame
    s22_tf.word_wrap = True

    refs = [
        "[1] S. Vosoughi, D. Roy, and S. Aral, \"The spread of true and false news online,\" Science, vol. 359, no. 6380, pp. 1146-1151, Mar. 2018.",
        "[2] J. Thorne, A. Vlachos, C. Christodoulopoulos, and A. Mittal, \"FEVER: a large-scale dataset for Fact Extraction and VERification,\" in Proc. NAACL-HLT 2018, pp. 809-819.",
        "[3] R. Baly, G. Karadzhov, D. Alexandrov, J. Glass, and P. Nakov, \"Predicting factuality of reporting and bias of news media sources,\" in Proc. EMNLP 2018, pp. 3528-3539.",
        "[4] Y. Liu, M. Ott, N. Goyal, J. Du, M. Joshi, D. Chen, O. Levy, M. Lewis, L. Zettlemoyer, and V. Stoyanov, \"RoBERTa: A Robustly Optimized BERT Pretraining Approach,\" arXiv:1907.11692, 2019.",
        "[5] R. Baly, G. Karadzhov, J. Glass, and P. Nakov, \"We Can Detect Fake News with High Accuracy, but What Did We Learn? A Quantitative and Qualitative Analysis,\" in Proc. ACL 2020, pp. 5182-5197.",
        "[6] B. D. Horne and S. Adali, \"This Just In: Fake News Packs a Lot in Title, Uses Less Words, and Is More Repetitive,\" in Proc. AAAI ICWSM 2017, pp. 759-766.",
        "[7] J. Norregaard, B. D. Horne, and S. Adali, \"NELA-GT-2018: A Large Multi-Labelled News Dataset for The Study of Misinformation in News Articles,\" in Proc. AAAI ICWSM 2019, pp. 630-638.",
        "[8] IEEE Editorial Style Manual for Authors, IEEE Periodicals, Piscataway, NJ, USA, 2023.",
        "[9] ISO/IEC/IEEE 29148:2018, Systems and software engineering -- Life cycle processes -- Requirements engineering, IEEE Standards Association, 2018."
    ]

    for idx, ref in enumerate(refs):
        p = s22_tf.add_paragraph() if idx > 0 else s22_tf.paragraphs[0]
        p.text = ref
        p.font.name = "Arial"
        p.font.size = Pt(10.5)
        p.font.color.rgb = TEXT_DARK
        p.space_after = Pt(4)

    # Save presentations
    saved_paths = []
    try:
        prs.save(DST_PPT)
        saved_paths.append(DST_PPT)
    except PermissionError:
        alt_path = r"C:\Users\shubh\Desktop\AI_News_Credibility_Scorer_Review4_Updated.pptx"
        prs.save(alt_path)
        saved_paths.append(alt_path)
        print(f"[!] Note: '{DST_PPT}' is open in PowerPoint. Saved to '{alt_path}' instead.")

    prs.save(DOCS_PPT)
    saved_paths.append(DOCS_PPT)
    print("Successfully generated Review 4 (85% Milestone) PPT at:")
    for p in saved_paths:
        print(f"  - {p}")


if __name__ == "__main__":
    create_review4_presentation()
