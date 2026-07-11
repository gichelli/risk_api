from locust import HttpUser, task, between


class RiskAPIUser(HttpUser):

    wait_time = between(1, 3)


    @task
    def predict_request(self):

        self.client.post(
            "/predict",
            json={
                "text": "armed conflict reported"
            }
        )


    @task
    def health_check(self):

        self.client.get(
            "/health"
        )