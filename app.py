# app.py (Smart parsing + partial compliance + OCR fallback)

import streamlit.components.v1 as components
import tempfile
import os
import streamlit as st
import base64
import re
from PIL import Image
import pytesseract
from io import BytesIO


# --- COMPLIANCE CHECK FUNCTIONS ---
def check_opt_in_compliance(text):
    results = {}
    suggestions = []

    checks = {
        "Consent checkbox": r"(?i)(checkbox).*?(unchecked|not\s+checked)",
        "Privacy policy link": r"(?i)(privacy\s+policy).*?(link|available|visit)",
        "Message frequency disclosure": r"(?i)(message\s+frequency).*?(var(y|ies)|may\s+vary)",
        "Data rates disclosure": r"(?i)data\s+rates\s+may\s+apply",
        "STOP/Opt-out instructions": r"(?i)(STOP|unsubscribe).*?(reply|opt\s*out)",
        "Consent language": r"(?i)(by\s+providing).*?(agree|consent).*?(sms|text\s+messages?)"
    }

    for key, pattern in checks.items():
        match = re.search(pattern, text)
        if match:
            results[key] = "✅"
        else:
            if any(word in text.lower() for word in key.lower().split()):
                results[key] = "⚠️"
            else:
                results[key] = "❌"

    if re.search(r"\bmesage\b|frequncy|repply|privace|chekbox", text, re.IGNORECASE):
        suggestions.append("✏️ Grammar or spelling issue detected. Please proofread the input.")

    return results, suggestions

def check_privacy_compliance(text):
    results = {}
    suggestions = []

    checks = {
        "Consent for SMS messaging": r"(?i)sms.*?text.*?consent.*?(automated|messages)",
        "Message frequency disclosure": r"(?i)message\s+frequency\s+may\s+vary",
        "Data rates disclaimer": r"(?i)data\s+rates\s+may\s+apply",
        "STOP/Opt-out instruction": r"(?i)reply.*?STOP.*?opt\s*out",
        "No third-party sharing": r"(?i)we\s+do\s+not\s+share.*?(third|marketing|promotional)",
        "Subcontractor disclosure": r"(?i)subcontractors.*?support\s+services"
    }

    for key, pattern in checks.items():
        match = re.search(pattern, text)
        if match:
            results[key] = "✅"
        else:
            if any(word in text.lower() for word in key.lower().split()):
                results[key] = "⚠️"
            else:
                results[key] = "❌"

    if re.search(r"\bmesage\b|concent|automatd|repply", text, re.IGNORECASE):
        suggestions.append("✏️ Grammar or spelling issue detected. Please proofread the input.")

    return results, suggestions

# --- UI ---
st.set_page_config("A2P Compliance Assistant", layout="wide")
st.title("📱 A2P Compliance Assistant")
st.caption("Verify A2P 10DLC & Toll-Free opt-in flows and privacy policies for CTIA compliance.")
st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.subheader("📥 Opt-In Flow")
    optin_text = st.text_area("Paste opt-in text, URL, or description here", height=120)
    optin_image = st.file_uploader("📸 Upload or paste screenshot of opt-in flow (PNG/JPG)", type=["png", "jpg", "jpeg"])

    image_text = ""
    if optin_image:
        image = Image.open(optin_image)
        st.image(image, caption="Uploaded Screenshot", use_column_width=True)
        try:
            image_text = pytesseract.image_to_string(image)
            if not image_text.strip():
                image_text = "We couldn’t extract any text from the image. Please upload a higher-quality image or paste the opt-in text manually."
        except Exception as e:
            image_text = f"❌ OCR failed: {e}"
        st.text_area("📝 Extracted Text from Screenshot", value=image_text, height=100)

    combined_optin_text = (optin_text or "") + "\n" + image_text
    optin_results, optin_suggestions = {}, []

    if combined_optin_text.strip():
        optin_results, optin_suggestions = check_opt_in_compliance(combined_optin_text)
        st.markdown("### 📊 Opt-In Compliance Breakdown")
        for item, status in optin_results.items():
            if status == "✅":
                st.success(f"{status} {item}")
            elif status == "⚠️":
                st.warning(f"{status} {item} — Partially detected, but unclear wording")
            else:
                st.error(f"{status} {item}")
        for tip in optin_suggestions:
            st.warning(tip)

