import time
import random
from locust import HttpUser, task, between
from datetime import datetime
import json

with open("user_payloads.json", "r") as f:
    user_payloads = json.load(f)

class User(HttpUser):
    wait_time = between(1, 3)

    @task
    def create_user(self):
        payload = random.choice(user_payloads)
        with self.client.post("/users", json=payload, catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Failed with status code: {response.status_code}")
