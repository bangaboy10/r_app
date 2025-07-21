import pytesseract
from PIL import Image
from pdf2image import convert_from_path
import re
from datetime import datetime

# Set Tesseract path for Windows
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_text_from_image(file):
    image = Image.open(file)
    return pytesseract.image_to_string(image)

def extract_text_from_pdf(file_path):
    pages = convert_from_path(file_path)  # ✅ Expects a file path (not BytesIO)
    text = ""
    for page in pages:
        text += pytesseract.image_to_string(page)
    return text

def parse_receipt_text(text):
    vendor = re.findall(r"(Amazon|Flipkart|Airtel|Reliance|Vodafone|BigBazaar)", text, re.IGNORECASE)
    date = re.findall(r"\d{2}/\d{2}/\d{4}", text)
    amount = re.findall(r'₹\s?(\d+(?:\.\d{2})?)', text)

    return {
        "vendor": vendor[0] if vendor else "Unknown",
        "date": datetime.strptime(date[0], "%d/%m/%Y") if date else datetime.now(),
        "amount": float(amount[0]) if amount else 0.0,
        "category": "Auto"  # Optionally map by vendor
    }
