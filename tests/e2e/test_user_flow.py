import os
import requests


BASE_URL = os.environ["STAGING_URL"]


def test_complete_prediction_workflow():

    # Step 1: Check application availability

    health = requests.get(
        f"{BASE_URL}/health",
        timeout=10
    )

    assert health.status_code == 200


    # Step 2: Submit prediction request

    response = requests.post(
        f"{BASE_URL}/predict",
        json={
            "text": "armed conflict reported"
        },
        timeout=10
    )


    assert response.status_code == 200


    # Step 3: Validate business response

    result = response.json()

    assert result["risk_level"] == "HIGH"