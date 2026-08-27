"""
PSAIAC_61: Automated Phase 2 Deliverables & EDA Report Generator
"""

import sys
import json
import sqlite3
import time
from pathlib import Path
from tabulate import tabulate

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.config import MBFC_DB_PATH, BENCHMARK_CLAIMS_PATH, LEXICONS_PATH, DOCS_DIR
from src.database.source_reputation_db import SourceReputationDB
from src.manipulation.manipulation_detector import ManipulationDetector


def generate_eda_report():
    print("=" * 70)
    print("  PSAIAC_61: Generating Phase 2 Deliverable Analysis & EDA Report")
    print("=" * 70)

    db = SourceReputationDB()
    stats = db.get_statistics()
    
    # 1. Factuality Distribution Table
    fact_data = [[tier.title(), count, f"{(count / stats['total_sources']) * 100:.1f}%"] 
                 for tier, count in stats["factuality_distribution"].items()]
    fact_table = tabulate(fact_data, headers=["Factuality Tier", "Outlets Count", "Share (%)"], tablefmt="grid")
    
    # 2. Bias Distribution Table
    bias_data = [[bias.title(), count, f"{(count / stats['total_sources']) * 100:.1f}%"] 
                 for bias, count in stats["bias_distribution"].items() if count > 5]
    bias_table = tabulate(bias_data, headers=["Political Bias Tier", "Outlets Count", "Share (%)"], tablefmt="grid")
    
    # 3. Top Countries Table
    country_data = [[country.upper(), count] for country, count in stats["top_countries"].items()]
    country_table = tabulate(country_data, headers=["Country", "Registered Media Outlets"], tablefmt="grid")

    # 4. Latency Benchmark
    test_domains = [
        "reuters.com", "apnews.com", "bbc.co.uk", "thehindu.com", "theguardian.com",
        "wsj.com", "nytimes.com", "nature.com", "infowars.com", "theonion.com",
        "foxnews.com", "dailymail.co.uk", "altnews.in", "cdc.gov", "unlisted-outlet.org"
    ]
    latencies = []
    for _ in range(5):
        for d in test_domains:
            t0 = time.perf_counter()
            _ = db.lookup(d)
            latencies.append((time.perf_counter() - t0) * 1000.0)

    avg_lat = sum(latencies) / len(latencies)
    min_lat = min(latencies)
    max_lat = max(latencies)

    # 5. Benchmark Claims Analysis
    with open(BENCHMARK_CLAIMS_PATH, "r", encoding="utf-8") as f:
        bench_data = json.load(f)
    total_claims = len(bench_data.get("claims", []))

    # 6. Lexicons Analysis
    with open(LEXICONS_PATH, "r", encoding="utf-8") as f:
        lex_data = json.load(f)
    total_categories = len(lex_data.get("categories", {}))
    total_lexicon_terms = sum(
        len(v.get("phrases", [])) + len(v.get("keywords", [])) 
        for v in lex_data.get("categories", {}).values()
    )

    # Console Output
    print("\n--- [1] MBFC Database Coverage & Stats ---")
    print(f"Total Verified Domains: {stats['total_sources']}")
    print(f"Average Factuality Score: {stats['average_credibility_score'] * 100:.2f} / 100")
    print(f"Satire Domains Isolated: {stats['satire_sources']}")
    print(f"Conspiracy / Pseudoscience Sources: {stats['conspiracy_sources']}")
    print("\nFactuality Distribution:")
    print(fact_table)
    print("\nTop Media Bias Categories:")
    print(bias_table)
    print("\nTop 10 Source Countries:")
    print(country_table)

    print("\n--- [2] Performance & Benchmark Latency ---")
    print(f"Sampled Lookups: {len(latencies)} queries")
    print(f"Average Lookup Latency: {avg_lat:.4f} ms")
    print(f"Min Latency (Cached):   {min_lat:.4f} ms")
    print(f"Max Latency:           {max_lat:.4f} ms")

    print("\n--- [3] Manipulation Lexicons & Benchmark Datasets ---")
    print(f"Ground-Truth Benchmark Claims: {total_claims} test cases")
    print(f"Manipulation Categories:       {total_categories}")
    print(f"Total Linguistic Triggers:     {total_lexicon_terms} patterns")

    db.close()
    print("\n[OK] Phase 2 Analysis successfully completed!")


if __name__ == "__main__":
    generate_eda_report()
