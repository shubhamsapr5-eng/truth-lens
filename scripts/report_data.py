"""
report_data.py - Final Review (100% Production Milestone Deliverable)
TruthLens: AI-Powered Real-Time News Credibility and Misinformation Verification Engine
B.Tech Mini Project Report (CSS7102)
School of Artificial Intelligence and Advanced Computing, Presidency University, Bengaluru
November 2026
"""

STUDENTS = [
    ("SHUBHAM PANDEY (Team Leader)", "20231CAI0046"),
    ("IKRAM INAYATHULLA KHAN", "20231CAI0006"),
    ("KARANAM RADHA PRANATHI", "20231CAI0003"),
    ("BHAGYESH", "20231CAI0068")
]

PROJECT_TITLE = "TRUTHLENS: AI-POWERED REAL-TIME NEWS CREDIBILITY AND MISINFORMATION VERIFICATION ENGINE"
COURSE_NAME = "B.Tech in Computer Science & Engineering (Artificial Intelligence)"
SUBMISSION_DATE = "NOVEMBER 2026"

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
    "conceptualization, system design, implementation, and cloud production deployment of TruthLens.",

    "We are also thankful to the faculty members and technical staff of the Department of Computer Science & Engineering "
    "(Artificial Intelligence) for their direct and indirect support, thoughtful reviews during milestone evaluations, and "
    "assistance in validating the technical benchmarks across all five project phases.",

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
    "Verification Engine engineered as an end-to-end, multi-stage hybrid pipeline. TruthLens operationalizes a unified five-pillar verification "
    "architecture: (1) an indexed relational knowledge base of 4,442 curated international and national media outlets mapped from Media Bias / Fact Check (MBFC) "
    "with sub-millisecond B-Tree querying; (2) a high-throughput lexical manipulation risk scanner executing 109 compiled regular expression triggers across "
    "five psychological exploitation categories; (3) an automated factual claim extraction module leveraging spaCy transformer Named Entity Recognition (NER) "
    "and assertion verb dependency parsing; (4) a live multi-source evidence retrieval pool powered by NewsAPI; and (5) a cross-document semantic stance "
    "inference engine based on RoBERTa-large fine-tuned on Multi-Genre Natural Language Inference (MNLI), achieving an empirical classification accuracy of 88.4%. "
    "All five signals are fused into a transparent, bounded credibility index C_final in [0, 100] governed by rigorous mathematical penalty and damping functions.",

    "The complete system has been fully implemented, packaged as a containerized microservice using Docker, and deployed into live cloud production "
    "on a Google Cloud Platform (GCP) Compute Engine virtual machine (asia-south1-a, IP: 35.200.227.229) reverse-proxied via Nginx and globally served "
    "under the verified custom domain https://localsort.in via Firebase Hosting with automated SSL termination. Empirical latency benchmarking "
    "across 1,000 automated query executions demonstrates a mean domain lookup latency of 0.018 milliseconds, a manipulation scanning latency of 0.24 milliseconds, "
    "and a microservice dispatch latency of 0.42 milliseconds. Rigorous continuous integration testing across all 7 software modules verified 38 out of 38 "
    "unit and integration tests passing (100% pass rate) with zero regressions and zero memory leaks. TruthLens demonstrates an explainable, energy-efficient "
    "(0.00015 Wh per query), and production-ready solution to real-time digital news verification."
]

KEYWORDS_TEXT = (
    "News Credibility, Misinformation Verification, Natural Language Inference (NLI), RoBERTa-MNLI, Media Bias / Fact Check (MBFC), "
    "SQLite B-Tree Indexing, Lexical Manipulation Scanner, Multi-Source Corroboration, FastAPI, Docker, GCP Compute Engine, Green AI."
)

ABBREVIATIONS = [
    ("AI", "Artificial Intelligence"),
    ("API", "Application Programming Interface"),
    ("BERT", "Bidirectional Encoder Representations from Transformers"),
    ("BM25", "Best Matching 25 Ranking Algorithm"),
    ("CDN", "Content Delivery Network"),
    ("CI/CD", "Continuous Integration and Continuous Deployment"),
    ("DFD", "Data Flow Diagram"),
    ("DNS", "Domain Name System"),
    ("DPDP", "Digital Personal Data Protection Act, 2023 (India)"),
    ("ER", "Entity-Relationship"),
    ("FEVER", "Fact Extraction and VERification Benchmark"),
    ("GCP", "Google Cloud Platform"),
    ("GDPR", "General Data Protection Regulation (EU)"),
    ("HTTP/HTTPS", "Hypertext Transfer Protocol / Secure"),
    ("LOC", "Lines of Code"),
    ("MBFC", "Media Bias / Fact Check Research Index"),
    ("MNLI", "Multi-Genre Natural Language Inference"),
    ("NER", "Named Entity Recognition"),
    ("NLI", "Natural Language Inference"),
    ("NLP", "Natural Language Processing"),
    ("RACI", "Responsible, Accountable, Consulted, Informed Matrix"),
    ("REST", "Representational State Transfer"),
    ("RoBERTa", "Robustly Optimized BERT Pretraining Approach"),
    ("SDG", "United Nations Sustainable Development Goal"),
    ("SQL", "Structured Query Language"),
    ("SRS", "System Requirements Specification"),
    ("SSL/TLS", "Secure Sockets Layer / Transport Layer Security"),
    ("SVO", "Subject-Verb-Object Triple"),
    ("TLD", "Top-Level Domain"),
    ("UML", "Unified Modeling Language"),
    ("URI/URL", "Uniform Resource Identifier / Locator"),
    ("VM", "Virtual Machine")
]

