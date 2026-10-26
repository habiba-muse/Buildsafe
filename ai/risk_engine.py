import json
import os

RULES_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "knowledge",
    "severity_rules.json",
)

CATEGORIES = ["structural", "flood_drainage", "architectural", "materials"]

WEIGHTS = {
    "structural": 0.35,
    "flood_drainage": 0.30,
    "architectural": 0.20,
    "materials": 0.15,
}

HIGH_SEVERITY_CONFIDENCE = 0.7


def load_rules():
    with open(RULES_PATH, encoding="utf-8-sig") as f:
        return json.load(f)


def compute_overall(categories):
    total = sum(categories[c] * WEIGHTS[c] for c in CATEGORIES)
    return round(total)


def risk_level(score):
    if score >= 60:
        return "high"
    if score >= 30:
        return "moderate"
    return "low"


def compute_risk(findings, rules=None):
    if rules is None:
        rules = load_rules()

    totals = {c: 0.0 for c in CATEGORIES}
    severity = {}
    has_serious_issue = False

    for f in findings:
        rule = rules.get(f["issue"])
        if rule is None:
            severity[f["issue"]] = "unknown"
            continue
        severity[f["issue"]] = rule["severity"]
        if rule["severity"] == "high" and f["confidence"] >= HIGH_SEVERITY_CONFIDENCE:
            has_serious_issue = True
        for category, points in rule["impact"].items():
            totals[category] += points * f["confidence"]

    categories = {c: min(100, round(v)) for c, v in totals.items()}
    overall = compute_overall(categories)
    level = risk_level(overall)

    floor_applied = False
    if has_serious_issue and level == "low":
        level = "moderate"
        floor_applied = True

    return {
        "overall_score": overall,
        "risk_level": level,
        "floor_applied": floor_applied,
        "categories": categories,
        "severity": severity,
    }
