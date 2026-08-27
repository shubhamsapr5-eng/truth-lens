"""
PSAIAC_61 Global Configuration & Constants
"""

import os
from pathlib import Path

# Base Paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
BENCHMARK_DATA_DIR = DATA_DIR / "benchmarks"
DOCS_DIR = PROJECT_ROOT / "docs"

# Data Files
MBFC_RAW_CSV = RAW_DATA_DIR / "mbfc_raw.csv"
MBFC_DB_PATH = PROCESSED_DATA_DIR / "mbfc_sources.sqlite3"
MBFC_JSON_PATH = PROCESSED_DATA_DIR / "mbfc_sources_processed.json"
LEXICONS_PATH = RAW_DATA_DIR / "manipulation_lexicons.json"
BENCHMARK_CLAIMS_PATH = BENCHMARK_DATA_DIR / "test_claims_benchmark.json"
SAMPLE_ARTICLES_PATH = BENCHMARK_DATA_DIR / "sample_articles.json"

# Remote MBFC Data Sources (Research Mirrors)
IDIAP_MBFC_RAW_URL = "https://raw.githubusercontent.com/idiap/Factual-Reporting-and-Political-Bias-Web-Interactions/master/data/mbfc_raw.csv"
IDIAP_MBFC_NORMALIZED_URL = "https://raw.githubusercontent.com/idiap/Factual-Reporting-and-Political-Bias-Web-Interactions/master/data/mbfc.csv"

# Numerical Credibility Scores (0.0 to 1.0)
FACTUALITY_WEIGHTS = {
    "very high": 1.00,
    "high": 0.85,
    "mostly factual": 0.70,
    "mixed": 0.45,
    "low": 0.20,
    "very low": 0.05,
    "conspiracy-pseudoscience": 0.02,
    "satire": 0.00,
    "unknown": 0.50,
}

# TLD Heuristic Fallbacks (for domains not in MBFC)
TLD_CREDIBILITY_FALLBACKS = {
    "gov": 0.95,
    "gov.in": 0.95,
    "gov.uk": 0.95,
    "edu": 0.90,
    "ac.in": 0.90,
    "ac.uk": 0.90,
    "mil": 0.90,
    "org": 0.60,
    "int": 0.92,
}

# Bias Categories Mapping
BIAS_CATEGORIES = {
    "left": -0.8,
    "left-center": -0.4,
    "least biased": 0.0,
    "neutral": 0.0,
    "right-center": 0.4,
    "right": 0.8,
    "extreme left": -1.0,
    "extreme right": 1.0,
    "conspiracy/pseudoscience": 0.0,
    "questionable sources": 0.0,
    "pro-science": 0.0,
    "satire": 0.0,
}

# Credibility Score Tiers
TIER_HIGH_CONFIDENCE = 75.0
TIER_MODERATE_CONFIDENCE = 50.0
TIER_QUESTIONABLE = 30.0
TIER_UNRELIABLE = 0.0
