from utils import contains_required_language, extract_noncompliant_phrases

# Acceptable opt-in language patterns
opt_in_patterns = [
    r"message\s+frequency\s+varies",
    r"message\s+and\s+data\s+rates\s+may\s+apply",
    r"reply\s+STOP\s+to\s+opt\s+out",
    r"reply\s+HELP\s+for\s+help",
    r"\bagree\s+to\s+receive\s+SMS",
    r"by\s+providing\s+your\s+phone\s+number.*?(consent|agree)",
]

# Acceptable privacy policy language patterns
privacy_policy_patterns = [
    r"we\s+do\s+not\s+share.*?(third\s+parties|affiliates).*?marketing",
    r"text\s+messaging\s+originator.*?will\s+not\s+be\s+shared",
    r"subcontractors.*?(support|services|customer service)",
]

# Known non-compliant or misleading phrases
blocked_opt_in_phrases = [
    r"free\s+SMS",                      # implies no data rates ever
    r"no\s+cost\s+messages",            # misleading
    r"we\s+may\s+share\s+your\s+number" # privacy concern
]

blocked_privacy_phrases = [
    r"we\s+may\s+share.*?with\s+partners",
    r"your\s+information\s+may\s+be\s+sold",
    r"may\s+disclose.*?without\s+notice",
]

def check_opt_in_compliance(text: str) -> dict:
    matches = contains_required_language(text, opt_in_patterns)
    violations = extract_noncompliant_phrases(text, blocked_opt_in_phrases)
    return {
        "compliant": len(matches) >= 4 and not violations,
        "matches": matches,
        "violations": violations
    }

def check_privacy_compliance(text: str) -> dict:
    matches = contains_required_language(text, privacy_policy_patterns)
    violations = extract_noncompliant_phrases(text, blocked_privacy_phrases)
    return {
        "compliant": len(matches) >= 2 and not violations,
        "matches": matches,
        "violations": violations
    }

def check_compliance(opt_in_text: str, privacy_policy_text: str, use_case: str = None) -> dict:
    """
    Wrapper function for the main app to evaluate both opt-in and privacy policy compliance.
    """
    return {
        "opt_in_result": check_opt_in_compliance(opt_in_text),
        "privacy_result": check_privacy_compliance(privacy_policy_text),
    }
