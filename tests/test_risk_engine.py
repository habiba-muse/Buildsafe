from ai.risk_engine import compute_risk

# empty -> all zero
r = compute_risk([])
assert r["categories"] == {"structural": 0, "flood_drainage": 0, "architectural": 0, "materials": 0}

# one finding at full confidence
r = compute_risk([{"issue": "exposed_reinforcement", "confidence": 1.0}])
assert r["categories"]["structural"] == 50
assert r["categories"]["materials"] == 40
assert r["severity"]["exposed_reinforcement"] == "high"

# confidence scales the score
r = compute_risk([{"issue": "wall_crack", "confidence": 0.5}])
assert r["categories"]["structural"] == 20

# score is capped at 100
r = compute_risk([
    {"issue": "damaged_roofing", "confidence": 1.0},
    {"issue": "exposed_reinforcement", "confidence": 1.0},
    {"issue": "wall_crack", "confidence": 1.0},
])
assert r["categories"]["structural"] == 100

# unknown issue is ignored safely
r = compute_risk([{"issue": "alien_goo", "confidence": 0.9}])
assert r["severity"]["alien_goo"] == "unknown"
assert r["categories"]["structural"] == 0

print("risk_engine: all tests passed")
