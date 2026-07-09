from src.app import app


def test_health():

    client = app.test_client()

    response = client.get("/health")

    assert response.status_code == 200


def test_prediction():

    client = app.test_client()

    response = client.post(
        "/predict",
        json={
            "text": "armed conflict reported"
        }
    )

    data = response.get_json()

    assert data["risk_level"] == "HIGH"