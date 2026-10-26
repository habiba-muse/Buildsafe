import json
import os

RULES_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "knowledge",
    "severity_rules.json",
)

CATEGORIES = ["structural", "flood_drainage", "architectural", "materials"]


def load_rules():
    with open(RULES_PATH, encoding="utf-8-sig") as f:
        return json.load(f)


def compute_risk(findings, rules=None):
    if rules is None:
        rules = load_rules()

    totals = {c: 0.0 for c in CATEGORIES}
    severity = {}

    for f in findings:
        rule = rules.get(f["issue"])
        if rule is None:
            severity[f["issue"]] = "unknown"
            continue
        severity[f["issue"]] = rule["severity"]
        for category, points in rule["impact"].items():
            totals[category] += points * f["confidence"]

    categories = {c: min(100, round(v)) for c, v in totals.items()}
    return {"categories": categories, "severity": severity}
