import os
import requests


BASE_URL = os.environ["BASE_URL"]


def test_prediction_api_returns_required_fields():

    response = requests.post(
        f"{BASE_URL}/predict",
        json={
            "text": "armed conflict reported"
        },
        timeout=10
    )

    assert response.status_code == 200

    data = response.json()

    assert "risk_level" in data



def test_prediction_api_accepts_valid_text():

    response = requests.post(
        f"{BASE_URL}/predict",
        json={
            "text": "market conditions are stable"
        },
        timeout=10
    )

    assert response.status_code == 200

    data = response.json()

    assert data["risk_level"] in [
        "LOW",
        "MEDIUM",
        "HIGH"
    ]



def test_health_endpoint_available():

    response = requests.get(
        f"{BASE_URL}/health",
        timeout=10
    )

    assert response.status_code == 200