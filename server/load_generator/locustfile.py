import time
import random
from locust import HttpUser, task, between
from locust.clients import ResponseContextManager
import json
    

with open("user_payloads.json", "r") as f:
    user_payloads = json.load(f)
    
with open("posts_payloads.json", "r") as f:
    post_payloads = json.load(f)
    
def get_client_response(resp: ResponseContextManager):
    if resp.status_code == 200:
        resp.success()
    else:
        resp.failure(f"Failed with status code: {resp.status_code}")

class User(HttpUser):
    wait_time = between(1, 3)
    def on_start(self):
        self.user_ids = []

    @task(6)
    def create_user(self):
        payload = random.choice(user_payloads)
        response = self.client.post("/users", json=payload)
            
        if response.status_code == 200:
            user_id = response.json().get("id")
            self.user_ids.append(user_id)
            response.success()
        else:
            response.failure()

    @task
    def get_users(self):
        if self.user_ids:
            for user_uuid in self.user_ids:
                response = self.client.get(f"/users/{user_uuid}")
                
                if response.status_code == 200:
                    response.success()
                else:
                    response.failure()
        else:
            print("No user ID available")
