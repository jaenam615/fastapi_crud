import json
import sys

import requests

API_URL = "http://localhost"
USERNAME = "loadtest"
PASSWORD = "loadtest"


def generate_jwt():
    response = requests.post(
        f"{API_URL}/auth/login",
        data={"username": USERNAME, "password": PASSWORD},
    )

    if response.status_code != 200:
        print("❌ Failed to generate JWT:", response.status_code, response.text)
        sys.exit(1)

    token = response.json().get("access_token")
    if not token:
        print("❌ No access_token returned")
        sys.exit(1)

    with open("token.json", "w") as f:
        json.dump({"access_token": token}, f)

    print("✔ JWT generated and saved to token.json")


if __name__ == "__main__":
    generate_jwt()
