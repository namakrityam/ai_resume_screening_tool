import re
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from collections import Counter

from utils.pdf_parser import extract_text
from utils.text_cleaner import clean_text

# ===============================
# NLP
# =============================
import spacy

try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    nlp = None



# ===============================
# COMPREHENSIVE SKILL ONTOLOGY - ALL HIGH-DEMAND ROLES
# ===============================
SKILL_ONTOLOGY = {
    # ==========================================
    # 1. FRONTEND DEVELOPMENT
    # ==========================================
    "frontend": {
        "html": 2.5,
        "html5": 2.5,
        "css": 2.5,
        "css3": 2.5,
        "javascript": 3.5,
        "js": 3.5,
        "react": 4.0,
        "reactjs": 4.0,
        "react.js": 4.0,
        "nextjs": 3.5,
        "next.js": 3.5,
        "tailwind": 2.0,
        "tailwind css": 2.0,
        "bootstrap": 2.0,
        "responsive": 2.0,
        "responsive design": 2.0,
        "ui": 1.5,
        "ux": 1.5,
        "frontend": 2.0,
        "front-end": 2.0,
        "jquery": 1.5,
        "typescript": 3.0,
        "angular": 3.5,
        "vue": 3.5,
        "vuejs": 3.5,
        "vue.js": 3.5,
        "sass": 1.5,
        "scss": 1.5,
        "less": 1.5,
        "webpack": 2.0,
        "vite": 2.0,
        "redux": 2.5,
        "mobx": 2.0,
        "styled-components": 1.5,
        "material-ui": 2.0,
        "mui": 2.0,
        "chakra ui": 2.0,
        "figma": 1.5,
        "adobe xd": 1.5,
        "sketch": 1.5
    },
    
    # ==========================================
    # 2. BACKEND DEVELOPMENT
    # ==========================================
    "backend": {
        "node": 2.5,
        "nodejs": 2.5,
        "node.js": 2.5,
        "express": 2.5,
        "expressjs": 2.5,
        "express.js": 2.5,
        "nestjs": 3.0,
        "api": 3.0,
        "rest": 2.5,
        "rest api": 2.5,
        "restful": 2.5,
        "graphql": 3.0,
        "backend": 2.0,
        "back-end": 2.0,
        "python": 3.5,
        "java": 3.5,
        "django": 2.5,
        "flask": 2.5,
        "fastapi": 3.0,
        "spring": 3.0,
        "spring boot": 3.0,
        "mongodb": 2.5,
        "mysql": 2.5,
        "postgresql": 2.5,
        "postgres": 2.5,
        "sql": 2.5,
        "nosql": 2.0,
        "redis": 2.0,
        "php": 2.5,
        "laravel": 2.5,
        "c++": 2.5,
        "c#": 2.5,
        ".net": 3.0,
        "asp.net": 3.0,
        "ruby": 2.5,
        "rails": 2.5,
        "ruby on rails": 2.5,
        "go": 3.0,
        "golang": 3.0,
        "rust": 3.0,
        "scala": 2.5,
        "kotlin": 2.5,
        "microservices": 3.0,
        "serverless": 2.5,
        "lambda": 2.0,
        "elasticsearch": 2.0,
        "rabbitmq": 2.0,
        "kafka": 2.5
    },
    
    # ==========================================
    # 3. DATA SCIENCE & MACHINE LEARNING
    # ==========================================
    "data_science": {
        "python": 4.0,
        "r": 3.0,
        "pandas": 3.5,
        "numpy": 3.5,
        "scipy": 2.5,
        "scikit-learn": 3.5,
        "sklearn": 3.5,
        "tensorflow": 4.0,
        "keras": 3.5,
        "pytorch": 4.0,
        "machine learning": 4.0,
        "ml": 4.0,
        "deep learning": 4.0,
        "neural networks": 3.5,
        "cnn": 3.0,
        "rnn": 3.0,
        "lstm": 3.0,
        "nlp": 3.5,
        "natural language processing": 3.5,
        "computer vision": 3.5,
        "opencv": 3.0,
        "data analysis": 3.0,
        "data visualization": 2.5,
        "matplotlib": 2.5,
        "seaborn": 2.5,
        "plotly": 2.5,
        "tableau": 3.0,
        "power bi": 3.0,
        "powerbi": 3.0,
        "statistics": 3.0,
        "probability": 2.5,
        "linear algebra": 2.5,
        "feature engineering": 3.0,
        "model deployment": 3.0,
        "mlops": 3.0,
        "a/b testing": 2.5,
        "hypothesis testing": 2.5,
        "regression": 2.5,
        "classification": 2.5,
        "clustering": 2.5,
        "time series": 3.0,
        "xgboost": 3.0,
        "lightgbm": 3.0,
        "random forest": 2.5,
        "svm": 2.5,
        "pca": 2.0,
        "dimensionality reduction": 2.5
    },
    
    # ==========================================
    # 4. DATA ENGINEERING & BIG DATA
    # ==========================================
    "data_engineering": {
        "sql": 3.5,
        "python": 3.5,
        "scala": 3.0,
        "spark": 4.0,
        "apache spark": 4.0,
        "pyspark": 4.0,
        "hadoop": 3.5,
        "hive": 3.0,
        "pig": 2.5,
        "kafka": 3.5,
        "airflow": 3.5,
        "apache airflow": 3.5,
        "etl": 3.5,
        "data pipeline": 3.5,
        "data warehousing": 3.0,
        "snowflake": 3.5,
        "redshift": 3.0,
        "bigquery": 3.5,
        "databricks": 3.5,
        "dbt": 3.0,
        "data modeling": 3.0,
        "dimensional modeling": 2.5,
        "data lake": 2.5,
        "delta lake": 2.5,
        "aws": 3.0,
        "azure": 3.0,
        "gcp": 3.0,
        "s3": 2.5,
        "glue": 2.5,
        "lambda": 2.5,
        "postgres": 3.0,
        "mysql": 3.0,
        "mongodb": 2.5,
        "cassandra": 2.5,
        "dynamodb": 2.5
    },
    
    # ==========================================
    # 5. DEVOPS & CLOUD ENGINEERING
    # ==========================================
    "devops": {
        "docker": 4.0,
        "kubernetes": 4.0,
        "k8s": 4.0,
        "jenkins": 3.0,
        "ci/cd": 3.5,
        "cicd": 3.5,
        "gitlab": 2.5,
        "github actions": 3.0,
        "terraform": 3.5,
        "ansible": 3.0,
        "puppet": 2.5,
        "chef": 2.5,
        "aws": 4.0,
        "azure": 3.5,
        "gcp": 3.5,
        "google cloud": 3.5,
        "ec2": 2.5,
        "s3": 2.5,
        "iam": 2.0,
        "vpc": 2.0,
        "cloudformation": 2.5,
        "linux": 3.5,
        "bash": 3.0,
        "shell scripting": 3.0,
        "python": 3.0,
        "monitoring": 3.0,
        "prometheus": 3.0,
        "grafana": 3.0,
        "elk": 2.5,
        "elasticsearch": 2.5,
        "logstash": 2.0,
        "kibana": 2.0,
        "nagios": 2.0,
        "datadog": 2.5,
        "new relic": 2.0,
        "nginx": 2.5,
        "apache": 2.0,
        "load balancing": 2.5,
        "microservices": 3.0,
        "service mesh": 2.5,
        "istio": 2.5,
        "helm": 2.5,
        "argocd": 2.5,
        "gitops": 2.5
    },
    
    # ==========================================
    # 6. CYBERSECURITY
    # ==========================================
    "cybersecurity": {
        "cybersecurity": 4.0,
        "security": 3.5,
        "information security": 3.5,
        "ethical hacking": 4.0,
        "penetration testing": 4.0,
        "pen testing": 4.0,
        "vulnerability assessment": 3.5,
        "network security": 3.5,
        "cryptography": 3.5,
        "encryption": 3.0,
        "firewall": 3.0,
        "ids": 3.0,
        "ips": 3.0,
        "intrusion detection": 3.0,
        "siem": 3.5,
        "splunk": 3.0,
        "wireshark": 3.0,
        "metasploit": 3.5,
        "burp suite": 3.5,
        "nmap": 3.0,
        "kali linux": 3.5,
        "owasp": 3.0,
        "web application security": 3.5,
        "malware analysis": 3.5,
        "forensics": 3.0,
        "incident response": 3.5,
        "threat intelligence": 3.0,
        "security operations": 3.0,
        "soc": 3.0,
        "iso 27001": 2.5,
        "nist": 2.5,
        "compliance": 2.5,
        "gdpr": 2.0,
        "pci dss": 2.0,
        "vulnerability management": 3.0,
        "risk assessment": 3.0,
        "security audit": 3.0,
        "identity management": 2.5,
        "access control": 2.5,
        "zero trust": 2.5,
        "cloud security": 3.5,
        "aws security": 3.0,
        "azure security": 3.0
    },
    
    # ==========================================
    # 7. MOBILE DEVELOPMENT
    # ==========================================
    "mobile": {
        "android": 4.0,
        "ios": 4.0,
        "react native": 4.0,
        "flutter": 4.0,
        "dart": 3.5,
        "kotlin": 3.5,
        "swift": 3.5,
        "java": 3.0,
        "objective-c": 2.5,
        "mobile development": 3.5,
        "xamarin": 3.0,
        "ionic": 2.5,
        "cordova": 2.0,
        "firebase": 3.0,
        "push notifications": 2.5,
        "rest api": 3.0,
        "graphql": 2.5,
        "sqlite": 2.5,
        "realm": 2.0,
        "core data": 2.5,
        "ui/ux": 2.5,
        "app store": 2.0,
        "google play": 2.0,
        "mvvm": 2.5,
        "mvc": 2.0,
        "clean architecture": 2.5,
        "jetpack compose": 3.0,
        "swiftui": 3.0
    },
    
    # ==========================================
    # 8. BLOCKCHAIN & WEB3
    # ==========================================
    "blockchain": {
        "blockchain": 4.0,
        "ethereum": 4.0,
        "solidity": 4.0,
        "smart contracts": 4.0,
        "web3": 3.5,
        "web3.js": 3.5,
        "ethers.js": 3.5,
        "cryptocurrency": 3.0,
        "bitcoin": 3.0,
        "defi": 3.5,
        "nft": 3.0,
        "dapp": 3.5,
        "truffle": 3.0,
        "hardhat": 3.0,
        "metamask": 2.5,
        "ipfs": 2.5,
        "consensus algorithms": 3.0,
        "proof of work": 2.5,
        "proof of stake": 2.5,
        "hyperledger": 3.0,
        "polygon": 2.5,
        "binance smart chain": 2.5,
        "rust": 3.0,
        "solana": 3.0,
        "cardano": 2.5,
        "distributed systems": 3.0
    },
    
    # ==========================================
    # 9. GAME DEVELOPMENT
    # ==========================================
    "game_dev": {
        "unity": 4.0,
        "unreal engine": 4.0,
        "c#": 3.5,
        "c++": 3.5,
        "game development": 4.0,
        "3d modeling": 3.0,
        "2d graphics": 2.5,
        "game design": 3.5,
        "physics": 3.0,
        "animation": 3.0,
        "blender": 3.0,
        "maya": 3.0,
        "3ds max": 2.5,
        "opengl": 3.0,
        "directx": 3.0,
        "shader programming": 3.0,
        "multiplayer": 3.0,
        "networking": 2.5,
        "ar": 3.0,
        "vr": 3.0,
        "augmented reality": 3.0,
        "virtual reality": 3.0,
        "godot": 3.0,
        "cocos2d": 2.5,
        "photon": 2.5,
        "playfab": 2.0
    },
    
    # ==========================================
    # 10. UI/UX DESIGN
    # ==========================================
    "design": {
        "ui design": 4.0,
        "ux design": 4.0,
        "user interface": 3.5,
        "user experience": 3.5,
        "figma": 4.0,
        "adobe xd": 3.5,
        "sketch": 3.5,
        "photoshop": 3.0,
        "illustrator": 3.0,
        "wireframing": 3.5,
        "prototyping": 3.5,
        "user research": 3.5,
        "usability testing": 3.0,
        "design thinking": 3.0,
        "interaction design": 3.0,
        "visual design": 3.0,
        "typography": 2.5,
        "color theory": 2.5,
        "responsive design": 3.0,
        "mobile design": 3.0,
        "web design": 3.0,
        "design systems": 3.5,
        "accessibility": 3.0,
        "html": 2.5,
        "css": 2.5,
        "invision": 2.5,
        "zeplin": 2.0,
        "framer": 2.5,
        "principle": 2.0,
        "after effects": 2.5
    },
    
    # ==========================================
    # 11. ARTIFICIAL INTELLIGENCE
    # ==========================================
    "ai": {
        "artificial intelligence": 4.0,
        "ai": 4.0,
        "machine learning": 4.0,
        "deep learning": 4.0,
        "neural networks": 4.0,
        "tensorflow": 4.0,
        "pytorch": 4.0,
        "keras": 3.5,
        "transformers": 4.0,
        "bert": 3.5,
        "gpt": 3.5,
        "llm": 4.0,
        "large language models": 4.0,
        "nlp": 4.0,
        "computer vision": 4.0,
        "opencv": 3.5,
        "reinforcement learning": 3.5,
        "gan": 3.5,
        "generative ai": 4.0,
        "prompt engineering": 3.5,
        "langchain": 3.5,
        "hugging face": 3.5,
        "scikit-learn": 3.5,
        "python": 4.0,
        "numpy": 3.5,
        "pandas": 3.5,
        "model optimization": 3.0,
        "hyperparameter tuning": 3.0,
        "transfer learning": 3.5,
        "attention mechanisms": 3.5,
        "chatbots": 3.0,
        "conversational ai": 3.0,
        "speech recognition": 3.0,
        "recommendation systems": 3.0
    },
    
    # ==========================================
    # 12. QUALITY ASSURANCE & TESTING
    # ==========================================
    "qa_testing": {
        "testing": 3.5,
        "qa": 3.5,
        "quality assurance": 3.5,
        "test automation": 4.0,
        "selenium": 4.0,
        "cypress": 3.5,
        "playwright": 3.5,
        "jest": 3.0,
        "junit": 3.0,
        "testng": 3.0,
        "pytest": 3.0,
        "manual testing": 3.0,
        "test cases": 3.0,
        "test plans": 3.0,
        "regression testing": 3.0,
        "api testing": 3.5,
        "postman": 3.5,
        "rest assured": 3.0,
        "performance testing": 3.5,
        "jmeter": 3.5,
        "load testing": 3.0,
        "security testing": 3.0,
        "ui testing": 3.0,
        "integration testing": 3.0,
        "unit testing": 3.0,
        "bdd": 3.0,
        "tdd": 3.0,
        "cucumber": 3.0,
        "appium": 3.5,
        "mobile testing": 3.0,
        "sql": 2.5,
        "jira": 2.5,
        "bug tracking": 2.5,
        "test management": 2.5,
        "agile": 2.5,
        "scrum": 2.5,
        "ci/cd": 3.0
    },
    
    # ==========================================
    # 13. PRODUCT MANAGEMENT
    # ==========================================
    "product_management": {
        "product management": 4.0,
        "product strategy": 4.0,
        "roadmap": 3.5,
        "product roadmap": 3.5,
        "user stories": 3.5,
        "agile": 4.0,
        "scrum": 4.0,
        "jira": 3.5,
        "product development": 3.5,
        "market research": 3.5,
        "competitive analysis": 3.0,
        "user research": 3.5,
        "a/b testing": 3.0,
        "analytics": 3.5,
        "google analytics": 3.0,
        "mixpanel": 3.0,
        "amplitude": 3.0,
        "kpi": 3.0,
        "metrics": 3.0,
        "stakeholder management": 3.5,
        "prioritization": 3.5,
        "mvp": 3.0,
        "product launch": 3.0,
        "go-to-market": 3.0,
        "sql": 3.0,
        "wireframing": 2.5,
        "prototyping": 2.5,
        "figma": 2.5,
        "user experience": 3.0,
        "customer feedback": 3.0,
        "requirements gathering": 3.5
    },
    
    # ==========================================
    # 14. BUSINESS ANALYST
    # ==========================================
    "business_analyst": {
        "business analysis": 4.0,
        "requirements gathering": 4.0,
        "requirements analysis": 3.5,
        "business requirements": 3.5,
        "functional requirements": 3.5,
        "use cases": 3.5,
        "user stories": 3.5,
        "process modeling": 3.5,
        "bpmn": 3.0,
        "uml": 3.0,
        "data analysis": 3.5,
        "sql": 4.0,
        "excel": 3.5,
        "power bi": 3.5,
        "tableau": 3.5,
        "data visualization": 3.0,
        "stakeholder management": 3.5,
        "agile": 3.5,
        "scrum": 3.5,
        "jira": 3.0,
        "confluence": 2.5,
        "documentation": 3.5,
        "gap analysis": 3.0,
        "swot analysis": 3.0,
        "feasibility study": 3.0,
        "cost-benefit analysis": 3.0,
        "risk analysis": 3.0,
        "process improvement": 3.0,
        "change management": 3.0,
        "testing": 2.5,
        "uat": 3.0,
        "user acceptance testing": 3.0
    },
    
    # ==========================================
    # 15. DIGITAL MARKETING & SEO
    # ==========================================
    "digital_marketing": {
        "digital marketing": 4.0,
        "seo": 4.0,
        "search engine optimization": 4.0,
        "sem": 3.5,
        "google ads": 4.0,
        "ppc": 3.5,
        "social media marketing": 3.5,
        "smm": 3.5,
        "facebook ads": 3.5,
        "instagram marketing": 3.0,
        "linkedin marketing": 3.0,
        "content marketing": 3.5,
        "email marketing": 3.5,
        "google analytics": 4.0,
        "analytics": 3.5,
        "conversion optimization": 3.5,
        "cro": 3.5,
        "a/b testing": 3.0,
        "keyword research": 3.5,
        "link building": 3.0,
        "content strategy": 3.5,
        "copywriting": 3.0,
        "marketing automation": 3.0,
        "hubspot": 3.0,
        "mailchimp": 2.5,
        "wordpress": 3.0,
        "html": 2.0,
        "css": 2.0,
        "google search console": 3.0,
        "semrush": 3.0,
        "ahrefs": 3.0,
        "moz": 2.5,
        "campaign management": 3.5,
        "roi analysis": 3.0
    },
    
    # ==========================================
    # 16. CLOUD ARCHITECTURE
    # ==========================================
    "cloud_architect": {
        "cloud architecture": 4.0,
        "aws": 4.5,
        "azure": 4.0,
        "gcp": 4.0,
        "google cloud": 4.0,
        "cloud computing": 4.0,
        "microservices": 4.0,
        "serverless": 3.5,
        "lambda": 3.5,
        "s3": 3.0,
        "ec2": 3.5,
        "rds": 3.0,
        "dynamodb": 3.0,
        "cloudformation": 3.5,
        "terraform": 4.0,
        "infrastructure as code": 3.5,
        "iac": 3.5,
        "docker": 4.0,
        "kubernetes": 4.5,
        "eks": 3.5,
        "ecs": 3.0,
        "fargate": 2.5,
        "api gateway": 3.0,
        "load balancing": 3.5,
        "auto scaling": 3.0,
        "networking": 3.5,
        "vpc": 3.5,
        "cdn": 3.0,
        "cloudfront": 3.0,
        "security": 4.0,
        "iam": 3.5,
        "monitoring": 3.5,
        "cloudwatch": 3.0,
        "cost optimization": 3.5,
        "high availability": 3.5,
        "disaster recovery": 3.5,
        "multi-cloud": 3.0,
        "hybrid cloud": 3.0
    },
    
    # ==========================================
    # 17. GENERAL TOOLS & SOFT SKILLS
    # ==========================================
    "tools": {
        "git": 3.0,
        "github": 3.0,
        "gitlab": 2.5,
        "bitbucket": 2.0,
        "version control": 3.0,
        "debugging": 2.5,
        "problem solving": 3.0,
        "docker": 3.0,
        "jenkins": 2.5,
        "jira": 2.5,
        "confluence": 2.0,
        "slack": 1.5,
        "vs code": 2.0,
        "intellij": 2.0,
        "pycharm": 2.0,
        "postman": 2.5,
        "swagger": 2.0,
        "linux": 3.0,
        "unix": 2.5,
        "bash": 2.5,
        "shell scripting": 2.5,
        "vim": 1.5,
        "agile": 2.5,
        "scrum": 2.5,
        "kanban": 2.0,
        "rest": 3.0,
        "soap": 2.0,
        "json": 2.5,
        "xml": 2.0,
        "yaml": 2.0
    },
    
    "soft_skills": {
        "communication": 2.5,
        "presentation": 2.0,
        "teamwork": 2.5,
        "collaboration": 2.5,
        "leadership": 2.5,
        "confidence": 1.5,
        "analytical": 2.5,
        "critical thinking": 2.5,
        "problem solving": 3.0,
        "creativity": 2.0,
        "adaptability": 2.0,
        "time management": 2.0,
        "project management": 2.5,
        "client communication": 2.0,
        "stakeholder management": 2.5,
        "mentoring": 2.0,
        "documentation": 2.0,
        "research": 2.0,
        "learning": 2.0
    }
}