with col2:
    st.subheader("🔐 Privacy Policy")
    privacy_text = st.text_area("Paste privacy policy text, URL, or description here", height=120)
    privacy_results, privacy_suggestions = {}, []
    if privacy_text:
        privacy_results, privacy_suggestions = check_privacy_compliance(privacy_text)
        st.markdown("### 📊 Privacy Compliance Breakdown")
        for item, status in privacy_results.items():
            if status == "✅":
                st.success(f"{status} {item}")
            elif status == "⚠️":
                st.warning(f"{status} {item} — Mentioned, but not clearly stated")
            else:
                st.error(f"{status} {item}")
        for tip in privacy_suggestions:
            st.warning(tip)

# --- EVALUATION ---
all_optin_pass = all(v == "✅" for v in optin_results.values()) if optin_results else False
all_privacy_pass = all(v == "✅" for v in privacy_results.values()) if privacy_results else False

if all_optin_pass and all_privacy_pass:
    st.markdown("---")
    st.subheader("🎉 All Clear! Your submission is CTIA compliant.")
    st.markdown("**📋 Copy for Customer:**")
    st.code("""Hi there! We've reviewed your submission and found that both your opt-in flow and privacy policy meet CTIA compliance standards. No further updates are required at this time. Thanks for ensuring everything is in order!""", language="text")

elif optin_results or privacy_results:
    st.markdown("---")
    st.subheader("🛠️ How to Address These Issues")
    st.info("To ensure the privacy policy/opt-in flow is compliant, please ensure:\n\n- Your privacy policy includes SMS/Text Messaging disclosure with opt-out and data handling terms.\n- Your opt-in flow clearly presents an unchecked checkbox for consent, a privacy policy link, and required disclaimers.")

    if not all_optin_pass:
        st.markdown("**Opt-In Fix Template:**")
        st.code("""
☐ By providing your phone number, you agree to receive SMS notifications about this event from [Organization Name].
Message frequency varies. Message & data rates may apply.
You can reply STOP to opt out at any time. [Privacy Policy Link]""", language="text")

    if not all_privacy_pass:
        st.markdown("**Privacy Policy Fix Template:**")
        st.code("""
SMS/Text Messaging
By providing your mobile number, you consent to receive automated text messages from [Company Name] for order or event notifications.
Message frequency may vary. Message and data rates may apply. To opt out, reply “STOP” to any message.

We do not share mobile contact information with third parties or affiliates for marketing or promotional purposes.
Information may be shared with subcontractors in support services, such as customer service.
All other categories exclude text messaging originator opt-in data and consent; this information will not be shared with any third parties.""", language="text")

    st.markdown("**📋 Copy for Customer:**")
    summary = "Hi there! Based on our review, the following updates are needed to comply with CTIA regulations:\n"
    if not all_optin_pass:
        summary += "\n📥 *Opt-In Flow Issues:*\n"
        summary += "\n".join(f"- {k} ({v})" for k, v in optin_results.items() if v != "✅")
    if not all_privacy_pass:
        summary += "\n\n🔐 *Privacy Policy Issues:*\n"
        summary += "\n".join(f"- {k} ({v})" for k, v in privacy_results.items() if v != "✅")
    summary += "\n\nPlease refer to the suggested fix template(s) above and make the necessary updates."
    st.text_area("Customer Message:", value=summary, height=250)

# --- FOOTER ---
st.markdown("---")
st.caption("Created by Monica Prasad · Built by mprasad@twilio.com · Internal Use Only")
