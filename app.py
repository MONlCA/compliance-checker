import streamlit as st
import re
import requests
from PIL import Image
import pytesseract
from io import BytesIO

st.set_page_config(layout="wide", page_title="A2P/TFV Compliance Assistance")

st.title("A2P/TFV Compliance Assistance")
st.caption("Ensure your opt-in flows and privacy policies meet 10DLC and Toll-Free compliance standards.")

# Campaign use case dropdown
use_case = st.selectbox("Select the campaign use case", [
    "2FA", "Account Notifications", "Customer Care", "Delivery Notifications", "Fraud Alert Messaging",
    "Higher Education", "Marketing", "Mixed", "Polling and voting", "Public Service Announcement",
    "Security Alert", "Charity / 501(c)(3)", "Emergency Services", "Political", "Low Volume Mixed",
    "Sole Proprietor"
])

# Layout
col1, col2 = st.columns(2)

# Opt-in input
with col1:
    st.markdown("### Opt-in")
    optin_type = st.radio("How would you like to submit your Opt-in content?", ["Text", "Image"], key="optin_type")
    optin_text = ""

    if optin_type == "Text":
        optin_text = st.text_area("Paste your Opt-in message, script, or flow here", height=200)
    else:
        optin_image = st.file_uploader("Upload an Opt-in image", type=["png", "jpg", "jpeg"], key="optin_img")
        if optin_image:
            image = Image.open(optin_image)
            optin_text = pytesseract.image_to_string(image)

# Privacy Policy input
with col2:
    st.markdown("### Privacy Policy")
    privacy_type = st.radio("How would you like to submit your Privacy Policy?", ["Text", "Image"], key="privacy_type")
    privacy_text = ""

    if privacy_type == "Text":
        privacy_text = st.text_input("Paste your Privacy Policy here or URL")
        if privacy_text.lower().startswith("http"):
            try:
                response = requests.get(privacy_text)
                privacy_text = response.text
            except:
                privacy_text = ""
    else:
        privacy_image = st.file_uploader("Upload a Privacy Policy image", type=["png", "jpg", "jpeg"], key="privacy_img")
        if privacy_image:
            image = Image.open(privacy_image)
            privacy_text = pytesseract.image_to_string(image)

# Check compliance on button click or Enter
check = st.button("Check Compliance")
if not check:
    check = st.session_state.get("compliance_triggered", False)

# Key binding for Enter
def submit_on_enter():
    st.session_state.compliance_triggered = True

st.text_input("Press Enter to check compliance", key="hidden_input", on_change=submit_on_enter, label_visibility="collapsed")

# Compliance logic
if check and (optin_text or privacy_text):
    st.markdown("## 🧾 Compliance Results")

    optin_issues = []
    privacy_issues = []

    # Opt-in checks
    if optin_text:
        if not re.search(r"STOP", optin_text, re.IGNORECASE):
            optin_issues.append("❌ Missing keyword: STOP to opt out.")
        if not re.search(r"HELP", optin_text, re.IGNORECASE):
            optin_issues.append("❌ Missing keyword: HELP for help.")
        if not re.search(r"message.*data.*rates.*apply", optin_text, re.IGNORECASE):
            optin_issues.append("❌ Missing or inaccurate clause: Message & Data Rates May Apply.")
        if not re.search(r"(privacy policy|terms of use|view.*policy)", optin_text, re.IGNORECASE):
            optin_issues.append("❌ Missing reference to Privacy Policy or Terms of Use.")
        if "consent" not in optin_text.lower():
            optin_issues.append("❌ Missing clear user consent for SMS communication.")

    # Privacy Policy checks
    if privacy_text:
        if not re.search(r"not.*share.*(third.*parties|affiliates).*marketing", privacy_text, re.IGNORECASE):
            privacy_issues.append("❌ Missing or inaccurate disclosure about sharing mobile contact information.")
        if not re.search(r"(exclude|not.*shared).*opt-in.*data", privacy_text, re.IGNORECASE):
            privacy_issues.append("❌ Missing or inaccurate clause about opt-in data protection.")

    if optin_issues:
        st.error("Opt-in message is not compliant. Issues found:")
        for issue in optin_issues:
            st.markdown(f"- {issue}")
    else:
        st.success("✅ Opt-in message is compliant.")

    if privacy_issues:
        st.error("Privacy Policy is not compliant. Issues found:")
        for issue in privacy_issues:
            st.markdown(f"- {issue}")
    else:
        st.success("✅ Privacy Policy is compliant.")

    # Copy/paste summary
    st.markdown("---")
    st.markdown("### 📋 Copy/Paste Summary to Send to Customers")
    st.code(
        "Opt-in: " + ("Compliant ✅" if not optin_issues else "Non-compliant ❌") + "\n" +
        "\n".join(optin_issues or ["No issues found."]) + "\n\n" +
        "Privacy Policy: " + ("Compliant ✅" if not privacy_issues else "Non-compliant ❌") + "\n" +
        "\n".join(privacy_issues or ["No issues found."]),
        language="text"
    )

# Docs
st.markdown("---")
st.markdown("### 📚 Documentation")
st.markdown("- [A2P 10DLC Campaign Approval Requirements](https://help.twilio.com/articles/11847054539547-A2P-10DLC-Campaign-Approval-Requirements)")
st.markdown("- [Required Information for Toll-Free Verification](https://help.twilio.com/articles/13264118705051-Required-Information-for-Toll-Free-Verification)")

# Watermark footer
st.markdown(
    "<div style='text-align: center; color: gray; font-size: 13px; margin-top: 50px;'>"
    "🔒 For Internal Use Only — Built by Monica Prasad — mprasad@twilio.com"
    "</div>",
    unsafe_allow_html=True
)
