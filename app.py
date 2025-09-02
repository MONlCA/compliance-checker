import streamlit as st
from utils import extract_text_from_image, extract_text_from_url
from compliance_logic import check_opt_in_compliance, check_privacy_compliance

st.set_page_config(page_title="A2P/TFV Compliance Assistant", layout="wide")
st.title("📲 A2P/TFV Compliance Assistance")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Opt-in")
    optin_text = st.text_area("Paste Opt-in Language or Upload Image", height=150)
    optin_image = st.file_uploader("Or upload Opt-in Screenshot", type=["png", "jpg", "jpeg"])

with col2:
    st.subheader("Privacy Policy")
    privacy_text = st.text_area("Paste Privacy Policy Language or Upload Image / URL", height=150)
    privacy_image = st.file_uploader("Or upload Privacy Policy Screenshot", type=["png", "jpg", "jpeg"])

st.markdown("")

if st.button("✅ Check Compliance"):
    with st.expander("📝 Compliance Results", expanded=True):
        if not optin_text and optin_image:
            optin_text = extract_text_from_image(optin_image)
        elif optin_text.startswith("http"):
            optin_text = extract_text_from_url(optin_text)

        if not privacy_text and privacy_image:
            privacy_text = extract_text_from_image(privacy_image)
        elif privacy_text.startswith("http"):
            privacy_text = extract_text_from_url(privacy_text)

        optin_result = check_opt_in_compliance(optin_text)
        privacy_result = check_privacy_compliance(privacy_text)

        st.subheader("✅ Opt-in Feedback")
        st.write(optin_result["message"])
        if not optin_text.strip():
            st.info("No opt-in language provided.")

        st.subheader("📄 Privacy Policy Feedback")
        st.write(f"**Compliance Status:** {'✅ Compliant' if privacy_result['compliant'] else '❌ Not compliant'}")
        st.write(f"**Detected Required Phrases:** {privacy_result['present']}")
        st.write(f"**Prohibited Phrases Found:** {privacy_result['prohibited']}")

        st.subheader("📋 Copy/Paste for Customer")
        customer_msg = (
            f"✅ Opt-in is {'compliant' if optin_result['compliant'] else 'not compliant'}.\n"
            f" - Required present: {optin_result['present']}\n"
            f" - Prohibited phrases: {optin_result['prohibited']}\n\n"
            f"✅ Privacy Policy is {'compliant' if privacy_result['compliant'] else 'not compliant'}.\n"
            f" - Required present: {privacy_result['present']}\n"
            f" - Prohibited phrases: {privacy_result['prohibited']}\n"
        )
        st.code(customer_msg, language="markdown")

st.divider()
st.subheader("📚 Reference Documentation")
st.markdown("- [A2P 10DLC Campaign Approval Requirements](https://support.twilio.com/hc/en-us/articles/1500001471602)")
st.markdown("- [Required Information for Toll-Free Verification](https://support.twilio.com/hc/en-us/articles/360052171013)")

st.markdown("---")
st.markdown("For Internal Use Only — Built By Monica Prasad — [mprasad@twilio.com](mailto:mprasad@twilio.com)")
