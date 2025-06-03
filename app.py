# app.py

import streamlit as st
import base64
import re
from PIL import Image

# --- FUNCTIONS ---
def check_opt_in_compliance(text):
    issues = []
    snippets = []

    if not re.search(r"(?i)i\s+agree\s+to\s+receive|consent\s+to\s+receive", text):
        issues.append("❌ Consent to receive messages")
        snippets.append("✉️ Please ensure your opt-in message includes: 'I agree to receive recurring SMS updates from [Your Brand Name].'")

    if not re.search(r"(?i)message\s+frequency\s+may\s+vary", text):
        issues.append("❌ Message frequency disclosed")
        snippets.append("✉️ Please include: 'Message frequency may vary.'")

    if not ("STOP" in text.upper() and "HELP" in text.upper()):
        issues.append("❌ STOP/HELP instructions")
        snippets.append("✉️ Please include opt-out info: 'Reply STOP to unsubscribe or HELP for help.'")

    if not re.search(r"(?i)privacy\s+policy|terms\s+of\s+service", text):
        issues.append("❌ Link to privacy policy or terms")
        snippets.append("✉️ Please include a link to your privacy policy or terms of service in the opt-in flow.")

    return issues, snippets

def check_privacy_compliance(text):
    issues = []
    snippets = []

    if not re.search(r"(?i)data (we )?collect|information you provide", text):
        issues.append("❌ Data collection explained")
        snippets.append("✉️ Please update your privacy policy to explain what data is collected from users.")

    if not re.search(r"(?i)opt[- ]?out", text):
        issues.append("❌ Opt-out process available")
        snippets.append("✉️ Please describe how users can opt out of your messages or services.")

    if not re.search(r"(?i)third[- ]?part(y|ies)", text):
        issues.append("❌ Data sharing practices disclosed")
        snippets.append("✉️ Please mention whether data is shared with third parties or affiliates.")

    if not re.search(r"(?i)no mobile information will be shared with third parties.*?promotional purposes", text):
        issues.append("❌ SMS disclosure")
        snippets.append("✉️ Include this standard disclosure: 'No mobile information will be shared with third parties or affiliates for marketing/promotional purposes.'")

    return issues, snippets

# --- PAGE CONFIG ---
st.set_page_config("A2P Compliance Assistant", layout="wide")
st.title("📱 A2P Compliance Assistant")
st.caption("Easily verify A2P 10DLC & Toll-Free opt-in flows and privacy policies for compliance.")
st.markdown("---")

# --- SIDE BY SIDE INPUTS ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("📥 Opt-In Flow")
    optin_text = st.text_area("Paste opt-in text, URL, or description", height=80)
    optin_img = st.file_uploader("...or upload an image (screenshot of opt-in flow)", type=["png", "jpg", "jpeg"], key="optin")
    if optin_text or optin_img:
        if optin_img:
            image = Image.open(optin_img)
            st.image(image, caption="Opt-In Flow Screenshot", use_column_width=True)
        issues, snippets = check_opt_in_compliance(optin_text if optin_text else "")
        st.markdown("### 📋 Compliance Check")
        if not issues:
            st.success("✅ Opt-in flow is Compliant")
        elif len(issues) < 4:
            st.warning("⚠️ Opt-in flow is Partially Compliant")
        else:
            st.error("❌ Opt-in flow is Not Compliant")
        for i, issue in enumerate(issues):
            st.error(issue)
            st.code(snippets[i], language="text")

with col2:
    st.subheader("🔐 Privacy Policy")
    privacy_text = st.text_area("Paste privacy policy text, URL, or description", height=80)
    privacy_img = st.file_uploader("...or upload an image (screenshot of privacy policy)", type=["png", "jpg", "jpeg"], key="privacy")
    if privacy_text or privacy_img:
        if privacy_img:
            image = Image.open(privacy_img)
            st.image(image, caption="Privacy Policy Screenshot", use_column_width=True)
        issues, snippets = check_privacy_compliance(privacy_text if privacy_text else "")
        st.markdown("### 📋 Compliance Check")
        if not issues:
            st.success("✅ Privacy Policy is Compliant")
        elif len(issues) < 4:
            st.warning("⚠️ Privacy Policy is Partially Compliant")
        else:
            st.error("❌ Privacy Policy is Not Compliant")
        for i, issue in enumerate(issues):
            st.error(issue)
            st.code(snippets[i], language="text")

# --- FOOTER ---
st.markdown("---")
st.caption("Created by Monica Prasad · mprasad@twilio.com · Internal Use Only")
