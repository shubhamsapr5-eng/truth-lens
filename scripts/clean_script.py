with open(r"C:\Users\shubh\Desktop\truth-lens\scripts\report_chapters.py", "r", encoding="utf-8") as f:
    text = f.read()

# Replace any character with ord < 32 except \n, \r, \t
cleaned = []
for c in text:
    if ord(c) < 32 and c not in "\n\r\t":
        if ord(c) == 8:
            cleaned.append("\\\\b")
        else:
            cleaned.append(" ")
    else:
        cleaned.append(c)

with open(r"C:\Users\shubh\Desktop\truth-lens\scripts\report_chapters.py", "w", encoding="utf-8") as f:
    f.write("".join(cleaned))

print("Cleaned properly.")
