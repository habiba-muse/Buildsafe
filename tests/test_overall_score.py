from ai.risk_engine import compute_overall, risk_level, compute_risk

# empty
r = compute_risk([])
assert r["overall_score"] == 0
assert r["risk_level"] == "low"

# weighted formula (matches the spec example: 72/58/76/61 -> 67)
cats = {"structural": 72, "flood_drainage": 58, "architectural": 76, "materials": 61}
assert compute_overall(cats) == 67

# all 100 -> 100
cats = {"structural": 100, "flood_drainage": 100, "architectural": 100, "materials": 100}
assert compute_overall(cats) == 100

# level boundaries
assert risk_level(29) == "low"
assert risk_level(30) == "moderate"
assert risk_level(59) == "moderate"
assert risk_level(60) == "high"

# serious issue raises low -> moderate
r = compute_risk([{"issue": "exposed_reinforcement", "confidence": 0.9}])
assert r["overall_score"] == 21
assert r["risk_level"] == "moderate"
assert r["floor_applied"] is True

# same issue, low confidence -> no raise
r = compute_risk([{"issue": "exposed_reinforcement", "confidence": 0.5}])
assert r["risk_level"] == "low"
assert r["floor_applied"] is False

print("overall score: all tests passed")
