import sys
sys.path.append(r"C:\Users\shubh\Desktop\truth-lens\scripts")
import report_chapters

for ch in report_chapters.CHAPTERS:
    for sec in ch["sections"]:
        if "table" in sec:
            t = sec["table"]
            for r_idx, row in enumerate(t["rows"]):
                for c_idx, val in enumerate(row):
                    bad = [c for c in str(val) if ord(c) < 32 and c not in "\t\n\r"]
                    if bad:
                        print(f"Bad char in Ch {ch['num']} Table {t['num']} Row {r_idx} Col {c_idx}: {[ord(c) for c in bad]}")
                        print("Value:", repr(val))
