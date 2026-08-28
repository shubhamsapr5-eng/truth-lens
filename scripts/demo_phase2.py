"""
PSAIAC_61: Interactive Phase 2 Demonstration CLI
"""

import sys
import json
import time
from pathlib import Path
try:
    from tabulate import tabulate
except ImportError:
    def tabulate(rows, headers=None, tablefmt="grid"):
        if not rows:
            return ""
        all_rows = [headers] + list(rows) if headers else list(rows)
        num_cols = max(len(r) for r in all_rows)
        col_widths = [max(len(str(r[i])) if i < len(r) else 0 for r in all_rows) for i in range(num_cols)]
        sep = "+" + "+".join("-" * (w + 2) for w in col_widths) + "+"
        lines = [sep]
        if headers:
            lines.append("| " + " | ".join(f"{str(h):<{col_widths[i]}}" for i, h in enumerate(headers)) + " |")
            lines.append("+" + "+".join("=" * (w + 2) for w in col_widths) + "+")
        for r in rows:
            row_vals = [str(r[i]) if i < len(r) else "" for i in range(num_cols)]
            lines.append("| " + " | ".join(f"{val:<{col_widths[i]}}" for i, val in enumerate(row_vals)) + " |")
            lines.append(sep)
        return "\n".join(lines)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.database.source_reputation_db import SourceReputationDB
from src.manipulation.manipulation_detector import ManipulationDetector
from src.config import BENCHMARK_CLAIMS_PATH, SAMPLE_ARTICLES_PATH


def print_banner():
    print("\n" + "=" * 76)
    print("       PSAIAC_61: Real-Time News Credibility Verification Engine")
    print("                 PHASE 2 INTERACTIVE DEMONSTRATION SUITE")
    print("=" * 76)


def demo_domain_lookup(db: SourceReputationDB):
    print("\n[+] --- 1. Source Reputation & MBFC Domain Lookup ---")
    query = input("Enter a news domain, hostname, or full article URL: ").strip()
    if not query:
        query = "https://edition.cnn.com/2024/01/15/business/market-update/index.html"
        print(f"[*] No input provided. Using sample URL: {query}")

    start = time.perf_counter()
    rep = db.lookup(query)
    lat_ms = (time.perf_counter() - start) * 1000.0

    print("\n--- Lookup Results ---")
    rows = [
        ["Queried Input", query],
        ["Resolved Canonical Domain", rep.domain],
        ["Source Entity Name", rep.source_name],
        ["Credibility Score", f"{rep.percentage_score}%"],
        ["Credibility Rating Tier", rep.credibility_rating],
        ["Factual Reporting Quality", rep.factual_reporting.upper()],
        ["Political Bias", rep.bias.upper()],
        ["Country of Origin", rep.country.upper()],
        ["Conspiracy / Pseudoscience", "FLAGGED" if rep.is_conspiracy else "Clean"],
    ]
    print(tabulate(rows, headers=["Attribute", "Value"], tablefmt="grid"))


def demo_manipulation_analysis(detector: ManipulationDetector):
    print("\n[+] --- 2. Manipulation & Sensationalism Indicator Analysis ---")
    print("Enter a sample headline to analyze (or press Enter for sample clickbait):")
    h_input = input("Headline: ").strip()
    if not h_input:
        h_input = "SHOCKING BOMBSHELL: Mainstream Media Hiding Deadly 5G Secrets That Will Blow Your Mind!!!"
        print(f"[*] Using sample: {h_input}")

    b_input = input("Article Body (optional, press Enter to skip): ").strip()
    if not b_input and "SHOCKING BOMBSHELL" in h_input:
        b_input = "Doctors are baffled as terrifying secret documents expose deep state cabal agenda. Act now before it is too late!"

    start = time.perf_counter()
    report = detector.analyze(headline=h_input, body=b_input)
    lat_ms = (time.perf_counter() - start) * 1000.0

    print("\n--- Manipulation Detection Report ---")
    rows = [
        ["Overall Manipulation Score", f"{report.overall_manipulation_score:.1f} / 100.0"],
        ["Risk Assessment Level", report.risk_level],
        ["Sensationalism / Clickbait Score", f"{report.sensationalism_score:.1f} / 100.0"],
        ["Fear & Emotional Urgency Score", f"{report.fear_urgency_score:.1f} / 100.0"],
        ["Conspiracy & Paranoia Score", f"{report.conspiracy_score:.1f} / 100.0"],
        ["Pseudoscience Marker Score", f"{report.pseudoscience_score:.1f} / 100.0"],
        ["Stylistic Formatting Score", f"{report.stylistic_score:.1f} / 100.0"],
        ["Analysis Latency", f"{lat_ms:.3f} ms"],
    ]
    print(tabulate(rows, headers=["Metric", "Result"], tablefmt="grid"))

    if report.flagged_phrases:
        print("\nFlagged Manipulative Phrases / Buzzwords:")
        p_rows = [[item["term"], item["category"], item["location"], item["severity"].upper()] 
                  for item in report.flagged_phrases]
        print(tabulate(p_rows, headers=["Trigger Word/Phrase", "Category", "Location", "Severity"], tablefmt="grid"))

    if report.stylistic_flags:
        print("\nStylistic Formatting Flags:")
        for sf in report.stylistic_flags:
            print(f"  * {sf}")

    print(f"\nSummary Verdict: {report.summary_warning}")