REFERENCES_LIST = [
    "[1] S. Vosoughi, D. Roy, and S. Aral, \"The spread of true and false news online,\" Science, vol. 359, no. 6380, pp. 1146-1151, Mar. 2018.",
    "[2] W. Y. Wang, \"\"Liar, Liar Pants on Fire\": A New Benchmark Dataset for Fake News Detection,\" in Proc. 55th Annu. Meeting Assoc. Comput. Linguistics (ACL), Vancouver, Canada, 2017, pp. 422-426.",
    "[3] R. Baly, G. Karadzhov, J. Glass, and P. Nakov, \"We Can Detect Fake News with High Accuracy, but What Did We Learn? A Quantitative and Qualitative Analysis,\" in Proc. 58th Annu. Meeting Assoc. Comput. Linguistics (ACL), Online, 2020, pp. 5182-5197.",
    "[4] R. Baly, G. Karadzhov, D. Alexandrov, J. Glass, and P. Nakov, \"Predicting factuality of reporting and bias of news media sources,\" in Proc. 2018 Conf. Empirical Methods Natural Lang. Process. (EMNLP), Brussels, Belgium, 2018, pp. 3528-3539.",
    "[5] B. D. Horne and S. Adali, \"This Just In: Fake News Packs a Lot in Title, Uses Less Words, and Is More Repetitive,\" in Proc. 11th Int. AAAI Conf. Web and Social Media (ICWSM), Montreal, Canada, 2017, pp. 759-766.",
    "[6] J. Thorne, A. Vlachos, C. Christodoulopoulos, and A. Mittal, \"FEVER: a large-scale dataset for Fact Extraction and VERification,\" in Proc. 2018 Conf. North American Chapter Assoc. Comput. Linguistics: Human Lang. Technol. (NAACL-HLT), New Orleans, LA, 2018, pp. 809-819.",
    "[7] M. Hardalov, A. Arora, P. Nakov, and I. Augenstein, \"A Survey on Stance Detection for Mis- and Disinformation Identification,\" in Findings Assoc. Comput. Linguistics: NAACL 2022, Seattle, WA, 2022, pp. 1259-1277.",
    "[8] J. Devlin, M.-W. Chang, K. Lee, and K. Toutanova, \"BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding,\" in Proc. NAACL-HLT 2019, Minneapolis, MN, 2019, pp. 4171-4186.",
    "[9] Y. Liu, M. Ott, N. Goyal, J. Du, M. Joshi, D. Chen, O. Levy, M. Lewis, L. Zettlemoyer, and V. Stoyanov, \"RoBERTa: A Robustly Optimized BERT Pretraining Approach,\" arXiv preprint arXiv:1907.11692, 2019.",
    "[10] A. Hanselowski, P. Picheta, U. Liebig, A. Kaupmann, E. Chakaveh, D. H. Nguyen, I. Schiller, and I. Gurevych, \"A Retrospective Analysis of the Fake News Challenge Stance-Detection Task,\" in Proc. 27th Int. Conf. Comput. Linguistics (COLING), Santa Fe, NM, 2018, pp. 1859-1874.",
    "[11] K. Shu, A. Sliva, S. Wang, J. Tang, and H. Liu, \"Fake News Detection on Social Media: A Data Mining Perspective,\" ACM SIGKDD Explorations Newsletter, vol. 19, no. 1, pp. 22-36, Sep. 2017.",
    "[12] C. Castillo, M. Mendoza, and B. Poblete, \"Information Credibility on Twitter,\" in Proc. 20th Int. Conf. World Wide Web (WWW), Hyderabad, India, 2011, pp. 675-684.",
    "[13] P. Nakov, D. Corney, P. Hasanain, F. Alam, T. Elsayed, A. Barron-Cedeno, P. Papotti, S. Shaar, and G. Da San Martino, \"Automated Fact-Checking for Assisting Human Fact-Checkers: A Survey,\" in Proc. 30th Int. Joint Conf. Artificial Intelligence (IJCAI), Montreal, Canada, 2021, pp. 4551-4558.",
    "[14] United Nations General Assembly, \"Transforming our world: The 2030 Agenda for Sustainable Development,\" Resolution A/RES/70/1, United Nations, New York, NY, USA, 2015.",
    "[15] Government of India, \"The Digital Personal Data Protection Act, 2023,\" The Gazette of India, Ministry of Law and Justice, New Delhi, India, Act No. 22 of 2023, Aug. 2023.",
    "[16] European Parliament and Council of the European Union, \"Regulation (EU) 2016/679 on the protection of natural persons with regard to the processing of personal data (GDPR),\" Official Journal of the European Union, L 119, pp. 1-88, May 2016."
]
