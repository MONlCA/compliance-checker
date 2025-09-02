import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from compliance_logic import check_compliance

from utils import extract_text_from_image, extract_text_from_url

st.set_page_config(page_title="A2P/TFV Compliance Assistance", layout="wide")

# --- Title ---
st.title("A2P/TFV Compliance Assistance")

# --- Dropdowns for Use Case Selection ---
use_case = st.selectbox(
    "Primary Use Case (optional)",
    ["None"] + [
        "2FA",
        "Account Notifications",
        "Customer Care",
        "Delivery Notifications",
        "Fraud Alert Messaging",
        "Higher Education",
        "Marketing",
        "Mixed",
        "Polling and Voting",
        "Public Service Announcement",
        "Security Alert"
    ]
)

special_use_case = st.selectbox(
    "Special Use Case (optional)",
    ["None"] + [
        "Agents; franchise; local branches",
        "Charity / 501(c)(3) Nonprofit",
        "K-12 Education",
        "Proxy",
        "Emergency",
        "Political",
        "Social"
    ]
)

st.markdown("---")

# --- Side-by-Side Input Boxes ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("Opt-in")
    opt_in_input = st.text_area("Paste Opt-in Language or Upload Image (OCR supported)", key="opt_in")

with col2:
    st.subheader("Privacy Policy")
    privacy_input = st.text_area("Paste Privacy Policy Language or Upload Image (OCR supported)", key="privacy")

# --- Submit Button or ENTER Key ---
def on_enter():
    if st.session_state.get("opt_in") or st.session_state.get("privacy"):
        st.session_state.run_check = True

st.text_input("Press Enter to Check Compliance", value="", key="enter_input", on_change=on_enter)

if st.button("Check Compliance") or st.session_state.get("run_check"):
    with st.spinner("Checking compliance..."):
        results = check_compliance(opt_in_input, privacy_input, use_case, special_use_case)

        st.markdown("### 📝 Compliance Results")

        if results.get("opt_in_feedback"):
            st.markdown("#### ✅ Opt-in Feedback")
            st.write(results["opt_in_feedback"])
        
        if results.get("privacy_feedback"):
            st.markdown("#### 🔒 Privacy Policy Feedback")
            st.write(results["privacy_feedback"])

        if results.get("customer_copy"):
            st.markdown("#### 📋 Copy/Paste for Customer")
            st.code(results["customer_copy"], language="markdown")

        st.session_state.run_check = False

# --- Footer with Helpful Links ---
st.markdown("---")
st.markdown("#### 📚 Reference Documentation")
st.markdown("- [A2P 10DLC Campaign Approval Requirements](https://help.twilio.com/articles/11847054539547-A2P-10DLC-Campaign-Approval-Requirements)")
st.markdown("- [Required Information for Toll-Free Verification](https://help.twilio.com/articles/13264118705051-Required-Information-for-Toll-Free-Verification)")

# --- Watermark ---
st.markdown(
    "<div style='text-align: center; color: gray; font-size: small; padding-top: 20px;'>"
    "For Internal Use Only — Built By Monica Prasad — mprasad@twilio.com"
    "</div>",
    unsafe_allow_html=True
)
