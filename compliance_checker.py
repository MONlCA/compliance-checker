import streamlit as st
from PIL import Image
import pytesseract
import requests
from bs4 import BeautifulSoup
import io
import os

# Try to point pytesseract to the Tesseract executable
if not os.path.exists(pytesseract.pytesseract.tesseract_cmd):
    pytesseract.pytesseract.tesseract_cmd = "/usr/local/bin/tesseract"  # Default for Mac Homebrew

st.set_page_config(page_title="📲 A2P 10DLC & Toll-Free Compliance Assistant")
st.title("📲 A2P 10DLC & Toll-Free Compliance Assistant")

st.header("📷 Opt-In Flow Screenshot Compliance")
uploaded_file = st.file_uploader("Upload a screenshot of the opt-in flow", type=["png", "jpg", "jpeg"])

# Section for privacy policy check
st.header("🔗 Privacy Policy Compliance Check")
privacy_policy_url = st.text_input("Paste the privacy policy URL")

# Use uploaded screenshot only
image_source = uploaded_file

if image_source:
    st.image(image_source, caption="Uploaded Screenshot", use_container_width=True)
    image = Image.open(image_source)
    try:
        extracted_text = pytesseract.image_to_string(image)

        st.subheader("Extracted Text from Screenshot")
        st.text_area("Opt-In Text Detected:", extracted_text, height=200)

        st.subheader("Compliance Results (Screenshot)")
        issues = []
        if "consent" not in extracted_text.lower():
            issues.append("❌ Missing clear consent language")
        if "stop" not in extracted_text.lower():
            issues.append("❌ Missing opt-out instructions (e.g., 'STOP to cancel')")
        if "terms" not in extracted_text.lower():
            issues.append("❌ Missing reference to Terms of Service or Privacy Policy")

        if issues:
            for issue in issues:
                st.write(issue)
        else:
            st.success("✅ Screenshot appears compliant with A2P 10DLC and Toll-Free requirements.")
    except pytesseract.pytesseract.TesseractNotFoundError:
        st.error("Tesseract OCR not found. Please ensure it is installed and in your PATH.")

if privacy_policy_url:
    st.subheader("Fetched Privacy Policy Text")
    try:
        response = requests.get(privacy_policy_url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text()
        st.text_area("Privacy Policy Content:", text[:5000], height=200)

        st.subheader("Compliance Results (Privacy Policy)")
        pp_issues = []
        if "data" not in text.lower():
            pp_issues.append("❌ No mention of data collection or usage.")
        if "consent" not in text.lower():
            pp_issues.append("❌ No mention of user consent or opt-in/opt-out.")
        if "third party" not in text.lower() and "share" not in text.lower():
            pp_issues.append("❌ No mention of third-party data sharing or disclosure.")

        if pp_issues:
            for issue in pp_issues:
                st.write(issue)
        else:
            st.success("✅ Privacy Policy appears to meet standard compliance indicators.")

    except Exception as e:
        st.error(f"Failed to fetch or parse the privacy policy: {e}")