def demo_benchmark_verification(db: SourceReputationDB, detector: ManipulationDetector):
    print("\n[+] --- 3. Ground-Truth Benchmark Claims Verification ---")
    if not BENCHMARK_CLAIMS_PATH.exists():
        print("[-] Benchmark claims file not found.")
        return

    with open(BENCHMARK_CLAIMS_PATH, "r", encoding="utf-8") as f:
        bench = json.load(f)

    claims = bench.get("claims", [])
    print(f"Loaded {len(claims)} benchmark verification test cases:\n")

    summary_rows = []
    for c in claims:
        cid = c["claim_id"]
        category = c["category"]
        veracity = c["ground_truth_veracity"]
        headline = c["headline"]
        
        # Analyze headline manipulation
        m_rep = detector.analyze(headline=headline)
        
        # Check domain reputations if available
        corrob_domains = c.get("trusted_corroborating_domains", [])
        corrob_scores = [db.lookup(d).percentage_score for d in corrob_domains]
        avg_corrob = f"{sum(corrob_scores)/len(corrob_scores):.0f}%" if corrob_scores else "N/A"

        summary_rows.append([
            cid,
            category,
            headline[:38] + "..." if len(headline) > 38 else headline,
            veracity,
            f"{m_rep.overall_manipulation_score:.0f}/100",
            avg_corrob
        ])

    headers = ["ID", "Category", "Headline", "Ground Truth", "Manip. Score", "Avg Source Cred."]
    print(tabulate(summary_rows, headers=headers, tablefmt="grid"))


def demo_batch_domain_scoring(db: SourceReputationDB):
    print("\n[+] --- 4. Multi-Source Corroboration Pool Simulation ---")
    print("Simulating a retrieved pool of 8 diverse news sources for an incoming claim:")
    sample_pool = [
        "reuters.com",
        "bbc.co.uk",
        "thehindu.com",
        "nytimes.com",
        "foxnews.com",
        "dailymail.co.uk",
        "theonion.com",
        "infowars.com"
    ]
    
    results = db.batch_lookup(sample_pool)
    rows = []
    total_weight = 0.0
    for r in results:
        rows.append([
            r.domain,
            r.source_name,
            f"{r.percentage_score}%",
            r.factual_reporting.upper(),
            r.bias.upper(),
            f"{r.weight_factor:.2f}",
            "SATIRE" if r.is_satire else ("CONSPIRACY" if r.is_conspiracy else "VALID")
        ])
        total_weight += r.weight_factor

    headers = ["Domain", "Source Name", "Credibility Score", "Factuality", "Political Bias", "Trust Weight", "Status"]
    print(tabulate(rows, headers=headers, tablefmt="grid"))
    print(f"\nCombined Mean Source Pool Trust Weight: {total_weight / len(results):.2f}")


def main():
    print_banner()
    db = SourceReputationDB()
    detector = ManipulationDetector()

    while True:
        print("\n" + "-" * 76)
        print("Select Demonstration Module:")
        print("  1. Query Single Source Reputation (Domain / Article URL)")
        print("  2. Detect Manipulation & Sensationalism in Text")
        print("  3. Simulate Multi-Source Evidence Pool Scoring (Batch)")
        print("  4. View Database Coverage & Statistics")
        print("  0. Exit")
        print("-" * 76)

        choice = input("Enter choice (0-4) [default=1]: ").strip()
        if not choice:
            choice = "1"

        if choice == "1":
            demo_domain_lookup(db)
        elif choice == "2":
            demo_manipulation_analysis(detector)
        elif choice == "3":
            demo_batch_domain_scoring(db)
        elif choice == "4":
            stats = db.get_statistics()
            print(f"\n[+] Total Indexed Outlets: {stats['total_sources']}")
            print(f"[+] Average Factuality Score: {stats['average_credibility_score']*100:.1f}%")
            print(f"[+] Satire Sources Flagged: {stats['satire_sources']}")
            print(f"[+] Conspiracy Outlets Flagged: {stats['conspiracy_sources']}")
        elif choice == "0" or choice.lower() in ["exit", "q", "quit"]:
            print("\nExiting demonstration suite. Good luck with Phase 2 review!")
            break
        else:
            print("[-] Invalid choice. Please select 0-4.")

    db.close()


if __name__ == "__main__":
    main()
