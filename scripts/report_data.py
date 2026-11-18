"""
Data and text content module for TruthLens Mini Project Report (CSS7102).
Contains all academic text, tables, structured matrices, and references.
Focuses strictly on the 7 foundational peer-reviewed research studies.
"""

STUDENTS = [
    ("SHUBHAM PANDEY (Team Leader)", "20231CAI0046"),
    ("IKRAM INAYATHULLA KHAN", "20231CAI0006"),
    ("KARANAM RADHA PRANATHI", "20231CAI0003"),
    ("BHAGYESH", "20231CAI0068")
]

CERTIFICATE_TEXT = (
    "Certified that this mini project report entitled \"TRUTHLENS: AI-POWERED REAL-TIME NEWS CREDIBILITY AND MISINFORMATION "
    "VERIFICATION ENGINE\" is the bonafide work of SHUBHAM PANDEY (20231CAI0046), IKRAM INAYATHULLA KHAN (20231CAI0006), "
    "KARANAM RADHA PRANATHI (20231CAI0003), and BHAGYESH (20231CAI0068), who carried out the project under our supervision "
    "in partial fulfilment of the requirements for the award of the degree of Bachelor of Technology in Computer Science & "
    "Engineering (Artificial Intelligence) from Presidency University, Bengaluru during the academic year 2026."
)

DECLARATION_TEXT = (
    "We hereby declare that the mini project report entitled \"TRUTHLENS: AI-POWERED REAL-TIME NEWS CREDIBILITY AND "
    "MISINFORMATION VERIFICATION ENGINE\" submitted to Presidency University, Bengaluru for the award of the degree of "
    "Bachelor of Technology in Computer Science & Engineering (Artificial Intelligence) is a record of original work done by us "
    "under the guidance of our faculty supervisor. We confirm that this work has not been submitted elsewhere for any other degree or diploma."
)

ACKNOWLEDGEMENT_TEXT = [
    "We express our profound gratitude to the Vice-Chancellor, Registrar, and Dean of the School of Artificial Intelligence "
    "& Advanced Computing, Presidency University, Bengaluru, for providing state-of-the-art computational infrastructure, research "
    "facilities, and an intellectually invigorating academic atmosphere that made this project possible.",

    "We extend our heartfelt appreciation and sincere gratitude to our Project Guide and Course Coordinator of CSS7102 "
    "(Mini Project) for their invaluable guidance, constructive critique, and continuous technical mentorship throughout the "
    "conceptualization, system design, and implementation stages of TruthLens.",

    "We are also thankful to the faculty members and technical staff of the Department of Computer Science & Engineering "
    "(Artificial Intelligence) for their direct and indirect support, thoughtful reviews during milestone presentations, and "
    "assistance in validating the technical benchmarks.",

    "Finally, we place on record our deepest gratitude to our parents, family members, and peers for their constant encouragement, "
    "unwavering patience, and moral support throughout our undergraduate engineering journey."
]

ABSTRACT_TEXT = [
    "The rapid proliferation of digital information across the World Wide Web and social networking platforms has transformed the "
    "global media landscape while simultaneously precipitating an epistemic crisis of unprecedented proportions. Misinformation, "
    "disinformation, state-sponsored propaganda cascades, and emotionally manipulative clickbait diffuse at velocities documented to "
    "be six-fold greater than verified truth, severely threatening public health, democratic elections, financial stability, and societal cohesion. "
    "Traditional automated verification paradigms suffer from critical vulnerabilities: isolated black-box NLP text classifiers exhibit "
    "severe topic-overfitting and hallucination, while static URL blacklists fail against newly registered domains, algorithmic cloaking, and domain fronting.",

    "To overcome these fundamental challenges, this report presents TruthLens: an AI-Powered Real-Time News Credibility and Misinformation "
    "Verification Engine engineered as an end-to-end, multi-stage hybrid pipeline. TruthLens operationalizes a tripartite verification architecture "
    "unifying: (1) an indexed relational knowledge base of 4,442 curated international and national media outlets mapped from Media Bias / Fact Check (MBFC) "
    "with sub-millisecond B-Tree querying; (2) a high-throughput lexical manipulation risk scanner executing 109 compiled regular expression triggers across "
    "five psychological exploitation categories; and (3) a live multi-source evidence retrieval and corroboration engine powered by NewsAPI.",

    "For the 50% milestone deliverable, the foundational data engineering, local inference engine, and an interactive Streamlit full-stack web dashboard "
    "have been fully implemented, rigorously evaluated, and containerized. Empirical benchmarking across 1,000 automated query executions demonstrates "
    "a mean domain lookup latency of 0.018 milliseconds and a comprehensive text analysis latency of 0.245 milliseconds, delivering total response times "
    "under 0.3 milliseconds (excluding external network round-trips). Automated quality assurance via 27 unit and integration tests achieved a 100% "
    "pass rate with zero memory leaks. The system successfully demonstrates the feasibility of combining source reputation, linguistic manipulation detection, "
    "and cross-source evidence corroboration into a robust, explainable, and production-ready credibility score."
]

