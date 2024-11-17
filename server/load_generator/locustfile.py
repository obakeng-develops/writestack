import time
import random
from locust import HttpUser, task, between
from locust.clients import ResponseContextManager
import json

with open("user_payloads.json", "r") as f:
    user_payloads = json.load(f)
    
def get_client_response(resp: ResponseContextManager):
    if resp.status_code == 200:
        resp.success()
    else:
        resp.failure(f"Failed with status code: {resp.status_code}")

class User(HttpUser):
    wait_time = between(1, 3)
    payload = random.choice(user_payloads)

    @task
    def create_user(self):
        with self.client.post("/users", json=self.payload, catch_response=True) as response:
            get_client_response(response)
            
    @task
    def get_user(self):
        with self.client.get("/users/{user_uuid}", json=self.payload, catch_response=True) as response:
            get_client_response(response)
            
    @task
    def get_newsletters_for_users(self):
        with self.client.get("/users/newsletters/{user_uuid}", payload=self.payload, catch_response=True) as response:
            get_client_response(response)
