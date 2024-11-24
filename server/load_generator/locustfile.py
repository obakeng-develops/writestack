import time
import random
from locust import HttpUser, task, between
from locust.clients import ResponseContextManager
import json
    

with open("user_payloads.json", "r") as f:
    user_payloads = json.load(f)
    
with open("posts_payloads.json", "r") as f:
    post_payloads = json.load(f)
    
with open("newsletter_payloads.json", "r") as f:
    newsletter_payloads = json.load(f)
    
def get_client_response(resp: ResponseContextManager):
    if resp.status_code == 200:
        resp.success()
    else:
        resp.failure(f"Failed with status code: {resp.status_code}")

class WebAPIBehaviour(HttpUser):
    wait_time = between(1, 3)
    def on_start(self):
        self.user_ids = []
        self.newsletter_ids = []
        self.post_ids = []

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
            
    @task
    def create_newsletter(self):
        if self.user_ids:
            user_uuid = random.choice(self.user_uids)
            newsletter_payload = random.choice(newsletter_payloads)
            
            augmented_payload = {
                **newsletter_payload,
                "user": user_uuid
            }
            
            response = self.client.post("/newsletters", json=augmented_payload)
            
            if response.status_code == 200:
                newsletter_id = response.json().get("id")
                self.newsletter_ids.append(newsletter_id)
                response.success()
            else:
                response.failure(f"Failed to create a newsletter: {response.text}")
        else:
            print("No user ID available to create a newsletter")
            
    @task
    def get_newsletter(self):
        if self.newsletter_ids:
            for newsletter_uuid in self.newsletter_ids:
                response = self.client.get(f"/newsletter/{newsletter_uuid}")
                
                if response.status_code == 200:
                    response.success()
                else:
                    response.failure("Failed to fetch a newsletter")
        else:
            print("No newsletter IDs available")

    @task
    def update_newsletter(self):
        if self.newsletter_ids:
            for newsletter_uuid in self.newsletter_ids:
                user_uuid = random.choice(self.user_ids)
                newsletter_payload = random.choice(newsletter_payloads)
                
                augmented_payload = {
                    **newsletter_payload,
                    "user": user_uuid
                }
                
                response = self.client.patch(f"/newsletter/{newsletter_uuid}", json=augmented_payload)
                
                if response.status_code == 200:
                    response.success()
                else:
                    response.failure()
        else:
            print("No newsletter IDs available")
                
    @task
    def get_newsletters_for_user(self):
        if self.newsletter_ids and self.user_ids:
            for user_uuid in self.user_ids:
                response = self.client.get(f"/users/newsletters/{user_uuid}")
                
                if response.status_code == 200:
                    response.success()
                else:
                    response.failure()
        else:
            print("No newsletter or user IDs available")
            
    @task
    def create_post(self):
        if self.newsletter_ids:
            for newsletter_uuid in self.newsletter_ids:
                post_payload = random.choice(self.post_payloads)
                
                augmented_payload = {
                    **post_payload,
                    "newsletter": newsletter_uuid
                }
                
                response = self.client.post("/posts", json=augmented_payload)
                
                if response.status_code == 200:
                    post_id = response.json().get("id")
                    self.post_ids.append(post_id)
                    response.success()
                else:
                    response.failure()       
        else:
            print("No newsletter IDs available")
            
    @task
    def get_post(self):
        if self.post_ids:
            for post_uuid in self.post_ids:
                response = self.client.get(f"/posts/{post_uuid}")
                
                if response.status_code == 200:
                    response.success()
                else:
                    response.failure()
        else:
            print("No post IDs available")
            
    @task
    def update_post(self):
        if self.post_ids and self.newsletter_ids:
            for post_uuid in self.post_ids:
                newsletter_uuid = random.choice(self.newsletter_ids)
                post_payload = random.choice(self.post_payloads)
                
                augmented_payload = {
                    **post_payload,
                    "newsletter": newsletter_uuid
                }
                
                response = self.client.patch(f"/posts/{post_uuid}", json=augmented_payload)
                
                if response.status_code == 200:
                    response.success()
                else:
                    response.failure()
        else:
            print("No post or newsletter IDs available")