# ===============================
# CONTACT EXTRACTION
# ===============================
EMAIL_REGEX = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"

def extract_email(text):
    """Extract email with special character handling"""
    matches = re.findall(EMAIL_REGEX, text, re.IGNORECASE)
    
    if matches:
        for email in matches:
            if len(email) > 8 and '@' in email:
                return email.lower()
    
    return "—"

PHONE_PATTERNS = [
    r"\+91[-\s]?[6-9]\d{9}",
    r"\+91[-\s]?\d{10}",
    r"[6-9]\d{9}",
    r"\d{10}",
    r"\d{5}\s?\d{5}",
]

def extract_phone(text):
    """Extract phone with multiple pattern matching"""
    for pattern in PHONE_PATTERNS:
        matches = re.findall(pattern, text)
        if matches:
            phone = matches[0].replace(" ", "").replace("-", "")
            phone = re.sub(r'^\+91', '', phone)
            if len(phone) == 10:
                return phone
    
    return "—"

# ===============================
# FONT-BASED NAME EXTRACTION (NEW!)
# ===============================
INVALID_HEADERS = {
    "skills", "experience", "education",
    "projects", "summary", "profile",
    "objective", "certifications", "technical skills",
    "work experience", "personal details", "contact",
    "career objective", "professional summary",
    "technical", "about me", "declaration", "resume",
    "curriculum vitae", "cv"
}

