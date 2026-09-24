# 🔍 TruthLens: Real-Time News Credibility & Misinformation Verification Engine

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.64+-FF4B4B.svg)](https://streamlit.io)
[![Database](https://img.shields.io/badge/SQLite-4%2C442%20Domains-lightgrey)](https://mediabiasfactcheck.com/)
[![Tests](https://img.shields.io/badge/pytest-16%20passed-brightgreen)](https://docs.pytest.org/)

> **Problem Statement (PSAIAC_61):** Misinformation spreads ~6x faster than real news online (*Science*, 2018). **TruthLens** evaluates news articles in real time and scores them on **factual accuracy**, **source credibility**, and **manipulation indicators** using Natural Language Inference (NLI) and cross-source consensus.

---

## 📑 Project Review & Evaluation Documents

- 🚀 **[50% Project Milestone Deliverable Report](docs/50_PERCENT_MILESTONE.md)** *(Comprehensive 50% completion matrix & remaining 50% roadmap)*
- 📊 **[Slide-by-Slide Presentation Deck](docs/REVIEW_2_SLIDES.md)** *(Mapped to evaluation rubric)*
- 📄 **[Comprehensive Academic Project Report](docs/REVIEW_2_REPORT.md)** *(Complete with 12 IEEE/Scopus papers critical analysis)*
- 🗺️ **[5-Phase Project Roadmap](docs/FIVE_PHASE_PROJECT_ROADMAP.md)** *(Detailed milestone & mathematical formulation breakdown)*

---

## 🏗️ System Architecture & Workflow

TruthLens moves beyond naive single-text classifiers by verifying claims against independent global reporting:

```
[ User Input: URL / Text ]
          │
          ▼
1. Article Ingestion & Scraper (trafilatura)
          │
          ├──────────────────────────────────────────┐
          ▼                                          ▼
2. Factual Claim Extraction             5. Manipulation Detector
   (Syntactic & NER Heuristics)             (109 Lexical & Stylistic Triggers)
          │                                          │
          ▼                                          │
3. Evidence Retrieval Engine (NewsAPI / GNews)       │
          │                                          │
          ▼                                          │
4. Corroboration Pool (5-10 Outlets)                 │
    ├── MBFC Source DB (4,442 Domains) ──► W_rep     │
    └── RoBERTa-MNLI Stance Engine    ──► Phi_NLI    │
          │                                          │
          └───────────────────┬──────────────────────┘
                              ▼
        6. Multi-Factor Weighted Aggregation Formula
                              │
                              ▼
            Credibility Score (0-100) + Evidence Cards
```

---

## ⚡ Quickstart & Live Demo

### 1. Clone & Install Dependencies
```bash
git clone https://github.com/shubhamsapr5-eng/truth-lens.git
cd truth-lens
pip install -r requirements.txt
```

### 2. Configure API Keys (Optional for Phase 2)
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
Fill in free API keys from [NewsAPI](https://newsapi.org/register) and [GNews](https://gnews.io/).

### 3. Build & Verify Source Reputation Database
```bash
python scripts/build_mbfc_db.py
```

### 4. Run Automated Test Suite (16/16 Passing)
```bash
python -m pytest tests/ -v
```

### 5. Launch the 50% Milestone Web Dashboard
```bash
python -m streamlit run app.py
```
*(On Windows: Simply double-click `Run_TruthLens.bat` on your Desktop).*

### 6. Alternative: Interactive Phase 2 Demo CLI
```bash
python scripts/demo_phase2.py
```

---

## 🗓️ 5-Phase Project Roadmap

| Phase | Timeline | Focus Area | Status |
|:---|:---:|---|:---:|
| **Phase 1** | Weeks 1–2 | Problem Formulation, Literature Survey (12 Papers) & Architecture Blueprint | ✅ **Completed** |
| **Phase 2** | Weeks 3–4 | Dataset Acquisition, MBFC Source DB (4,442 outlets) & Manipulation Lexicons | ✅ **Completed (Review 2)** |
| **Phase 3** | Weeks 5–6 | Live NewsAPI Retrieval Pool & Interactive Streamlit Web Dashboard | 🚀 **Completed (50% Milestone)** |
| **Phase 4** | Weeks 7–8 | RoBERTa-MNLI Pairwise Cross-Checking & Factual Claim Extraction | ⏳ *Scheduled (Next)* |
| **Phase 5** | Weeks 9–12 | Weighted Score Aggregator, Production REST API & Final Evaluation | ⏳ *Scheduled (Final Review)* |

---

## 📂 Repository Structure

```
truth-lens/
├── data/
│   ├── raw/
│   │   ├── mbfc_raw.csv                   # Raw MBFC dataset (4,497 source records)
│   │   └── manipulation_lexicons.json     # 109 manipulation/clickbait triggers
│   ├── processed/
│   │   ├── mbfc_sources.sqlite3           # High-speed indexed SQLite DB (4,442 unique domains)
│   │   └── mbfc_sources_processed.json    # JSON lookup cache
│   └── benchmarks/
│       ├── test_claims_benchmark.json     # Ground-truth test claims with labels
│       └── sample_articles.json           # Sample articles (real, clickbait, satire)
├── src/
│   ├── config.py                          # Global scoring constants & paths
│   ├── database/
│   │   ├── schema.py                      # SourceReputation dataclasses and enums
│   │   ├── db_loader.py                   # Data ingestion, cleaning & normalization
│   │   └── source_reputation_db.py        # Multi-tier domain lookup engine
│   ├── manipulation/
│   │   └── manipulation_detector.py       # Lexical & stylistic manipulation detector
│   └── utils/
│       └── url_helper.py                  # Canonical domain & TLD normalization
├── scripts/
│   ├── build_mbfc_db.py                   # Database builder script
│   ├── generate_phase2_report.py          # EDA analysis generator
│   └── demo_phase2.py                     # Interactive presentation CLI
├── tests/
│   ├── test_source_reputation.py          # 9 domain lookup tests
│   └── test_manipulation.py               # 4 manipulation scoring tests
├── docs/
│   ├── REVIEW_2_SLIDES.md                 # Slide-by-slide presentation deck
│   ├── REVIEW_2_REPORT.md                 # Full academic project report (20 marks)
│   ├── FIVE_PHASE_PROJECT_ROADMAP.md      # Detailed 5-phase engineering blueprint
│   └── PHASE_2_DELIVERABLE_REPORT.md      # Phase 2 technical verification report
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

## 📜 License
MIT License. Open for educational and research purposes.
