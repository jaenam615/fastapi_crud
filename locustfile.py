import json
import random

from locust import HttpUser, between, task

# -----------------------------
# Load pre-generated JWT token
# -----------------------------
with open("token.json", "r") as f:
    TEST_TOKEN = json.load(f)["access_token"]

HEADERS = {"Authorization": f"Bearer {TEST_TOKEN}"}

DEFAULT_PAGE = 1
DEFAULT_SIZE = 20


class BoardUser(HttpUser):
    wait_time = between(1, 3)
    post_ids: list[int] = []

    # ============================================================
    # on_start: Load first page of posts (pagination applied)
    # ============================================================
    def on_start(self):
        response = self.client.get(
            f"/posts?page={DEFAULT_PAGE}&size={DEFAULT_SIZE}",
            headers=HEADERS,
        )

        if response.status_code == 200:
            posts = response.json()
            self.post_ids = [p["id"] for p in posts]

        # fallback: ensure non-empty list
        if not self.post_ids:
            self.post_ids = [1]

    # ============================================================
    # Read posts (pagination)
    # ============================================================
    @task(20)
    def list_posts(self):
        self.client.get(
            f"/posts?page={DEFAULT_PAGE}&size={DEFAULT_SIZE}",
            headers=HEADERS,
        )

    # ============================================================
    # Create a post
    # ============================================================
    @task(1)
    def create_post(self):
        post_data = {
            "title": f"Post title {random.randint(1, 10000)}",
            "content": "This is a sample post content for load testing.",
        }

        response = self.client.post("/posts/", json=post_data, headers=HEADERS)

        # Successfully created → add to local post_ids
        if response.status_code == 201:
            post_id = response.json()["id"]
            # 새 글은 page=1 최상단이므로 맨 앞에 추가
            self.post_ids.insert(0, post_id)

    # ============================================================
    # Create a comment + list comments with pagination
    # ============================================================
    @task(2)
    def create_comment(self):
        if not self.post_ids:
            return

        post_id = random.choice(self.post_ids)

        comment_data = {
            "post_id": post_id,
            "content": f"Comment {random.randint(1,10000)}",
        }

        # ----- Create a comment -----
        res = self.client.post("/comments/", json=comment_data, headers=HEADERS)

        # Deleted post → remove orphan ID
        if res.status_code == 404:
            if post_id in self.post_ids:
                self.post_ids.remove(post_id)
            return

        # ----- Read comments with pagination -----
        list_res = self.client.get(
            f"/comments/post/{post_id}?page={DEFAULT_PAGE}&size={DEFAULT_SIZE}",
            headers=HEADERS,
        )

        # Again: deleted post → clean orphan ID
        if list_res.status_code == 404:
            if post_id in self.post_ids:
                self.post_ids.remove(post_id)

        # Hard limit post_ids to avoid infinite growth
        if len(self.post_ids) > 200:
            self.post_ids = self.post_ids[:200]
