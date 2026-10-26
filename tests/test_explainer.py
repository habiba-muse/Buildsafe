from ai.explainer import explain_result

risk = {"overall_score": 21, "risk_level": "moderate", "floor_applied": True}
findings = [
    {"issue": "exposed_reinforcement", "confidence": 0.9},
    {"issue": "wall_crack", "confidence": 0.8},
]
recs = [{"issue": "exposed_reinforcement", "why_it_matters": "Exposed steel can rust."}]

out = explain_result(findings, risk, recs)
text = out["summary"]
assert "21 out of 100" in text
assert "moderate" in text
assert "2 visible indicators" in text
assert "exposed reinforcement" in text
assert "Exposed steel can rust." in text
assert "raised" in text
assert "not a professional engineering inspection" in text
assert out["source"] == "template"

# no findings
out = explain_result([], {"overall_score": 0, "risk_level": "low", "floor_applied": False})
assert "does not mean" in out["summary"]
assert "not a professional engineering inspection" in out["summary"]

# one finding uses singular
out = explain_result([{"issue": "wall_crack", "confidence": 0.7}], {"overall_score": 10, "risk_level": "low", "floor_applied": False})
assert "1 visible indicator " in out["summary"]

print("explainer: all tests passed")
