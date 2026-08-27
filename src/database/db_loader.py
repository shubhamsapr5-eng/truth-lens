"""
MBFC Dataset Downloader, Normalizer, and SQLite Database Loader
"""

import os
import re
import sqlite3
import json
import logging
import requests
import pandas as pd
from pathlib import Path
from typing import Dict, List, Any, Optional

from ..config import (
    PROJECT_ROOT,
    RAW_DATA_DIR,
    PROCESSED_DATA_DIR,
    MBFC_RAW_CSV,
    MBFC_DB_PATH,
    MBFC_JSON_PATH,
    IDIAP_MBFC_RAW_URL,
    FACTUALITY_WEIGHTS,
    BIAS_CATEGORIES
)
from ..utils.url_helper import extract_canonical_domain
from .schema import SourceReputation

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

# Essential Major Outlets Supplemental Knowledge Base
SUPPLEMENTAL_SOURCES: List[Dict[str, Any]] = [
    # Top Tier International Wire Agencies & Fact Checkers
    {"domain": "reuters.com", "source_name": "Reuters", "bias": "least biased", "factual_reporting": "very high", "country": "uk", "press_freedom": "mostly free", "media_type": "news agency", "popularity": "high traffic", "mbfc_credibility_rating": "high credibility"},
    {"domain": "apnews.com", "source_name": "Associated Press", "bias": "least biased", "factual_reporting": "very high", "country": "usa", "press_freedom": "mostly free", "media_type": "news agency", "popularity": "high traffic", "mbfc_credibility_rating": "high credibility"},
    {"domain": "afp.com", "source_name": "Agence France-Presse", "bias": "least biased", "factual_reporting": "very high", "country": "france", "press_freedom": "mostly free", "media_type": "news agency", "popularity": "high traffic", "mbfc_credibility_rating": "high credibility"},
    {"domain": "snopes.com", "source_name": "Snopes", "bias": "least biased", "factual_reporting": "very high", "country": "usa", "press_freedom": "mostly free", "media_type": "fact checking", "popularity": "high traffic", "mbfc_credibility_rating": "high credibility"},
    {"domain": "politifact.com", "source_name": "PolitiFact", "bias": "left-center", "factual_reporting": "high", "country": "usa", "press_freedom": "mostly free", "media_type": "fact checking", "popularity": "high traffic", "mbfc_credibility_rating": "high credibility"},
    {"domain": "factcheck.org", "source_name": "FactCheck.org", "bias": "least biased", "factual_reporting": "very high", "country": "usa", "press_freedom": "mostly free", "media_type": "fact checking", "popularity": "medium traffic", "mbfc_credibility_rating": "high credibility"},
    
    # Global Major Media
    {"domain": "bbc.com", "source_name": "BBC News", "bias": "left-center", "factual_reporting": "high", "country": "uk", "press_freedom": "mostly free", "media_type": "tv station", "popularity": "high traffic", "mbfc_credibility_rating": "high credibility"},
    {"domain": "bbc.co.uk", "source_name": "BBC UK", "bias": "left-center", "factual_reporting": "high", "country": "uk", "press_freedom": "mostly free", "media_type": "tv station", "popularity": "high traffic", "mbfc_credibility_rating": "high credibility"},
    {"domain": "nytimes.com", "source_name": "New York Times", "bias": "left-center", "factual_reporting": "high", "country": "usa", "press_freedom": "mostly free", "media_type": "newspaper", "popularity": "high traffic", "mbfc_credibility_rating": "high credibility"},
    {"domain": "wsj.com", "source_name": "Wall Street Journal", "bias": "right-center", "factual_reporting": "high", "country": "usa", "press_freedom": "mostly free", "media_type": "newspaper", "popularity": "high traffic", "mbfc_credibility_rating": "high credibility"},
    {"domain": "bloomberg.com", "source_name": "Bloomberg", "bias": "least biased", "factual_reporting": "high", "country": "usa", "press_freedom": "mostly free", "media_type": "news website", "popularity": "high traffic", "mbfc_credibility_rating": "high credibility"},
    {"domain": "ft.com", "source_name": "Financial Times", "bias": "least biased", "factual_reporting": "high", "country": "uk", "press_freedom": "mostly free", "media_type": "newspaper", "popularity": "high traffic", "mbfc_credibility_rating": "high credibility"},
    {"domain": "theguardian.com", "source_name": "The Guardian", "bias": "left-center", "factual_reporting": "high", "country": "uk", "press_freedom": "mostly free", "media_type": "newspaper", "popularity": "high traffic", "mbfc_credibility_rating": "high credibility"},
    {"domain": "washingtonpost.com", "source_name": "The Washington Post", "bias": "left-center", "factual_reporting": "high", "country": "usa", "press_freedom": "mostly free", "media_type": "newspaper", "popularity": "high traffic", "mbfc_credibility_rating": "high credibility"},
    {"domain": "dw.com", "source_name": "Deutsche Welle", "bias": "least biased", "factual_reporting": "very high", "country": "germany", "press_freedom": "mostly free", "media_type": "broadcast network", "popularity": "high traffic", "mbfc_credibility_rating": "high credibility"},
    {"domain": "aljazeera.com", "source_name": "Al Jazeera English", "bias": "left-center", "factual_reporting": "mostly factual", "country": "qatar", "press_freedom": "limited freedom", "media_type": "tv station", "popularity": "high traffic", "mbfc_credibility_rating": "medium credibility"},
    {"domain": "cnn.com", "source_name": "CNN", "bias": "left", "factual_reporting": "mostly factual", "country": "usa", "press_freedom": "mostly free", "media_type": "tv station", "popularity": "high traffic", "mbfc_credibility_rating": "medium credibility"},
    {"domain": "foxnews.com", "source_name": "Fox News", "bias": "right", "factual_reporting": "mixed", "country": "usa", "press_freedom": "mostly free", "media_type": "tv station", "popularity": "high traffic", "mbfc_credibility_rating": "mixed credibility"},
    {"domain": "dailymail.co.uk", "source_name": "Daily Mail", "bias": "right", "factual_reporting": "mixed", "country": "uk", "press_freedom": "mostly free", "media_type": "tabloid", "popularity": "high traffic", "mbfc_credibility_rating": "mixed credibility"},
    {"domain": "breitbart.com", "source_name": "Breitbart News", "bias": "extreme right", "factual_reporting": "low", "country": "usa", "press_freedom": "mostly free", "media_type": "website", "popularity": "high traffic", "mbfc_credibility_rating": "low credibility"},
    {"domain": "infowars.com", "source_name": "InfoWars", "bias": "extreme right", "factual_reporting": "conspiracy-pseudoscience", "country": "usa", "press_freedom": "mostly free", "media_type": "conspiracy", "popularity": "medium traffic", "mbfc_credibility_rating": "low credibility"},
    {"domain": "naturalnews.com", "source_name": "Natural News", "bias": "extreme right", "factual_reporting": "conspiracy-pseudoscience", "country": "usa", "press_freedom": "mostly free", "media_type": "conspiracy", "popularity": "medium traffic", "mbfc_credibility_rating": "low credibility"},

    # Satire Outlets
    {"domain": "theonion.com", "source_name": "The Onion", "bias": "satire", "factual_reporting": "satire", "country": "usa", "press_freedom": "mostly free", "media_type": "satire", "popularity": "high traffic", "mbfc_credibility_rating": "satire"},
    {"domain": "babylonbee.com", "source_name": "The Babylon Bee", "bias": "satire", "factual_reporting": "satire", "country": "usa", "press_freedom": "mostly free", "media_type": "satire", "popularity": "high traffic", "mbfc_credibility_rating": "satire"},
    {"domain": "fakingnews.com", "source_name": "Faking News", "bias": "satire", "factual_reporting": "satire", "country": "india", "press_freedom": "mostly free", "media_type": "satire", "popularity": "medium traffic", "mbfc_credibility_rating": "satire"},

    # Science & Academic Publishers
    {"domain": "nature.com", "source_name": "Nature Publishing", "bias": "pro-science", "factual_reporting": "very high", "country": "uk", "press_freedom": "mostly free", "media_type": "journal", "popularity": "high traffic", "mbfc_credibility_rating": "high credibility"},
    {"domain": "sciencemag.org", "source_name": "Science / AAAS", "bias": "pro-science", "factual_reporting": "very high", "country": "usa", "press_freedom": "mostly free", "media_type": "journal", "popularity": "high traffic", "mbfc_credibility_rating": "high credibility"},
    {"domain": "scientificamerican.com", "source_name": "Scientific American", "bias": "pro-science", "factual_reporting": "very high", "country": "usa", "press_freedom": "mostly free", "media_type": "magazine", "popularity": "high traffic", "mbfc_credibility_rating": "high credibility"},
    {"domain": "newscientist.com", "source_name": "New Scientist", "bias": "pro-science", "factual_reporting": "very high", "country": "uk", "press_freedom": "mostly free", "media_type": "magazine", "popularity": "high traffic", "mbfc_credibility_rating": "high credibility"},

    # Major Indian News Outlets
    {"domain": "thehindu.com", "source_name": "The Hindu", "bias": "left-center", "factual_reporting": "high", "country": "india", "press_freedom": "mostly free", "media_type": "newspaper", "popularity": "high traffic", "mbfc_credibility_rating": "high credibility"},
    {"domain": "indianexpress.com", "source_name": "The Indian Express", "bias": "least biased", "factual_reporting": "high", "country": "india", "press_freedom": "mostly free", "media_type": "newspaper", "popularity": "high traffic", "mbfc_credibility_rating": "high credibility"},
    {"domain": "ndtv.com", "source_name": "NDTV", "bias": "left-center", "factual_reporting": "mostly factual", "country": "india", "press_freedom": "mostly free", "media_type": "tv station", "popularity": "high traffic", "mbfc_credibility_rating": "high credibility"},
    {"domain": "timesofindia.indiatimes.com", "source_name": "The Times of India", "bias": "right-center", "factual_reporting": "mostly factual", "country": "india", "press_freedom": "mostly free", "media_type": "newspaper", "popularity": "high traffic", "mbfc_credibility_rating": "medium credibility"},
    {"domain": "hindustantimes.com", "source_name": "Hindustan Times", "bias": "least biased", "factual_reporting": "mostly factual", "country": "india", "press_freedom": "mostly free", "media_type": "newspaper", "popularity": "high traffic", "mbfc_credibility_rating": "high credibility"},
    {"domain": "livemint.com", "source_name": "Mint (Livemint)", "bias": "least biased", "factual_reporting": "high", "country": "india", "press_freedom": "mostly free", "media_type": "newspaper", "popularity": "high traffic", "mbfc_credibility_rating": "high credibility"},
    {"domain": "theprint.in", "source_name": "ThePrint", "bias": "least biased", "factual_reporting": "mostly factual", "country": "india", "press_freedom": "mostly free", "media_type": "website", "popularity": "high traffic", "mbfc_credibility_rating": "high credibility"},
    {"domain": "thewire.in", "source_name": "The Wire India", "bias": "left", "factual_reporting": "mostly factual", "country": "india", "press_freedom": "mostly free", "media_type": "website", "popularity": "high traffic", "mbfc_credibility_rating": "medium credibility"},
    {"domain": "scroll.in", "source_name": "Scroll.in", "bias": "left", "factual_reporting": "high", "country": "india", "press_freedom": "mostly free", "media_type": "website", "popularity": "medium traffic", "mbfc_credibility_rating": "high credibility"},
    {"domain": "altnews.in", "source_name": "Alt News", "bias": "left-center", "factual_reporting": "very high", "country": "india", "press_freedom": "mostly free", "media_type": "fact checking", "popularity": "medium traffic", "mbfc_credibility_rating": "high credibility"},
    {"domain": "boomlive.in", "source_name": "BOOM FactCheck", "bias": "least biased", "factual_reporting": "very high", "country": "india", "press_freedom": "mostly free", "media_type": "fact checking", "popularity": "medium traffic", "mbfc_credibility_rating": "high credibility"},
    {"domain": "indiatoday.in", "source_name": "India Today", "bias": "right-center", "factual_reporting": "mostly factual", "country": "india", "press_freedom": "mostly free", "media_type": "tv station", "popularity": "high traffic", "mbfc_credibility_rating": "medium credibility"},
    {"domain": "opindia.com", "source_name": "OpIndia", "bias": "extreme right", "factual_reporting": "low", "country": "india", "press_freedom": "mostly free", "media_type": "website", "popularity": "high traffic", "mbfc_credibility_rating": "low credibility"},

    # Tech Outlets
    {"domain": "techcrunch.com", "source_name": "TechCrunch", "bias": "least biased", "factual_reporting": "high", "country": "usa", "press_freedom": "mostly free", "media_type": "tech news", "popularity": "high traffic", "mbfc_credibility_rating": "high credibility"},
    {"domain": "theverge.com", "source_name": "The Verge", "bias": "left-center", "factual_reporting": "high", "country": "usa", "press_freedom": "mostly free", "media_type": "tech news", "popularity": "high traffic", "mbfc_credibility_rating": "high credibility"},
    {"domain": "wired.com", "source_name": "Wired", "bias": "left-center", "factual_reporting": "high", "country": "usa", "press_freedom": "mostly free", "media_type": "magazine", "popularity": "high traffic", "mbfc_credibility_rating": "high credibility"},
    {"domain": "arstechnica.com", "source_name": "Ars Technica", "bias": "least biased", "factual_reporting": "very high", "country": "usa", "press_freedom": "mostly free", "media_type": "tech news", "popularity": "high traffic", "mbfc_credibility_rating": "high credibility"},
]


