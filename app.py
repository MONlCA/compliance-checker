import streamlit as st
import pytesseract
from PIL import Image
import re

st.set_page_config(page_title="A2P/TFV Compliance Assistance", layout="centered")
st.title("A2P/TFV Compliance Assistance")
st.caption("Ensure your opt-in flows and privacy policies meet 10DLC and Toll-Free compliance standards.")

# -- Use Case Dropdown -- #
use_case = st.selectbox(
    "Select the campaign use case",
    [
        "2FA",
        "Account Notifications",
        "Customer Care",
        "Delivery Notifications",
        "Fraud Alert Messaging",
        "Higher Education",
        "Marketing",
        "Mixed",
        "Polling and voting",
        "Public Service Announcement",
        "Security Alert",
        "Low Volume Mixed",
        "Sole Proprietor"
    ]
)

st.markdown("---")

# -- Helper Functions -- #
def extract_text_from_image(uploaded_image):
    try:
        image = Image.open(uploaded_image)
        return pytesseract.image_to_string(image)
    except Exception as e:
        return f"Error reading image: {e}"

def is_opt_in_compliant(text, use_case):
    issues = []

    # Normalize text
    text = text.lower()

    # General required elements
    if not re.search(r"\bproviding your phone number\b", text):
        issues.append("Missing phrase: 'By providing your phone number'.")

    if not re.search(r"\bagree to receive(.*?)sms|text messages\b", text):
        issues.append("Missing user consent to receive SMS/text messages.")

    if not re.search(r"\bmessage (frequency|rate).*?apply\b", text):
        issues.append("Missing message frequency or 'Message and data rates may apply' disclosure.")

    if not re.search(r"reply\s+stop\b", text):
        issues.append("Missing opt-out instruction (e.g. 'Reply STOP to opt out').")

    if not re.search(r"reply\s+help\b", text):
        issues.append("Missing help instruction (e.g. 'Reply HELP for help').")

    if not re.search(r"privacy policy|terms of service|terms of use", text):
        issues.append("Missing reference to Privacy Policy or Terms of Service.")

    return issues

def is_privacy_policy_compliant(text):
    text = text.lower()
    issues = []

    if "we do not share mobile contact information with third parties or affiliates for marketing or promotional purposes" not in text:
        issues.append("Missing or inaccurate disclosure about sharing mobile contact information.")

    if "text messaging originator opt-in data and consent; this information will not be shared with any third parties" not in text:
        issues.append("Missing or inaccurate clause about opt-in data protection.")

    return issues

# -- Input Sections -- #
optin_input_method = st.radio("How would you like to submit your Opt-in content?", ["Text", "Image"])
if optin_input_method == "Text":
    optin_text = st.text_area("Paste your Opt-in message, script, or flow here")
else:
    optin_image = st.file_uploader("Upload image of Opt-in flow", type=["png", "jpg", "jpeg"])
    optin_text = extract_text_from_image(optin_image) if optin_image else ""

privacy_input_method = st.radio("How would you like to submit your Privacy Policy?", ["Text", "Image"])
if privacy_input_method == "Text":
    privacy_text = st.text_area("Paste your Privacy Policy here")
else:
    privacy_image = st.file_uploader("Upload image of Privacy Policy", type=["png", "jpg", "jpeg"])
    privacy_text = extract_text_from_image(privacy_image) if privacy_image else ""

# -- Submit Button -- #
if st.button("Check Compliance"):
    if optin_text:
        optin_issues = is_opt_in_compliant(optin_text, use_case)
        if not optin_issues:
            st.success("✅ Opt-in flow is compliant.")
        else:
            st.error("❌ Opt-in flow is not compliant. Issues found:")
            for issue in optin_issues:
                st.write("-", issue)

    if privacy_text:
        privacy_issues = is_privacy_policy_compliant(privacy_text)
        if not privacy_issues:
            st.success("✅ Privacy Policy is compliant.")
        else:
            st.error("❌ Privacy Policy is not compliant. Issues found:")
            for issue in privacy_issues:
                st.write("-", issue)

# Footer notes
st.markdown("""
---
ℹ️ This tool uses pattern detection to help verify compliance with 10DLC and TFV messaging rules. For full requirements, visit [Twilio's Compliance Docs](https://help.twilio.com/articles/11847054539547-A2P-10DLC-Campaign-Approval-Requirements).
""")
