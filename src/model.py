from typing import Dict


def predict_risk(text: str) -> Dict:
    """
    Simple rule-based model placeholder.
    Later replaced by trained ML model.
    """

    text = text.lower()

    high_risk_words = [
        "attack",
        "explosion",
        "armed",
        "conflict",
        "weapon"
    ]

    medium_risk_words = [
        "protest",
        "disruption",
        "incident"
    ]

    for word in high_risk_words:
        if word in text:
            return {
                "risk_level": "HIGH",
                "confidence": 0.90
            }

    for word in medium_risk_words:
        if word in text:
            return {
                "risk_level": "MEDIUM",
                "confidence": 0.80
            }

    return {
        "risk_level": "LOW",
        "confidence": 0.95
    }