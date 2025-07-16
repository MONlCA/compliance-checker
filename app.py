# app.py (v10: Enhanced compliant detection + clarity)

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

# --- Explanation templates ---
EXPLANATIONS = {
    "Consent for SMS messaging": "Missing clear consent language such as 'you consent to receive automated text messages'.",
    "Message frequency disclosure": "Must include a message like 'message frequency may vary' so users know what to expect.",
    "Data rates disclaimer": "Should disclose that 'message and data rates may apply' to comply with carrier rules.",
    "STOP/Opt-out instruction": "You need to include instructions like 'Reply STOP to opt out' to meet CTIA guidelines.",
    "No third-party sharing": "Policy should explicitly state mobile contact info is not shared with third parties.",
    "Subcontractor disclosure": "Must mention that information may be shared with subcontractors for service purposes.",

    "Consent checkbox": "Include an unchecked checkbox or language confirming user consent before opt-in.",
    "Privacy policy link": "You need to show a clear link to your privacy policy on the opt-in form.",
    "Consent language": "Include consent wording such as 'by providing your number, you agree to receive texts'."
}

REQUIRED_PRIVACY_POLICY = """SMS/Text Messaging\nBy providing your mobile number, you consent to receive automated text messages from [Company Name] for order [type of messages] notifications. Message frequency may vary. Message and data rates may apply. To opt out, reply “STOP” to any message.\n\nWe do not share mobile contact information with third parties or affiliates for marketing or promotional purposes. Information may be shared with subcontractors in support services, such as customer service. All other categories exclude text messaging originator opt-in data and consent; this information will not be shared with any third parties."""

REQUIRED_OPTIN = """By providing your phone number, you agree to receive text messages from [Your Company Name] regarding [brief, clear message purpose, e.g., 'order updates,' 'appointment reminders,' 'marketing promotions']. Message frequency will vary [or 'is X messages per month' if fixed]. Message and data rates may apply. Reply STOP to unsubscribe at any time. Reply HELP for assistance. For more information, please see our Privacy Policy at [Link to your Privacy Policy] and Terms of Service at [Link to your Terms of Service]."""

# --- COMPLIANCE CRITERIA ---
PRIVACY_CHECKS = {
    "Consent for SMS messaging": [
        "you consent to receive automated text messages",
        "by providing your mobile number",
        "you agree to receive messages",
        "you consent to text messages",
        "sms/text messaging"
    ],
    "Message frequency disclosure": [
        "message frequency may vary",
        "messages may be sent periodically",
        "frequency of messages may vary"
    ],
    "Data rates disclaimer": [
        "message and data rates may apply",
        "msg & data rates may apply",
        "standard messaging rates apply",
        "carrier charges may apply"
    ],
    "STOP/Opt-out instruction": [
        "reply STOP to opt out",
        "text STOP to unsubscribe",
        "you may opt out at any time by texting stop"
    ],
    "No third-party sharing": [
        "we do not share mobile contact information with third parties",
        "not shared with third parties",
        "exclude text messaging originator opt-in data",
        "information not be shared with any third parties",
        "will not disclose your contact information to affiliates"
    ],
    "Subcontractor disclosure": [
        "shared with subcontractors",
        "subcontractors in support services",
        "information sharing to subcontractors is permitted",
        "disclosed to subcontractors"
    ]
}

OPTIN_CHECKS = {
    "Consent checkbox": [
        "unchecked checkbox",
        "tick box to agree",
        "check box to consent",
        "checkbox to opt-in"
    ],
    "Privacy policy link": [
        "privacy policy link",
        "see our privacy policy",
        "click here for privacy policy",
        "privacy policy at"
    ],
    "Message frequency disclosure": [
        "message frequency may vary",
        "frequency of messages may vary"
    ],
    "Data rates disclosure": [
        "message and data rates may apply",
        "msg & data rates may apply",
        "carrier charges may apply"
    ],
    "STOP/Opt-out instructions": [
        "reply STOP to opt out",
        "text STOP to unsubscribe",
        "you may opt out at any time",
        "reply STOP to unsubscribe"
    ],
    "Consent language": [
        "by providing your phone number",
        "you agree to receive SMS notifications",
        "you consent to receiving text messages",
        "you agree to receive text messages about this event"
    ]
}

