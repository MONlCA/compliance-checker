from utils import contains_required_language, extract_noncompliant_phrases

# Acceptable language patterns
opt_in_patterns = [
    r"message\s+frequency\s+varies",
    r"message\s+and\s+data\s+rates\s+may\s+apply",
    r"reply\s+STOP\s+to\s+opt\s+out",
    r"reply\s+HELP\s+for\s+help",
    r"\bagree\s+to\s+receive\s+SMS",
    r"by\s+providing\s+your\s+phone\s+number.*?(consent|agree)",
]

privacy_policy_patterns = [
    r"we\s+do\s+not\s+share.*?(third\s+parties|affiliates).*?marketing",
    r"text\s+messaging\s+originator.*?will\s+not\s+be\s+shared",
    r"subcontractors.*?(support|services|customer service)",
]

# Blocked / misleading phrases
blocked_opt_in_phrases = [
    r"free\s+SMS",
    r"no\s+cost\s+messages",
    r"we\s+may\s+share\s+your\s+number",
]

blocked_privacy_phrases = [
    r"we\s+may\s+share.*?with\s+partners",
    r"your\s+information\s+may\s+be\s+sold",
    r"may\s+disclose.*?without\s+notice",
]

def check_opt_in_compliance(text: str) -> dict:
    matches, missing = contains_required_language(text, opt_in_patterns)
    violations = extract_noncompliant_phrases(text, blocked_opt_in_phrases)
    return {
        "compliant": len(matches) >= 4 and not violations,
        "matches": matches,
        "missing": missing,
        "violations": violations
    }

def check_privacy_compliance(text: str) -> dict:
    matches, missing = contains_required_language(text, privacy_policy_patterns)
    violations = extract_noncompliant_phrases(text, blocked_privacy_phrases)
    return {
        "compliant": len(matches) >= 2 and not violations,
        "matches": matches,
        "missing": missing,
        "violations": violations
    }
