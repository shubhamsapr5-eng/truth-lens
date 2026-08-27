"""
PSAIAC_61 Build Script: Ingest MBFC Dataset & Construct SQLite Database
"""

import sys
import time
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.database.db_loader import build_unified_mbfc_database
from src.database.source_reputation_db import SourceReputationDB


def main():
    print("=" * 70)
    print("  PSAIAC_61: Building Source Reputation Database (Phase 2)")
    print("=" * 70)
    
    start_time = time.time()
    total_records = build_unified_mbfc_database()
    elapsed = time.time() - start_time
    
    print(f"\n[+] Ingestion completed in {elapsed:.2f} seconds.")
    print(f"[+] Total verified unique source domains indexed: {total_records}")

    # Verify lookups
    print("\n[-] Running Self-Verification Test...")
    db = SourceReputationDB()
    test_domains = [
        "reuters.com",
        "edition.cnn.com",
        "news.bbc.co.uk",
        "thehindu.com",
        "theonion.com",
        "infowars.com",
        "cdc.gov",
        "randomblog123.xyz"
    ]
    
    for dom in test_domains:
        lookup_start = time.perf_counter()
        rep = db.lookup(dom)
        lookup_ms = (time.perf_counter() - lookup_start) * 1000.0
        print(f"  * {dom:<22} -> Score: {rep.percentage_score:>5.1f}% | Tier: {rep.factual_reporting:<16} | Method: {rep.lookup_method:<16} ({lookup_ms:.3f} ms)")

    stats = db.get_statistics()
    print("\n[-] Database Summary Statistics:")
    print(f"  * Total sources: {stats['total_sources']}")
    print(f"  * Average credibility score: {stats['average_credibility_score'] * 100:.1f}%")
    print(f"  * Satire sources identified: {stats['satire_sources']}")
    print(f"  * Conspiracy/Pseudoscience: {stats['conspiracy_sources']}")
    
    db.close()
    print("\n[OK] Phase 2 Source Reputation Database Build Complete & Verified!")


if __name__ == "__main__":
    main()
