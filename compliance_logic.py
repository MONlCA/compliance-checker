required_optin_phrases = [
    "consent to receive messages",
    "message and data rates may apply",
    "reply STOP to unsubscribe",
    "reply HELP for help"
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
