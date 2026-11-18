with open(r"C:\Users\shubh\Desktop\truth-lens\scripts\generate_report_figures.py", "r", encoding="utf-8") as f:
    code = f.read()

import re

# Update fig4_1_gantt
old_gantt_pattern = r"def generate_fig4_1_gantt\(\):.*?(?=def generate_fig7_1_benchmarks\(\):)"
new_gantt = '''def generate_fig4_1_gantt():
    """Figure 4.1: Project Timeline Gantt Chart (100% Final Review Milestone)."""
    fig, ax = plt.subplots(figsize=(9.5, 4.5), dpi=300)

    phases = [
        "Phase 1: Literature Survey & Architecture",
        "Phase 2: MBFC Knowledge Base & Lexicons",
        "Phase 3: Live NewsAPI & Web Dashboard",
        "Phase 4: RoBERTa-MNLI Stance Engine & Claims",
        "Phase 5: Docker, FastAPI & GCP Cloud (100%)"
    ]
    starts = [1, 3, 5, 7, 9]
    durations = [2, 2, 2, 2, 4]
    colors = ['#10B981', '#10B981', '#10B981', '#10B981', '#059669']
    status_tags = [
        "Completed (100%)",
        "Completed (100%)",
        "Completed (100%)",
        "Completed (100%)",
        "Completed (100%)"
    ]

    y_pos = np.arange(len(phases))[::-1]

    for i in range(len(phases)):
        bar = ax.barh(y_pos[i], durations[i], left=starts[i], height=0.55,
                      color=colors[i], edgecolor='#1E293B', linewidth=1)
        ax.text(starts[i] + durations[i] / 2, y_pos[i], f"{status_tags[i]}",
                ha='center', va='center', color='white', fontweight='bold', fontsize=8.5)

    ax.set_yticks(y_pos)
    ax.set_yticklabels(phases, fontsize=9.5, fontweight='bold', color='#1E293B')
    ax.set_xlabel("Development Timeline (Weeks 1 to 12)", fontsize=10, fontweight='bold', labelpad=8)
    ax.set_xlim(0, 14)
    ax.set_xticks(range(1, 14))
    ax.set_xticklabels([f"W{w}" for w in range(1, 14)])
    ax.grid(axis='x', linestyle='--', alpha=0.5)

    # Highlight completion milestone line at Week 12
    ax.axvline(x=12.2, color='#059669', linestyle='-', linewidth=2.5)
    ax.text(12.3, 4.3, "Final Review\\n(100% Completed)", color='#059669', fontweight='bold', fontsize=8.5)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    plt.tight_layout()
    out_path = OUTPUT_DIR / "fig4_1_gantt.png"
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Generated: {out_path}")


'''

code = re.sub(old_gantt_pattern, new_gantt, code, flags=re.DOTALL)

