# 🎯 TruthLens: 50% Project Milestone Deliverable Report

**Problem Statement Number:** PSAIAC_61  
**Project Title:** TruthLens — Real-Time News Credibility & Misinformation Verification Engine  
**Institution:** School of Artificial Intelligence and Advanced Computing (AI&AC), Presidency University  
**Degree Program:** B.Tech — Computer Science & Engineering (Artificial Intelligence)  
**Evaluation Stage:** 50% Mid-Term Project Review  

---

## 👥 Team Members & Responsibilities

| Roll Number | Name | Role & Core Responsibilities |
| :--- | :--- | :--- |
| **20231CAI0046** | **Shubham Pandey (Team Leader)** | Source Profiling Engine, SQLite Database (4,442 outlets), System Architecture & Integration |
| **20231CAI0006** | **Ikram Inayathulla Khan** | Manipulation & Sensationalism Detection Engine (109 lexical triggers, risk classification) |
| **20231CAI0003** | **Karanam Radha Pranathi** | News Retrieval Engine, NewsAPI live integration, Ground-Truth Benchmark datasets |
| **20231CAI0068** | **Bhagyesh** | Streamlit Interactive Web Application, UI design, and RoBERTa-MNLI model staging |

---

## 📊 The 50% / 50% Engineering Breakdown

TruthLens splits its engineering lifecycle into two equal halves: **Data & Retrieval Infrastructure (50%)** and **Deep Learning Semantic Inference (50%)**.

```
┌────────────────────────────────────────────────────────┐
│             TRUTHLENS COMPLETE LIFECYCLE               │
├───────────────────────────┬────────────────────────────┤
│   COMPLETED TODAY (50%)   │   REMAINING PHASES (50%)   │
│   (Phases 1, 2, and 3)    │      (Phases 4 and 5)      │
├───────────────────────────┼────────────────────────────┤
│ • MBFC SQLite DB (4,442)  │ • RoBERTa-MNLI NLI Engine  │
│ • Domain Resolver (<1ms)  │ • Factual Claim Extractor  │
│ • Manipulation Scanner    │ • Unified Mathematical Math│
│ • Live NewsAPI Retrieval  │ • End-to-End Evaluation    │
│ • Streamlit Web Dashboard │ • Production REST API      │
│ • 16 Passing Unit Tests   │ • Final Project Thesis     │
└───────────────────────────┴────────────────────────────┘
```

---

## ✅ Completed Deliverables Matrix (The First 50%)

### 1. Source Reputation Knowledge Base (Phase 2)
* Indexed **4,442 global news outlets** into a local SQLite database (`data/processed/mbfc_sources.sqlite3`).
* Built a multi-tier canonical domain resolver (`src/utils/url_helper.py`) that strips protocols, subdomains (`edition.cnn.com` → `cnn.com`), and country extensions (`.co.uk`, `.gov.in`) with **sub-millisecond (<0.02ms) query latency**.
* Standardized qualitative ratings (*High, Mixed, Satire, Conspiracy*) into normalized mathematical weights ($0.0 \le W_{\text{rep}} \le 1.0$).

### 2. Linguistic Manipulation & Sensationalism Engine (Phase 2)
* Built a lexical analysis engine (`src/manipulation/manipulation_detector.py`) scanning against **109 curated trigger patterns**:
  * Sensationalism & clickbait phrases (*"SHOCKING"*, *"YOU WON'T BELIEVE"*)
  * Emotional panic & fear markers (*"ACT NOW BEFORE IT'S TOO LATE"*)
  * Conspiratorial & pseudoscience terms (*"WHAT THEY ARE HIDING"*, *"MIRACLE CURE"*)
* Stylistic analysis capturing excessive punctuation (`!!!`, `???`) and multiple ALL-CAPS words.
* Generates an explainable **Manipulation Risk Score (0–100%)** with color-coded risk tiers.

### 3. Live News Evidence Retrieval Pipeline (Phase 3)
* Engineered `src/retrieval/news_retriever.py` connecting directly to live global news APIs (**NewsAPI & GNews API**).
* Programmatically retrieves an independent **Corroboration Evidence Pool (5–10 articles)** covering the queried claim.
* Automatically cross-references each retrieved article's domain against our MBFC database to attach publisher trust ratings.
* Built-in offline fallback caching ensures reliable demonstrations even under unstable college networks.

### 4. Interactive Web Application Dashboard (Phase 3)
* Deployed a responsive web dashboard (`app.py`) built with **Streamlit**:
  * **🔐 Project Login Screen:** Includes a *"⚡ 1-Click Demo Login"* for seamless review presentations.
  * **Tab 1 — URL Inspector:** Instant domain resolution, credibility gauges, factual tier, and political bias.
  * **Tab 2 — Article Text Analyzer:** Highlights manipulation keywords directly in the text with colored tags.
  * **Tab 3 — Live Claim Cross-Search:** Real-time NewsAPI query returning live evidence cards with publisher scores.
  * **📰 Media Directory:** Search and filter through all 4,442 outlets by Country, Factuality, and Bias.
  * **ℹ️ Architecture & Methodology:** Outlines PSAIAC_61 context, formulas, and roadmap.
* Created a **1-Click Desktop Launcher** (`Run_TruthLens.bat`).

### 5. Automated Quality Assurance & Testing
* **16/16 Unit Tests Passing** across all modules via `pytest`:
  * Domain resolution and TLD normalization tests (`test_source_reputation.py`)
  * Manipulation detection and keyword boundary tests (`test_manipulation.py`)
  * Live news evidence retrieval tests (`test_news_retriever.py`)

---

## ⏳ Planned Deliverables for the Remaining 50%

| Phase | Component | Weight | Technical Description |
| :--- | :--- | :--- | :--- |
| **Phase 4** | **RoBERTa-MNLI Transformer Stance Inference** | **25%** | Integrating `roberta-large-mnli` from Hugging Face to classify claim-evidence sentence pairs into 3-way stance signals: **Entailment (+1.0)**, **Contradiction (-1.0)**, and **Neutral (0.0)**. |
| **Phase 4** | **Automated Factual Claim Extraction** | **10%** | Developing an NLP module using Named Entity Recognition (NER) and syntactic parsing to automatically extract checkable assertions from long articles. |
| **Phase 5** | **Unified Mathematical Fusion Engine** | **10%** | Implementing the core formula: $$C_{\text{final}} = 0.70 \times S_{\text{evidence}} + 0.30 \times W_{\text{origin}} - (0.25 \times M_{\text{index}})$$ combining all three orthogonal signals into a final 0–100 score. |
| **Phase 5** | **Benchmarking & Final Thesis Report** | **5%** | Evaluating performance across 100 benchmark claims (Accuracy, Precision, Recall, F1), packaging the production REST API, and writing the final thesis report. |

---

## 🚀 How to Run the 50% Milestone Demo

```bash
# 1. Open project directory
cd truth-lens

# 2. Run the automated test suite (16 tests)
python -m pytest tests/

# 3. Launch the interactive web dashboard
python -m streamlit run app.py
# (Or simply double-click Run_TruthLens.bat on the Desktop)
```
