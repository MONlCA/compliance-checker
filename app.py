# app.py (Updated layout with grammar checks, dynamic customer message, and clear fix templates)

import streamlit as st
import base64
import re
from PIL import Image

# --- FUNCTIONS ---
def check_opt_in_compliance(text):
    issues = []
    suggestions = []

    checks = {
        "❌ Unchecked checkbox for consent": r"(?i)checkbox.*unchecked",
        "❌ Link to privacy policy missing": r"(?i)privacy\s+policy",
        "❌ Message frequency disclosure missing": r"(?i)message\s+frequency\s+var(y|ies)",
        "❌ Data rates disclosure missing": r"(?i)data\s+rates\s+may\s+apply",
        "❌ STOP/Opt-out instructions missing": r"(?i)STOP.*?opt\s*out",
        "❌ Consent language missing": r"(?i)by\s+providing.*?you\s+agree.*?sms.*?notifications"
    }

    for issue, pattern in checks.items():
        if not re.search(pattern, text):
            issues.append(issue)

    # Basic grammar/spelling check
    if re.search(r"\bmesage\b|frequncy|repply", text, re.IGNORECASE):
        suggestions.append("✏️ Grammar or spelling issue detected. Please proofread the input.")

    return issues, suggestions

def check_privacy_compliance(text):
    issues = []
    suggestions = []

    checks = {
        "❌ Consent for SMS messaging not clearly stated": r"(?i)sms.*?text\s+messaging.*?consent.*?automated",
        "❌ Message frequency not disclosed": r"(?i)message\s+frequency\s+may\s+vary",
        "❌ Data rates disclaimer missing": r"(?i)data\s+rates\s+may\s+apply",
        "❌ STOP/Opt-out instruction not clear": r"(?i)reply.*?STOP.*?opt\s*out",
        "❌ SMS data sharing disclaimer missing": r"(?i)we\s+do\s+not\s+share.*?marketing|promotional\s+purposes",
        "❌ Subcontractor disclosure missing": r"(?i)subcontractors.*?support\s+services"
    }

    for issue, pattern in checks.items():
        if not re.search(pattern, text):
            issues.append(issue)

    if re.search(r"\bmesage\b|concent|automatd|repply", text, re.IGNORECASE):
        suggestions.append("✏️ Grammar or spelling issue detected. Please proofread the input.")

    return issues, suggestions

# --- UI LAYOUT ---
st.set_page_config("A2P Compliance Assistant", layout="wide")
st.title("📱 A2P Compliance Assistant")
st.caption("Verify A2P 10DLC & Toll-Free opt-in flows and privacy policies for CTIA compliance.")
st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.subheader("📥 Opt-In Flow")
    optin_text = st.text_area("Paste opt-in text, URL, or description here", height=120)
    optin_issues, optin_suggestions = [], []
    if optin_text:
        optin_issues, optin_suggestions = check_opt_in_compliance(optin_text)
        st.markdown("### 📋 Compliance Check")
        if not optin_issues:
            st.success("✅ Opt-in flow is Compliant")
        else:
            st.error("❌ Opt-in flow is Not Compliant")
            for issue in optin_issues:
                st.error(issue)
            for tip in optin_suggestions:
                st.warning(tip)

with col2:
    st.subheader("🔐 Privacy Policy")
    privacy_text = st.text_area("Paste privacy policy text, URL, or description here", height=120)
    privacy_issues, privacy_suggestions = [], []
    if privacy_text:
        privacy_issues, privacy_suggestions = check_privacy_compliance(privacy_text)
        st.markdown("### 📋 Compliance Check")
        if not privacy_issues:
            st.success("✅ Privacy Policy is Compliant")
        else:
            st.error("❌ Privacy Policy is Not Compliant")
            for issue in privacy_issues:
                st.error(issue)
            for tip in privacy_suggestions:
                st.warning(tip)

# --- COMPLIANCE RESULTS ---
if not optin_issues and not privacy_issues and (optin_text or privacy_text):
    st.markdown("---")
    st.subheader("🎉 All Clear! Your submission is CTIA compliant.")

    st.markdown("**Opt-In Compliance Highlights**")
    st.markdown("- ✅ Consent checkbox present\n- ✅ Privacy policy linked\n- ✅ Message frequency and data rate disclosures included\n- ✅ Clear opt-out instructions")

    st.markdown("**Privacy Policy Compliance Highlights**")
    st.markdown("- ✅ SMS messaging consent included\n- ✅ Message frequency + opt-out terms disclosed\n- ✅ No third-party sharing for marketing\n- ✅ Subcontractor support services disclosed")

    st.markdown("**📋 Reply to Customer (Copy/Paste):**")
    st.code("""Hi there! We've reviewed your submission and found that both your opt-in flow and privacy policy meet CTIA compliance standards. No further updates are required at this time. Thanks for ensuring everything is in order!""", language="text")

# --- FIX TEMPLATE ---
if optin_issues or privacy_issues:
    st.markdown("---")
    st.subheader("🛠️ How to Address These Issues")
    st.info("To ensure the privacy policy/opt-in flow is compliant, please ensure:\n\n- Your privacy policy includes SMS/Text Messaging disclosure with opt-out and data handling terms.\n- Your opt-in flow clearly presents an unchecked checkbox for consent, a privacy policy link, and required disclaimers.")

    if optin_issues:
        st.markdown("**Opt-In Flow Fix Template:**")
        st.code("""
☐ By providing your phone number, you agree to receive SMS notifications about this event from [Organization Name].
Message frequency varies. Message & data rates may apply.
You can reply STOP to opt out at any time. [Privacy Policy Link]
""", language="text")

    if privacy_issues:
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
    if optin_issues:
        customer_message += "\n📥 *Opt-In Flow Issues:*\n"
        customer_message += "\n".join(f"- {issue[2:]}" for issue in optin_issues)
    if privacy_issues:
        customer_message += "\n\n🔐 *Privacy Policy Issues:*\n"
        customer_message += "\n".join(f"- {issue[2:]}" for issue in privacy_issues)
    customer_message += "\n\nPlease refer to the suggested fix template above and make the necessary updates. Let us know once you've completed the changes."
    st.text_area("Use this ready-made compliance message for your customer replies:", value=customer_message, height=200)

# --- FOOTER ---
st.markdown("---")
st.caption("Created by Monica Prasad · Built by mprasad@twilio.com · Internal Use Only")