LOCATION_KEYWORDS = {
    'nagar', 'city', 'delhi', 'mumbai', 'bangalore', 'pune', 'chennai',
    'hyderabad', 'kolkata', 'ahmedabad', 'lucknow', 'kanpur', 'meerut',
    'ghaziabad', 'noida', 'faridabad', 'gurgaon', 'uttar pradesh',
    'maharashtra', 'karnataka', 'tamil nadu', 'india', 'college',
    'university', 'institute', 'school', 'Pradesh'
}

def extract_candidate_name(text, metadata=None):
    """
    Extract name using FONT SIZE (largest text is usually the name)
    Falls back to other methods if font data unavailable
    """
    
    # STRATEGY 1: FONT-BASED EXTRACTION (MOST RELIABLE)
    if metadata and 'font_data' in metadata:
        name = extract_name_by_font(metadata['font_data'], text)
        if name and name != "Unknown Candidate":
            return name
    
    # STRATEGY 2: REGEX + POSITION (First valid name in first 20 lines)
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    
    for i, line in enumerate(lines[:20]):
        low = line.lower()
        
        # Skip headers
        if any(header in low for header in INVALID_HEADERS):
            continue
        
        # Skip locations
        if any(loc in low for loc in LOCATION_KEYWORDS):
            continue
        
        # Skip contact info
        if re.search(EMAIL_REGEX, line) or re.search(r'\d{5,}', line):
            continue
        
        # Skip special characters
        if re.search(r'[:|@#$%^&*()+=\[\]{};\'"<>?/\\]', line):
            continue
        
        # Skip too short/long
        if len(line) < 5 or len(line) > 40:
            continue
        
        # Valid name pattern: 2-4 capitalized words
        if re.fullmatch(r"[A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,3}", line):
            words = line.split()
            if 2 <= len(words) <= 4:
                common_words = {'technical', 'engineer', 'developer', 'software', 'senior', 'junior'}
                if not any(w.lower() in common_words for w in words):
                    return line.title()
    
