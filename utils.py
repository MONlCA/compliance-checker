import re

def contains_required_language(text: str, required_patterns: list[str]) -> list[str]:
    """
    Checks for the presence of required language patterns in a given text.
    Returns a list of matching patterns.
    """
    matches = []
    for pattern in required_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            matches.append(pattern)
    return matches

def extract_noncompliant_phrases(text: str, blocked_patterns: list[str]) -> list[str]:
    """
    Identifies known non-compliant phrases or patterns in the given text.
    Returns a list of problematic patterns found.
    """
    flagged = []
    for pattern in blocked_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            flagged.append(pattern)
    return flagged

def format_feedback(header: str, items: list[str], icon: str = "❌") -> str:
    """
    Formats the feedback message with an icon and bullet point list.
    """
    if not items:
        return f"✅ {header} appears compliant."
    
    message = f"{icon} **{header} issues found:**\n"
    for item in items:
        message += f"- {icon} `{item}`\n"
    return message
