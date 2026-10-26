import json
import os

REC_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "knowledge",
    "recommendations.json",
)


def load_recommendations():
    with open(REC_PATH, encoding="utf-8-sig") as f:
        return json.load(f)


def get_recommendations(findings, recs=None):
    if recs is None:
        recs = load_recommendations()

    results = []
    for f in findings:
        rec = recs.get(f["issue"])
        if rec is None:
            continue
        results.append({"issue": f["issue"], **rec})
    return results
