DISCLAIMER = "This is a preliminary assessment of visible issues only. It is not a professional engineering inspection."

LEVEL_TEXT = {
    "low": "The visible issues look limited, but this cannot be confirmed from photographs alone.",
    "moderate": "Some visible issues may need attention soon.",
    "high": "Several visible indicators may point to a serious problem. Please ask a registered engineer to inspect the building soon.",
}


def explain_result(findings, risk, recommendations=None):
    if not findings:
        text = (
            "No visible issues were detected in these photos. "
            "This does not mean the building is free of problems, "
            "because photographs cannot show hidden issues."
        )
        return {"summary": text + " " + DISCLAIMER, "source": "template"}

    score = risk["overall_score"]
    level = risk["risk_level"]
    count = len(findings)
    plural = "s" if count != 1 else ""

    parts = []
    parts.append(
        "BuildSafe found " + str(count) + " visible indicator" + plural
        + " in your photos. The overall preliminary risk score is "
        + str(score) + " out of 100 (" + level + ")."
    )

    top_issue = findings[0]["issue"]
    parts.append("The most noticeable indicator is " + top_issue.replace("_", " ") + ".")

    for rec in recommendations or []:
        if rec["issue"] == top_issue:
            parts.append(rec["why_it_matters"])
            break

    parts.append(LEVEL_TEXT.get(level, ""))

    if risk.get("floor_applied"):
        parts.append("The level was raised because a serious indicator was detected.")

    parts.append(DISCLAIMER)

    return {"summary": " ".join(p for p in parts if p), "source": "template"}
