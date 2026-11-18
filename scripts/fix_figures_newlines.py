import re

with open(r"C:\Users\shubh\Desktop\truth-lens\scripts\generate_report_figures.py", "r", encoding="utf-8") as f:
    text = f.read()

# Fix broken newlines inside strings caused by literal newlines in replacement
text = re.sub(r'ax\.text\(12\.3, 4\.3, "Final Review\s*\n\s*\(100% Completed\)"', 'ax.text(12.3, 4.3, "Final Review\\n(100% Completed)"', text)
text = text.replace("'Domain Lookup\n(SQLite Index)'", "'Domain Lookup\\n(SQLite Index)'")
text = text.replace("'Manipulation\n(109 Triggers)'", "'Manipulation\\n(109 Triggers)'")
text = text.replace("'API Dispatch\n(FastAPI /api)'", "'API Dispatch\\n(FastAPI /api)'")
text = text.replace("'Claim Parse\n(spaCy NER)'", "'Claim Parse\\n(spaCy NER)'")
text = text.replace("'Article Parse\n(Trafilatura)'", "'Article Parse\\n(Trafilatura)'")
text = text.replace("'Live Search\n(NewsAPI)'", "'Live Search\\n(NewsAPI)'")
text = text.replace("'Source DB\n(9 Tests)'", "'Source DB\\n(9 Tests)'")
text = text.replace("'Manip.\n(4 Tests)'", "'Manip.\\n(4 Tests)'")
text = text.replace("'Claims\n(3 Tests)'", "'Claims\\n(3 Tests)'")
text = text.replace("'News Ret.\n(3 Tests)'", "'News Ret.\\n(3 Tests)'")
text = text.replace("'Stance\n(4 Tests)'", "'Stance\\n(4 Tests)'")
text = text.replace("'Score\n(4 Tests)'", "'Score\\n(4 Tests)'")
text = text.replace("'REST API\n(11 Tests)'", "'REST API\\n(11 Tests)'")
text = text.replace('"Client Web Browser\n(Evaluator / User)"', '"Client Web Browser\\n(Evaluator / User)"')
text = text.replace('"Firebase Hosting\n(Global CDN & SSL)\nhttps://localsort.in"', '"Firebase Hosting\\n(Global CDN & SSL)\\nhttps://localsort.in"')
text = text.replace('"Google Cloud DNS\nManaged SSL Cert"', '"Google Cloud DNS\\nManaged SSL Cert"')
text = text.replace('"Nginx Reverse Proxy\n(Port 80 / SSL)\nReverse Proxy Router"', '"Nginx Reverse Proxy\\n(Port 80 / SSL)\\nReverse Proxy Router"')
text = text.replace('"Streamlit Dashboard\n(truthlens-ui.service • Port 8501)\nCredibility Dial & Directory"', '"Streamlit Dashboard\\n(truthlens-ui.service • Port 8501)\\nCredibility Dial & Directory"')
text = text.replace('"FastAPI Microservice\n(truthlens-api.service • Port 8000)\nAsync /api/verify & OpenAPI"', '"FastAPI Microservice\\n(truthlens-api.service • Port 8000)\\nAsync /api/verify & OpenAPI"')
text = text.replace('"Core Reasoning Engine\n• SQLite B-Tree (4,442)\n• 109-Trigger Scanner\n• spaCy Claim Parser\n• RoBERTa-MNLI Stance\n• C_final Algebraic Dial"', '"Core Reasoning Engine\\n• SQLite B-Tree (4,442)\\n• 109-Trigger Scanner\\n• spaCy Claim Parser\\n• RoBERTa-MNLI Stance\\n• C_final Algebraic Dial"')
text = text.replace('"HTTPS\n(Port 443)"', '"HTTPS\\n(Port 443)"')

with open(r"C:\Users\shubh\Desktop\truth-lens\scripts\generate_report_figures.py", "w", encoding="utf-8") as f:
    f.write(text)
print("File successfully fixed.")
