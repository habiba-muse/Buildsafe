import os
import tempfile
from PIL import Image
from ai.analyzer import analyze_images, build_result

tmp = tempfile.mkdtemp()
paths = []
for i in range(2):
    p = os.path.join(tmp, "img" + str(i) + ".jpg")
    Image.new("RGB", (50, 50), "gray").save(p)
    paths.append(p)

# stub is random, so run many times
for _ in range(50):
    findings = analyze_images(paths)
    issues = [f["issue"] for f in findings]
    assert len(issues) == len(set(issues)), "duplicate issues"

    result = build_result(findings)
    risk = result["risk"]
    assert 0 <= risk["overall_score"] <= 100
    assert risk["risk_level"] in ("low", "moderate", "high")
    for score in risk["categories"].values():
        assert 0 <= score <= 100
    assert len(result["recommendations"]) == len(findings)
    assert "not a professional engineering inspection" in result["explanation"]["summary"]

# empty input is safe
result = build_result([])
assert result["risk"]["overall_score"] == 0

print("pipeline: all tests passed")
