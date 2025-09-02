import pytesseract
from PIL import Image
import requests
from bs4 import BeautifulSoup
import io

def extract_text_from_image(uploaded_file):
    image = Image.open(uploaded_file)
    text = pytesseract.image_to_string(image)
    return text

def extract_text_from_url(url):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup.get_text(separator=' ')
    except Exception as e:
        return f"Failed to fetch content from URL: {e}"
