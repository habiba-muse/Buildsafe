from ai.vision import analyze_image
from ai.feature_extractor import normalize_findings
from ai.risk_engine import compute_risk
from ai.recommendation_engine import get_recommendations
from ai.explainer import explain_result


def analyze_images(image_paths):
    all_findings = []
    for path in image_paths:
        all_findings.extend(analyze_image(path))
    return normalize_findings(all_findings)


def build_result(findings):
    risk = compute_risk(findings)
    recommendations = get_recommendations(findings)
    explanation = explain_result(findings, risk, recommendations)
    return {
        "risk": risk,
        "recommendations": recommendations,
        "explanation": explanation,
    }
