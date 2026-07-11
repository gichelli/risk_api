import os
import requests


BASE_URL = os.environ["BASE_URL"]


def test_high_risk_classification_regression():

    response = requests.post(
        f"{BASE_URL}/predict",
        json={
            "text": "armed conflict reported"
        },
        timeout=10
    )

    assert response.status_code == 200

    result = response.json()

    # Previous expected behavior
    assert result["risk_level"] == "HIGH"



def test_low_risk_classification_regression():

    response = requests.post(
        f"{BASE_URL}/predict",
        json={
            "text": "weather is nice today"
        },
        timeout=10
    )

    assert response.status_code == 200

    result = response.json()

    # Previous expected behavior
    assert result["risk_level"] == "LOW"



def test_invalid_request_handling():

    response = requests.post(
        f"{BASE_URL}/predict",
        json={},
        timeout=10
    )

    assert response.status_code in [
        400,
        500
    ]