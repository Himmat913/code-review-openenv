def normalize(text):
    return (text or "").lower().replace("_", "").replace(" ", "")

def safe_match(expected, actual):
    if not expected.strip():
        return False
    return any(word for word in expected.split() if word in actual)

def grade(task, action):
    expected = task.get("expected", {})

    score = 0.0

    issue = normalize(action.get("issue"))
    impact = (action.get("impact") or "").lower()
    fix = (action.get("fix") or "").lower()

    expected_issue = normalize(expected.get("issue"))
    expected_impact = (expected.get("impact") or "").lower()
    expected_fix = (expected.get("fix") or "").lower()

    # FIX 1: prevent empty string auto-match
    if expected_issue and expected_issue in issue:
        score += 0.4

    if safe_match(expected_impact, impact):
        score += 0.3

    if safe_match(expected_fix, fix):
        score += 0.3

    # FIX 2: ALWAYS enforce strict range AFTER everything
    if score <= 0.0:
        score = 1e-6
    elif score >= 1.0:
        score = 1.0 - 1e-6

    return float(score)