# STRATEGY 3: NER with spaCy (SAFE GUARD)
if nlp:
    doc = nlp(text[:3000])

    for ent in doc.ents:
        if ent.label_ == "PERSON":
            low = ent.text.lower()

            if any(loc in low for loc in LOCATION_KEYWORDS):
                continue

            if any(header in low for header in INVALID_HEADERS):
                continue

            words = ent.text.split()
            if 2 <= len(words) <= 4 and not re.search(r'\d', ent.text):
                if all(
                    w[0].isupper() and w[1:].islower()
                    for w in words if len(w) > 1
                ):
                    return ent.text.title()


def extract_name_by_font(font_data, text):
    """
    Extract name by finding text with LARGEST font size
    This is the most reliable method - names are typically in largest font
    """
    if not font_data:
        return None
    
    # Group text by font size
    font_groups = {}
    current_text = ""
    current_size = None
    
    for char_info in font_data:
        char = char_info.get('text', '')
        size = round(char_info.get('size', 0), 1)
        
        if current_size is None:
            current_size = size
        
        # If same size, accumulate
        if abs(size - current_size) < 0.5:
            current_text += char
        else:
            # New size - save previous group
            if current_text.strip():
                if current_size not in font_groups:
                    font_groups[current_size] = []
                font_groups[current_size].append(current_text.strip())
            
            current_text = char
            current_size = size
    
    # Save last group
    if current_text.strip():
        if current_size not in font_groups:
            font_groups[current_size] = []
        font_groups[current_size].append(current_text.strip())
    
    # Find largest font size
    if not font_groups:
        return None
    
    largest_size = max(font_groups.keys())
    largest_texts = font_groups[largest_size]
    
    # Find valid name in largest font texts
    for text_chunk in largest_texts:
        # Combine consecutive words to form name
        words = text_chunk.split()
        
        # Try combinations of 2-4 consecutive words
        for i in range(len(words)):
            for length in [4, 3, 2]:  # Try longer names first
                if i + length <= len(words):
                    potential_name = " ".join(words[i:i+length])
                    
                    if is_valid_name(potential_name):
                        return potential_name.title()
    
    return None

