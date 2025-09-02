import streamlit as st
from PIL import Image
import pytesseract
import requests
from bs4 import BeautifulSoup
import io
import re

# --- Utility Functions (from utils.py) ---

def extract_text_from_image(uploaded_file):
    """
    Extracts text from an uploaded image file using OCR.
    """
    try:
        image = Image.open(uploaded_file)
        # Using pytesseract to perform OCR on the image
        text = pytesseract.image_to_string(image)
        return text
    except Exception as e:
        return f"Failed to extract text from image: {e}"

def extract_text_from_url(url):
    """
    Scrapes and extracts text content from a given URL.
    """
    try:
        response = requests.get(url, timeout=10)
        # Ensure the request was successful
        response.raise_for_status()  
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup.get_text(separator=' ', strip=True)
    except requests.exceptions.RequestException as e:
        return f"Failed to fetch content from URL: {e}"
    except Exception as e:
        return f"An error occurred during URL processing: {e}"

# --- Compliance Logic (from compliance_logic.py) ---

# Pre-defined compliance phrases
required_optin_phrases = [
    "consent to receive messages",
    "message and data rates may apply",
    "reply stop to unsubscribe",
    "reply help for help"
]

prohibited_optin_phrases = [
    "you will not receive any messages",
    "we will not contact you"
]

required_privacy_phrases = [
    "how information is collected",
    "how information is used",
    "how to opt-out",
    "third parties",
    "data security",
    "contact information"
]

prohibited_privacy_phrases = [
    "we sell your data",
    "no responsibility",
    "at your own risk"
]

def check_opt_in_compliance(text: str):
    """
    Checks opt-in language for compliance with required and prohibited phrases.
    """
    if not text.strip():
        return {
            "compliant": False,
            "message": "⚠️ No opt-in language provided.",
            "present_required": [],
            "missing_required": required_optin_phrases,
            "prohibited_phrases_found": []
        }

    lower_text = text.lower()
    present_required = [phrase for phrase in required_optin_phrases if phrase in lower_text]
    prohibited_found = [phrase for phrase in prohibited_optin_phrases if phrase in lower_text]
    missing_required = [phrase for phrase in required_optin_phrases if phrase not in lower_text]

    compliant = len(missing_required) == 0 and len(prohibited_found) == 0

    return {
        "compliant": compliant,
        "message": "✅ Opt-in is compliant." if compliant else "❌ Opt-in is not compliant.",
        "present_required": present_required,
        "missing_required": missing_required,
        "prohibited_phrases_found": prohibited_found
    }

def check_privacy_compliance(text: str):
    """
    Checks privacy policy for compliance with required and prohibited phrases.
    """
    if not text.strip():
        return {
            "compliant": False,
            "present_required": [],
            "missing_required": required_privacy_phrases,
            "prohibited_phrases_found": []
        }

    lower_text = text.lower()
    present_required = [phrase for phrase in required_privacy_phrases if phrase in lower_text]
    prohibited_found = [phrase for phrase in prohibited_privacy_phrases if phrase in lower_text]
    missing_required = [phrase for phrase in required_privacy_phrases if phrase not in lower_text]

    compliant = len(missing_required) == 0 and len(prohibited_found) == 0

    return {
        "compliant": compliant,
        "present_required": present_required,
        "missing_required": missing_required,
        "prohibited_phrases_found": prohibited_found
    }

# --- Streamlit Application UI ---

st.set_page_config(page_title="A2P/TFV Compliance Assistance", layout="wide")

st.markdown("## 📲 A2P/TFV Compliance Assistance")

# Input Sections
col1, col2 = st.columns(2)

with col1:
    st.markdown("### Opt-in")
    optin_text = st.text_area("Paste Opt-in Language or Upload Image", height=100, label_visibility="collapsed", key="optin_text_area")
    optin_image = st.file_uploader("Or upload Opt-in Screenshot", type=["png", "jpg", "jpeg"], label_visibility="visible", key="optin_uploader")

with col2:
    st.markdown("### Privacy Policy")
    privacy_text = st.text_area("Paste Privacy Policy Language or Upload Image / URL", height=100, label_visibility="collapsed", key="privacy_text_area")
    privacy_image = st.file_uploader("Or upload Privacy Policy Screenshot", type=["png", "jpg", "jpeg"], label_visibility="visible", key="privacy_uploader")

# --- Logic to handle different input types ---
processed_optin_text = ""
if optin_image:
    processed_optin_text = extract_text_from_image(optin_image)
