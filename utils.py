import re
import requests
from PIL import Image
import pytesseract

def extract_text_from_image(image_file):
    image = Image.open(image_file)
    return pytesseract.image_to_string(image)

def extract_text_from_url(url):
    try:
        response = requests.get(url, timeout=5)
        if response.ok:
            return response.text
    except Exception as e:
        return f"[Error fetching URL: {e}]"
    return ""

def contains_required_language(text: str, patterns: list) -> tuple:
    found = []
    missing = []
    for pattern in patterns:
        if re.search(pattern, text, re.IGNORECASE):
            found.append(pattern)
        else:
            missing.append(pattern)
    return found, missing

def extract_noncompliant_phrases(text: str, blocked_patterns: list) -> list:
    found = []
    for pattern in blocked_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            found.append(pattern)
    return found
