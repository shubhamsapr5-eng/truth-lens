"""
TruthLens: AI-Powered Real-Time News Credibility Verification Engine
Web Application Dashboard (50% Milestone - Phase 3 Deliverable)

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

load_dotenv()

# ==============================================================================
# 1. PAGE CONFIGURATION & STYLING
# ==============================================================================
st.set_page_config(
    page_title="TruthLens - AI News Credibility Scorer",
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

db = get_db()
detector = get_detector()
retriever = get_retriever()


# ==============================================================================
# 3. AUTHENTICATION & LOGIN PAGE
# ==============================================================================
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "username" not in st.session_state:
    st.session_state.username = ""

def render_login():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("""
        <div style="text-align: center; margin-bottom: 2rem;">
            <h1 style="color: #102c57; font-size: 2.6rem; font-weight: 800; margin-bottom: 0;">🛡️ TruthLens</h1>
            <p style="color: #3b82f6; font-size: 1.1rem; font-weight: 600;">Real-Time AI News Credibility & Misinformation Verification System</p>
            <p style="color: #6b7280; font-size: 0.9rem;">Presidency University • School of AI & AC • Project Review Portal (PSAIAC_61)</p>
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
    st.markdown("#### ⚙️ **Active Phase 3 Engines**")
    st.caption("• **SQLite DB:** 4,442 media outlets (<0.02ms)")
    st.caption("• **Lexicon Engine:** 109 manipulation markers")
    st.caption("• **Evidence Search:** NewsAPI & GNews Engine 🟢")
    st.caption("• **Target Review:** 50% Project Milestone")

    st.markdown("---")
    st.caption("© 2026 TruthLens Team | B.Tech CSE (AI) | PSAIAC_61")


