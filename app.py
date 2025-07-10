# app.py (Updated to include image upload + OCR for Opt-In screenshots)

import streamlit as st
import base64
import re
from PIL import Image
import pytesseract
from io import BytesIO

# --- FUNCTIONS ---
def check_opt_in_compliance(text):
    results = {}
    suggestions = []

    checks = {
        "Consent checkbox": r"(?i)checkbox.*unchecked",
        "Privacy policy link": r"(?i)privacy\s+policy",
        "Message frequency disclosure": r"(?i)message\s+frequency\s+var(y|ies)",
        "Data rates disclosure": r"(?i)data\s+rates\s+may\s+apply",
        "STOP/Opt-out instructions": r"(?i)STOP.*?opt\s*out",
        "Consent language": r"(?i)by\s+providing.*?you\s+agree.*?sms.*?notifications"
    }

    for key, pattern in checks.items():
        results[key] = bool(re.search(pattern, text))

    if re.search(r"\bmesage\b|frequncy|repply", text, re.IGNORECASE):
        suggestions.append("✏️ Grammar or spelling issue detected. Please proofread the input.")

    return results, suggestions

def check_privacy_compliance(text):
    results = {}
    suggestions = []

    checks = {
        "Consent for SMS messaging": r"(?i)sms.*?text\s+messaging.*?consent.*?automated",
        "Message frequency disclosure": r"(?i)message\s+frequency\s+may\s+vary",
        "Data rates disclaimer": r"(?i)data\s+rates\s+may\s+apply",
        "STOP/Opt-out instruction": r"(?i)reply.*?STOP.*?opt\s*out",
        "No third-party sharing": r"(?i)we\s+do\s+not\s+share.*?marketing|promotional\s+purposes",
        "Subcontractor disclosure": r"(?i)subcontractors.*?support\s+services"
    }

    for key, pattern in checks.items():
        results[key] = bool(re.search(pattern, text))

    if re.search(r"\bmesage\b|concent|automatd|repply", text, re.IGNORECASE):
        suggestions.append("✏️ Grammar or spelling issue detected. Please proofread the input.")

    return results, suggestions

# --- UI LAYOUT ---
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
        compliant_items = [k for k, v in optin_results.items() if v]
        non_compliant_items = [k for k, v in optin_results.items() if not v]

        st.markdown("### ✅ Compliant Opt-In Elements")
        for item in compliant_items:
            st.success(f"✅ {item}")

        if non_compliant_items:
            st.markdown("### ❌ Non-Compliant Opt-In Elements")
            for item in non_compliant_items:
                st.error(f"❌ {item}")

        for tip in optin_suggestions:
            st.warning(tip)

with col2:
    st.subheader("🔐 Privacy Policy")
    privacy_text = st.text_area("Paste privacy policy text, URL, or description here", height=120)
    privacy_results, privacy_suggestions = {}, []
    if privacy_text:
        privacy_results, privacy_suggestions = check_privacy_compliance(privacy_text)
        compliant_items = [k for k, v in privacy_results.items() if v]
        non_compliant_items = [k for k, v in privacy_results.items() if not v]

        st.markdown("### ✅ Compliant Privacy Elements")
        for item in compliant_items:
            st.success(f"✅ {item}")

        if non_compliant_items:
            st.markdown("### ❌ Non-Compliant Privacy Elements")
            for item in non_compliant_items:
                st.error(f"❌ {item}")

        for tip in privacy_suggestions:
            st.warning(tip)

# --- COMPLIANCE LOGIC ---
all_optin_pass = all(optin_results.values()) if optin_results else False
all_privacy_pass = all(privacy_results.values()) if privacy_results else False

# --- COMPLIANT STATE ---
if all_optin_pass and all_privacy_pass:
    st.markdown("---")
    st.subheader("🎉 All Clear! Your submission is CTIA compliant.")

    st.markdown("**Opt-In Compliance Highlights**")
    for item in optin_results:
        st.markdown(f"- ✅ {item}")

    st.markdown("**Privacy Policy Compliance Highlights**")
    for item in privacy_results:
        st.markdown(f"- ✅ {item}")

    st.markdown("**📋 Reply to Customer (Copy/Paste):**")
    st.code("""Hi there! We've reviewed your submission and found that both your opt-in flow and privacy policy meet CTIA compliance standards. No further updates are required at this time. Thanks for ensuring everything is in order!""", language="text")

# --- NON-COMPLIANT STATE ---
if (optin_text or privacy_text or optin_image) and (not all_optin_pass or not all_privacy_pass):
    st.markdown("---")
    st.subheader("🛠️ How to Address These Issues")
    st.info("To ensure the privacy policy/opt-in flow is compliant, please ensure:\n\n- Your privacy policy includes SMS/Text Messaging disclosure with opt-out and data handling terms.\n- Your opt-in flow clearly presents an unchecked checkbox for consent, a privacy policy link, and required disclaimers.")

    if not all_optin_pass:
        st.markdown("**Opt-In Flow Fix Template:**")
        st.code("""
☐ By providing your phone number, you agree to receive SMS notifications about this event from [Organization Name].
Message frequency varies. Message & data rates may apply.
You can reply STOP to opt out at any time. [Privacy Policy Link]
""", language="text")

    if not all_privacy_pass:
        st.markdown("**Privacy Policy Fix Template:**")
        st.code("""
SMS/Text Messaging
By providing your mobile number, you consent to receive automated text messages from [Company Name] for order or event notifications.
Message frequency may vary. Message and data rates may apply. To opt out, reply “STOP” to any message.

We do not share mobile contact information with third parties or affiliates for marketing or promotional purposes.
Information may be shared with subcontractors in support services, such as customer service.
All other categories exclude text messaging originator opt-in data and consent; this information will not be shared with any third parties.
""", language="text")

    st.markdown("**📋 Copy-Paste for Customer Replies:**")
    customer_message = "Hi there! Based on our review, the following updates are needed to comply with CTIA regulations:\n"
    if not all_optin_pass:
        customer_message += "\n📥 *Opt-In Flow Issues:*\n"
        customer_message += "\n".join(f"- {item}" for item, passed in optin_results.items() if not passed)
    if not all_privacy_pass:
        customer_message += "\n\n🔐 *Privacy Policy Issues:*\n"
        customer_message += "\n".join(f"- {item}" for item, passed in privacy_results.items() if not passed)
    customer_message += "\n\nPlease refer to the suggested fix template above and make the necessary updates. Let us know once you've completed the changes."
    st.text_area("Use this ready-made compliance message for your customer replies:", value=customer_message, height=200)

# --- FOOTER ---
st.markdown("---")
st.caption("Created by Monica Prasad · Built by mprasad@twilio.com · Internal Use Only")
