# app.py (Updated layout and simplified compliance summary)

import streamlit as st
import base64
import re
from PIL import Image

# --- FUNCTIONS ---
def check_opt_in_compliance(text):
    issues = []

    if not re.search(r"(?i)i\s+agree\s+to\s+receive|consent\s+to\s+receive", text):
        issues.append("❌ Consent to receive messages")

    if not re.search(r"(?i)message\s+frequency\s+may\s+vary", text):
        issues.append("❌ Message frequency disclosed")

    if not ("STOP" in text.upper() and "HELP" in text.upper()):
        issues.append("❌ STOP/HELP instructions")

    if not re.search(r"(?i)privacy\s+policy|terms\s+of\s+service", text):
        issues.append("❌ Link to privacy policy or terms")

    return issues

def check_privacy_compliance(text):
    issues = []

    if not re.search(r"(?i)data (we )?collect|information you provide", text):
        issues.append("❌ Data collection explained")

    if not re.search(r"(?i)opt[- ]?out", text):
        issues.append("❌ Opt-out process available")

    if not re.search(r"(?i)third[- ]?part(y|ies)", text):
        issues.append("❌ Data sharing practices disclosed")

    if not re.search(r"(?i)no mobile information will be shared with third parties.*?promotional purposes", text):
        issues.append("❌ SMS disclosure")

    return issues

# --- UI LAYOUT ---
st.set_page_config("A2P Compliance Assistant", layout="wide")
st.title("📱 A2P Compliance Assistant")
st.caption("Easily verify A2P 10DLC & Toll-Free opt-in flows and privacy policies for compliance.")
st.markdown("---")

# --- SIDE BY SIDE ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("📥 Opt-In Flow")
    optin_text = st.text_area("Paste opt-in text, URL, or description here", height=100)
    optin_issues = []
    if optin_text:
        optin_issues = check_opt_in_compliance(optin_text)
        st.markdown("### 📋 Compliance Check")
        if not optin_issues:
            st.success("✅ Opt-in flow is Compliant")
        elif len(optin_issues) < 4:
            st.warning("⚠️ Opt-in flow is Partially Compliant")
        else:
            st.error("❌ Opt-in flow is Not Compliant")
        for issue in optin_issues:
            st.error(issue)

with col2:
    st.subheader("🔐 Privacy Policy")
    privacy_text = st.text_area("Paste privacy policy text, URL, or description here", height=100)
    privacy_issues = []
    if privacy_text:
        privacy_issues = check_privacy_compliance(privacy_text)
        st.markdown("### 📋 Compliance Check")
        if not privacy_issues:
            st.success("✅ Privacy Policy is Compliant")
        elif len(privacy_issues) < 4:
            st.warning("⚠️ Privacy Policy is Partially Compliant")
        else:
            st.error("❌ Privacy Policy is Not Compliant")
        for issue in privacy_issues:
            st.error(issue)

# --- COMBINED FIX SUGGESTIONS ---
if optin_issues or privacy_issues:
    st.markdown("---")
    st.subheader("🛠️ How to Address These Issues")
    st.info("Here are the recommended corrections based on your input:")

    if optin_issues:
        st.markdown("**Opt-In Flow Fix Recommendation:**")
        st.code("""
I agree to receive recurring SMS updates from [Your Brand Name].
Message and data rates may apply. Message frequency may vary.
Reply STOP to unsubscribe or HELP for help.
View our Privacy Policy at [your-privacy-policy-link].
""", language="text")

    if privacy_issues:
        st.markdown("**Privacy Policy Fix Recommendation:**")
        st.code("""
We will not share mobile contact information with third parties or affiliates for marketing or promotional purposes.
Information sharing to subcontractors in support services, such as customer service, is permitted.
All other categories exclude text messaging originator opt-in data and consent; this information will not be shared with any third parties.
If you are receiving text messages from us and wish to stop receiving them, simply reply with ‘STOP’ to the number from which you received the message.
""", language="text")

# --- FOOTER ---
st.markdown("---")
st.caption("Created by Monica Prasad · Built by mprasad@twilio.com · Internal Use Only")
