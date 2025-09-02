import re
import requests
from bs4 import BeautifulSoup
from PIL import Image
import pytesseract


def contains_required_language(text: str, patterns: list) -> list:
    matches = []
    for pattern in patterns:
        if re.search(pattern, text, re.IGNORECASE):
            matches.append(pattern)
    return matches


def extract_noncompliant_phrases(text: str, blocked_patterns: list) -> list:
    violations = []
    for pattern in blocked_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            violations.append(pattern)
    return violations


def extract_text_from_image(image_file) -> str:
    try:
        image = Image.open(image_file)
        return pytesseract.image_to_string(image)
    except Exception as e:
        return f"OCR failed: {e}"


def extract_text_from_url(url: str) -> str:
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup.get_text(separator=' ', strip=True)
    except Exception as e:
        return f"Failed to fetch or parse URL: {e}"