def is_valid_name(name):
    """
    Validate if text is a proper name
    """
    # Basic checks
    if len(name) < 5 or len(name) > 40:
        return False
    
    # Must be mostly letters
    if not re.match(r'^[A-Za-z\s]+$', name):
        return False
    
    words = name.split()
    if len(words) < 2 or len(words) > 4:
        return False
    
    low = name.lower()
    
    # Check against invalid headers
    if any(header in low for header in INVALID_HEADERS):
        return False
    
    # Check against locations
    if any(loc in low for loc in LOCATION_KEYWORDS):
        return False
    
    # Each word should be properly capitalized
    for word in words:
        if len(word) < 2:
            return False
        if not word[0].isupper():
            return False
    
    return True

# ===============================
# SKILL EXTRACTION
# ===============================
def extract_jd_skills(job_desc):
    """Extract skills from job description"""
    text = job_desc.lower()
    jd_skills = {}

    for domain in SKILL_ONTOLOGY.values():
        for skill, weight in domain.items():
            pattern = r'\b' + re.escape(skill) + r'\b'
            if re.search(pattern, text):
                jd_skills[skill] = weight

    return jd_skills

def extract_resume_skills(resume_text, jd_skills):
    """Extract matching skills from resume"""
    text = resume_text.lower()
    found = {}

    for skill, weight in jd_skills.items():
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, text):
            found[skill] = weight

    return found

