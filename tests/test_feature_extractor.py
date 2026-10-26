from ai.feature_extractor import normalize_findings

data = [
    {"issue": "damaged_roofing", "confidence": 0.87, "evidence": ["a"]},
    {"issue": "damaged_roofing", "confidence": 0.86, "evidence": ["a", "b"]},
    {"issue": "wall_crack", "confidence": 0.90, "evidence": ["c"]},
]
out = normalize_findings(data)

assert len(out) == 2
assert out[0]["issue"] == "wall_crack"
roof = [x for x in out if x["issue"] == "damaged_roofing"][0]
assert roof["confidence"] == 0.87
assert roof["seen_in_images"] == 2
assert roof["evidence"] == ["a", "b"]
print("normalize_findings: all tests passed")
