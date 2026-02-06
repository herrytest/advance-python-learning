from locust import HttpUser, task, between

class MyUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def open_landing_page(self):
        self.client.get("https://www.linkedin.com/pulse/ai-tools-developers-key-benefits-drawbacks-hiren-kukadiya-0hqkf")
