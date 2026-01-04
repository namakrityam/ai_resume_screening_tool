import spacy
import re
from functools import lru_cache

# ===============================
# LOAD SPACY MODEL (OPTIMIZED)
# ===============================
try:
    nlp = spacy.load("en_core_web_sm", disable=["ner", "parser"])  # Faster: only tokenizer + POS
except:
    print("⚠️ spaCy model not found. Run: python -m spacy download en_core_web_sm")
    nlp = None

# ===============================
# MAIN CLEANING FUNCTION (ENHANCED)
# ===============================
@lru_cache(maxsize=128)  # Cache cleaned text to avoid reprocessing
def clean_text(text):
    """
    Enhanced text cleaning with:
    - Stop word removal
    - Special character removal
    - Number removal
    - Whitespace normalization
    - Lemmatization (optional)
    """
    if not text or not isinstance(text, str):
        return ""
    
    # Pre-processing: normalize whitespace and lowercase
    text = text.lower().strip()
    text = re.sub(r'\s+', ' ', text)  # Multiple spaces to single space
    
    # Remove URLs
    text = re.sub(r'http\S+|www\.\S+', '', text)
    
    # Remove email addresses (keep emails separate for extraction)
    text = re.sub(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', '', text)
    
    # Remove phone numbers (keep separate for extraction)
    text = re.sub(r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]', '', text)
    
    # Remove special characters but keep hyphens in compound words
    text = re.sub(r'[^\w\s-]', ' ', text)
    
    # Remove standalone numbers (but keep alphanumeric like "c++", "html5")
    text = re.sub(r'\b\d+\b', '', text)
    
    # Use spaCy for advanced cleaning
    if nlp:
        doc = nlp(text)
        tokens = []
        
        for token in doc:
            # Keep only:
            # - Alphabetic tokens (excluding pure numbers)
            # - Not stop words
            # - Length > 2 (avoid noise like "is", "a")
            if token.is_alpha and not token.is_stop and len(token.text) > 2:
                # Use lemma for better matching (e.g., "programming" -> "program")
                tokens.append(token.lemma_)
        
        return " ".join(tokens)
    
    # Fallback if spaCy not available: basic cleaning
    else:
        # Remove common stop words manually
        stop_words = {
            'the', 'is', 'at', 'which', 'on', 'and', 'a', 'an', 'as', 'are',
            'was', 'were', 'been', 'be', 'have', 'has', 'had', 'do', 'does',
            'did', 'will', 'would', 'should', 'could', 'may', 'might', 'must',
            'can', 'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she',
            'it', 'we', 'they', 'what', 'who', 'when', 'where', 'why', 'how',
            'all', 'each', 'every', 'both', 'few', 'more', 'most', 'other',
            'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so',
            'than', 'too', 'very', 'can', 'just', 'should', 'now'
        }
        
        words = text.split()
        filtered_words = [w for w in words if w not in stop_words and len(w) > 2]
        return " ".join(filtered_words)

# ===============================
# ADDITIONAL UTILITY FUNCTIONS
# ===============================
def clean_skill_text(text):
    """
    Specialized cleaning for skill extraction (preserves technical terms)
    """
    if not text:
        return ""
    
    text = text.lower().strip()
    
    # Keep important technical punctuation
    # e.g., "c++", "node.js", "asp.net"
    text = re.sub(r'(?<![+.])[^\w\s+.-](?![+.])', ' ', text)
    
    # Normalize spaces
    text = re.sub(r'\s+', ' ', text)
    
    return text

def extract_key_phrases(text, top_n=20):
    """
    Extract most important phrases using simple frequency analysis
    Useful for quick skill/keyword identification
    """
    if not nlp or not text:
        return []
    
    # Clean text
    clean = clean_text(text)
    
    # Get word frequency
    words = clean.split()
    from collections import Counter
    word_freq = Counter(words)
    
    # Return top N most common words
    return [word for word, count in word_freq.most_common(top_n)]

def preserve_technical_terms(text):
    """
    Preserve important technical terms during cleaning
    (for use before main clean_text if needed)
    """
    # Protect common technical terms from being split
    protected_terms = {
        'machine learning': 'machinelearning',
        'deep learning': 'deeplearning',
        'data science': 'datascience',
        'artificial intelligence': 'artificialintelligence',
        'computer vision': 'computervision',
        'natural language processing': 'naturallanguageprocessing',
        'rest api': 'restapi',
        'version control': 'versioncontrol',
        'web development': 'webdevelopment',
        'mobile development': 'mobiledevelopment',
        'cloud computing': 'cloudcomputing',
        'problem solving': 'problemsolving',
    }
    
    text_lower = text.lower()
    for term, replacement in protected_terms.items():
        text_lower = text_lower.replace(term, replacement)
    
    return text_lower

def remove_noise_words(text):
    """
    Remove resume-specific noise words that don't add value
    """
    noise_patterns = [
        r'\b(resume|curriculum vitae|cv|page \d+)\b',
        r'\b(references available upon request)\b',
        r'\b(confidential|private|personal)\b',
        r'\b(january|february|march|april|may|june|july|august|september|october|november|december)\b',
        r'\b(mon|tue|wed|thu|fri|sat|sun)\b',
        r'\b(mr|mrs|ms|dr|prof)\b',
    ]
    
    for pattern in noise_patterns:
        text = re.sub(pattern, '', text, flags=re.IGNORECASE)
    
    return text

# ===============================
# BATCH PROCESSING (PERFORMANCE)
# ===============================
def clean_texts_batch(texts):
    """
    Clean multiple texts efficiently using spaCy's pipe
    Much faster for processing many resumes
    """
    if not nlp or not texts:
        return [clean_text(t) for t in texts]
    
    cleaned = []
    
    # Use spaCy's pipe for batch processing (much faster)
    for doc in nlp.pipe(texts, batch_size=50):
        tokens = []
        for token in doc:
            if token.is_alpha and not token.is_stop and len(token.text) > 2:
                tokens.append(token.lemma_)
        cleaned.append(" ".join(tokens))
    
    return cleaned

# ===============================
# QUALITY CHECKS
# ===============================
def validate_cleaned_text(original, cleaned):
    """
    Ensure cleaning didn't remove too much important content
    Returns True if cleaning was successful, False if too aggressive
    """
    if not cleaned or len(cleaned) < 20:
        return False
    
    # Check if we retained at least 20% of original length
    ratio = len(cleaned) / len(original) if original else 0
    
    if ratio < 0.1:  # Less than 10% retained - likely too aggressive
        return False
    
    return True

# ===============================
# UTILITY FOR DEBUGGING
# ===============================
def compare_cleaning(text):
    """
    Debug function to see before/after cleaning
    Useful for testing
    """
    print("=" * 50)
    print("ORIGINAL TEXT:")
    print(text[:200] + "..." if len(text) > 200 else text)
    print("\n" + "=" * 50)
    print("CLEANED TEXT:")
    cleaned = clean_text(text)
    print(cleaned[:200] + "..." if len(cleaned) > 200 else cleaned)
    print("=" * 50)
    print(f"Original length: {len(text)}")
    print(f"Cleaned length: {len(cleaned)}")
    print(f"Retention ratio: {len(cleaned)/len(text)*100:.1f}%")
    return cleaned