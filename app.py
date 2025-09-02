import streamlit as st
from PIL import Image
import re
import base64
from utils import analyze_opt_in, analyze_privacy_policy, extract_text_from_image, get_examples_for_use_case

st.set_page_config(layout="wide", page_title="A2P/TFV Compliance Assistance")
st.markdown("""
    <style>
        .title-style {
            font-size: 28px;
            font-weight: bold;
            margin-bottom: 10px;
        }
        .subheader {
            font-size: 20px;
            font-weight: 600;
            margin-top: 30px;
        }
        .disclaimer {
            margin-top: 40px;
            font-size: 14px;
            color: gray;
            text-align: center;
        }
        .docs-link {
            font-size: 16px;
            margin-top: 20px;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="title-style">A2P/TFV Compliance Assistance</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Opt-In Flow")
    opt_in_text = st.text_area("Paste opt-in language, script, or upload screenshot", height=200, key="opt_in_text")
    opt_in_image = st.file_uploader("Upload Opt-In Screenshot (optional)", type=["png", "jpg", "jpeg"], key="opt_in_image")

with col2:
    st.subheader("Privacy Policy")
    privacy_policy_text = st.text_area("Paste privacy policy text or upload screenshot", height=200, key="privacy_policy_text")
    privacy_policy_image = st.file_uploader("Upload Privacy Policy Screenshot (optional)", type=["png", "jpg", "jpeg"], key="privacy_policy_image")

st.markdown("---")

st.subheader("Campaign Use Case")
standard_use_case = st.selectbox("Select a standard use case (optional)", ["None", "2FA", "Account Notifications", "Customer Care", "Delivery Notifications", "Fraud Alert Messaging", "Higher Education", "Marketing", "Mixed", "Polling and Voting", "Public Service Announcement", "Security Alert"])
special_use_case = st.selectbox("Select a special use case (optional)", ["None", "Agents; franchise; local branches", "Charity / 501(c)(3) Nonprofit", "K-12 Education", "Proxy", "Emergency", "Political", "Social"])

if st.button("Check Compliance") or st.session_state.get("check_triggered"):
    st.session_state.check_triggered = True

    # Extract from image if available
    if opt_in_image:
        opt_in_text = extract_text_from_image(opt_in_image)
    if privacy_policy_image:
        privacy_policy_text = extract_text_from_image(privacy_policy_image)

    use_case = standard_use_case if standard_use_case != "None" else special_use_case

    with st.expander("Opt-In Compliance Results", expanded=True):
        opt_in_result = analyze_opt_in(opt_in_text, use_case)
        st.markdown(opt_in_result["verdict"])
        for reason in opt_in_result["reasons"]:
            st.markdown(reason)

    with st.expander("Privacy Policy Compliance Results", expanded=True):
        privacy_result = analyze_privacy_policy(privacy_policy_text, use_case)
        st.markdown(privacy_result["verdict"])
        for reason in privacy_result["reasons"]:
            st.markdown(reason)

    with st.expander("Copy/Paste for Customer", expanded=True):
        combined_text = ""
        if opt_in_result:
            combined_text += "**Opt-In Review:**\n" + opt_in_result["summary"] + "\n\n"
        if privacy_result:
            combined_text += "**Privacy Policy Review:**\n" + privacy_result["summary"] + "\n"
        st.text_area("Copy this to paste into customer ticket:", value=combined_text, height=200)

st.markdown("---")

st.markdown('<div class="docs-link">📄 <a href="https://help.twilio.com/articles/11847054539547-A2P-10DLC-Campaign-Approval-Requirements" target="_blank">A2P 10DLC Campaign Approval Requirements</a></div>', unsafe_allow_html=True)
st.markdown('<div class="docs-link">📄 <a href="https://help.twilio.com/articles/13264118705051-Required-Information-for-Toll-Free-Verification" target="_blank">Required Information for Toll-Free Verification</a></div>', unsafe_allow_html=True)

st.markdown("""
    <div class="disclaimer">
        For Internal Use Only — Built By Monica Prasad — mprasad@twilio.com
    </div>
""", unsafe_allow_html=True)

# Allow Enter key to trigger compliance check
st.markdown("""
    <script>
        const textareas = parent.document.querySelectorAll('textarea');
        textareas.forEach(el => el.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' && e.metaKey === false && e.ctrlKey === false && !e.shiftKey) {
                const button = parent.document.querySelector('button[kind="primary"]');
                if (button) button.click();
            }
        }));
    </script>
""", unsafe_allow_html=True)
