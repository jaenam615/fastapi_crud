import random

from locust import HttpUser, between, task

USERS = [
    {"username": "user1", "password": "pass1"},
    {"username": "user2", "password": "pass2"},
    {"username": "user3", "password": "pass3"},
]


class BoardUser(HttpUser):
    token: str = None
    headers: dict = {}
    post_ids: list[int] = []
    wait_time = between(1, 3)

    def on_start(self):
        creds = random.choice(USERS)
        response = self.client.post("/auth/login", data=creds)
        if response.status_code == 200:
            self.token = response.json().get("access_token")
            self.headers = {"Authorization": f"Bearer {self.token}"}
        else:
            print("Login failed", response.text)
            self.headers = {}

        posts_response = self.client.get("/posts/", headers=self.headers)
        if posts_response.status_code == 200:
            posts = posts_response.json()
            self.post_ids = [post["id"] for post in posts]

    @task(5)
    def list_posts(self):
        self.client.get("/posts/", headers=self.headers)

    @task(1)
    def create_post(self):
        if not self.token:
            return

        headers = {"Authorization": f"Bearer {self.token}"}
        post_data = {
            "title": f"Post title {random.randint(1, 10000)}",
            "content": "This is a sample post content for load testing.",
        }

        response = self.client.post("/posts/", json=post_data, headers=self.headers)
        if response.status_code == 201:
            post = response.json()
            self.post_ids.append(post["id"])

    @task(2)
    def create_comment(self):
        if not self.post_ids:
            return

        post_id = random.choice(self.post_ids)
        comment_data = {
            "post_id": post_id,
            "content": f"Comment content {random.randint(1,10000)}",
        }
        self.client.post("/comments/", json=comment_data, headers=self.headers)
