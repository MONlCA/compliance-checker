import streamlit as st
from utils import extract_text_from_image, extract_text_from_url
from compliance_logic import check_opt_in_compliance, check_privacy_compliance

st.set_page_config(page_title="A2P/TFV Compliance Assistance", layout="wide")
st.title("📡 A2P/TFV Compliance Assistance")

st.markdown("---")
col1, col2 = st.columns(2)

# Opt-in Input
with col1:
    st.subheader("Opt-in")
    opt_in_text = st.text_area("Paste Opt-in Language or Upload Image", height=150, label_visibility="collapsed")
    opt_in_image = st.file_uploader("Or upload Opt-in Screenshot", type=["png", "jpg", "jpeg"])

# Privacy Policy Input
with col2:
    st.subheader("Privacy Policy")
    privacy_text = st.text_area("Paste Privacy Policy Language or URL or Upload Image", height=150, label_visibility="collapsed")
    privacy_image = st.file_uploader("Or upload Privacy Policy Screenshot", type=["png", "jpg", "jpeg"])

st.markdown("---")

# Compliance Button
if st.button("✅ Check Compliance"):
    # Process opt-in
    opt_in_final = ""
    if opt_in_image:
        opt_in_final = extract_text_from_image(opt_in_image)
    elif opt_in_text.strip():
        opt_in_final = opt_in_text.strip()

    # Process privacy policy
    privacy_final = ""
    if privacy_image:
        privacy_final = extract_text_from_image(privacy_image)
    elif privacy_text.strip().startswith("http"):
        privacy_final = extract_text_from_url(privacy_text.strip())
    else:
        privacy_final = privacy_text.strip()

    # Run checks
    optin_results = check_opt_in_compliance(opt_in_final)
    privacy_results = check_privacy_compliance(privacy_final)

    st.subheader("📝 Compliance Results")

    st.markdown("### ✅ Opt-in Feedback")
    if not opt_in_final:
        st.warning("No opt-in language provided.")
    else:
        st.markdown(f"**Compliance Status:** {'🟢 Compliant' if optin_results['compliant'] else '🔴 Not compliant'}")
        st.markdown(f"**Detected Required Phrases:** {optin_results['matches']}")
        st.markdown(f"**Prohibited Phrases Found:** {optin_results['violations']}")

    st.markdown("### 🔐 Privacy Policy Feedback")
    if not privacy_final:
        st.warning("No privacy policy provided.")
    else:
        st.markdown(f"**Compliance Status:** {'🟢 Compliant' if privacy_results['compliant'] else '🔴 Not compliant'}")
        st.markdown(f"**Detected Required Phrases:** {privacy_results['matches']}")
        st.markdown(f"**Prohibited Phrases Found:** {privacy_results['violations']}")

    st.markdown("### 📋 Copy/Paste for Customer")
    with st.expander("Click to Expand"):
        st.code(f"""
✅ Opt-in is {'compliant' if optin_results['compliant'] else 'not compliant'}.
  - Required present: {optin_results['matches']}
  - Prohibited phrases: {optin_results['violations']}

✅ Privacy Policy is {'compliant' if privacy_results['compliant'] else 'not compliant'}.
  - Required present: {privacy_results['matches']}
  - Prohibited phrases: {privacy_results['violations']}
""", language="text")

st.markdown("---")
st.subheader("📚 Reference Documentation")
st.markdown("- [A2P 10DLC Campaign Approval Requirements](https://support.twilio.com/hc/en-us/articles/1500001474481)")
st.markdown("- [Required Information for Toll-Free Verification](https://support.twilio.com/hc/en-us/articles/5376885637901)")

st.markdown(
    "<center><small>For Internal Use Only — Built By Monica Prasad — <a href='mailto:mprasad@twilio.com'>mprasad@twilio.com</a></small></center>",
    unsafe_allow_html=True
)
