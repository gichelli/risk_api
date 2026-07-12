import os
import requests


BASE_URL = os.environ["DEV_URL"]


def test_health_endpoint():

    response = requests.get(
        f"{BASE_URL}/health",
        timeout=10
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "healthy"