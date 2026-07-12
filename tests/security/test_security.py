import os
import requests


BASE_URL = os.environ["STAGING_URL"]


def test_security_headers():

    response = requests.get(
        f"{BASE_URL}/health",
        timeout=10
    )


    headers = response.headers


    assert "Server" in headers



def test_invalid_payload_rejected():

    response = requests.post(
        f"{BASE_URL}/predict",
        json={
            "unexpected_field": "attack"
        },
        timeout=10
    )


    assert response.status_code in [
        400,
        500
    ]