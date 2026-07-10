from src.model import predict_risk


def test_high_risk():
    result = predict_risk("armed conflict reported")

    assert result["risk_level"] == "HIGH"


def test_medium_risk():
    result = predict_risk("major protest downtown")

    assert result["risk_level"] == "MEDIUM"


def test_low_risk():
    result = predict_risk("beautiful sunny weather today")

    assert result["risk_level"] == "LOW"