import streamlit as st
from utils import extract_text_from_image, extract_text_from_url
from compliance_logic import check_compliance

st.set_page_config(layout="wide")
st.markdown("# A2P/TFV Compliance Assistance")

# --- Layout ---
col1, col2 = st.columns(2)

with col1:
    st.markdown("### Opt-in")
    opt_in_input = st.text_area("Paste Opt-in Language or Upload Image (OCR supported)", height=120)
    opt_in_image = st.file_uploader("Or upload Opt-in Screenshot", type=["png", "jpg", "jpeg"], key="opt_in_image")

with col2:
    st.markdown("### Privacy Policy")
    privacy_input = st.text_area("Paste Privacy Policy Language or Upload Image (OCR supported)", height=120)
    privacy_image = st.file_uploader("Or upload Privacy Policy Screenshot or Link", type=["png", "jpg", "jpeg"], key="privacy_image")
    privacy_url = st.text_input("Or enter Privacy Policy URL")

# --- OCR & Extraction Logic ---
if opt_in_image:
    opt_in_input = extract_text_from_image(opt_in_image)

if privacy_image:
    privacy_input = extract_text_from_image(privacy_image)

if privacy_url and not privacy_input:
    privacy_input = extract_text_from_url(privacy_url)

# --- Check Compliance Button ---
if st.button("Check Compliance"):
    with st.spinner("Checking compliance..."):
        if not opt_in_input.strip() and not privacy_input.strip():
            st.warning("Please enter at least Opt-in or Privacy Policy text.")
        else:
            try:
                results = check_compliance(opt_in_input, privacy_input)

                st.markdown("### 📝 Compliance Results")

                st.markdown("#### ✅ Opt-in Feedback")
                st.write(results.get("opt_in_feedback", "No opt-in input provided or match found."))

                st.markdown("#### 🔒 Privacy Policy Feedback")
                st.write(results.get("privacy_feedback", "No privacy policy input provided or match found."))

                st.markdown("#### 📋 Copy/Paste for Customer")
                st.code(results.get("customer_copy", "No customer message generated."), language="markdown")

            except Exception as e:
                st.error(f"An error occurred: {e}")

# --- Footer ---
st.divider()
st.markdown("### 📚 Reference Documentation")
st.markdown("- [A2P 10DLC Campaign Approval Requirements](https://support.twilio.com/hc/en-us/articles/1500001265802)")
st.markdown("- [Required Information for Toll-Free Verification](https://support.twilio.com/hc/en-us/articles/360056451333)")
st.markdown("<br><center><sub>For Internal Use Only — Built By Monica Prasad — mprasad@twilio.com</sub></center>", unsafe_allow_html=True)
