import time
import random
from locust import HttpUser, task, between
from locust.clients import ResponseContextManager
import json
    

with open("data/user_payloads.json", "r") as f:
    user_payloads = json.load(f)
    
with open("data/posts_payloads.json", "r") as f:
    post_payloads = json.load(f)
    
with open("data/newsletter_payloads.json", "r") as f:
    newsletter_payloads = json.load(f)
    
def get_client_response(resp: ResponseContextManager):
    if resp.status_code == 200:
        resp.success()
    else:
        resp.failure(f"Failed with status code: {resp.status_code}")

class WebAPIBehaviour(HttpUser):
    wait_time = between(3, 6)
    user_ids = []
    newsletter_ids = []
    post_ids = []
    
    
    def on_start(self):
        # Creating a user
        payload = random.choice(user_payloads)
        with self.client.post("/users", json=payload, catch_response=True) as response:
            if response.status_code == 201:
                user_id = response.json().get("id")
                self.user_ids.append(user_id)
                response.success()
            else:
                response.failure(f"Failed to create a user: {response.text}")
                
        # Creating a newsletter
        if self.user_ids:
            user_uuid = random.choice(self.user_ids)
            newsletter_payload = random.choice(newsletter_payloads)
            
            augmented_payload = {
                **newsletter_payload,
                "user": user_uuid
            }
            
            with self.client.post("/newsletters", json=augmented_payload, catch_response=True) as response:
                if response.status_code == 201:
                    newsletter_id = response.json().get("id")
                    self.newsletter_ids.append(newsletter_id)
                    response.success()
                else:
                    response.failure(f"Failed to create a newsletter: {response.text}")
        else:
            print("No user ID available to create a newsletter")
            
        # Creating a post
        if self.newsletter_ids and self.user_ids:
            newsletter_uuid = random.choice(self.newsletter_ids)
            post_payload = random.choice(post_payloads)
                
            augmented_payload = {
                **post_payload,
                "newsletter": newsletter_uuid
            }
                
            with self.client.post("/posts", json=augmented_payload, catch_response=True) as response:
                if response.status_code == 201:
                    post_id = response.json().get("id")
                    self.post_ids.append(post_id)
                    response.success()
                else:
                    response.failure(f"Failed to create a post: {response.text}")       
        else:
            print("No newsletter IDs available")

    @task
    def get_users(self):
        if self.user_ids:
            for user_uuid in self.user_ids:
                with self.client.get(f"/users/{user_uuid}", catch_response=True) as response:
                    if response.status_code == 200:
                        response.success()
                    else:
                        response.failure(f"Failed to get a user: {response.text}")
        else:
            print("No user ID available")
            
    @task
    def get_newsletter(self):
        if self.newsletter_ids:
            for newsletter_uuid in self.newsletter_ids:
                with self.client.get(f"/newsletter/{newsletter_uuid}", catch_response=True) as response:
                    if response.status_code == 200:
                        response.success()
                    else:
                        response.failure(f"Failed to fetch a newsletter: {response.text}")
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
                
                with self.client.patch(f"/newsletter/{newsletter_uuid}", json=augmented_payload, catch_response=True) as response:
                    if response.status_code == 200:
                        response.success()
                    else:
                        response.failure(f"Failed to update a newsletter: {response.text}")
        else:
            print("No newsletter IDs available")
                
    @task
    def get_newsletters_for_user(self):
        if self.newsletter_ids and self.user_ids:
            for user_uuid in self.user_ids:
                with self.client.get(f"/users/newsletters/{user_uuid}", catch_response=True) as response:
                    if response.status_code == 200:
                        response.success()
                    else:
                        response.failure(f"Failed to fetch user's newsletters: {response.text}")
        else:
            print("No newsletter or user IDs available")
            
    @task
    def get_post(self):
        if self.post_ids:
            for post_uuid in self.post_ids:
                with self.client.get(f"/posts/{post_uuid}", catch_response=True) as response:
                    if response.status_code == 200:
                        response.success()
                    else:
                        response.failure(f"Faield to get a post: {response.text}")
        else:
            print("No post IDs available")
            
    @task
    def update_post(self):
        if self.post_ids and self.newsletter_ids:
            for post_uuid in self.post_ids:
                newsletter_uuid = random.choice(self.newsletter_ids)
                post_payload = random.choice(post_payloads)
                
                augmented_payload = {
                    **post_payload,
                    "newsletter": newsletter_uuid
                }
                
                with self.client.patch(f"/posts/{post_uuid}", json=augmented_payload, catch_response=True) as response:
                    if response.status_code == 200:
                        response.success()
                    else:
                        response.failure(f"Failed to update a post: {response.text}")
        else:
            print("No post or newsletter IDs available")