def clean_country_name(val: Any) -> str:
    """Normalizes country names and strips press freedom annotations."""
    if not val or pd.isna(val):
        return "unknown"
    c_str = str(val).strip().lower()
    # Remove things like "(44/180 press freedom)"
    c_str = re.sub(r"\(.*?\)", "", c_str).strip()
    return c_str or "unknown"


def clean_bias_name(val: Any) -> str:
    """Normalizes political bias categories."""
    if not val or pd.isna(val):
        return "neutral / unrated"
    b_str = str(val).strip().lower()
    if b_str in ["nan", "none", "null", "not rated"]:
        return "neutral / unrated"
    return b_str


def normalize_factual_reporting(val: Any) -> str:
    """Standardizes textual factuality rating."""
    if not val or pd.isna(val):
        return "unknown"
    val_str = str(val).strip().lower()
    
    if "very high" in val_str:
        return "very high"
    if "high" in val_str and "very" not in val_str:
        return "high"
    if "mostly" in val_str or "mostly factual" in val_str:
        return "mostly factual"
    if "mixed" in val_str:
        return "mixed"
    if "very low" in val_str:
        return "very low"
    if "low" in val_str:
        return "low"
    if "conspiracy" in val_str or "pseudoscience" in val_str:
        return "conspiracy-pseudoscience"
    if "satire" in val_str:
        return "satire"
    return "unknown"


