import streamlit as st
from PIL import Image
import pytesseract
import requests
from bs4 import BeautifulSoup
from openai import OpenAI
import io
import os
import fitz  # PyMuPDF for PDF

# --- APP CONFIG ---
st.set_page_config(
    page_title="📲 A2P Compliance Assistant",
    page_icon="📲",
    layout="centered"
)

# Set your OpenAI API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Try to point pytesseract to the Tesseract executable
if not os.path.exists(pytesseract.pytesseract.tesseract_cmd):
    pytesseract.pytesseract.tesseract_cmd = "/usr/local/bin/tesseract"

# --- AUTH ---
PASSWORD = os.getenv("APP_PASSWORD")
if PASSWORD:
    st.title("🔒 Secure Access")
    pwd = st.text_input("Enter app password", type="password")
    if pwd != PASSWORD:
        st.warning("Incorrect password")
        st.stop()

# --- HEADER ---
st.markdown("""
<style>
    .css-18e3th9 {
        background-color: #0E1117;
    }
    .stApp {
        background-color: #0E1117;
        color: white;
    }
    .title-style {
        font-size: 2.5em;
        font-weight: bold;
        text-align: center;
        color: white;
        padding-bottom: 0.5em;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="title-style">📲 A2P 10DLC & Toll-Free Compliance Assistant</div>
""", unsafe_allow_html=True)

st.header("📷 Opt-In Flow Screenshot Compliance")
uploaded_file = st.file_uploader("Upload a screenshot or PDF of the opt-in flow", type=["png", "jpg", "jpeg", "pdf"])

# Section for privacy policy check
st.header("🔗 Privacy Policy Compliance Check")
privacy_policy_url = st.text_input("Paste the privacy policy URL")

if uploaded_file:
    file_type = uploaded_file.type
    extracted_text = ""
    if file_type == "application/pdf":
        doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        for page in doc:
            extracted_text += page.get_text()
    else:
        image = Image.open(uploaded_file)
        extracted_text = pytesseract.image_to_string(image)
        st.image(image, caption="Uploaded Screenshot", use_container_width=True)

    st.subheader("Extracted Text from Uploaded File")
    st.text_area("Opt-In Text Detected:", extracted_text, height=200)

    # GPT Analysis
    with st.spinner("Analyzing opt-in text with GPT..."):
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert in SMS and email marketing compliance, particularly for A2P 10DLC and Toll-Free verification."},
                {"role": "user", "content": f"Please review the following opt-in flow text and identify any compliance issues for A2P 10DLC and Toll-Free requirements. Text:\n{extracted_text}"}
            ]
        )
        gpt_feedback = response.choices[0].message.content
        st.subheader("GPT Compliance Analysis (Screenshot or PDF)")
        st.write(gpt_feedback)

if privacy_policy_url:
    st.subheader("Fetched Privacy Policy Text")
    try:
        response = requests.get(privacy_policy_url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text()
        st.text_area("Privacy Policy Content:", text[:5000], height=200)

        with st.spinner("Analyzing privacy policy with GPT..."):
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert in digital privacy compliance and must evaluate website privacy policies."},
                    {"role": "user", "content": f"Please review the following privacy policy text and identify any compliance gaps or concerns relevant to data collection, consent, and third-party sharing:\n{text[:4000]}"}
                ]
            )
            gpt_feedback = response.choices[0].message.content
            st.subheader("GPT Compliance Analysis (Privacy Policy)")
            st.write(gpt_feedback)

    except Exception as e:
        st.error(f"Failed to fetch or parse the privacy policy: {e}")
