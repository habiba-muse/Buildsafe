import random

POSSIBLE_ISSUES = [
    {
        "issue": "wall_crack",
        "evidence": ["visible crack line on wall surface"],
    },
    {
        "issue": "water_stain",
        "evidence": ["discoloration consistent with water exposure"],
    },
    {
        "issue": "damaged_roofing",
        "evidence": ["missing or displaced roofing material"],
    },
    {
        "issue": "exposed_reinforcement",
        "evidence": ["visible metal reinforcement bar"],
    },
    {
        "issue": "standing_water",
        "evidence": ["pooled water near structure base"],
    },
]

def analyze_image(filepath):
    """
    STUB vision function.
    Returns fake but realistically-shaped findings so the rest of the
    pipeline (risk engine, recommendations) can be built and tested
    before a real Vision API is connected.

    Real version will replace the body of this function only —
    the return shape stays the same for the rest of the app.
    """
    num_findings = random.randint(1, 3)
    chosen = random.sample(POSSIBLE_ISSUES, num_findings)

    findings = []
    for item in chosen:
        findings.append({
            "issue": item["issue"],
            "confidence": round(random.uniform(0.6, 0.95), 2),
            "evidence": item["evidence"],
        })

    return findings