def compute_credibility_score(factual_reporting: str, bias: str = "") -> float:
    """Computes a normalized 0.0 to 1.0 credibility score based on factuality."""
    norm_fact = normalize_factual_reporting(factual_reporting)
    score = FACTUALITY_WEIGHTS.get(norm_fact, 0.50)
    
    # Check for extreme conspiracy/satire in bias
    bias_str = str(bias).lower()
    if "satire" in bias_str:
        return 0.00
    if "conspiracy" in bias_str or "questionable" in bias_str:
        return min(score, 0.15)
        
    return score


def download_raw_mbfc_data() -> bool:
    """Downloads raw MBFC datasets from verified research mirrors."""
    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)

    urls = [
        (IDIAP_MBFC_RAW_URL, MBFC_RAW_CSV),
    ]

    for url, target_path in urls:
        try:
            logger.info(f"Downloading raw data from {url}...")
            resp = requests.get(url, timeout=25)
            if resp.status_code == 200:
                with open(target_path, "wb") as f:
                    f.write(resp.content)
                logger.info(f"Successfully saved to {target_path} ({len(resp.content)} bytes)")
                return True
            else:
                logger.warning(f"Failed to download {url}: HTTP {resp.status_code}")
        except Exception as e:
            logger.error(f"Error downloading {url}: {e}")
            
    return False


