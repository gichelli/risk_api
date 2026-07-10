import requests


BASE_URL = "http://localhost:8080"


def test_health_endpoint():

    response = requests.get(
        f"{BASE_URL}/health"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "healthy"



def test_prediction_endpoint():

    response = requests.post(
        f"{BASE_URL}/predict",
        json={
            "text": "armed conflict reported"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["risk_level"] == "HIGH"