"""
TruthLens: AI-Powered Real-Time News Credibility Verification Engine
Web Application Dashboard (65% Milestone - Phase 4 Deliverable)

Developed for PSAIAC_61 Evaluation
Presidency University - School of Artificial Intelligence and Advanced Computing
"""

import os
import sys
import time
import re
import urllib.parse
from datetime import datetime
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st
import pandas as pd
from dotenv import load_dotenv

from src.database.source_reputation_db import SourceReputationDB
from src.manipulation.manipulation_detector import ManipulationDetector
from src.retrieval.news_retriever import NewsRetriever
from src.claim_extraction.claim_extractor import ClaimExtractor
from src.stance.stance_classifier import StanceClassifier, StanceType
from src.scoring.score_aggregator import ScoreAggregator, VerdictTier

load_dotenv()

# ==============================================================================
# 1. PAGE CONFIGURATION & STYLING
# ==============================================================================
st.set_page_config(
    page_title="TruthLens - AI News Credibility Scorer (65% Milestone)",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern card UI, badges, and meters
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    
    /* Global Typography & Hero */
    .main-title {
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 50%, #2563eb 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.3rem;
        letter-spacing: -0.02em;
    }
    .sub-title {
        font-size: 1.05rem;
        color: #64748b;
        margin-bottom: 1.4rem;
        line-height: 1.5;
    }
    
    /* Modern Glassmorphic / Elevated Card */
    .metric-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 1.25rem 1.3rem;
        box-shadow: 0 4px 20px -2px rgba(15, 23, 42, 0.05);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        margin-bottom: 1rem;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 25px -4px rgba(15, 23, 42, 0.09);
        border-color: #cbd5e1;
    }
    .metric-value {
        font-size: 1.85rem;
        font-weight: 800;
        color: #0f172a;
        letter-spacing: -0.02em;
        line-height: 1.2;
    }
    .metric-label {
        font-size: 0.78rem;
        font-weight: 700;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 0.3rem;
    }
    
    /* Badges */
    .badge-verified {
        background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%);
        color: #065f46;
        border: 1px solid #a7f3d0;
        padding: 4px 14px;
        border-radius: 9999px;
        font-size: 0.82rem;
        font-weight: 700;
        display: inline-flex;
        align-items: center;
        gap: 5px;
    }
    .badge-mixed {
        background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%);
        color: #92400e;
        border: 1px solid #fde68a;
        padding: 4px 14px;
        border-radius: 9999px;
        font-size: 0.82rem;
        font-weight: 700;
        display: inline-flex;
        align-items: center;
        gap: 5px;
    }
    .badge-satire {
        background: linear-gradient(135deg, #f5f3ff 0%, #ede9fe 100%);
        color: #5b21b6;
        border: 1px solid #ddd6fe;
        padding: 4px 14px;
        border-radius: 9999px;
        font-size: 0.82rem;
        font-weight: 700;
        display: inline-flex;
        align-items: center;
        gap: 5px;
    }
    .badge-danger {
        background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%);
        color: #991b1b;
        border: 1px solid #fecaca;
        padding: 4px 14px;
        border-radius: 9999px;
        font-size: 0.82rem;
        font-weight: 700;
        display: inline-flex;
        align-items: center;
        gap: 5px;
    }

    /* Stance Badges */
    .badge-stance-supports {
        background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%);
        color: #065f46;
        border: 1.5px solid #10b981;
        padding: 5px 14px;
        border-radius: 9999px;
        font-size: 0.84rem;
        font-weight: 800;
        display: inline-flex;
        align-items: center;
        gap: 6px;
    }
    .badge-stance-refutes {
        background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%);
        color: #991b1b;
        border: 1.5px solid #ef4444;
        padding: 5px 14px;
        border-radius: 9999px;
        font-size: 0.84rem;
        font-weight: 800;
        display: inline-flex;
        align-items: center;
        gap: 6px;
    }
    .badge-stance-neutral {
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
        color: #475569;
        border: 1.5px solid #cbd5e1;
        padding: 5px 14px;
        border-radius: 9999px;
        font-size: 0.84rem;
        font-weight: 800;
        display: inline-flex;
        align-items: center;
        gap: 6px;
    }
    
    /* Evidence Card */
    .evidence-box {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-left: 5px solid #2563eb;
        border-radius: 12px;
        padding: 1.25rem 1.4rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 12px -2px rgba(15, 23, 42, 0.04);
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }
    .evidence-box:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px -3px rgba(15, 23, 42, 0.08);
    }
    .evidence-box.high { border-left-color: #10b981; }
    .evidence-box.mixed { border-left-color: #f59e0b; }
    .evidence-box.low { border-left-color: #ef4444; }

    /* Mono Pill */
    .mono-pill {
        font-family: 'JetBrains Mono', monospace;
        background: #f1f5f9;
        color: #334155;
        font-size: 0.78rem;
        padding: 3px 8px;
        border-radius: 6px;
        border: 1px solid #e2e8f0;
    }

    /* Math Formula Callout Box */
    .math-callout {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: #f8fafc;
        border-radius: 14px;
        padding: 1.2rem 1.5rem;
        margin: 1.2rem 0;
        border-left: 5px solid #3b82f6;
        box-shadow: 0 6px 20px -2px rgba(15, 23, 42, 0.15);
    }
</style>
""", unsafe_allow_html=True)


def render_circular_gauge(score: float, label: str, color_hex: str = "#2563eb", size: int = 140, subtitle: str = ""):
    """Renders a responsive, clean SVG circular score gauge."""
    radius = 42
    circumference = 2 * 3.14159265 * radius
    clamped_score = max(0.0, min(100.0, float(score)))
    dashoffset = circumference - (clamped_score / 100.0) * circumference
    
    return f"""
    <div style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 16px; padding: 1.2rem 1rem; box-shadow: 0 4px 20px -2px rgba(15,23,42,0.05); text-align: center; display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100%;">
        <div style="font-size: 0.78rem; font-weight: 700; color: #64748b; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 0.4rem;">{label}</div>
        <div style="position: relative; width: {size}px; height: {size}px; display: flex; align-items: center; justify-content: center;">
            <svg width="{size}" height="{size}" viewBox="0 0 100 100" style="transform: rotate(-90deg);">
                <circle cx="50" cy="50" r="{radius}" stroke="#f1f5f9" stroke-width="9" fill="transparent" />
                <circle cx="50" cy="50" r="{radius}" stroke="{color_hex}" stroke-width="9" stroke-linecap="round" fill="transparent"
                    stroke-dasharray="{circumference}" stroke-dashoffset="{dashoffset}" />
            </svg>
            <div style="position: absolute; text-align: center;">
                <div style="font-size: 1.65rem; font-weight: 800; color: #0f172a; line-height: 1;">{clamped_score:.0f}<span style="font-size: 0.95rem; font-weight: 600; color: #64748b;">%</span></div>
                <div style="font-size: 0.68rem; font-weight: 700; color: {color_hex}; text-transform: uppercase; margin-top: 2px;">{subtitle or 'Index'}</div>
            </div>
        </div>
    </div>
    """


# ==============================================================================
# 2. CACHED ENGINES INITIALIZATION
# ==============================================================================
@st.cache_resource
def get_db():
    return SourceReputationDB()

@st.cache_resource
def get_detector():
    return ManipulationDetector()

@st.cache_resource
def get_retriever():
    return NewsRetriever(db=get_db())

@st.cache_resource
def get_claim_extractor():
    return ClaimExtractor(use_spacy=True)

@st.cache_resource
def get_stance_classifier():
    return StanceClassifier()

@st.cache_resource
def get_score_aggregator():
    return ScoreAggregator()

db = get_db()
detector = get_detector()
retriever = get_retriever()
claim_extractor = get_claim_extractor()
stance_classifier = get_stance_classifier()
score_aggregator = get_score_aggregator()


# ==============================================================================
# 3. AUTHENTICATION & LOGIN PAGE
# ==============================================================================
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "active_claim" not in st.session_state:
    st.session_state.active_claim = "ISRO successfully landed Chandrayaan-3 on the lunar south pole"
if "claim_origin" not in st.session_state:
    st.session_state.claim_origin = "https://www.reuters.com"

def render_login():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("""
        <div style="text-align: center; margin-bottom: 2rem;">
            <h1 style="color: #102c57; font-size: 2.6rem; font-weight: 800; margin-bottom: 0;">🛡️ TruthLens</h1>
            <p style="color: #3b82f6; font-size: 1.1rem; font-weight: 600;">Real-Time AI News Credibility & Misinformation Verification System</p>
            <p style="color: #6b7280; font-size: 0.9rem;">Presidency University • School of AI & AC • Project Review Portal (PSAIAC_61)</p>
            <div style="margin-top: 8px;">
                <span style="background: #e0e7ff; color: #3730a3; padding: 4px 12px; border-radius: 9999px; font-weight: 700; font-size: 0.82rem;">🎯 65% Milestone: Stance NLI & Score Aggregator Active</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        with st.container(border=True):
            st.subheader("🔐 Project Review Evaluation Login")
            u_input = st.text_input("Username / Evaluator ID", value="Reviewer")
            p_input = st.text_input("Access Password", type="password", value="truthlens2026")
            
            c_btn1, c_btn2 = st.columns(2)
            with c_btn1:
                if st.button("Sign In", type="primary", use_container_width=True):
                    st.session_state.authenticated = True
                    st.session_state.username = u_input
                    st.rerun()
            with c_btn2:
                if st.button("⚡ 1-Click Demo Login", type="secondary", use_container_width=True):
                    st.session_state.authenticated = True
                    st.session_state.username = "Faculty Evaluator"
                    st.rerun()

            st.caption("💡 *Tip for evaluators: Click '1-Click Demo Login' for instant access to all evaluation modules.*")


if not st.session_state.authenticated:
    render_login()
    st.stop()


# ==============================================================================
# 4. SIDEBAR NAVIGATION & SYSTEM METRICS
# ==============================================================================
with st.sidebar:
    st.markdown("### 🛡️ **TruthLens Dashboard**")
    st.markdown(f"👤 Logged in as: **{st.session_state.username}**")
    if st.button("Logout", key="btn_logout"):
        st.session_state.authenticated = False
        st.rerun()

    st.markdown("---")
    menu = st.radio(
        "Select Portal Module:",
        [
            "🔍 Credibility Verification Suite",
            "📰 News Channel Directory (4,442)",
            "ℹ️ Project Methodology & Architecture"
        ],
        index=0
    )

    st.markdown("---")
    st.markdown("#### ⚙️ **Active Phase 4 Engines (65%)**")
    st.caption("• **SQLite DB:** 4,442 media outlets (<0.02ms) 🟢")
    st.caption("• **Lexicon Engine:** 109 manipulation markers 🟢")
    st.caption("• **Evidence Search:** NewsAPI & GNews Engine 🟢")
    st.caption("• **Claim Extractor:** spaCy & Entity Assertion 🟢")
    st.caption("• **Stance Engine:** Directional NLI (Phi) 🟢")
    st.caption("• **Unified Formula:** 0.70 S + 0.30 W - 0.25 M 🟢")
    st.caption("• **Target Review:** 65% Project Milestone Ready")

    st.markdown("---")
    st.caption("© 2026 TruthLens Team | B.Tech CSE (AI) | PSAIAC_61")


# ==============================================================================
# 5. MODULE 1: CREDIBILITY VERIFICATION SUITE
# ==============================================================================
if menu == "🔍 Credibility Verification Suite":
    st.markdown('<div class="main-title">🔍 News Credibility Verification Suite</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Multi-modal verification: Inspect news URLs, extract factual claims from articles, or execute full 65% stance-consensus verification.</div>', unsafe_allow_html=True)

    tab_url, tab_text, tab_claim = st.tabs([
        "🔗 1. Verify by News URL",
        "📄 2. Article Text & Claim Extractor",
        "🌐 3. Unified Stance & Credibility Dial (65% Milestone)"
    ])

    # ----------------------------------------------------
    # TAB 1: VERIFY BY NEWS URL
    # ----------------------------------------------------
    with tab_url:
        st.subheader("1. Web Domain & Article URL Inspector")
        st.write("Inspect any published news URL or domain against our indexed database of 4,442 media outlets.")

        # Quick test buttons
        st.markdown("**Quick Preset Outlets:**")
        c1, c2, c3, c4, c5 = st.columns(5)
        chosen_sample = None
        if c1.button("Reuters (100%)", use_container_width=True):
            chosen_sample = "https://www.reuters.com/world/india/space-mission-update/"
        if c2.button("BBC News (85%)", use_container_width=True):
            chosen_sample = "https://www.bbc.co.uk/news/technology-681923"
        if c3.button("The Onion (Satire)", use_container_width=True):
            chosen_sample = "https://www.theonion.com/scientists-discover-miracle-cure"
        if c4.button("Fox News (45%)", use_container_width=True):
            chosen_sample = "https://www.foxnews.com/politics/breaking-update"
        if c5.button("The Hindu (85%)", use_container_width=True):
            chosen_sample = "https://www.thehindu.com/news/national/economy-report"

        url_input = st.text_input(
            "Enter News Article URL or Domain:",
            value=chosen_sample or "https://edition.cnn.com/2026/08/15/business/markets-today/index.html",
            key="input_url_field"
        )

        if st.button("Inspect URL Reputation", type="primary", use_container_width=False):
            with st.spinner("Resolving canonical domain & querying database..."):
                t_start = time.perf_counter()
                rep = db.lookup(url_input)
                t_ms = (time.perf_counter() - t_start) * 1000.0

            st.success(f"Lookup resolved in **{t_ms:.3f} ms** via {rep.lookup_method.upper()} resolver!")

            # Metric Cards with Circular Gauge
            m1, m2, m3, m4 = st.columns([1.2, 1, 1, 1])
            with m1:
                g_col = "#10b981" if rep.percentage_score >= 80 else ("#f59e0b" if rep.percentage_score >= 40 else ("#8b5cf6" if rep.is_satire else "#ef4444"))
                g_sub = "Verified" if rep.percentage_score >= 80 else ("Mixed" if rep.percentage_score >= 40 else ("Satire" if rep.is_satire else "Low Trust"))
                st.markdown(render_circular_gauge(rep.percentage_score, "Credibility Score", color_hex=g_col, subtitle=g_sub), unsafe_allow_html=True)
            with m2:
                fact_color = "#065f46" if "HIGH" in rep.factual_reporting else ("#92400e" if "MIXED" in rep.factual_reporting else "#991b1b")
                st.markdown(f"""
                <div class="metric-card" style="height: 100%;">
                    <div class="metric-label">Factual Reporting</div>
                    <div class="metric-value" style="font-size: 1.35rem; color: {fact_color};">{rep.factual_reporting.upper()}</div>
                    <div style="font-size: 0.75rem; color: #64748b; margin-top: 6px;">Editorial standard evaluation</div>
                </div>
                """, unsafe_allow_html=True)
            with m3:
                st.markdown(f"""
                <div class="metric-card" style="height: 100%;">
                    <div class="metric-label">Political Bias</div>
                    <div class="metric-value" style="font-size: 1.35rem; color: #1e40af;">{rep.bias.upper()}</div>
                    <div style="font-size: 0.75rem; color: #64748b; margin-top: 6px;">Spectrum orientation</div>
                </div>
                """, unsafe_allow_html=True)
            with m4:
                st.markdown(f"""
                <div class="metric-card" style="height: 100%;">
                    <div class="metric-label">Corroboration Weight</div>
                    <div class="metric-value" style="font-size: 1.6rem; color: #0f172a;">{rep.weight_factor:.2f} <span style="font-size: 0.95rem; color: #64748b;">/ 1.0</span></div>
                    <div style="font-size: 0.75rem; color: #64748b; margin-top: 6px;">Equation factor (W_origin)</div>
                </div>
                """, unsafe_allow_html=True)

            # Details & Alerts
            if rep.is_satire:
                st.error("🚨 **SATIRE OUTLET DETECTED:** This source is flagged as 100% satirical humor. Its articles must not be treated as factual reporting.")
            elif rep.is_conspiracy:
                st.warning("⚠️ **CONSPIRACY / LOW FACTUALITY:** This source has a recorded history of promoting debunked conspiracy theories or pseudoscience.")
            else:
                st.info("✅ **VERIFIED PRESS OUTLET:** This source is cataloged in the global Media Bias / Fact Check index.")

            with st.expander("Detailed Domain Resolution Metadata", expanded=True):
                meta_df = pd.DataFrame([
                    {"Parameter": "Input Query", "Details": url_input},
                    {"Parameter": "Resolved Canonical Domain", "Details": rep.domain},
                    {"Parameter": "Source Name", "Details": rep.source_name},
                    {"Parameter": "Country of Origin", "Details": rep.country.upper()},
                    {"Parameter": "Rating Tier", "Details": rep.credibility_rating},
                    {"Parameter": "Resolution Method", "Details": rep.lookup_method}
                ])
                st.table(meta_df)

    # ----------------------------------------------------
    # TAB 2: VERIFY BY ARTICLE TEXT & CLAIM EXTRACTOR
    # ----------------------------------------------------
    with tab_text:
        st.subheader("2. Article Text, Manipulation Scanner & Automated Claim Extractor")
        st.write("Scan news articles for sensationalism and clickbait markers, or automatically isolate verifiable factual claims using NLP entity parsing.")

        if "tab2_text_val" not in st.session_state:
            st.session_state.tab2_text_val = "ISRO successfully launched the Chandrayaan-3 spacecraft from the Satish Dhawan Space Centre on July 14, 2023. The mission completed a soft landing on the lunar South Pole on August 23, 2023."

        b1, b2 = st.columns(2)
        if b1.button("Load Viral Clickbait Sample", use_container_width=True):
            st.session_state.tab2_text_val = "SHOCKING BOMBSHELL: Big Pharma is HIDING this one simple secret miracle cure that doctors DON'T want you to know about!!! You won't believe what happens next, act now before it's too late!"
            st.rerun()
        if b2.button("Load Factual News Article Sample", use_container_width=True):
            st.session_state.tab2_text_val = "ISRO successfully launched the Chandrayaan-3 spacecraft from the Satish Dhawan Space Centre on July 14, 2023. The mission completed a soft landing on the lunar South Pole on August 23, 2023. Prime Minister Modi congratulated the scientists in Bengaluru for this historic achievement. In my opinion, space exploration inspires the entire next generation."
            st.rerun()

        text_input = st.text_area(
            "Enter Article Headline or News Paragraph to Analyze:",
            value=st.session_state.tab2_text_val,
            height=130
        )
        st.session_state.tab2_text_val = text_input

        col_act1, col_act2 = st.columns(2)
        with col_act1:
            btn_scan_manip = st.button("🔎 Scan Linguistic Manipulation", type="primary", use_container_width=True)
        with col_act2:
            btn_extract_claims = st.button("⚡ Extract Factual Claims (65% Milestone)", type="secondary", use_container_width=True)

        if btn_scan_manip:
            res = detector.analyze(text_input)

            st.write("---")
            if res.overall_manipulation_score == 0 and not res.flagged_phrases:
                st.success("✅ **Clean Journalistic Phrasing:** No clickbait, sensationalism, or emotional panic triggers detected in this text.")
            
            # Manipulation Metric Cards with Circular Gauge
            k1, k2, k3 = st.columns([1.2, 1, 1])
            with k1:
                r_col = "#ef4444" if res.overall_manipulation_score > 40 else ("#f59e0b" if res.overall_manipulation_score > 15 else "#10b981")
                r_sub = "High Risk" if res.overall_manipulation_score > 40 else ("Moderate" if res.overall_manipulation_score > 15 else "Low Risk")
                st.markdown(render_circular_gauge(res.overall_manipulation_score, "Manipulation Risk", color_hex=r_col, subtitle=r_sub), unsafe_allow_html=True)
            with k2:
                st.markdown(f"""
                <div class="metric-card" style="height: 100%;">
                    <div class="metric-label">Risk Category</div>
                    <div class="metric-value" style="font-size: 1.35rem; color: {r_col};">{res.risk_level.upper()}</div>
                    <div style="font-size: 0.75rem; color: #64748b; margin-top: 6px;">Evaluated against 109 triggers</div>
                </div>
                """, unsafe_allow_html=True)
            with k3:
                st.markdown(f"""
                <div class="metric-card" style="height: 100%;">
                    <div class="metric-label">Triggers Caught</div>
                    <div class="metric-value" style="font-size: 1.6rem; color: #0f172a;">{len(res.flagged_phrases)} <span style="font-size: 1rem; color: #64748b;">triggers</span></div>
                    <div style="font-size: 0.75rem; color: #64748b; margin-top: 6px;">Sensational, panic & conspiracy flags</div>
                </div>
                """, unsafe_allow_html=True)

            if res.flagged_phrases:
                # Highlighting trigger words in the text
                st.markdown("#### 🔎 **Highlighted Manipulation Markers in Text:**")
                highlighted = text_input
                seen_terms = set()
                for fp in res.flagged_phrases:
                    term = fp.get("term", "")
                    cat = fp.get("category", "")
                    if term and term.lower() not in seen_terms:
                        seen_terms.add(term.lower())
                        if "sensational" in cat:
                            badge = f'<span style="background-color: #fef08a; padding: 2px 6px; border-radius: 4px; font-weight: bold; color: #854d0e;">{term} [Sensational]</span>'
                        elif "fear" in cat or "urgency" in cat:
                            badge = f'<span style="background-color: #fed7aa; padding: 2px 6px; border-radius: 4px; font-weight: bold; color: #9a3412;">{term} [Panic]</span>'
                        elif "conspiracy" in cat:
                            badge = f'<span style="background-color: #fecaca; padding: 2px 6px; border-radius: 4px; font-weight: bold; color: #991b1b;">{term} [Conspiracy]</span>'
                        else:
                            badge = f'<span style="background-color: #e0e7ff; padding: 2px 6px; border-radius: 4px; font-weight: bold; color: #3730a3;">{term} [Trigger]</span>'
                        highlighted = re.sub(re.escape(term), badge, highlighted, flags=re.IGNORECASE)
                
                st.markdown(f'<div style="background-color: #f3f4f6; padding: 1.2rem; border-radius: 8px; font-size: 1.1rem; line-height: 1.8;">{highlighted}</div>', unsafe_allow_html=True)

            if res.stylistic_flags:
                st.markdown("**Identified Stylistic Red Flags:**")
                for f in res.stylistic_flags:
                    st.warning(f"• {f}")

        if btn_extract_claims:
            with st.spinner("Extracting verifiable claims via spaCy NER and factual assertion heuristics..."):
                extracted = claim_extractor.extract_claims(text_input, max_claims=4)

            st.write("---")
            if not extracted:
                st.info("ℹ️ No testable empirical claims found. Ensure the text contains declarative statements.")
            else:
                st.success(f"🎯 Extracted **{len(extracted)} testable factual claim(s)** ranked by empirical salience:")
                for c in extracted:
                    with st.container(border=True):
                        ec1, ec2 = st.columns([3.5, 1])
                        with ec1:
                            if c.is_primary:
                                st.markdown('<span class="badge-verified">⭐ PRIMARY FACTUAL CLAIM</span>', unsafe_allow_html=True)
                            st.markdown(f"#### **Claim #{c.claim_id}:** \"{c.text}\"")
                            st.caption(f"🏷️ **Detected Entities:** {', '.join(c.entities) if c.entities else 'Standard declarative context'} | 🔍 **Heuristics:** {c.reasoning}")
                        with ec2:
                            st.metric("Salience Score", f"{c.salience_score * 100:.0f}%")
                            if st.button(f"Cross-Verify #{c.claim_id} ➔", key=f"btn_send_claim_{c.claim_id}", use_container_width=True):
                                st.session_state.active_claim = c.text
                                st.session_state.claim_origin = "https://www.reuters.com"
                                st.toast(f"Claim #{c.claim_id} loaded into Tab 3! Switch to Tab 3 to execute verification.")

    # ----------------------------------------------------
    # TAB 3: UNIFIED STANCE CONSENSUS & CREDIBILITY DIAL (65% MILESTONE)
    # ----------------------------------------------------
    with tab_claim:
        st.subheader("3. Unified Evidence Cross-Search, NLI Stance & Final Credibility Dial (65% Milestone)")
        st.write("Cross-examine any claim against live global news sources, compute directional Natural Language Inference (NLI) stances, and calculate the unified credibility score.")

        if "active_claim" not in st.session_state:
            st.session_state.active_claim = "ISRO successfully completed a soft landing of Chandrayaan-3 on the lunar south pole"
        if "claim_origin" not in st.session_state:
            st.session_state.claim_origin = "https://www.reuters.com"

        # Preset test cases for evaluation demo
        st.markdown("**Quick Preset Claims for Review Demo:**")
        qc1, qc2, qc3, qc4 = st.columns(4)
        if qc1.button("🟢 Chandrayaan-3 Landing (Verified)", use_container_width=True):
            st.session_state.active_claim = "ISRO successfully completed a soft landing of Chandrayaan-3 on the lunar south pole"
            st.session_state.claim_origin = "https://www.reuters.com"
            st.rerun()
        if qc2.button("🔴 Bleach Viral Cure (Debunked)", use_container_width=True):
            st.session_state.active_claim = "Drinking bleach is a proven miracle cure for viral infections"
            st.session_state.claim_origin = "https://viralnews-rumors.net"
            st.rerun()
        if qc3.button("🎭 The Onion Sleep Pill (Satire)", use_container_width=True):
            st.session_state.active_claim = "Scientists invent miracle pill that eliminates the need for human sleep"
            st.session_state.claim_origin = "https://www.theonion.com"
            st.rerun()
        if qc4.button("⚠️ Miracle Cancer Cure (Clickbait)", use_container_width=True):
            st.session_state.active_claim = "SHOCKING BOMBSHELL: Big Pharma is hiding a simple secret miracle cure from the public"
            st.session_state.claim_origin = "https://naturalcuretruth.com"
            st.rerun()

        f_col1, f_col2 = st.columns([2.5, 1.2])
        with f_col1:
            claim_input = st.text_input(
                "Enter Factual Claim to Cross-Examine:",
                value=st.session_state.active_claim
            )
            st.session_state.active_claim = claim_input
        with f_col2:
            origin_url_input = st.text_input(
                "Originating Publisher URL / Domain:",
                value=st.session_state.claim_origin
            )
            st.session_state.claim_origin = origin_url_input

        num_articles = st.slider("Number of independent news sources to retrieve for evidence pool:", 3, 8, 5)

        if st.button("🚀 Execute Full 65% Cross-Verification Pipeline", type="primary", use_container_width=True):
            with st.spinner("Step 1/4: Retrieving independent global news evidence articles..."):
                t_pipe_start = time.perf_counter()
                articles = retriever.search_evidence(claim_input, max_results=num_articles)

            with st.spinner("Step 2/4: Running Semantic Stance Classification & NLI Inference..."):
                stances = []
                for art in articles:
                    evidence_text = f"{art.title}. {art.snippet}"
                    res_st = stance_classifier.classify_pair(claim_input, evidence_text)
                    stances.append(res_st)

            with st.spinner("Step 3/4: Analyzing Linguistic Manipulation and Origin Source Reputation..."):
                manip_rep = detector.analyze(headline=claim_input, body="")
                origin_rep = db.lookup(origin_url_input)

            with st.spinner("Step 4/4: Computing Unified Mathematical Credibility Formula..."):
                assessment = score_aggregator.aggregate(
                    origin_score=origin_rep.percentage_score,
                    articles=articles,
                    stances=stances,
                    manipulation_report=manip_rep,
                    is_satire=origin_rep.is_satire,
                    is_conspiracy=origin_rep.is_conspiracy
                )
                t_total = time.perf_counter() - t_pipe_start

            st.write("---")

            # Executive Verdict Banner
            if assessment.verdict == VerdictTier.VERIFIED_CREDIBLE:
                st.success(f"### {assessment.verdict_badge} — Credibility Score: **{assessment.final_score:.1f}%**\n{assessment.summary_verdict}")
            elif assessment.verdict == VerdictTier.LIKELY_CREDIBLE:
                st.info(f"### {assessment.verdict_badge} — Credibility Score: **{assessment.final_score:.1f}%**\n{assessment.summary_verdict}")
            elif assessment.verdict in [VerdictTier.LOW_CREDIBILITY, VerdictTier.CONSPIRACY_PSEUDOSCIENCE]:
                st.error(f"### {assessment.verdict_badge} — Credibility Score: **{assessment.final_score:.1f}%**\n{assessment.summary_verdict}")
            elif assessment.verdict == VerdictTier.SATIRE_PARODY:
                st.warning(f"### {assessment.verdict_badge} — Credibility Score: **{assessment.final_score:.1f}%**\n{assessment.summary_verdict}")
            else:
                st.warning(f"### {assessment.verdict_badge} — Credibility Score: **{assessment.final_score:.1f}%**\n{assessment.summary_verdict}")

            # 4-Pillar Metric Gauges
            g1, g2, g3, g4 = st.columns([1.2, 1, 1, 1])
            with g1:
                fin_col = "#10b981" if assessment.final_score >= 75 else ("#f59e0b" if assessment.final_score >= 45 else ("#8b5cf6" if assessment.verdict == VerdictTier.SATIRE_PARODY else "#ef4444"))
                st.markdown(render_circular_gauge(assessment.final_score, "Final Credibility", color_hex=fin_col, subtitle=assessment.verdict.name[:10]), unsafe_allow_html=True)
            with g2:
                ev_col = "#10b981" if assessment.evidence_score >= 70 else ("#f59e0b" if assessment.evidence_score >= 40 else "#ef4444")
                st.markdown(f"""
                <div class="metric-card" style="height: 100%;">
                    <div class="metric-label">1. Evidence Consensus (S_ev)</div>
                    <div class="metric-value" style="color: {ev_col};">{assessment.evidence_score:.1f}%</div>
                    <div style="font-size: 0.75rem; color: #64748b; margin-top: 6px;">
                        Weight: <strong>70%</strong> | Phi: <strong>{assessment.weighted_consensus_phi:+.2f}</strong><br>
                        🟢 {assessment.supporting_sources_count} Sup | 🔴 {assessment.refuting_sources_count} Ref | ⚪ {assessment.neutral_sources_count} Neu
                    </div>
                </div>
                """, unsafe_allow_html=True)
            with g3:
                st.markdown(f"""
                <div class="metric-card" style="height: 100%;">
                    <div class="metric-label">2. Origin Authority (W_org)</div>
                    <div class="metric-value" style="color: #1e40af;">{assessment.origin_score:.1f}%</div>
                    <div style="font-size: 0.75rem; color: #64748b; margin-top: 6px;">
                        Weight: <strong>30%</strong> | Domain: <strong>{origin_rep.domain}</strong><br>
                        MBFC Rating: <strong>{origin_rep.factual_reporting.upper()}</strong>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            with g4:
                m_color = "#ef4444" if assessment.manipulation_index > 40 else ("#f59e0b" if assessment.manipulation_index > 15 else "#10b981")
                st.markdown(f"""
                <div class="metric-card" style="height: 100%;">
                    <div class="metric-label">3. Manipulation Penalty (M)</div>
                    <div class="metric-value" style="color: {m_color};">-{assessment.manipulation_penalty:.1f}</div>
                    <div style="font-size: 0.75rem; color: #64748b; margin-top: 6px;">
                        Raw Index: <strong>{assessment.manipulation_index:.1f}/100</strong><br>
                        Equation penalty: <strong>-0.25 × M_index</strong>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            # Mathematical Formula Callout Box
            st.markdown(f"""
            <div class="math-callout">
                <div style="font-size: 0.82rem; font-weight: 700; color: #93c5fd; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 0.3rem;">
                    📐 Verified Mathematical Audit Formula (PSAIAC_61)
                </div>
                <div style="font-family: 'JetBrains Mono', monospace; font-size: 1.05rem; color: #ffffff; line-height: 1.6;">
                    {assessment.math_formula_explanation}
                </div>
                <div style="font-size: 0.8rem; color: #94a3b8; margin-top: 0.4rem;">
                    Pipeline verified across {len(articles)} independent media outlets in <strong>{t_total:.2f} seconds</strong> (<0.05s NLI inference).
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Retrieved Evidence Pool with Stance Badges
            st.markdown("#### 📰 **Corroborating Evidence Articles with Semantic Stance Badges:**")
            for idx, (art, st_res) in enumerate(zip(articles, stances), 1):
                # Stance badge rendering
                if st_res.stance == StanceType.SUPPORTS:
                    stance_badge_html = f'<span class="badge-stance-supports">🟢 SUPPORTS (+1.0) • {st_res.confidence * 100:.0f}% Conf</span>'
                    card_border = "#10b981"
                elif st_res.stance == StanceType.REFUTES:
                    stance_badge_html = f'<span class="badge-stance-refutes">🔴 REFUTES (-1.0) • {st_res.confidence * 100:.0f}% Conf</span>'
                    card_border = "#ef4444"
                else:
                    stance_badge_html = f'<span class="badge-stance-neutral">⚪ NEUTRAL (0.0) • {st_res.confidence * 100:.0f}% Conf</span>'
                    card_border = "#94a3b8"

                st.markdown(f"""
                <div class="evidence-box" style="border-left-color: {card_border};">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem; flex-wrap: wrap; gap: 8px;">
                        <div>
                            <span class="mono-pill">Source #{idx}</span>
                            <strong style="font-size: 1.05rem; color: #0f172a; margin-left: 6px;">{art.source_name}</strong>
                            <span style="color: #64748b; font-size: 0.85rem; margin-left: 4px;">({art.domain})</span>
                        </div>
                        <div style="display: flex; gap: 8px; align-items: center;">
                            {stance_badge_html}
                            <span class="badge-verified">Trust: {art.percentage_score:.0f}%</span>
                        </div>
                    </div>
                    <h4 style="margin: 0.3rem 0; font-size: 1.15rem; font-weight: 700;">
                        <a href="{art.url}" target="_blank" style="text-decoration: none; color: #1e40af;">{art.title}</a>
                    </h4>
                    <p style="color: #334155; font-size: 0.95rem; margin: 0.4rem 0 0.6rem 0; line-height: 1.5;">{art.snippet}</p>
                    <div style="background: #f8fafc; border-radius: 6px; padding: 6px 10px; font-size: 0.82rem; color: #475569; margin-bottom: 8px;">
                        💡 <strong>NLI Stance Analysis:</strong> {st_res.explanation}
                    </div>
                    <div style="display: flex; gap: 12px; font-size: 0.8rem; color: #64748b; flex-wrap: wrap; border-top: 1px solid #f1f5f9; padding-top: 6px;">
                        <span>📅 Published: <strong>{art.published_at}</strong></span>
                        <span>⚖️ Political Bias: <strong>{art.bias}</strong></span>
                        <span>📊 Consensus Weight (W_rep): <strong>{art.weight_factor:.2f}</strong></span>
                        <span>🎯 Overlap: <strong>{st_res.overlap_score * 100:.0f}%</strong></span>
                    </div>
                </div>
                """, unsafe_allow_html=True)


# ==============================================================================
# 6. MODULE 2: NEWS CHANNEL DIRECTORY (4,442 OUTLETS)
# ==============================================================================
elif menu == "📰 News Channel Directory (4,442)":
    st.markdown('<div class="main-title">📰 Global News Media Knowledge Base</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Explore 4,442 indexed news outlets cataloged with credibility, bias, and factuality scores from Media Bias/Fact Check (MBFC).</div>', unsafe_allow_html=True)

    stats = db.get_statistics()
    s1, s2, s3, s4 = st.columns(4)
    with s1:
        st.metric("Total Indexed Media Outlets", f"{stats['total_sources']:,}")
    with s2:
        st.metric("Average Factuality Score", f"{stats['average_credibility_score']*100:.1f}%")
    with s3:
        st.metric("Satire Publishers Flagged", stats['satire_sources'])
    with s4:
        st.metric("Conspiracy Outlets Flagged", stats['conspiracy_sources'])

    st.write("---")
    sc1, sc2, sc3 = st.columns([2, 1, 1])
    with sc1:
        search_query = st.text_input("🔎 Search by Outlet Name or Domain (e.g., 'Reuters', 'BBC', 'Hindu', 'Onion'):", "")
    with sc2:
        fact_filter = st.selectbox("Filter by Factuality:", ["ALL", "VERY HIGH", "HIGH", "MIXED", "LOW", "SATIRE", "CONSPIRACY"])
    with sc3:
        bias_filter = st.selectbox("Filter by Political Bias:", ["ALL", "LEFT", "LEFT-CENTER", "LEAST BIASED", "RIGHT-CENTER", "RIGHT"])

    # Query SQLite database for matching records
    with st.spinner("Filtering database..."):
        query_sql = "SELECT domain, source_name, credibility_score, factual_reporting, bias, country, is_satire, is_conspiracy FROM sources WHERE 1=1"
        params = []
        if search_query.strip():
            query_sql += " AND (domain LIKE ? OR source_name LIKE ?)"
            params.extend([f"%{search_query.strip()}%", f"%{search_query.strip()}%"])
        if fact_filter != "ALL":
            if fact_filter == "SATIRE":
                query_sql += " AND is_satire = 1"
            elif fact_filter == "CONSPIRACY":
                query_sql += " AND is_conspiracy = 1"
            else:
                query_sql += " AND UPPER(factual_reporting) = ?"
                params.append(fact_filter)
        if bias_filter != "ALL":
            query_sql += " AND UPPER(bias) = ?"
            params.append(bias_filter)

        query_sql += " ORDER BY credibility_score DESC LIMIT 200"

        cur = db.conn.cursor()
        cur.execute(query_sql, params)
        rows = cur.fetchall()

    if not rows:
        st.info("No media outlets matched the selected criteria.")
    else:
        st.write(f"Showing **{len(rows)} media outlets** matching your criteria:")
        display_data = []
        for r in rows:
            display_data.append({
                "Domain": r[0],
                "Source Name": r[1],
                "Trust Score": f"{r[2]*100:.0f}%",
                "Factuality": r[3].upper(),
                "Political Bias": r[4].upper(),
                "Country": r[5].upper() if r[5] else "GLOBAL",
                "Category": "SATIRE" if r[6] else ("CONSPIRACY" if r[7] else "STANDARD NEWS")
            })
        st.dataframe(pd.DataFrame(display_data), use_container_width=True, height=450)


# ==============================================================================
# 7. MODULE 3: PROJECT METHODOLOGY & ARCHITECTURE
# ==============================================================================
elif menu == "ℹ️ Project Methodology & Architecture":
    st.markdown('<div class="main-title">ℹ️ TruthLens Project Architecture</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">System design, mathematical scoring model, and team roles for PSAIAC_61 (65% Milestone).</div>', unsafe_allow_html=True)

    a1, a2 = st.columns(2)
    with a1:
        st.subheader("🎯 Problem Statement (PSAIAC_61)")
        st.write("""
        • **6x Misinformation Speed:** Peer-reviewed research (*Science*, Vosoughi et al., 2018) proves false news spreads 6 times faster than verified journalism due to emotional shock value.
        • **Failure of Traditional Classifiers:** Basic NLP text classifiers overfit to topic keywords and fail when falsehoods are written in formal journalistic language.
        • **The TruthLens Solution:** Instead of guessing if text looks fake, TruthLens cross-examines factual claims against the **consensus of independent reputable news outlets** using Natural Language Inference (NLI).
        """)

        st.subheader("🧮 Mathematical Scoring Model (65% Implementation)")
        st.latex(r"C_{\text{final}} = 0.70 \times S_{\text{evidence}} + 0.30 \times W_{\text{origin}} - (0.25 \times M_{\text{index}})")
        st.write("""
        Where:
        • **$S_{\text{evidence}}$:** Multi-source weighted consensus score derived from NLI stance ($\Phi \in \{-1.0, 0.0, +1.0\}$) and publisher authority weights ($W_{\text{rep}}$) mapped to $[0, 100]$.
        • **$W_{\text{origin}}$:** Media Bias/Fact Check (MBFC) reputation weight ($0.0 \le W_{\text{rep}} \le 1.0$) of the publishing domain mapped to $[0, 100]$.
        • **$M_{\text{index}}$:** Lexical and structural manipulation penalty ($0 \text{ to } 100$).
        • **$C_{\text{final}}$:** Clamped between $[0.0, 100.0]$ with categorical overrides for satire ($C = 0$) and conspiracy ($C \le 15$).
        """)

    with a2:
        st.subheader("👥 Team Member Roles & Contributions (Review 4 / 65%)")
        with st.container(border=True):
            st.markdown("**1. Shubham Pandey (Team Leader — 20231CAI0046):**")
            st.caption("Engineered Unified Mathematical Score Aggregator (C_final), SQLite B-Tree domain database (4,442 outlets, <0.02ms), system architecture, and 27-suite pytest pipeline.")
            
            st.markdown("**2. Ikram Inayathulla Khan (20231CAI0006):**")
            st.caption("Engineered the Automated Factual Claim Extraction module (spaCy NER, numerical parsing, assertion verbs) and the 109-trigger linguistic manipulation detector.")
            
            st.markdown("**3. Karanam Radha Pranathi (20231CAI0003):**")
            st.caption("Engineered the Semantic Stance & NLI Classifier (SUPPORTS/REFUTES/NEUTRAL), confidence calibration, and NewsAPI live corroboration retrieval.")
            
            st.markdown("**4. Bhagyesh (20231CAI0068):**")
            st.caption("Engineered the interactive Streamlit web UI, Stance Badges, Executive Score Dial, evaluator authentication, and responsive visual layout.")

    st.markdown("---")
    st.subheader("🗺️ 5-Phase Project Roadmap")
    roadmap_df = pd.DataFrame([
        {"Phase": "Phase 1 (Review 1)", "Scope": "Literature Survey (12 IEEE Papers), Problem Definition & Architecture", "Status": "Completed (100%)"},
        {"Phase": "Phase 2 (Review 2)", "Scope": "MBFC Knowledge Base (4,442 Outlets), Manipulation Engine, Benchmark Tests", "Status": "Completed (100%)"},
        {"Phase": "Phase 3 (Review 3 - 50%)", "Scope": "Interactive Web Dashboard, NewsAPI Live Retrieval, Multi-Source Pool", "Status": "Completed (100%)"},
        {"Phase": "Phase 4 (Review 4 - 65%)", "Scope": "Automated Claim Extractor, NLI Stance Classifier, Unified Score Dial", "Status": "Completed (65% Milestone Verified)"},
        {"Phase": "Phase 5 (Final Review)", "Scope": "Production REST API, Multi-lingual NLP, Final Comprehensive Report & Demo", "Status": "Scheduled for Review 5"}
    ])
    st.table(roadmap_df)
