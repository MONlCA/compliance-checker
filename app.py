import streamlit as st
from utils import extract_text_from_image, extract_text_from_url
from compliance_logic import check_opt_in_compliance, check_privacy_compliance

st.set_page_config(page_title="A2P/TFV Compliance Assistance", layout="wide")

st.markdown("## 📲 A2P/TFV Compliance Assistance")

# Input Sections
st.markdown("### Opt-in")
optin_text = st.text_area("Paste Opt-in Language or Upload Image", height=100, label_visibility="collapsed")

optin_image = st.file_uploader("Or upload Opt-in Screenshot", type=["png", "jpg", "jpeg"], label_visibility="visible")

st.markdown("### Privacy Policy")
privacy_text = st.text_area("Paste Privacy Policy Language or Upload Image / URL", height=100, label_visibility="collapsed")

privacy_image = st.file_uploader("Or upload Privacy Policy Screenshot", type=["png", "jpg", "jpeg"], label_visibility="visible")

# Extract OCR text if images are uploaded
if optin_image:
    optin_text = extract_text_from_image(optin_image)

if privacy_image:
    privacy_text = extract_text_from_image(privacy_image)
elif privacy_text.startswith("http"):
    privacy_text = extract_text_from_url(privacy_text)

# Button to trigger compliance check
if st.button("✅ Check Compliance"):
    st.markdown("### 🗂️ Compliance Results")

    # --- Opt-in Check ---
    st.markdown("#### ✅ Opt-in Feedback")
    optin_result = check_opt_in_compliance(optin_text)
    st.write(optin_result["message"])

    # --- Privacy Policy Check ---
    st.markdown("#### 📄 Privacy Policy Feedback")
    privacy_result = check_privacy_compliance(privacy_text)
    st.write("**Compliance Status:**", "🟥 Not compliant" if not privacy_result["compliant"] else "🟩 Compliant")
    st.write("**Detected Required Phrases:**", privacy_result["present_required"])
    st.write("**Prohibited Phrases Found:**", privacy_result["prohibited_phrases_found"])

    # --- Copy/Paste Summary ---
    st.markdown("#### 🧾 Copy/Paste for Customer")
    with st.expander("📋 Click to Expand"):
        st.code(f"""✅ Opt-in is {'' if optin_result['compliant'] else 'not '}compliant.
- Required present: {optin_result['present_required']}
- Prohibited phrases: {optin_result['prohibited_phrases_found']}

✅ Privacy Policy is {'compliant.' if privacy_result['compliant'] else 'not compliant..'}
- Required present: {privacy_result['present_required']}
- Prohibited phrases: {privacy_result['prohibited_phrases_found']}
        """, language="markdown")

# Reference Section
st.markdown("---")
st.markdown("### 📚 Reference Documentation")
st.markdown("- [A2P 10DLC Campaign Approval Requirements](https://support.twilio.com/hc/en-us/articles/1260805599530)")
st.markdown("- [Required Information for Toll-Free Verification](https://support.twilio.com/hc/en-us/articles/10624736761299)")

# Footer
st.markdown("""<div style='text-align: center; color: gray; font-size: 0.8em;'>
For Internal Use Only — Built By Monica Prasad — <a style='color: gray;' href='mailto:mprasad@twilio.com'>mprasad@twilio.com</a>
</div>""", unsafe_allow_html=True)
