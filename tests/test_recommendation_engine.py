from ai.recommendation_engine import get_recommendations, load_recommendations
from ai.risk_engine import load_rules

REQUIRED = ["title", "why_it_matters", "possible_causes", "actions", "materials", "see_professional"]

# every issue in the risk rules must have a full recommendation
recs = load_recommendations()
for issue in load_rules():
    assert issue in recs, "missing recommendation for " + issue
    for key in REQUIRED:
        assert recs[issue][key], issue + " is missing " + key

# matching
out = get_recommendations([{"issue": "wall_crack", "confidence": 0.9}])
assert len(out) == 1
assert out[0]["issue"] == "wall_crack"

# unknown issue and empty input are safe
assert get_recommendations([{"issue": "alien_goo", "confidence": 0.9}]) == []
assert get_recommendations([]) == []

print("recommendation_engine: all tests passed")
