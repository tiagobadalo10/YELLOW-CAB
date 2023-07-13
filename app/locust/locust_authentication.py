from locust import HttpUser, task, between

class QuickstartUser(HttpUser):
    wait_time = between(5, 15)

    @task
    def home(self):
        base_url = "api/authentication"

        self.client.get(base_url, verify=False, timeout=60)
        