elif optin_text:
    processed_optin_text = optin_text

processed_privacy_text = ""
if privacy_image:
    processed_privacy_text = extract_text_from_image(privacy_image)
elif privacy_text and privacy_text.startswith("http"):
    processed_privacy_text = extract_text_from_url(privacy_text)
elif privacy_text:
    processed_privacy_text = privacy_text

# Button to trigger compliance check
if st.button("✅ Check Compliance", key="check_button"):
    st.markdown("### 🗂️ Compliance Results")

    col_optin, col_privacy = st.columns(2)

    with col_optin:
        st.markdown("#### ✅ Opt-in Feedback")
        optin_result = check_opt_in_compliance(processed_optin_text)
        
        # New logic to handle empty opt-in and display errors line-by-line
        if not processed_optin_text.strip():
            st.warning("⚠️ No opt-in language provided.")
        else:
            st.write(optin_result["message"])
            st.markdown("**Required Phrases:**")
            for p in required_optin_phrases:
                if p in processed_optin_text.lower():
                    st.markdown(f"✔️ {p}")
                else:
                    st.markdown(f"❌ {p}")

        if optin_result["prohibited_phrases_found"]:
            st.markdown("**Non-Compliant Phrases Found:**")
            for p in optin_result['prohibited_phrases_found']:
                st.markdown(f"🟥 {p}")

    with col_privacy:
        st.markdown("#### 📄 Privacy Policy Feedback")
        privacy_result = check_privacy_compliance(processed_privacy_text)
        
        # Corrected logic to only show checkmarks if compliant
        if not processed_privacy_text.strip():
            st.warning("⚠️ No privacy policy language provided.")
        else:
            st.markdown(f"**Compliance Status:** {'🟩 Compliant' if privacy_result['compliant'] else '🟥 Not Compliant'}")
            st.markdown("**Required Phrases:**")
            
            # Updated logic to show a checkmark only if the policy is compliant
            # This is to avoid showing a checkmark for a phrase when the overall policy is not compliant
            if privacy_result['compliant']:
                for p in required_privacy_phrases:
                    st.markdown(f"✔️ {p}")
            else:
                for p in required_privacy_phrases:
                    st.markdown(f"❌ {p}")
            
            if privacy_result["prohibited_phrases_found"]:
                st.markdown("**Non-Compliant Phrases Found:**")
                for p in privacy_result['prohibited_phrases_found']:
                    st.markdown(f"🟥 {p}")

    # --- Copy/Paste Summary ---
    st.markdown("---")
    st.markdown("#### 🧾 Copy/Paste for Customer")
    with st.expander("📋 Click to Expand"):
        # The f-string is now more carefully constructed to handle newlines and indentation
        summary = f"""**Opt-in Compliance:** {'Compliant' if optin_result['compliant'] else 'Not Compliant'}
- Required Phrases Present: {', '.join(optin_result['present_required']) if optin_result['present_required'] else 'None'}
- Missing Required Phrases: {', '.join(optin_result['missing_required']) if optin_result['missing_required'] else 'None'}
- Non-Compliant Phrases Found: {', '.join(optin_result['prohibited_phrases_found']) if optin_result['prohibited_phrases_found'] else 'None'}

**Privacy Policy Compliance:** {'Compliant' if privacy_result['compliant'] else 'Not Compliant'}
- Required Phrases Present: {', '.join(privacy_result['present_required']) if privacy_result['present_required'] else 'None'}
- Missing Required Phrases: {', '.join(privacy_result['missing_required']) if privacy_result['missing_required'] else 'None'}
- Non-Compliant Phrases Found: {', '.join(privacy_result['prohibited_phrases_found']) if privacy_result['prohibited_phrases_found'] else 'None'}
"""
        st.code(summary, language="markdown")

# Reference Section
st.markdown("---")
st.markdown("### 📚 Reference Documentation")
st.markdown("- [A2P 10DLC Campaign Approval Requirements](https://support.twilio.com/hc/en-us/articles/1260805599530)")
st.markdown("- [Required Information for Toll-Free Verification](https://support.twilio.com/hc/en-us/articles/10624736761299)")

# Footer
st.markdown("""<div style='text-align: center; color: gray; font-size: 0.8em;'>
For Internal Use Only — Built By Monica Prasad — <a style='color: gray;' href='mailto:mprasad@twilio.com'>mprasad@twilio.com</a>
</div>""", unsafe_allow_html=True)