# Update fig7_1_benchmarks
old_benchmarks_pattern = r"def generate_fig7_1_benchmarks\(\):.*?(?=def generate_fig2_1_literature_taxonomy\(\):)"
new_benchmarks = '''def generate_fig7_1_benchmarks():
    """Figure 7.1: Latency Benchmark & Automated Testing Results (100% Production Milestone)."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.5, 4.5), dpi=300)

    # Subplot A: Latency Comparison across 6 core operations (ms)
    ops = [
        'Domain Lookup\\n(SQLite Index)',
        'Manipulation\\n(109 Triggers)',
        'API Dispatch\\n(FastAPI /api)',
        'Claim Parse\\n(spaCy NER)',
        'Article Parse\\n(Trafilatura)',
        'Live Search\\n(NewsAPI)'
    ]
    latencies = [0.018, 0.24, 0.42, 45, 210, 1120]  # in ms
    colors1 = ['#059669', '#10B981', '#06B6D4', '#3B82F6', '#6366F1', '#8B5CF6']

    bars = ax1.bar(ops, latencies, color=colors1, edgecolor='#1E293B', width=0.55)
    ax1.set_yscale('log')
    ax1.set_title("(a) Pipeline Module Latency Benchmarks (Log Scale)", fontsize=9.5, fontweight='bold', pad=10)
    ax1.set_ylabel("Execution Time (Milliseconds, Log Scale)", fontsize=9)
    ax1.grid(axis='y', linestyle=':', alpha=0.6)
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)

    for bar, lat in zip(bars, latencies):
        yval = bar.get_height()
        txt = f"{lat} ms" if lat < 1000 else f"{lat/1000:.2f} s"
        ax1.text(bar.get_x() + bar.get_width()/2.0, yval * 1.3, txt, ha='center', va='bottom', fontsize=7.5, fontweight='bold')

    # Subplot B: Automated Test Suite (38/38 Passed across 7 Modules)
    test_modules = [
        'Source DB\\n(9 Tests)',
        'Manip.\\n(4 Tests)',
        'Claims\\n(3 Tests)',
        'News Ret.\\n(3 Tests)',
        'Stance\\n(4 Tests)',
        'Score\\n(4 Tests)',
        'REST API\\n(11 Tests)'
    ]
    passed = [9, 4, 3, 3, 4, 4, 11]

    ax2.bar(test_modules, passed, color='#10B981', edgecolor='#065F46', width=0.55)
    ax2.set_title("(b) Automated Pytest Validation Suite (38/38 Passed - 100%)", fontsize=9.5, fontweight='bold', pad=10)
    ax2.set_ylabel("Passing Unit Tests Count", fontsize=9)
    ax2.set_ylim(0, 13)
    ax2.grid(axis='y', linestyle=':', alpha=0.6)
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)

    for idx, p in enumerate(passed):
        ax2.text(idx, p + 0.35, f"{p}/{p}", ha='center', va='bottom', fontsize=8, fontweight='bold', color='#065F46')

    plt.tight_layout()
    out_path = OUTPUT_DIR / "fig7_1_benchmarks.png"
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Generated: {out_path}")


def generate_fig6_5_cloud_deployment():
    """Figure 6.5: Cloud Infrastructure & Production Deployment Architecture."""
    fig, ax = plt.subplots(figsize=(10.5, 5.2), dpi=300)
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 5.5)
    ax.axis('off')
    fig.patch.set_facecolor('#FFFFFF')

    # 1. Edge & Client Layer
    rect_client = patches.FancyBboxPatch((0.4, 0.4), 2.2, 4.6, boxstyle="round,pad=0.1,rounding_size=0.15",
                                         facecolor='#F8FAFC', edgecolor='#3B82F6', linewidth=2)
    ax.add_patch(rect_client)
    ax.text(1.5, 4.75, "Client & Edge Layer", ha='center', va='center', fontsize=10, fontweight='bold', color='#1E40AF')
    
    ax.text(1.5, 3.8, "Client Web Browser\\n(Evaluator / User)", ha='center', va='center', fontsize=8.5,
            bbox=dict(boxstyle='round,pad=0.4', facecolor='#EFF6FF', edgecolor='#3B82F6'))
    ax.text(1.5, 2.3, "Firebase Hosting\\n(Global CDN & SSL)\\nhttps://localsort.in", ha='center', va='center', fontsize=8.5,
            bbox=dict(boxstyle='round,pad=0.4', facecolor='#FEF3C7', edgecolor='#D97706'))
    ax.text(1.5, 0.9, "Google Cloud DNS\\nManaged SSL Cert", ha='center', va='center', fontsize=8,
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#F1F5F9', edgecolor='#94A3B8'))

    ax.annotate("", xy=(3.3, 3.8), xytext=(2.6, 3.8),
                arrowprops=dict(arrowstyle="->", color='#2563EB', lw=2))
    ax.text(2.95, 4.05, "HTTPS\\n(Port 443)", ha='center', va='center', fontsize=7.5, color='#1E293B')

    # 2. GCP Production Compute Engine VM
    rect_vm = patches.FancyBboxPatch((3.3, 0.4), 7.3, 4.6, boxstyle="round,pad=0.1,rounding_size=0.15",
                                     facecolor='#F8FAFC', edgecolor='#10B981', linewidth=2)
    ax.add_patch(rect_vm)
    ax.text(6.95, 4.75, "GCP Compute Engine VM (truthlens-vm • 35.200.227.229 • asia-south1-a)",
            ha='center', va='center', fontsize=10, fontweight='bold', color='#065F46')

    # Nginx Reverse Proxy
    ax.text(4.4, 2.8, "Nginx Reverse Proxy\\n(Port 80 / SSL)\\nReverse Proxy Router", ha='center', va='center', fontsize=8.5,
            bbox=dict(boxstyle='round,pad=0.4', facecolor='#ECFDF5', edgecolor='#10B981', lw=1.5))

    ax.annotate("", xy=(5.8, 3.8), xytext=(5.1, 3.2),
                arrowprops=dict(arrowstyle="->", color='#059669', lw=1.8))
    ax.text(5.3, 3.7, "/ -> UI", fontsize=7.5, fontweight='bold', color='#065F46')

    ax.annotate("", xy=(5.8, 1.8), xytext=(5.1, 2.4),
                arrowprops=dict(arrowstyle="->", color='#059669', lw=1.8))
    ax.text(5.3, 1.9, "/api -> REST", fontsize=7.5, fontweight='bold', color='#065F46')

    ax.text(7.2, 3.8, "Streamlit Dashboard\\n(truthlens-ui.service • Port 8501)\\nCredibility Dial & Directory", ha='center', va='center', fontsize=8,
            bbox=dict(boxstyle='round,pad=0.4', facecolor='#EFF6FF', edgecolor='#3B82F6'))

    ax.text(7.2, 1.8, "FastAPI Microservice\\n(truthlens-api.service • Port 8000)\\nAsync /api/verify & OpenAPI", ha='center', va='center', fontsize=8,
            bbox=dict(boxstyle='round,pad=0.4', facecolor='#F0FDF4', edgecolor='#10B981'))

    ax.text(9.6, 2.8, "Core Reasoning Engine\\n• SQLite B-Tree (4,442)\\n• 109-Trigger Scanner\\n• spaCy Claim Parser\\n• RoBERTa-MNLI Stance\\n• C_final Algebraic Dial",
            ha='center', va='center', fontsize=7.8,
            bbox=dict(boxstyle='round,pad=0.4', facecolor='#FAF5FF', edgecolor='#8B5CF6', lw=1.5))

    ax.annotate("", xy=(8.5, 3.8), xytext=(8.2, 3.8),
                arrowprops=dict(arrowstyle="<->", color='#8B5CF6', lw=1.5))
    ax.annotate("", xy=(8.5, 1.8), xytext=(8.2, 1.8),
                arrowprops=dict(arrowstyle="<->", color='#8B5CF6', lw=1.5))

    plt.tight_layout()
    out_path = OUTPUT_DIR / "fig6_5_cloud_deployment.png"
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Generated: {out_path}")


'''

code = re.sub(old_benchmarks_pattern, new_benchmarks, code, flags=re.DOTALL)

# Add to __main__
if "generate_fig6_5_cloud_deployment()" not in code:
    code = code.replace("generate_fig7_2_case_studies()", "generate_fig7_2_case_studies()\n    generate_fig6_5_cloud_deployment()")
    code = code.replace("All 12 publication figures", "All 13 publication figures")

with open(r"C:\Users\shubh\Desktop\truth-lens\scripts\generate_report_figures.py", "w", encoding="utf-8") as f:
    f.write(code)

print("generate_report_figures.py successfully updated!")
