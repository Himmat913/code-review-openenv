def normalize(text):
    return text.lower().replace("_", "").replace(" ", "")

def grade(task, action):
    expected = task["expected"]

    score = 0.0

    issue = normalize(action.get("issue", ""))
    impact = action.get("impact", "").lower()
    fix = action.get("fix", "").lower()

    expected_issue = normalize(expected["issue"])
    expected_impact = expected["impact"].lower()
    expected_fix = expected["fix"].lower()

    if expected_issue in issue:
        score += 0.4

    if any(word in impact for word in expected_impact.split()):
        score += 0.3

    if any(word in fix for word in expected_fix.split()):
        score += 0.3

    score = round(score, 4)
    score = max(0.0001, min(score, 0.9999))

    return score