def build_unified_mbfc_database() -> int:
    """
    Parses raw MBFC data, cleans/normalizes domains, merges supplemental entries,
    and writes to SQLite database with index and JSON cache.
    """
    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Download if missing
    if not MBFC_RAW_CSV.exists() or MBFC_RAW_CSV.stat().st_size == 0:
        download_raw_mbfc_data()

    records_dict: Dict[str, Dict[str, Any]] = {}

    # 2. Parse CSV if available
    if MBFC_RAW_CSV.exists() and MBFC_RAW_CSV.stat().st_size > 0:
        try:
            df = pd.read_csv(MBFC_RAW_CSV)
            logger.info(f"Loaded {len(df)} rows from {MBFC_RAW_CSV}")

            for _, row in df.iterrows():
                raw_domain = str(row.get("source", "")).strip()
                if not raw_domain or raw_domain.lower() == "nan":
                    continue

                canonical_domain = extract_canonical_domain(raw_domain)
                if not canonical_domain:
                    continue

                bias = clean_bias_name(row.get("bias", "neutral"))
                factual_reporting = normalize_factual_reporting(row.get("factual_reporting", "unknown"))
                cred_score = compute_credibility_score(factual_reporting, bias)
                country = clean_country_name(row.get("country", "unknown"))
                press_freedom = str(row.get("press_freedom", "unknown")).strip().lower()
                media_type = str(row.get("media_type", "website")).strip().lower()
                popularity = str(row.get("popularity", "unknown")).strip().lower()
                mbfc_rating = str(row.get("mbfc_credibility_rating", "unverified")).strip().title()

                is_satire = "satire" in bias or factual_reporting == "satire"
                is_conspiracy = "conspiracy" in bias or "pseudoscience" in factual_reporting

                # Derive clean source name from domain
                name_part = canonical_domain.split(".")[0].replace("-", " ").title()

                record = {
                    "domain": canonical_domain,
                    "source_name": name_part,
                    "bias": bias,
                    "factual_reporting": factual_reporting,
                    "credibility_score": cred_score,
                    "credibility_rating": mbfc_rating,
                    "country": country,
                    "press_freedom": press_freedom,
                    "media_type": media_type,
                    "popularity": popularity,
                    "is_satire": int(is_satire),
                    "is_conspiracy": int(is_conspiracy),
                    "is_fallback": 0,
                    "notes": "MBFC Research Dataset"
                }

                if canonical_domain not in records_dict or records_dict[canonical_domain]["factual_reporting"] == "unknown":
                    records_dict[canonical_domain] = record

        except Exception as e:
            logger.error(f"Error parsing MBFC_RAW_CSV: {e}")

    # 3. Merge Supplemental High-Value Sources
    for supp in SUPPLEMENTAL_SOURCES:
        c_dom = extract_canonical_domain(supp["domain"])
        f_rep = normalize_factual_reporting(supp["factual_reporting"])
        clean_b = clean_bias_name(supp["bias"])
        c_score = compute_credibility_score(f_rep, clean_b)
        is_sat = "satire" in clean_b or f_rep == "satire"
        is_con = "conspiracy" in clean_b or "pseudoscience" in f_rep

        records_dict[c_dom] = {
            "domain": c_dom,
            "source_name": supp["source_name"],
            "bias": clean_b,
            "factual_reporting": f_rep,
            "credibility_score": c_score,
            "credibility_rating": supp["mbfc_credibility_rating"].title(),
            "country": clean_country_name(supp["country"]),
            "press_freedom": supp["press_freedom"],
            "media_type": supp["media_type"],
            "popularity": supp["popularity"],
            "is_satire": int(is_sat),
            "is_conspiracy": int(is_con),
            "is_fallback": 0,
            "notes": "Curated / Verified Outlets"
        }

    total_records = len(records_dict)
    logger.info(f"Total unified unique source domains: {total_records}")

    # 4. Save to SQLite Database
    if MBFC_DB_PATH.exists():
        try:
            MBFC_DB_PATH.unlink()
        except Exception:
            pass

    conn = sqlite3.connect(MBFC_DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sources (
            domain TEXT PRIMARY KEY,
            source_name TEXT,
            bias TEXT,
            factual_reporting TEXT,
            credibility_score REAL,
            credibility_rating TEXT,
            country TEXT,
            press_freedom TEXT,
            media_type TEXT,
            popularity TEXT,
            is_satire INTEGER,
            is_conspiracy INTEGER,
            is_fallback INTEGER,
            notes TEXT
        )
    """)

    cursor.execute("CREATE INDEX IF NOT EXISTS idx_sources_domain ON sources (domain)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_sources_credibility ON sources (credibility_score)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_sources_bias ON sources (bias)")

    insert_rows = list(records_dict.values())
    cursor.executemany("""
        INSERT OR REPLACE INTO sources (
            domain, source_name, bias, factual_reporting, credibility_score,
            credibility_rating, country, press_freedom, media_type, popularity,
            is_satire, is_conspiracy, is_fallback, notes
        ) VALUES (
            :domain, :source_name, :bias, :factual_reporting, :credibility_score,
            :credibility_rating, :country, :press_freedom, :media_type, :popularity,
            :is_satire, :is_conspiracy, :is_fallback, :notes
        )
    """, insert_rows)

    conn.commit()
    conn.close()
    logger.info(f"Successfully populated SQLite database at {MBFC_DB_PATH} with {total_records} records.")

    # 5. Export JSON Cache
    with open(MBFC_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(records_dict, f, indent=2)
    logger.info(f"Exported JSON lookup cache to {MBFC_JSON_PATH}")

    return total_records


if __name__ == "__main__":
    build_unified_mbfc_database()