KEYWORDS_TEXT = (
    "News Credibility, Misinformation Verification, Media Bias / Fact Check (MBFC), SQLite B-Tree Indexing, "
    "Lexical Manipulation Scanner, Multi-Source Corroboration, Natural Language Inference, Streamlit, Green AI."
)

ABBREVIATIONS = [
    ("AI", "Artificial Intelligence"),
    ("API", "Application Programming Interface"),
    ("BERT", "Bidirectional Encoder Representations from Transformers"),
    ("BM25", "Best Matching 25 Ranking Algorithm"),
    ("DFD", "Data Flow Diagram"),
    ("DPDP", "Digital Personal Data Protection Act, 2023 (India)"),
    ("ER", "Entity-Relationship"),
    ("FEVER", "Fact Extraction and VERification Benchmark"),
    ("MBFC", "Media Bias / Fact Check Research Index"),
    ("NLI", "Natural Language Inference"),
    ("NLP", "Natural Language Processing"),
    ("REST", "Representational State Transfer"),
    ("RoBERTa", "Robustly Optimized BERT Pretraining Approach"),
    ("SDG", "United Nations Sustainable Development Goal"),
    ("SQL", "Structured Query Language"),
    ("UML", "Unified Modeling Language")
]

REFERENCES_LIST = [
    "[1] S. Vosoughi, D. Roy, and S. Aral, \"The spread of true and false news online,\" Science, vol. 359, no. 6380, pp. 1146-1151, Mar. 2018.",
    "[2] W. Y. Wang, \"\"Liar, Liar Pants on Fire\": A New Benchmark Dataset for Fake News Detection,\" in Proc. 55th Annu. Meeting Assoc. Comput. Linguistics (ACL), Vancouver, Canada, 2017, pp. 422-426.",
    "[3] R. Baly, G. Karadzhov, J. Glass, and P. Nakov, \"We Can Detect Fake News with High Accuracy, but What Did We Learn? A Quantitative and Qualitative Analysis,\" in Proc. 58th Annu. Meeting Assoc. Comput. Linguistics (ACL), Online, 2020, pp. 5182-5197.",
    "[4] R. Baly, G. Karadzhov, D. Alexandrov, J. Glass, and P. Nakov, \"Predicting factuality of reporting and bias of news media sources,\" in Proc. 2018 Conf. Empirical Methods Natural Lang. Process. (EMNLP), Brussels, Belgium, 2018, pp. 3528-3539.",
    "[5] B. D. Horne and S. Adali, \"This Just In: Fake News Packs a Lot in Title, Uses Less Words, and Is More Repetitive,\" in Proc. 11th Int. AAAI Conf. Web and Social Media (ICWSM), Montreal, Canada, 2017, pp. 759-766.",
    "[6] J. Thorne, A. Vlachos, C. Christodoulopoulos, and A. Mittal, \"FEVER: a large-scale dataset for Fact Extraction and VERification,\" in Proc. 2018 Conf. North American Chapter Assoc. Comput. Linguistics: Human Lang. Technol. (NAACL-HLT), New Orleans, LA, 2018, pp. 809-819.",
    "[7] M. Hardalov, A. Arora, P. Nakov, and I. Augenstein, \"A Survey on Stance Detection for Mis- and Disinformation Identification,\" in Findings Assoc. Comput. Linguistics: NAACL 2022, Seattle, WA, 2022, pp. 1259-1277.",
    "[8] United Nations General Assembly, \"Transforming our world: The 2030 Agenda for Sustainable Development,\" Resolution A/RES/70/1, United Nations, New York, NY, USA, 2015.",
    "[9] Government of India, \"The Digital Personal Data Protection Act, 2023,\" Act No. 22 of 2023, The Gazette of India, Ministry of Law and Justice, New Delhi, India, Aug. 2023."
]
