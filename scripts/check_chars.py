import sys
sys.path.append(r"C:\Users\shubh\Desktop\truth-lens\scripts")
import report_chapters

for ch in report_chapters.CHAPTERS:
    for sec in ch["sections"]:
        for i, p in enumerate(sec.get("paras", [])):
            bad = [c for c in p if ord(c) < 32 and c not in "\t\n\r"]
            if bad:
                print(f"Bad char in Ch {ch['num']} Sec {sec['num']} Para {i}: {[ord(c) for c in bad]}")
                print("Text snippet:", repr(p[:100]))
