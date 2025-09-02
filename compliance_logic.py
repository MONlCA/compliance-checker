from utils import contains_required_language, extract_noncompliant_phrases

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


def check_compliance(opt_in_text: str, privacy_text: str) -> dict:
    results = {}

    # Opt-in logic
    if opt_in_text.strip():
        opt_results = check_opt_in_compliance(opt_in_text)
        if opt_results["compliant"]:
            results["opt_in_feedback"] = "✅ Opt-in language is compliant."
        else:
            results["opt_in_feedback"] = f"❌ Opt-in language is **not compliant**.\n\nMissing elements: {opt_results['matches']}\nProhibited phrases: {opt_results['violations']}"
    else:
        results["opt_in_feedback"] = "No opt-in language provided."

    # Privacy logic
    if privacy_text.strip():
        priv_results = check_privacy_compliance(privacy_text)
        if priv_results["compliant"]:
            results["privacy_feedback"] = "✅ Privacy policy language is compliant."
        else:
            results["privacy_feedback"] = f"❌ Privacy policy is **not compliant**.\n\nMissing elements: {priv_results['matches']}\nProhibited phrases: {priv_results['violations']}"
    else:
        results["privacy_feedback"] = "No privacy policy provided."

    results["customer_copy"] = (
        f"{results['opt_in_feedback']}\n\n{results['privacy_feedback']}"
    )

    return results
