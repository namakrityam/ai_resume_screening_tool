🚀 AI Resume Screening Tool

An intelligent, production-ready AI-powered Resume Screening System that automatically evaluates resumes against a given Job Description (JD), extracts key candidate details, and ranks candidates based on skill relevance and semantic similarity.

📌 Overview

The AI Resume Screening Tool is designed to streamline the hiring process by eliminating manual resume shortlisting.
It uses NLP, skill ontology matching, and semantic analysis to provide accurate, explainable, and ranked candidate evaluations.

This tool is suitable for:

Recruiters & HR teams

Internship & placement screening

Hackathons & academic projects

AI/NLP portfolio demonstrations

✨ Key Features

📄 Multi-Resume Upload (PDF & DOCX)

🧠 AI-based Skill Matching using weighted skill ontology

🔍 Job Description Parsing

📊 Candidate Ranking with Matching Percentage

👤 Automatic Candidate Name Extraction

📧 Email & Phone Number Detection

📈 Semantic Similarity Scoring using TF-IDF

🧾 Matched & Missing Skills Breakdown

⚡ Optimized for Streamlit Cloud Deployment

🧠 How It Works

User uploads one or multiple resumes

User provides a job description

The system:

Extracts text from resumes

Identifies candidate details

Extracts required skills from JD

Matches skills with resume content

Computes semantic similarity

Candidates are ranked and scored

Final results are displayed in a clean, sortable table

🧪 Scoring Methodology

The final Matching Percentage is calculated using:

Skill Coverage (50%) – weighted skill match accuracy

Skill Count Match (30%) – number of matched skills

Semantic Similarity (20%) – contextual similarity between resume & JD

Critical Skill Bonus – extra weight for high-impact skills

This ensures fair, explainable, and role-relevant scoring.

🛠️ Tech Stack

Frontend & App Framework: Streamlit

Backend Language: Python

NLP: spaCy (safe fallback enabled)

Machine Learning: Scikit-learn

Text Similarity: TF-IDF + Cosine Similarity

Document Parsing: pdfplumber, python-docx

📂 Project Structure
ai_resume_screening_tool/
│
├── app.py
├── requirements.txt
├── utils/
│   ├── pdf_parser.py
│   ├── text_cleaner.py
│   └── analyzer.py
├── assets/
├── README.md

⚙️ Installation & Setup
1️⃣ Clone the repository
git clone https://github.com/namakrityam/ai_resume_screening_tool.git
cd ai_resume_screening_tool

2️⃣ Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

3️⃣ Install dependencies
pip install -r requirements.txt

4️⃣ Run the application
streamlit run app.py

🌐 Deployment

The application is deployed on Streamlit Cloud.

Note:
Streamlit Cloud free-tier apps may go into sleep mode during inactivity.
If the app appears inactive, please wait 30–60 seconds for it to wake up.

📸 Demo

A demo video/screenshots can be added here to demonstrate:

Resume upload

JD input

Candidate ranking output

(Recommended for evaluations)

🔒 Limitations

Free-tier hosting may cause cold starts

Skill extraction is keyword-based (intentional for explainability)

Deep learning models are avoided to ensure fast deployment and stability

🚀 Future Enhancements

Role auto-classification (Frontend / Backend / Data / Cyber)

Resume-JD explainability dashboard

Recruiter feedback loop

Multi-language resume support

ATS-friendly scoring export (CSV / PDF)

👨‍💻 Author

NAMA Krityam
Computer Science Engineering Student
AI | NLP | Full Stack | Cybersecurity

🔗 GitHub: https://github.com/namakrityam

📄 License

This project is licensed for educational and demonstration purposes.
For commercial usage, please contact the author.
