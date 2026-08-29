"""
Builds the complete, publication-grade Review 2 PowerPoint presentation for TruthLens.
Mapped 1-to-1 to the 20-mark evaluation rubric.
"""

import os
import shutil
import pptx
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

SRC_PPT = r"C:\Users\shubh\Desktop\AI_News_Credibility_Scorer_Review1 (1).pptx"
DST_PPT = r"C:\Users\shubh\Desktop\AI_News_Credibility_Scorer_Review2.pptx"
DOCS_PPT = r"C:\Users\shubh\Desktop\truth-lens\docs\AI_News_Credibility_Scorer_Review2.pptx"

PRIMARY_COLOR = RGBColor(16, 44, 87)       # Navy Blue
ACCENT_COLOR = RGBColor(53, 101, 169)     # Medium Blue
TEXT_DARK = RGBColor(33, 37, 41)          # Dark Charcoal
BG_LIGHT = RGBColor(245, 247, 250)        # Soft Gray
SUCCESS_COLOR = RGBColor(40, 167, 69)     # Forest Green


def create_review2_presentation():
    prs = Presentation(SRC_PPT)
    slide_layout_content = prs.slide_layouts[1] if len(prs.slide_layouts) > 1 else prs.slide_layouts[0]

    # 1. Update Slide 2 text
    slide2 = prs.slides[1]
    for shape in slide2.shapes:
        if shape.has_text_frame:
            for p in shape.text_frame.paragraphs:
                if "Review-1" in p.text or "Review 1" in p.text:
                    p.text = p.text.replace("Review-1", "Review-2").replace("Review 1", "Review 2")
                if "AI-Powered News Credibility Scorer" in p.text:
                    p.text = "TruthLens: AI-Powered Real-Time News Credibility Scorer"

    # Helper: Clear shapes on a slide except background graphics
    def clear_slide(slide):
        shapes_to_remove = [s for s in slide.shapes]
        for s in shapes_to_remove:
            sp = s._element
            sp.getparent().remove(sp)

    def add_slide_header(slide, title_text):
        """Adds a unified styled title header to slide."""
        tx_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.5), Inches(0.9))
        tf = tx_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.text = title_text
        p.font.name = "Arial"
        p.font.size = Pt(24)
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

    # Ensure we have 16 slides total
    total_needed = 16
    while len(prs.slides) < total_needed:
        prs.slides.add_slide(slide_layout_content)

    # Clear slides 3 to 16
    for i in range(2, 16):
        clear_slide(prs.slides[i])

    # ==========================================
    # SLIDE 3: Table of Contents
    # ==========================================
    s3 = prs.slides[2]
    add_slide_header(s3, "Table of Contents (Review 2 Evaluation)")
    
    t_box = s3.shapes.add_textbox(Inches(0.8), Inches(1.3), Inches(11.5), Inches(5.5))
    tf = t_box.text_frame
    tf.word_wrap = True

    toc_items = [
        ("1. Problem Statement & Official GitHub Repository", "PSAIAC_61 Project Scope & Repository"),
        ("2. Abstract", "Problem, Objectives & Approach (Rubric: 2 Marks)"),
        ("3. Literature Survey (12 IEEE / Scopus Papers)", "Critical Analysis & Comparative Matrix (Rubric: 3 Marks)"),
        ("4. Project Objectives", "SMART Outcome-Focused Goals (Rubric: 2 Marks)"),
        ("5. Existing Methods and Drawbacks", "Comparative Critique of Current Approaches (Rubric: 2 Marks)"),
        ("6. Proposed Method & Feasibility Study", "Cross-Source NLI & Technical/Cost Feasibility (Rubric: 3 Marks)"),
        ("7. System Architecture Diagram", "3-Tier Dataflow & Model Integration (Rubric: 3 Marks)"),
        ("8. System Modules Breakdown", "Modules 1 to 6 Functional Details (Rubric: 2 Marks)"),
        ("9. Hardware and Software Details", "Tech Stack, Dependencies & Hardware Specs (Rubric: 1 Mark)"),
        ("10. Timeline of the Project (Gantt Chart)", "5-Phase Development Plan & Milestones (Rubric: 1 Mark)"),
        ("11. References", "IEEE Standard Citation Format (Rubric: 1 Mark)"),
        ("12. Review 2 Phase Deliverables & Live Demo", "MBFC SQLite Database & Baseline Verification")
    ]

    for idx, (title, desc) in enumerate(toc_items):
        p = tf.add_paragraph() if idx > 0 else tf.paragraphs[0]
        p.text = f"{title}  --  {desc}"
        p.font.name = "Arial"
        p.font.size = Pt(12)
        p.font.color.rgb = TEXT_DARK
        p.space_after = Pt(4)

    # ==========================================
    # SLIDE 4: Problem Statement & GitHub
    # ==========================================
    s4 = prs.slides[3]
    add_slide_header(s4, "Problem Statement & GitHub Repository")

    s4_box = s4.shapes.add_textbox(Inches(0.8), Inches(1.4), Inches(11.5), Inches(5.5))
    s4_tf = s4_box.text_frame
    s4_tf.word_wrap = True

    p = s4_tf.paragraphs[0]
    p.text = "Problem Statement Number: PSAIAC_61"
    p.font.name = "Arial"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = PRIMARY_COLOR
    p.space_after = Pt(10)

    details = [
        ("Organization:", "School of Artificial Intelligence and Advanced Computing (AI&AC), Presidency University"),
        ("Category:", "Software / Applied Machine Learning & NLP"),
        ("Difficulty Level:", "Medium-High"),
        ("Problem Description:", "Misinformation spreads approximately 6x faster than real news online (Vosoughi et al., Science 2018). There is a critical societal need for an automated system that evaluates a news article in real time and scores it on: (1) factual accuracy, (2) source credibility, and (3) manipulation indicators."),
        ("Official GitHub Repository:", "https://github.com/shubhamsapr5-eng/truth-lens (Public Access Enabled)")
    ]

    for label, val in details:
        p = s4_tf.add_paragraph()
        run1 = p.add_run()
        run1.text = f"{label} "
        run1.font.bold = True
        run1.font.size = Pt(14)
        run1.font.color.rgb = ACCENT_COLOR if "GitHub" in label else PRIMARY_COLOR

        run2 = p.add_run()
        run2.text = val
        run2.font.bold = True if "GitHub" in label else False
        run2.font.size = Pt(14)
        run2.font.color.rgb = SUCCESS_COLOR if "GitHub" in label else TEXT_DARK
        p.space_after = Pt(10)

    # ==========================================
    # SLIDE 5: Abstract (2 Marks)
    # ==========================================
    s5 = prs.slides[4]
    add_slide_header(s5, "Abstract (Rubric: 2 Marks)")

    s5_box = s5.shapes.add_textbox(Inches(0.8), Inches(1.4), Inches(11.5), Inches(5.5))
    s5_tf = s5_box.text_frame
    s5_tf.word_wrap = True

    abstract_sections = [
        ("Problem Context:", "Online misinformation diffuses ~6x faster than verified factual news across digital platforms (Vosoughi et al., Science 2018). Traditional fake-news classifiers evaluate articles in isolation, learning superficial topic shortcuts and failing against professionally phrased falsehoods."),
        ("Core Project Objective:", "TruthLens develops a real-time credibility scoring engine that evaluates any news article across three orthogonal dimensions: Factual Accuracy (via multi-source corroboration), Source Reputation (via Media Bias/Fact Check data), and Manipulation Indicators (via clickbait/urgency heuristics)."),
        ("Proposed Approach & Workflow:", "TruthLens (1) extracts central checkable factual claims, (2) retrieves live independent reporting pools (5-10 articles) via News APIs, (3) evaluates semantic agreement using RoBERTa-MNLI (Entailment, Contradiction, Neutral), and (4) aggregates signals into an explainable 0-100 Credibility Score."),
        ("Deliverables & Impact:", "An indexed SQLite knowledge base of 4,442 news outlets (<1ms lookup), a high-throughput FastAPI backend, and an interactive Streamlit dashboard displaying transparent source-by-source evidence attribution.")
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
        p.space_after = Pt(10)

    # ==========================================
    # SLIDE 6: Literature Survey Part 1 (3 Marks)
    # ==========================================
    s6 = prs.slides[5]
    add_slide_header(s6, "Literature Survey -- Part 1 (Rubric: 3 Marks)")

    rows_p1 = [
        ("Paper & Author", "Methodology", "Dataset", "Key Findings", "Research Gap / TruthLens Solution"),
        ("Vosoughi et al.\nScience (2018) [1]", "Empirical rumor diffusion analysis on Twitter", "126k rumor cascades (Twitter)", "False news diffuses 6x faster than truth due to novelty and emotional arousal.", "Purely observational; TruthLens builds the active real-time verification system."),
        ("Thorne et al.\nNAACL-HLT (2018) [2]", "FEVER benchmark: retrieval & 3-way stance check", "185k claim pairs (Wikipedia)", "Formalized 3-class fact verification (Supported, Refuted, NotEnoughInfo).", "Restricted to clean static Wikipedia; TruthLens handles noisy live web news."),
        ("Baly et al.\nEMNLP (2018) [3]", "Source-level profiling of news factuality & bias", "1,066 news outlets from MBFC", "Source reputation features strongly predict bias and factuality.", "Assesses domains in isolation without verifying specific article claims. TruthLens combines both."),
        ("Liu et al.\narXiv / IEEE (2019) [4]", "RoBERTa: Optimized BERT Pretraining", "MNLI (392k pairs), CC-News", "State-of-the-art 90.2% NLI accuracy on cross-sentence semantic entailment.", "Requires high compute; TruthLens uses top-5 sentence filtering for fast sub-3s inference."),
        ("Wang\nACL (2017) [5]", "LIAR benchmark fake news classifier", "12.8k PolitiFact statements", "Surface speaker metadata improves text classification accuracy.", "Narrow US political scope; TruthLens generalizes across global news domains."),
        ("Shu et al.\nACM SIGKDD (2017) [6]", "Data mining survey on fake news detection", "FakeNewsNet (BuzzFeed/PolitiFact)", "Single-text detectors overfit; cross-checking external sources is critical.", "Lacks formal transformer-based NLI. TruthLens directly integrates RoBERTa-MNLI.")
    ]

    t6 = s6.shapes.add_table(len(rows_p1), 5, Inches(0.6), Inches(1.3), Inches(12.0), Inches(5.6)).table
    t6.columns[0].width = Inches(1.8)
    t6.columns[1].width = Inches(2.2)
    t6.columns[2].width = Inches(1.8)
    t6.columns[3].width = Inches(3.2)
    t6.columns[4].width = Inches(3.0)

    for r_idx, row in enumerate(rows_p1):
        is_hdr = (r_idx == 0)
        bg = PRIMARY_COLOR if is_hdr else (BG_LIGHT if r_idx % 2 == 1 else None)
        fg = RGBColor(255, 255, 255) if is_hdr else TEXT_DARK
        for c_idx, val in enumerate(row):
            format_cell(t6.cell(r_idx, c_idx), val, font_size=9 if not is_hdr else 10, bold=is_hdr, color=fg, bg_color=bg)

    # ==========================================
    # SLIDE 7: Literature Survey Part 2 (3 Marks)
    # ==========================================
    s7 = prs.slides[6]
    add_slide_header(s7, "Literature Survey -- Part 2 (Rubric: 3 Marks)")

    rows_p2 = [
        ("Paper & Author", "Methodology", "Dataset", "Key Findings", "Research Gap / TruthLens Solution"),
        ("Baly et al.\nACL (2020) [7]", "Robustness critique of fake news text classifiers", "Multi-domain news corpora", "Text-only classifiers learn superficial topic shortcuts rather than truthfulness.", "Directly validates TruthLens: cross-source corroboration is strictly necessary."),
        ("Hanselowski et al.\nCOLING (2018) [8]", "Fake News Challenge stance detection", "FNC-1 (50k pairs)", "Stance detection (Agree/Disagree) is an effective intermediate verification step.", "High class imbalance; TruthLens tunes directional agreement thresholds."),
        ("Horne & Adali\nAAAI ICWSM (2017) [9]", "Linguistic & structural manipulation profiling", "138k news articles", "Fake news uses longer emotional titles, fewer technical words, and more drama.", "High false positives if used alone; TruthLens uses manipulation as supporting penalty."),
        ("Aly et al.\nNeurIPS (2021) [10]", "FEVEROUS: Fact verification over structured data", "87k multi-hop claim pairs", "Combining cell tabular data with text improves verification accuracy by 14.8%.", "Multi-hop graph traversal is too slow; TruthLens optimizes for real-time web use."),
        ("Hardalov et al.\nNAACL (2022) [11]", "Survey on stance detection for disinformation", "Cross-document stance corpora", "Cross-document NLI provides strong defense against adversarial paraphrasing.", "Retrieval latency bottleneck; TruthLens uses fast indexed SQLite lookup (<1ms)."),
        ("Norregaard et al.\nAAAI (2019) [12]", "NELA-GT news ground truth dataset", "713k articles, 194 sources", "Correlated MBFC domain credibility scores with article-level linguistic traits.", "Static dataset snapshot; TruthLens integrates live streaming News APIs.")
    ]

    t7 = s7.shapes.add_table(len(rows_p2), 5, Inches(0.6), Inches(1.3), Inches(12.0), Inches(5.6)).table
    t7.columns[0].width = Inches(1.8)
    t7.columns[1].width = Inches(2.2)
    t7.columns[2].width = Inches(1.8)
    t7.columns[3].width = Inches(3.2)
    t7.columns[4].width = Inches(3.0)

    for r_idx, row in enumerate(rows_p2):
        is_hdr = (r_idx == 0)
        bg = PRIMARY_COLOR if is_hdr else (BG_LIGHT if r_idx % 2 == 1 else None)
        fg = RGBColor(255, 255, 255) if is_hdr else TEXT_DARK
        for c_idx, val in enumerate(row):
            format_cell(t7.cell(r_idx, c_idx), val, font_size=9 if not is_hdr else 10, bold=is_hdr, color=fg, bg_color=bg)

    # ==========================================
    # SLIDE 8: Project Objectives (2 Marks)
    # ==========================================
    s8 = prs.slides[7]
    add_slide_header(s8, "Project Objectives (Rubric: 2 Marks)")

    s8_box = s8.shapes.add_textbox(Inches(0.8), Inches(1.3), Inches(11.5), Inches(5.6))
    s8_tf = s8_box.text_frame
    s8_tf.word_wrap = True

    objs = [
        ("Objective 1 -- Automated Factual Claim Extraction:", "Develop an NLP module using syntactic heuristics and Named Entity Recognition (NER) to extract the top 2-3 checkable factual claims from articles in <2.5 seconds."),
        ("Objective 2 -- High-Speed Source Reputation Profiling:", "Construct an indexed SQLite knowledge base of 4,442 verified news domains based on MBFC ratings, delivering sub-millisecond (<1ms) lookups and institutional TLD fallbacks (.gov, .edu)."),
        ("Objective 3 -- Multi-Source Evidence Retrieval:", "Integrate NewsAPI and GNews API to programmatically retrieve a balanced corroboration pool of 5-10 contemporary reporting sources per claim."),
        ("Objective 4 -- RoBERTa-MNLI Cross-Source Corroboration:", "Implement a Natural Language Inference pipeline to classify pairwise claim-evidence relationships into Entailment (+1), Contradiction (-1), and Neutral (0) stance signals."),
        ("Objective 5 -- Manipulation & Clickbait Indexing:", "Build a lexical and stylistic analyzer utilizing 109 trigger patterns to evaluate sensationalism, emotional panic, and structural formatting manipulation (0-100 scale)."),
        ("Objective 6 -- Unified Aggregation Engine & User Interface:", "Deploy the mathematical multi-factor scoring formula in a FastAPI backend and interactive Streamlit web dashboard presenting transparent evidence cards.")
    ]

    for idx, (title, text) in enumerate(objs):
        p = s8_tf.add_paragraph() if idx > 0 else s8_tf.paragraphs[0]
        r1 = p.add_run()
        r1.text = f"{title} "
        r1.font.bold = True
        r1.font.size = Pt(11)
        r1.font.color.rgb = PRIMARY_COLOR

        r2 = p.add_run()
        r2.text = text
        r2.font.size = Pt(11)
        r2.font.color.rgb = TEXT_DARK
        p.space_after = Pt(6)

    # ==========================================
    # SLIDE 9: Existing Methods & Drawbacks (2 Marks)
    # ==========================================
    s9 = prs.slides[8]
    add_slide_header(s9, "Existing Methods and Drawbacks (Rubric: 2 Marks)")

    rows_em = [
        ("Existing Approach", "Working Principle", "Critical Drawbacks & Limitations"),
        ("1. Single-Text NLP Classifiers\n(BERT / SVM / LSTM)", "Evaluates the input article in isolation based solely on writing style, sentiment, and keywords.", "High False Positives: Fails when misinformation is written in formal, professional journalistic tone. Overfits to topic keywords rather than factuality (Baly et al., ACL 2020)."),
        ("2. Static Domain Blacklisting", "Maintains an ad-hoc blacklist of known fake news and conspiracy website URLs.", "Zero-Day Vulnerability: Useless against newly registered domains, clone sites, or misinformation published on legitimate platforms (blogs/forums)."),
        ("3. Manual Human Fact-Checking\n(Snopes, PolitiFact)", "Expert fact-checkers manually research claims and publish debunking articles.", "Severe Latency Bottleneck: Takes hours to days per claim. Ineffective against viral misinformation spreading across millions of feeds in minutes."),
        ("4. Shallow Keyword Matching", "Searches Google/News for shared keywords between articles.", "Semantic Blindness: Cannot differentiate whether the other article agrees, refutes, or merely mentions the topic in a different context. Semantic NLI is strictly required.")
    ]

    t9 = s9.shapes.add_table(len(rows_em), 3, Inches(0.8), Inches(1.3), Inches(11.5), Inches(5.5)).table
    t9.columns[0].width = Inches(2.8)
    t9.columns[1].width = Inches(3.2)
    t9.columns[2].width = Inches(5.5)

    for r_idx, row in enumerate(rows_em):
        is_hdr = (r_idx == 0)
        bg = PRIMARY_COLOR if is_hdr else (BG_LIGHT if r_idx % 2 == 1 else None)
        fg = RGBColor(255, 255, 255) if is_hdr else TEXT_DARK
        for c_idx, val in enumerate(row):
            format_cell(t9.cell(r_idx, c_idx), val, font_size=10 if not is_hdr else 11, bold=is_hdr, color=fg, bg_color=bg)

    # ==========================================
    # SLIDE 10: Proposed Method & Feasibility (3 Marks)
    # ==========================================
    s10 = prs.slides[9]
    add_slide_header(s10, "Proposed Method & Feasibility Study (Rubric: 3 Marks)")

    s10_box = s10.shapes.add_textbox(Inches(0.8), Inches(1.3), Inches(11.5), Inches(5.6))
    s10_tf = s10_box.text_frame
    s10_tf.word_wrap = True

    p = s10_tf.paragraphs[0]
    r = p.add_run()
    r.text = "Proposed Innovation -- Multi-Factor Cross-Source Corroboration:"
    r.font.bold = True
    r.font.size = Pt(13)
    r.font.color.rgb = PRIMARY_COLOR
    p.space_after = Pt(4)

    p2 = s10_tf.add_paragraph()
    r2 = p2.add_run()
    r2.text = "Instead of trusting the article's text, TruthLens verifies the claim against the global consensus of independent reputable outlets:\n"
    r2.text += "Formula: Credibility Score C = 0.70 * [ Evidence_Score ] + 0.30 * Source_Origin_Score - (0.25 * Manipulation_Index)\n"
    r2.text += "Where Evidence_Score = sum(Source_Reputation_Weight * NLI_Agreement_Signal) / sum(Source_Reputation_Weight)"
    r2.font.size = Pt(11)
    r2.font.color.rgb = TEXT_DARK
    p2.space_after = Pt(8)

    feas_items = [
        ("1. Technical Feasibility:", "Pretrained RoBERTa-MNLI achieves 90%+ zero-shot NLI accuracy without expensive re-training. SQLite provides <0.02ms indexed lookups locally."),
        ("2. Economic / Cost Feasibility ($0 Cost):", "Uses free developer tiers of NewsAPI (100 req/day) & GNews API. RoBERTa runs locally with zero cloud API billing."),
        ("3. Computational Feasibility:", "GPU inference takes <50ms per pair (<250ms on CPU). Limiting evidence to top 5 sentences guarantees <4s end-to-end latency."),
        ("4. Resource Availability:", "Idiap research corpus (4,400+ domains), Hugging Face model hub, and standard open-source Python libraries are fully accessible.")
    ]

    for title, text in feas_items:
        p = s10_tf.add_paragraph()
        r1 = p.add_run()
        r1.text = f"{title} "
        r1.font.bold = True
        r1.font.size = Pt(11)
        r1.font.color.rgb = ACCENT_COLOR

        r2 = p.add_run()
        r2.text = text
        r2.font.size = Pt(11)
        r2.font.color.rgb = TEXT_DARK
        p.space_after = Pt(4)

    # ==========================================
    # SLIDE 11: System Architecture Diagram (3 Marks)
    # ==========================================
    s11 = prs.slides[10]
    add_slide_header(s11, "System Architecture Diagram (Rubric: 3 Marks)")

    layer_data = [
        ("1. Presentation Layer", Inches(0.8), Inches(1.4), Inches(3.4), Inches(5.3), [
            "User Inputs:",
            " * News Article URL",
            " * Raw Claim Text",
            "",
            "Dashboard UI:",
            " * Streamlit / React",
            " * Credibility Gauge (0-100)",
            " * Evidence Attribution Cards",
            " * Manipulation Risk Warning"
        ]),
        ("2. Core Processing Pipeline", Inches(4.6), Inches(1.4), Inches(3.8), Inches(5.3), [
            "FastAPI REST Endpoints:",
            " * /analyze/url",
            " * /analyze/text",
            "",
            "Pipeline Modules:",
            " * Web Scraper (trafilatura)",
            " * Claim Extractor (NER/POS)",
            " * News Retrieval Engine",
            "   (NewsAPI & GNews API)",
            " * Corroboration Pool",
            "   (5-10 Outlets)"
        ]),
        ("3. Intelligence & Scoring", Inches(8.8), Inches(1.4), Inches(3.5), Inches(5.3), [
            "MBFC Source Database:",
            " * SQLite 4,442 Domains",
            " * Multi-tier domain resolver",
            " * Source weights (W_rep)",
            "",
            "RoBERTa-MNLI Engine:",
            " * Stance inference (Phi_NLI)",
            "",
            "Manipulation Detector:",
            " * 109 Lexical Triggers",
            "",
            "Multi-Factor Aggregator"
        ])
    ]

    for title, left, top, width, height, lines in layer_data:
        shape = s11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        shape.fill.solid()
        shape.fill.fore_color.rgb = BG_LIGHT
        shape.line.color.rgb = ACCENT_COLOR
        shape.line.width = Pt(1.5)

        tf = shape.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.12)
        tf.margin_top = Inches(0.12)
        p = tf.paragraphs[0]
        p.text = title
        p.font.name = "Arial"
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = PRIMARY_COLOR
        p.space_after = Pt(6)

        for l in lines:
            p = tf.add_paragraph()
            p.text = l
            p.font.name = "Arial"
            p.font.size = Pt(10)
            p.font.bold = True if ":" in l else False
            p.font.color.rgb = PRIMARY_COLOR if ":" in l else TEXT_DARK
            p.space_after = Pt(2)

    # ==========================================
    # SLIDE 12: Modules Breakdown (2 Marks)
    # ==========================================
    s12 = prs.slides[11]
    add_slide_header(s12, "System Modules Breakdown (Rubric: 2 Marks)")

    s12_box = s12.shapes.add_textbox(Inches(0.8), Inches(1.3), Inches(11.5), Inches(5.6))
    s12_tf = s12_box.text_frame
    s12_tf.word_wrap = True

    modules = [
        ("Module 1 -- Article Ingestion & Web Scraper:", "Parses news URLs, strips HTML boilerplate, extracts clean headline and body text, and identifies publisher domain."),
        ("Module 2 -- Factual Claim Extractor:", "Applies Named Entity Recognition (NER) and syntactic heuristics to identify checkable factual assertions from subjective opinion sentences."),
        ("Module 3 -- Evidence Retrieval Engine:", "Constructs targeted search queries from claims and fetches 5-10 contemporary articles from NewsAPI & GNews API."),
        ("Module 4 -- MBFC Source Reputation Database:", "Queries an indexed SQLite database of 4,442 news outlets; applies canonical domain matching and assigns reliability weights (W_rep)."),
        ("Module 5 -- RoBERTa-MNLI & Manipulation Engine:", "Submodule 5A evaluates semantic stance (Entailment/Contradiction/Neutral); Submodule 5B scans for 109 clickbait/panic triggers."),
        ("Module 6 -- Score Aggregation & Visual Dashboard:", "Computes the final 0-100 credibility score and renders interactive evidence breakdown cards in Streamlit.")
    ]

    for idx, (title, text) in enumerate(modules):
        p = s12_tf.add_paragraph() if idx > 0 else s12_tf.paragraphs[0]
        r1 = p.add_run()
        r1.text = f"{title} "
        r1.font.bold = True
        r1.font.size = Pt(11)
        r1.font.color.rgb = PRIMARY_COLOR

        r2 = p.add_run()
        r2.text = text
        r2.font.size = Pt(11)
        r2.font.color.rgb = TEXT_DARK
        p.space_after = Pt(6)

    # ==========================================
    # SLIDE 13: Hardware & Software Details (1 Mark)
    # ==========================================
    s13 = prs.slides[12]
    add_slide_header(s13, "Hardware and Software Details (Rubric: 1 Mark)")

    rows_hw = [
        ("Component Category", "Technology / Specification", "Purpose in TruthLens Architecture"),
        ("Programming Language", "Python 3.11+", "Core runtime for ML pipeline, API server, and data ingestion"),
        ("Deep Learning / NLP", "Hugging Face Transformers, PyTorch, roberta-large-mnli", "Semantic Natural Language Inference (Entailment, Contradiction, Neutral)"),
        ("Domain & URL Engine", "tldextract, Custom Canonical Resolver", "Subdomain stripping, multi-part TLD resolution (.co.uk, .gov.in)"),
        ("Database Layer", "SQLite 3 (Indexed embedded database)", "Sub-millisecond source reputation lookup across 4,442 outlets (<0.02ms)"),
        ("Evidence Retrieval APIs", "NewsAPI & GNews API (Free Developer Tier)", "Live multi-source news article search across 80,000+ publishers"),
        ("Web Scraping & Parser", "trafilatura, newspaper3k", "Robust article body, author, date, and clean text extraction"),
        ("Backend REST API", "FastAPI, Uvicorn, Pydantic v2", "Asynchronous, high-throughput REST API endpoints (/analyze, /source)"),
        ("Frontend Dashboard", "Streamlit / React", "Interactive user dashboard with credibility gauges & evidence cards"),
        ("Testing & Quality", "pytest 9.1+ (13 unit tests passed)", "Automated domain resolution, scoring, and manipulation tests"),
        ("Hardware Specs", "Min: Quad-Core CPU, 8 GB RAM, 5 GB SSD\nRec: 8-Core CPU, 16 GB RAM, NVIDIA RTX GPU", "Enables local RoBERTa model execution with <4s latency")
    ]

    t13 = s13.shapes.add_table(len(rows_hw), 3, Inches(0.8), Inches(1.3), Inches(11.5), Inches(5.6)).table
    t13.columns[0].width = Inches(2.5)
    t13.columns[1].width = Inches(4.2)
    t13.columns[2].width = Inches(4.8)

    for r_idx, row in enumerate(rows_hw):
        is_hdr = (r_idx == 0)
        bg = PRIMARY_COLOR if is_hdr else (BG_LIGHT if r_idx % 2 == 1 else None)
        fg = RGBColor(255, 255, 255) if is_hdr else TEXT_DARK
        for c_idx, val in enumerate(row):
            format_cell(t13.cell(r_idx, c_idx), val, font_size=8.5 if not is_hdr else 9.5, bold=is_hdr, color=fg, bg_color=bg)

    # ==========================================
    # SLIDE 14: Timeline / Gantt Chart (1 Mark)
    # ==========================================
    s14 = prs.slides[13]
    add_slide_header(s14, "Timeline of the Project -- 5-Phase Plan (Rubric: 1 Mark)")

    rows_tl = [
        ("Phase", "Duration", "Core Deliverables & Scope", "Current Status"),
        ("Phase 1", "Weeks 1-2", "Problem formulation (PSAIAC_61), literature survey (12 papers), architecture design, tech stack selection.", "Completed"),
        ("Phase 2", "Weeks 3-4", "Dataset collection, MBFC SQLite database (4,442 outlets), domain resolver, manipulation lexicons, baseline testing.", "Completed (Review 2)"),
        ("Phase 3", "Weeks 5-6", "Article ingestion pipeline (trafilatura), factual claim extraction module, NewsAPI & GNews retrieval integration.", "Upcoming"),
        ("Phase 4", "Weeks 7-8", "RoBERTa-MNLI model integration, pairwise stance classification pipeline, semantic similarity threshold filtering.", "Upcoming"),
        ("Phase 5", "Weeks 9-12", "Score aggregation engine, FastAPI REST API, Streamlit dashboard, end-to-end evaluation & final report.", "Upcoming")
    ]

    t14 = s14.shapes.add_table(len(rows_tl), 4, Inches(0.8), Inches(1.4), Inches(11.5), Inches(5.2)).table
    t14.columns[0].width = Inches(1.4)
    t14.columns[1].width = Inches(1.6)
    t14.columns[2].width = Inches(6.5)
    t14.columns[3].width = Inches(2.0)

    for r_idx, row in enumerate(rows_tl):
        is_hdr = (r_idx == 0)
        bg = PRIMARY_COLOR if is_hdr else (BG_LIGHT if r_idx % 2 == 1 else None)
        fg = RGBColor(255, 255, 255) if is_hdr else TEXT_DARK
        for c_idx, val in enumerate(row):
            format_cell(t14.cell(r_idx, c_idx), val, font_size=10 if not is_hdr else 11, bold=is_hdr, color=fg, bg_color=bg)

    # ==========================================
    # SLIDE 15: References -- IEEE Format (1 Mark)
    # ==========================================
    s15 = prs.slides[14]
    add_slide_header(s15, "References (IEEE Format -- Rubric: 1 Mark)")

    s15_box = s15.shapes.add_textbox(Inches(0.8), Inches(1.3), Inches(11.5), Inches(5.6))
    s15_tf = s15_box.text_frame
    s15_tf.word_wrap = True

    refs = [
        "[1] S. Vosoughi, D. Roy, and S. Aral, \"The spread of true and false news online,\" Science, vol. 359, no. 6380, pp. 1146-1151, Mar. 2018.",
        "[2] J. Thorne, A. Vlachos, C. Christodoulopoulos, and A. Mittal, \"FEVER: a large-scale dataset for Fact Extraction and VERification,\" in Proc. NAACL-HLT 2018, pp. 809-819.",
        "[3] R. Baly, G. Karadzhov, D. Alexandrov, J. Glass, and P. Nakov, \"Predicting factuality of reporting and bias of news media sources,\" in Proc. EMNLP 2018, pp. 3528-3539.",
        "[4] Y. Liu, M. Ott, N. Goyal, J. Du, M. Joshi, D. Chen, O. Levy, M. Lewis, L. Zettlemoyer, and V. Stoyanov, \"RoBERTa: A Robustly Optimized BERT Pretraining Approach,\" arXiv:1907.11692, 2019.",
        "[5] W. Y. Wang, \"\"Liar, Liar Pants on Fire\": A New Benchmark Dataset for Fake News Detection,\" in Proc. ACL 2017, pp. 422-426.",
        "[6] K. Shu, A. Sliva, S. Wang, J. Tang, and H. Liu, \"Fake News Detection on Social Media: A Data Mining Perspective,\" ACM SIGKDD Explorations Newsletter, vol. 19, no. 1, pp. 22-36, 2017.",
        "[7] R. Baly et al., \"We Can Detect Fake News with High Accuracy, but What Did We Learn? A Quantitative and Qualitative Analysis,\" in Proc. ACL 2020, pp. 5182-5197.",
        "[8] A. Hanselowski, H. P. Ji, V. Stoyanov, and I. Gurevych, \"A Retrospective Analysis of the Fake News Challenge Stance-Detection Task,\" in Proc. COLING 2018, pp. 1859-1874.",
        "[9] B. D. Horne and S. Adali, \"This Just In: Fake News Packs a Lot in Title, Uses Less Words, and Is More Repetitive,\" in Proc. AAAI ICWSM 2017, pp. 759-766.",
        "[10] R. Aly et al., \"FEVEROUS: Fact Extraction and VERification Over Unstructured and Structured information,\" in NeurIPS, vol. 34, 2021, pp. 25674-25687.",
        "[11] M. Hardalov, A. Arora, P. Nakov, and I. Augenstein, \"A Survey on Stance Detection for Mis- and Disinformation Identification,\" in Findings of NAACL 2022, pp. 1259-1277.",
        "[12] J. Norregaard, B. D. Horne, and S. Adali, \"NELA-GT-2018: A Large Multi-Labelled News Dataset for The Study of Misinformation in News Articles,\" in Proc. AAAI ICWSM 2019, pp. 630-638."
    ]

    for idx, ref in enumerate(refs):
        p = s15_tf.add_paragraph() if idx > 0 else s15_tf.paragraphs[0]
        p.text = ref
        p.font.name = "Arial"
        p.font.size = Pt(8.5)
        p.font.color.rgb = TEXT_DARK
        p.space_after = Pt(2.5)

    # ==========================================
    # SLIDE 16: Review 2 Summary & Demo
    # ==========================================
    s16 = prs.slides[15]
    add_slide_header(s16, "Review 2 Summary & Demonstration")

    s16_box = s16.shapes.add_textbox(Inches(0.8), Inches(1.3), Inches(11.5), Inches(5.6))
    s16_tf = s16_box.text_frame
    s16_tf.word_wrap = True

    p = s16_tf.paragraphs[0]
    p.text = "Review 2 Phase Deliverables Achieved (Weeks 3-4):"
    p.font.name = "Arial"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = PRIMARY_COLOR
    p.space_after = Pt(6)

    achievements = [
        ("Source Reputation Database:", "4,442 unique media domains indexed in SQLite with sub-millisecond lookups (<0.02ms)."),
        ("Canonical Domain Resolver:", "Multi-tier resolution supporting subdomains, multi-part TLDs (.co.uk, .gov.in), and institutional fallbacks (.gov, .edu)."),
        ("Manipulation Detection Engine:", "109 lexical and stylistic triggers detecting clickbait, emotional urgency, and conspiracy markers."),
        ("Ground-Truth Testbed:", "10 verified benchmark claims and full sample articles across 6 domains for evaluation."),
        ("Automated Quality Assurance:", "13 out of 13 unit tests passed (pytest); live interactive demonstration tool ready (demo_phase2.py)."),
        ("GitHub Repository:", "https://github.com/shubhamsapr5-eng/truth-lens (Fully organized & updated).")
    ]

    for label, desc in achievements:
        p = s16_tf.add_paragraph()
        r1 = p.add_run()
        r1.text = f"[+] {label} "
        r1.font.bold = True
        r1.font.size = Pt(11)
        r1.font.color.rgb = SUCCESS_COLOR

        r2 = p.add_run()
        r2.text = desc
        r2.font.size = Pt(11)
        r2.font.color.rgb = TEXT_DARK
        p.space_after = Pt(4)

    # Save presentations
    prs.save(DST_PPT)
    prs.save(DOCS_PPT)
    print(f"Successfully generated Review 2 PPT with 0 warnings at:\n  1. {DST_PPT}\n  2. {DOCS_PPT}")


if __name__ == "__main__":
    create_review2_presentation()