# --- COMPLIANCE LOGIC ---
def check_compliance(text, criteria):
    results = {}
    scores = []
    for label, phrases in criteria.items():
        match_score = 0.0
        for phrase in phrases:
            score = fuzzy_match(phrase, text)
            scores.append(score)
            if score > match_score:
                match_score = score
        if match_score > 0.75:
            results[label] = "✅"
        elif match_score > 0.5:
            results[label] = "⚠️"
        else:
            results[label] = "❌"
    avg_score = round(sum(scores) / len(scores) * 100, 1) if scores else 0
    return results, avg_score

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
optin_results, privacy_results = {}, {}
optin_final, privacy_final = "", ""
optin_score = privacy_score = 0

with col1:
    st.subheader("📥 Opt-In Flow")
    optin_text = st.text_area("Paste opt-in text, URL, or description here", height=120)
    optin_image = st.file_uploader("📸 Upload screenshot of opt-in flow (PNG/JPG)", type=["png", "jpg", "jpeg"])

    optin_final = optin_text
    if optin_text.startswith("http"):
        optin_final = extract_text_from_url(optin_text)
    if optin_image:
        optin_final += "\n" + extract_text_from_image(optin_image)

    if optin_final.strip():
        optin_results, optin_score = check_compliance(optin_final, OPTIN_CHECKS)
        st.markdown("### 📊 Opt-In Compliance Breakdown")
        st.progress(optin_score / 100, text=f"Confidence Score: {optin_score}%")
        for item, result in optin_results.items():
            if result == "✅": st.success(f"{result} {item}")
            elif result == "⚠️": st.warning(f"{result} {item} — Possibly present but unclear.")
            else: st.error(f"{result} {item} — {EXPLANATIONS.get(item, 'Missing required language.')}")

with col2:
    st.subheader("🔐 Privacy Policy")
    privacy_text = st.text_area("Paste privacy policy text, URL, or description here", height=120)
    privacy_final = privacy_text
    if privacy_text.startswith("http"):
        privacy_final = extract_text_from_url(privacy_text)
    if privacy_final.strip():
        privacy_results, privacy_score = check_compliance(privacy_final, PRIVACY_CHECKS)
        st.markdown("### 📊 Privacy Compliance Breakdown")
        st.progress(privacy_score / 100, text=f"Confidence Score: {privacy_score}%")
        for item, result in privacy_results.items():
            if result == "✅": st.success(f"{result} {item}")
            elif result == "⚠️": st.warning(f"{result} {item} — Possibly present but unclear.")
            else: st.error(f"{result} {item} — {EXPLANATIONS.get(item, 'Missing required language.')}")

# --- COMPLIANCE SUMMARY ---
st.markdown("---")
st.subheader("📋 Summary Message for Customer")

if optin_results or privacy_results:
    if all(v == "✅" for v in list(privacy_results.values()) + list(optin_results.values())):
        st.success("All sections appear compliant!")
        st.code("Hi there! We've reviewed your submission and everything looks compliant with CTIA regulations. ✅")
    else:
        st.warning("Some areas need attention:")
        msg = "Hi there! Based on our review, please address the following items to meet CTIA compliance:\n"
        if any(v != "✅" for v in optin_results.values()):
            msg += "\n📥 *Opt-In Issues:*\n"
            for k, v in optin_results.items():
                if v != "✅":
                    msg += f"- {k} ({v}) — {EXPLANATIONS.get(k, 'Missing required language.')}\n"
        if any(v != "✅" for v in privacy_results.values()):
            msg += "\n🔐 *Privacy Policy Issues:*\n"
            for k, v in privacy_results.items():
                if v != "✅":
                    msg += f"- {k} ({v}) — {EXPLANATIONS.get(k, 'Missing required language.')}\n"
        msg += f"\n🔍 Confidence Scores:\n- Opt-In: {optin_score}%\n- Privacy: {privacy_score}%"

        if any(v != "✅" for v in privacy_results.values()):
            msg += "\n\n📄 What a Compliant Privacy Policy should state:\n" + REQUIRED_PRIVACY_POLICY
        if any(v != "✅" for v in optin_results.values()):
            msg += "\n\n📝 What a Compliant Opt-In Message should include:\n" + REQUIRED_OPTIN

        st.text_area("Copy to Customer:", value=msg.strip(), height=400)
else:
    st.info("Please upload a valid URL, screenshot, or text to start your compliance check.")

st.markdown("---")
st.caption("Created by Monica Prasad · Built by mprasad@twilio.com · Internal Use Only")