# ===============================
# MAIN ANALYZER
# ===============================
def analyze_resumes(resume_files, job_desc):
    """
    Analyze resumes with font-based name extraction
    """
    if not resume_files or not job_desc.strip():
        return []

    jd_skills = extract_jd_skills(job_desc)
    job_desc_clean = clean_text(job_desc)

    results = []

    for file in resume_files:
        try:
            # Extract text + metadata (including font info)
            extraction_result = extract_text(file)
            
            # Handle tuple unpacking
            if isinstance(extraction_result, tuple):
                raw_text, metadata = extraction_result
            else:
                raw_text = extraction_result
                metadata = {}
            
            clean_resume = clean_text(raw_text)

            # Use font-based name extraction
            name = extract_candidate_name(raw_text, metadata)
            email = extract_email(raw_text)
            phone = extract_phone(raw_text)

            resume_skills = extract_resume_skills(raw_text, jd_skills)

            matched_skills = set(resume_skills.keys())
            missing_skills = set(jd_skills.keys()) - matched_skills

            # SCORING
            total_weight = sum(jd_skills.values())
            matched_weight = sum(resume_skills.values())

            skill_coverage = matched_weight / total_weight if total_weight else 0
            skill_count_score = len(matched_skills) / len(jd_skills) if jd_skills else 0

            try:
                tfidf = TfidfVectorizer(ngram_range=(1, 2), max_features=500)
                vectors = tfidf.fit_transform([clean_resume, job_desc_clean])
                semantic_similarity = cosine_similarity(
                    vectors[0:1], vectors[1:2]
                )[0][0]
            except:
                semantic_similarity = 0.0

            base_score = (
                0.50 * skill_coverage +
                0.30 * skill_count_score +
                0.20 * semantic_similarity
            )
            
            critical_skills = {'react', 'reactjs', 'javascript', 'js', 'html', 'css', 'python', 'java'}
            critical_matched = len(matched_skills & critical_skills)
            critical_bonus = (critical_matched / 4) * 0.15
            
            final_score = round(
                min((base_score + critical_bonus) * 100, 100),
                2
            )

            results.append({
                "Candidate": name,
                "Email": email,
                "Phone": phone,
                "Matching Percentage": final_score,
                "Matched Skills": ", ".join(sorted(matched_skills)) or "—",
                "Missing Skills": ", ".join(sorted(missing_skills)) or "—"
            })

        except Exception as e:
            print(f"Error processing {file.name}: {str(e)}")
            continue

    results.sort(key=lambda x: x["Matching Percentage"], reverse=True)
    return results