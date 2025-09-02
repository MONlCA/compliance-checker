import streamlit as st
from utils import extract_text_from_image, extract_text_from_url
from compliance_logic import check_opt_in_compliance, check_privacy_compliance

st.set_page_config(page_title="📲 A2P/TFV Compliance Assistance", layout="wide")

st.markdown("## 📲 A2P/TFV Compliance Assistance")
st.markdown("---")

# Layout Columns
optin_col, privacy_col = st.columns(2)

with optin_col:
    st.subheader("Opt-in")
    optin_input = st.text_area("Paste Opt-in Language or Upload Image", height=150, label_visibility="collapsed")
    optin_image = st.file_uploader("Or upload Opt-in Screenshot", type=["png", "jpg", "jpeg"])

with privacy_col:
    st.subheader("Privacy Policy")
    privacy_input = st.text_area("Paste Privacy Policy Language or Upload Image / URL", height=150, label_visibility="collapsed")
    privacy_image = st.file_uploader("Or upload Privacy Policy Screenshot", type=["png", "jpg", "jpeg"])

if st.button("✅ Check Compliance"):
    st.markdown("### 📋 Compliance Results")
    with st.expander("✅ Opt-in Feedback", expanded=True):
        if not optin_input and not optin_image:
            st.warning("⚠️ No opt-in language provided.")
        else:
            optin_text = optin_input or extract_text_from_image(optin_image)
            optin_result = check_opt_in_compliance(optin_text)
            if optin_result["compliant"]:
                st.success("✅ Opt-in is compliant.")
            else:
                st.error("❌ Opt-in is not compliant.")
            st.markdown(f"- **Missing elements**: {optin_result['missing']}")
            st.markdown(f"- **Prohibited phrases**: {optin_result['prohibited']}")

    with st.expander("📄 Privacy Policy Feedback", expanded=True):
        if not privacy_input and not privacy_image:
            st.warning("⚠️ No privacy policy provided.")
        else:
            privacy_text = privacy_input
            if not privacy_input and privacy_image:
                privacy_text = extract_text_from_image(privacy_image)
            elif privacy_input.startswith("http"):
                privacy_text = extract_text_from_url(privacy_input)

            privacy_result = check_privacy_compliance(privacy_text)

            if privacy_result["compliant"]:
                st.success("✅ Privacy policy is compliant.")
            else:
                st.error("❌ Privacy policy is not compliant.")

            st.markdown(f"**Missing Required Phrases:**\n```\n{privacy_result['missing']}\n```")
            st.markdown(f"**Prohibited Phrases Found:**\n```\n{privacy_result['prohibited']}\n```")

    with st.expander("📝 Copy/Paste for Customer"):
        st.code(f"""✅ Opt-in is {'compliant' if optin_result['compliant'] else 'not compliant'}.
- Missing elements: {optin_result['missing']}
- Prohibited phrases: {optin_result['prohibited']}

✅ Privacy Policy is {'compliant' if privacy_result['compliant'] else 'not compliant'}.
- Missing elements: {privacy_result['missing']}
- Prohibited phrases: {privacy_result['prohibited']}
""")

st.markdown("---")
st.markdown("### 📚 Reference Documentation")
st.markdown("- [A2P 10DLC Campaign Approval Requirements](https://support.twilio.com/hc/en-us/articles/1260805599430)")
st.markdown("- [Required Information for Toll-Free Verification](https://support.twilio.com/hc/en-us/articles/1260805413030)")
st.markdown("---")
st.markdown("For Internal Use Only — Built By Monica Prasad — [mprasad@twilio.com](mailto:mprasad@twilio.com)")
