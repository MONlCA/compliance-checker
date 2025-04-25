import streamlit as st
from PIL import Image
import pytesseract
import requests
from bs4 import BeautifulSoup
import io
import os
import fitz  # PyMuPDF for PDF

# --- APP CONFIG ---
st.set_page_config(
    page_title="📲 A2P Compliance Assistant",
    page_icon="📲",
    layout="centered"
)

# Set up pytesseract path if needed
if not os.path.exists(pytesseract.pytesseract.tesseract_cmd):
    pytesseract.pytesseract.tesseract_cmd = "/usr/local/bin/tesseract"

# --- PASSWORD PROTECTION ---
PASSWORD = os.getenv("APP_PASSWORD")
if PASSWORD:
    st.title("🔒 Secure Access")
    pwd = st.text_input("Enter app password", type="password")
    if pwd != PASSWORD:
        st.warning("Incorrect password")
        st.stop()

# --- HEADER STYLES ---
st.markdown("""
<style>
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

# --- OPT-IN FLOW UPLOAD ---
st.header("📷 Opt-In Flow Screenshot Compliance")
uploaded_file = st.file_uploader("Upload a screenshot or PDF of the opt-in flow", type=["png", "jpg", "jpeg", "pdf"])

# --- PRIVACY POLICY ---
st.header("🔗 Privacy Policy Compliance Check")
privacy_policy_url = st.text_input("Paste the privacy policy URL")

def dummy_opt_in_feedback(text):
    return "✅ Text appears to be mostly compliant. Make sure your opt-in clearly states:\n- Who is sending the messages\n- That consent is not a condition of purchase\n- How to opt-out (STOP/HELP keywords)"

def dummy_privacy_policy_feedback(text):
    return "📋 Privacy policy review:\n- Ensure the document covers data collection, sharing, and contact info\n- Add explicit mention of SMS consent and opt-out rights if missing"

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

    if extracted_text.strip():
        with st.spinner("Simulating opt-in analysis..."):
            st.subheader("GPT Compliance Analysis (Screenshot or PDF)")
            st.write(dummy_opt_in_feedback(extracted_text))
    else:
        st.warning("No text was extracted from the uploaded file. Please try another image or PDF.")

if privacy_policy_url:
    st.subheader("Fetched Privacy Policy Text")
    try:
        response = requests.get(privacy_policy_url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text()
        st.text_area("Privacy Policy Content:", text[:5000], height=200)

        with st.spinner("Simulating privacy policy analysis..."):
            st.subheader("GPT Compliance Analysis (Privacy Policy)")
            st.write(dummy_privacy_policy_feedback(text[:4000]))
    except Exception as e:
        st.error(f"Failed to fetch or parse the privacy policy: {e}")
