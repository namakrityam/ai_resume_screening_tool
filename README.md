AI Powered Resume Screening Tool

An AI powered resume screening application that automatically analyzes resumes against a given job description, extracts key candidate information, and ranks resumes based on skill matching percentage.

This tool is designed to help recruiters and hiring teams save time, reduce manual effort, and shortlist candidates more efficiently using NLP and machine learning techniques.

Features

Upload and analyze multiple resumes (PDF and DOCX)

Automatic resume text extraction

AI based skill matching with job description

Matching percentage calculation

Resume ranking system

Extracts candidate details:

Name

Email

Phone number

Displays matched and missing skills

Clean and interactive Streamlit interface

Cloud deployable (Streamlit Cloud compatible)

Tech Stack

Python

Streamlit

spaCy (NLP)

Scikit-learn

TF-IDF Vectorizer


ai_resume_screening_tool/
│
├── app.py
├── requirements.txt
├── README.md
│
├── utils/
│   ├── pdf_parser.py
│   ├── text_cleaner.py
│   ├── skill_matcher.py
│   ├── info_extractor.py
│
├── assets/
│   └── How_it_works.png
│
└── data/
    └── sample_resumes/

Cosine Similarity

pdfplumber

python-docx

Tesseract OCR (for scanned resumes)