# ==============================================================================
# 5. MODULE 1: CREDIBILITY VERIFICATION SUITE
# ==============================================================================
if menu == "🔍 Credibility Verification Suite":
    st.markdown('<div class="main-title">🔍 News Credibility Verification Suite</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Multi-modal verification engine: Inspect news URLs, analyze article body text, or cross-check live claims.</div>', unsafe_allow_html=True)

    tab_url, tab_text, tab_claim = st.tabs([
        "🔗 Verify by News URL",
        "📄 Verify by Article Text",
        "🌐 Live Claim Cross-Search (NewsAPI)"
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
            value=chosen_sample or "https://edition.cnn.com/2026/08/15/business/markets-today/index.html"
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
    # TAB 2: VERIFY BY ARTICLE TEXT
    # ----------------------------------------------------
    with tab_text:
        st.subheader("2. Article Text & Clickbait Manipulation Scanner")
        st.write("Scan news headlines or article text for sensationalism, emotional panic triggers, and manipulative formatting.")

        b1, b2 = st.columns(2)
        sample_text = None
        if b1.button("Load Viral Clickbait Sample", use_container_width=True):
            sample_text = "SHOCKING BOMBSHELL: Big Pharma is HIDING this one simple secret miracle cure that doctors DON'T want you to know about!!! You won't believe what happens next, act now before it's too late!"
        if b2.button("Load Serious News Sample", use_container_width=True):
            sample_text = "The Federal Reserve concluded its quarterly policy meeting on Wednesday, maintaining the federal funds benchmark interest rate at 5.25%. Committee officials cited stable employment data and moderate inflation indices."

        text_input = st.text_area(
            "Enter Article Headline or Paragraph to Analyze:",
            value=sample_text or "BREAKING NEWS: SHOCKING discovery reveals what corrupt politicians are secretly hiding from the public!!!",
            height=130
        )

        if st.button("Scan Text for Manipulation", type="primary"):
            res = detector.analyze(text_input)

            st.write("---")
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

    # ----------------------------------------------------
    # TAB 3: LIVE CLAIM & NEWSAPI CROSS-SEARCH (PHASE 3 CORE)
    # ----------------------------------------------------
    with tab_claim:
        st.subheader("3. Live Claim Cross-Search & Corroboration Pool (Phase 3)")
        st.write("Query live global news channels via NewsAPI to cross-examine factual claims across independent reporting outlets.")

        c_claim1, c_claim2, c_claim3 = st.columns(3)
        sample_q = None
        if c_claim1.button("Test: Artificial Intelligence Safety", use_container_width=True):
            sample_q = "Artificial intelligence safety regulations"
        if c_claim2.button("Test: Chandrayaan Moon Landing", use_container_width=True):
            sample_q = "Chandrayaan moon landing mission"
        if c_claim3.button("Test: Global Climate Conference", use_container_width=True):
            sample_q = "Global climate summit agreement"

        claim_input = st.text_input(
            "Enter Factual Claim / Topic to Cross-Check:",
            value=sample_q or "Artificial intelligence safety regulations"
        )

        num_articles = st.slider("Number of independent news sources to retrieve:", 3, 10, 5)

        if st.button("Fetch Live Corroboration Pool", type="primary"):
            with st.spinner(f"Querying global news APIs and cross-referencing MBFC database for: '{claim_input}'..."):
                t_start = time.perf_counter()
                articles = retriever.search_evidence(claim_input, max_results=num_articles)
                t_ret = (time.perf_counter() - t_start)

            if not articles:
                st.warning("No related articles found. Please try different keywords.")
            else:
                st.success(f"Retrieved **{len(articles)} independent reporting sources** in **{t_ret:.2f}s**!")

                # Calculate average pool trust
                avg_pool_trust = sum(a.percentage_score for a in articles) / len(articles)
                
                # Consensus Pool Metric Cards with Circular Gauge
                p1, p2, p3 = st.columns([1.2, 1, 1])
                with p1:
                    pool_col = "#10b981" if avg_pool_trust >= 75 else ("#f59e0b" if avg_pool_trust >= 50 else "#ef4444")
                    pool_sub = "Consensus" if avg_pool_trust >= 75 else ("Contested" if avg_pool_trust >= 50 else "Low Trust")
                    st.markdown(render_circular_gauge(avg_pool_trust, "Consensus Pool Trust", color_hex=pool_col, subtitle=pool_sub), unsafe_allow_html=True)
                with p2:
                    st.markdown(f"""
                    <div class="metric-card" style="height: 100%;">
                        <div class="metric-label">Reporting Outlets</div>
                        <div class="metric-value" style="font-size: 1.6rem; color: #1e40af;">{len(articles)} <span style="font-size: 1rem; color: #64748b;">sources</span></div>
                        <div style="font-size: 0.75rem; color: #64748b; margin-top: 6px;">Independent publishers retrieved</div>
                    </div>
                    """, unsafe_allow_html=True)
                with p3:
                    high_trust_cnt = sum(1 for a in articles if a.credibility_score >= 0.7)
                    st.markdown(f"""
                    <div class="metric-card" style="height: 100%;">
                        <div class="metric-label">Tier-1 Authoritative</div>
                        <div class="metric-value" style="font-size: 1.6rem; color: #065f46;">{high_trust_cnt} / {len(articles)}</div>
                        <div style="font-size: 0.75rem; color: #64748b; margin-top: 6px;">High / Very High MBFC rating</div>
                    </div>
                    """, unsafe_allow_html=True)

                st.markdown("#### 📰 **Retrieved Cross-Examination Articles (Evidence Pool):**")
                for idx, art in enumerate(articles, 1):
                    badge_style = "badge-verified" if art.credibility_score >= 0.7 else ("badge-mixed" if art.credibility_score >= 0.4 else "badge-danger")
                    card_tier = "high" if art.credibility_score >= 0.7 else ("mixed" if art.credibility_score >= 0.4 else "low")
                    st.markdown(f"""
                    <div class="evidence-box {card_tier}">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                            <div>
                                <span class="mono-pill">#{idx}</span>
                                <strong style="font-size: 1.05rem; color: #0f172a; margin-left: 6px;">{art.source_name}</strong>
                                <span style="color: #64748b; font-size: 0.85rem; margin-left: 4px;">({art.domain})</span>
                            </div>
                            <span class="{badge_style}">Trust: {art.percentage_score:.0f}% • {art.factuality}</span>
                        </div>
                        <h4 style="margin: 0.3rem 0; font-size: 1.15rem; font-weight: 700;">
                            <a href="{art.url}" target="_blank" style="text-decoration: none; color: #1e40af;">{art.title}</a>
                        </h4>
                        <p style="color: #334155; font-size: 0.95rem; margin: 0.4rem 0 0.6rem 0; line-height: 1.5;">{art.snippet}</p>
                        <div style="display: flex; gap: 12px; font-size: 0.8rem; color: #64748b; flex-wrap: wrap; border-top: 1px solid #f1f5f9; padding-top: 6px;">
                            <span>📅 Published: <strong>{art.published_at}</strong></span>
                            <span>⚖️ Bias: <strong>{art.bias}</strong></span>
                            <span>📊 Weight (W_rep): <strong>{art.weight_factor:.2f}</strong></span>
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
    st.markdown('<div class="sub-title">System design, mathematical scoring model, and team roles for PSAIAC_61.</div>', unsafe_allow_html=True)

    a1, a2 = st.columns(2)
    with a1:
        st.subheader("🎯 Problem Statement (PSAIAC_61)")
        st.write("""
        • **6x Misinformation Speed:** Peer-reviewed research (*Science*, Vosoughi et al., 2018) proves false news spreads 6 times faster than verified journalism due to emotional shock value.
        • **Failure of Traditional Classifiers:** Basic NLP text classifiers overfit to topic keywords and fail when falsehoods are written in formal journalistic language.
        • **The TruthLens Solution:** Instead of guessing if text looks fake, TruthLens cross-examines factual claims against the **consensus of independent reputable news outlets**.
        """)

        st.subheader("🧮 Mathematical Scoring Model")
        st.latex(r"C_{\text{final}} = 0.70 \times S_{\text{evidence}} + 0.30 \times W_{\text{origin}} - (0.25 \times M_{\text{index}})")
        st.write("""
        Where:
        • **$S_{\text{evidence}}$:** Weighted consensus agreement of retrieved sources via RoBERTa Natural Language Inference ($\Phi_{\text{NLI}}$).
        • **$W_{\text{origin}}$:** Media Bias/Fact Check (MBFC) reputation weight ($0.0 \le W_{\text{rep}} \le 1.0$) of the publishing domain.
        • **$M_{\text{index}}$:** Lexical and structural manipulation penalty ($0 \text{ to } 100$).
        """)

    with a2:
        st.subheader("👥 Team Member Roles & Responsibilities")
        with st.container(border=True):
            st.markdown("**1. Shubham Pandey (Team Leader — 20231CAI0046):**")
            st.caption("Engineered the Multi-Tier Canonical Domain Resolution Engine (<0.02ms), MBFC SQLite knowledge base (4,442 outlets), core schemas, and system architecture.")
            
            st.markdown("**2. Ikram Inayathulla Khan (20231CAI0006):**")
            st.caption("Engineered the 109-trigger lexical manipulation detection engine, stylistic pattern matching, and emotional panic indicators.")
            
            st.markdown("**3. Karanam Radha Pranathi (20231CAI0003):**")
            st.caption("Developed the NewsAPI live multi-source article retrieval pipeline, evidence pool builder, and ground-truth benchmark datasets.")
            
            st.markdown("**4. Bhagyesh (20231CAI0068):**")
            st.caption("Engineered the interactive Streamlit web dashboard, evaluator authentication portal, UI card design, and RoBERTa environment.")

    st.markdown("---")
    st.subheader("🗺️ 5-Phase Project Roadmap")
    roadmap_df = pd.DataFrame([
        {"Phase": "Phase 1 (Review 1)", "Scope": "Literature Survey (12 IEEE Papers), Problem Definition & Architecture", "Status": "Completed"},
        {"Phase": "Phase 2 (Review 2)", "Scope": "MBFC Knowledge Base (4,442 Outlets), Manipulation Engine, Benchmark Tests", "Status": "Completed"},
        {"Phase": "Phase 3 (Current 50%)", "Scope": "Interactive Web Dashboard, NewsAPI Live Retrieval, Multi-Source Pool", "Status": "50% Milestone Ready"},
        {"Phase": "Phase 4 (Next Phase)", "Scope": "RoBERTa-MNLI Pairwise Cross-Checking & Semantic Stance Detection", "Status": "Scheduled"},
        {"Phase": "Phase 5 (Final Review)", "Scope": "Unified Score Aggregator, Production REST API, Final Comprehensive Report", "Status": "Scheduled"}
    ])
    st.table(roadmap_df)
