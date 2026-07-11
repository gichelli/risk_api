import os
import requests


DEV_URL = os.environ["DEV_URL"]


def test_high_risk_prediction():

    response = requests.post(
        f"{DEV_URL}/predict",
        json={
            "text": "armed conflict reported"
        },
        timeout=10
    )

    assert response.status_code == 200

    data = response.json()

    assert data["risk_level"] == "HIGH"



def test_low_risk_prediction():

    response = requests.post(
        f"{DEV_URL}/predict",
        json={
            "text": "the weather is nice today"
        },
        timeout=10
    )

    assert response.status_code == 200

    data = response.json()

    assert data["risk_level"] == "LOW"