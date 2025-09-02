def check_opt_in_compliance(text):
    required_phrases = ["consent", "recurring messages", "message and data rates may apply"]
    prohibited_phrases = ["free trial", "no charges", "anonymous"]

    found = text.lower()
    missing = [phrase for phrase in required_phrases if phrase not in found]
    detected_prohibited = [phrase for phrase in prohibited_phrases if phrase in found]

    return {
        "compliant": len(missing) == 0 and len(detected_prohibited) == 0,
        "missing": missing,
        "prohibited": detected_prohibited
    }

def check_privacy_compliance(text):
    required_phrases = ["third parties", "contact information", "how data is collected", "how data is shared"]
    prohibited_phrases = ["we sell your data", "no privacy", "no protection"]

    found = text.lower()
    missing = [phrase for phrase in required_phrases if phrase not in found]
    detected_prohibited = [phrase for phrase in prohibited_phrases if phrase in found]

    return {
        "compliant": len(missing) == 0 and len(detected_prohibited) == 0,
        "missing": missing,
        "prohibited": detected_prohibited
    }
