# app.py (v3: Enhanced compliance logic, paste support, and crash fix)

import streamlit as st
import base64
import re
import requests
from bs4 import BeautifulSoup
from PIL import Image
import pytesseract
from io import BytesIO
from difflib import SequenceMatcher

# --- Helper: Fuzzy match score ---
def fuzzy_match(a, b):
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

# --- COMPLIANCE CRITERIA (flexible) ---
PRIVACY_CHECKS = {
    "Consent for SMS messaging": [
        "you consent to receive automated text messages",
        "By providing your mobile number"
    ],
    "Message frequency disclosure": [
        "Message frequency may vary",
        "frequency of messages may vary"
    ],
    "Data rates disclaimer": [
        "Message and data rates may apply",
        "Msg & data rates may apply"
    ],
    "STOP/Opt-out instruction": [
        "reply STOP to opt out",
        "Text STOP to unsubscribe"
    ],
    "No third-party sharing": [
        "we do not share your mobile contact information",
        "will not be shared with any third parties"
    ],
    "Subcontractor disclosure": [
        "shared with subcontractors",
        "subcontractors in support services"
    ]
}

OPTIN_CHECKS = {
    "Consent checkbox": [
        "unchecked checkbox",
        "tick box to agree"
    ],
    "Privacy policy link": [
        "privacy policy link",
        "see our privacy policy"
    ],
    "Message frequency disclosure": [
        "Message frequency may vary"
    ],
    "Data rates disclosure": [
        "Message and data rates may apply",
        "Msg & data rates may apply"
    ],
    "STOP/Opt-out instructions": [
        "Reply STOP to opt out",
        "Text STOP to unsubscribe"
    ],
    "Consent language": [
        "By providing your phone number",
        "you agree to receive SMS notifications"
    ]
}

# --- COMPLIANCE LOGIC ---
def check_compliance(text, criteria):
    results = {}
    for label, phrases in criteria.items():
        matched = False
        for phrase in phrases:
            if fuzzy_match(phrase, text) > 0.75:
                matched = True
                break
        results[label] = "✅" if matched else "❌"
    return results

# --- TEXT EXTRACTION ---
def extract_text_from_url(url):
    try:
        res = requests.get(url, timeout=5)
        soup = BeautifulSoup(res.text, 'html.parser')
        return soup.get_text(separator=" ", strip=True)
    except Exception:
        return ""

def extract_text_from_image(img_file):
    try:
        image = Image.open(img_file)
        return pytesseract.image_to_string(image)
    except:
        return ""

# --- STREAMLIT UI ---
st.set_page_config("A2P Compliance Assistant", layout="wide")
st.title("📱 A2P Compliance Assistant")
st.caption("Verify A2P 10DLC & Toll-Free opt-in flows and privacy policies for CTIA compliance.")

col1, col2 = st.columns(2)
optin_results = {}
privacy_results = {}
optin_final = ""
privacy_final = ""

with col1:
    st.subheader("📥 Opt-In Flow")
    optin_text = st.text_area("Paste opt-in text, URL, or description here", height=120)
    optin_image = st.file_uploader("📸 Upload or paste screenshot of opt-in flow (PNG/JPG)", type=["png", "jpg", "jpeg"])
    optin_final = optin_text
    if optin_text.startswith("http"):
        optin_final = extract_text_from_url(optin_text)
    if optin_image:
        optin_final += "\n" + extract_text_from_image(optin_image)
    if optin_final.strip():
        optin_results = check_compliance(optin_final, OPTIN_CHECKS)
        st.markdown("### 📊 Opt-In Compliance Breakdown")
        for item, result in optin_results.items():
            if result == "✅": st.success(f"{result} {item}")
            else: st.error(f"{result} {item}")

with col2:
    st.subheader("🔐 Privacy Policy")
    privacy_text = st.text_area("Paste privacy policy text, URL, or description here", height=120)
    privacy_final = privacy_text
    if privacy_text.startswith("http"):
        privacy_final = extract_text_from_url(privacy_text)
    if privacy_final.strip():
        privacy_results = check_compliance(privacy_final, PRIVACY_CHECKS)
        st.markdown("### 📊 Privacy Compliance Breakdown")
        for item, result in privacy_results.items():
            if result == "✅": st.success(f"{result} {item}")
            else: st.error(f"{result} {item}")

# --- COMPLIANCE SUMMARY ---
if privacy_final.strip() or optin_final.strip():
    st.markdown("---")
    st.subheader("📋 Summary Message for Customer")

    if privacy_results and optin_results:
        all_ok = all(v == "✅" for v in list(privacy_results.values()) + list(optin_results.values()))
        if all_ok:
            st.success("All sections appear compliant!")
            st.code("Hi there! We've reviewed your submission and everything looks compliant with CTIA regulations. ✅")
        else:
            st.warning("Some areas need attention:")
            msg = "Hi there! Based on our review, please address the following items to meet CTIA compliance:\n"
            if any(v != "✅" for v in optin_results.values()):
                msg += "\n📥 *Opt-In Issues:*\n"
                msg += "\n".join(f"- {k} ({v})" for k, v in optin_results.items() if v != "✅") + "\n"
            if any(v != "✅" for v in privacy_results.values()):
                msg += "\n🔐 *Privacy Policy Issues:*\n"
                msg += "\n".join(f"- {k} ({v})" for k, v in privacy_results.items() if v != "✅") + "\n"
            st.text_area("Copy to Customer:", value=msg, height=250)
    else:
        st.info("Please upload a valid URL, screenshot, or text to start your compliance check.")

st.markdown("---")
st.caption("Created by Monica Prasad · Built by mprasad@twilio.com · Internal Use Only")
