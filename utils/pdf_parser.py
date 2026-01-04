from docx import Document
from PIL import Image
import pdfplumber
import io
import os
import platform

# ===============================
# OPTIONAL OCR SUPPORT (CLOUD SAFE)
# ===============================
try:
    import pytesseract
    from pdf2image import convert_from_path
    OCR_ENABLED = True
except ImportError:
    OCR_ENABLED = False

# ===============================
# TESSERACT PATH CONFIGURATION
# ===============================
def setup_tesseract():
    """Auto-detect Tesseract installation path"""
    if not OCR_ENABLED:
        return False

    system = platform.system()

    if system == "Windows":
        possible_paths = [
            r"C:\Program Files\Tesseract-OCR\tesseract.exe",
            r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
            r"C:\Users\{}\AppData\Local\Programs\Tesseract-OCR\tesseract.exe".format(
                os.getenv('USERNAME')
            )
        ]

        for path in possible_paths:
            if os.path.exists(path):
                pytesseract.pytesseract.tesseract_cmd = path
                return True

        print("WARNING: Tesseract not found. OCR fallback may not work.")
        return False

    return True

if OCR_ENABLED:
    setup_tesseract()

# ===============================
# TEXT + METADATA EXTRACTION
# ===============================
def extract_text(file):
    """
    Main entry point - returns tuple (text, metadata)
    metadata includes font sizes for name detection
    """
    if file.name.endswith(".pdf"):
        return extract_pdf(file)
    elif file.name.endswith(".docx"):
        text = extract_docx(file)
        return text, {}
    return "", {}

def extract_pdf(file):
    """
    Extract text and font metadata from PDF
    Returns: (text, metadata_dict)
    """
    text = ""
    font_data = []  # Store (text, font_size) pairs

    try:
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                try:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"

                    chars = page.chars
                    if chars:
                        for char in chars:
                            if 'text' in char and 'size' in char:
                                font_data.append({
                                    'text': char['text'],
                                    'size': char['size']
                                })

                except Exception:
                    continue

    except Exception as e:
        print(f"Error with pdfplumber: {e}")

    metadata = {'font_data': font_data}

    if is_text_meaningful(text):
        return text, metadata

    # OCR fallback (ONLY if enabled)
    if OCR_ENABLED:
        print(f"⚠️ Image-based PDF detected: {file.name}. Using OCR...")
        ocr_text = extract_pdf_with_ocr(file)
        return ocr_text, {}

    print("⚠️ OCR disabled. Skipping image-based PDF.")
    return "", {}

def is_text_meaningful(text):
    """Check if extracted text is meaningful"""
    if not text or len(text.strip()) < 50:
        return False
    alpha_chars = sum(c.isalpha() for c in text)
    return alpha_chars > 20

def extract_pdf_with_ocr(file):
    """OCR-based extraction for image PDFs"""
    if not OCR_ENABLED:
        return ""

    text = ""

    try:
        temp_path = f"temp_{file.name}"

        with open(temp_path, "wb") as f:
            f.write(file.getbuffer())

        try:
            images = convert_from_path(temp_path, dpi=300)
        except Exception as e:
            print(f"Error converting PDF: {e}")
            if os.path.exists(temp_path):
                os.remove(temp_path)
            return ""

        for i, image in enumerate(images):
            try:
                page_text = pytesseract.image_to_string(
                    image,
                    lang='eng',
                    config='--psm 6'
                )

                if page_text:
                    text += page_text + "\n"

            except Exception as e:
                print(f"Error OCR page {i+1}: {e}")
                continue

        if os.path.exists(temp_path):
            os.remove(temp_path)

        text = clean_ocr_text(text)
        return text

    except Exception as e:
        print(f"OCR failed: {e}")
        return ""

def clean_ocr_text(text):
    """Clean OCR artifacts"""
    import re

    text = re.sub(r' +', ' ', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r'[|]', 'I', text)
    text = re.sub(r'[\x00-\x08\x0b-\x0c\x0e-\x1f\x7f-\x9f]', '', text)

    ocr_fixes = {
        r'\bJavascript\b': 'JavaScript',
        r'\bReactjs\b': 'React',
        r'\bNodejs\b': 'Node',
        r'\bHtml\b': 'HTML',
        r'\bCss\b': 'CSS',
        r'\bApi\b': 'API',
        r'\bPython\b': 'Python',
        r'\bJava\b': 'Java',
    }

    for pattern, replacement in ocr_fixes.items():
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)

    return text.strip()

def extract_docx(file):
    """Extract text from DOCX"""
    try:
        doc = Document(file)
        text = "\n".join(p.text for p in doc.paragraphs if p.text.strip())
        return text
    except Exception as e:
        print(f"Error extracting DOCX: {e}")
        return ""

def test_ocr_availability():
    """Test OCR configuration"""
    if not OCR_ENABLED:
        return False
    try:
        test_img = Image.new('RGB', (200, 50), color='white')
        pytesseract.image_to_string(test_img)
        return True
    except:
        return False

if OCR_ENABLED:
    if not test_ocr_availability():
        print("⚠️ WARNING: OCR not configured. Image PDFs may not work.")
