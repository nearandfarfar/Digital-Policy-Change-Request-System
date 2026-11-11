
import os
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = (
    "https://digital-policy-change-request-system-v1-f57-e259db36.crewai.com"
)

token = os.getenv("CREWAI_BEARER_TOKEN")

if not token:
    raise RuntimeError("CREWAI_BEARER_TOKEN is missing")

headers = {
    "Authorization": f"Bearer {token}"
}

response = requests.get(
    f"{BASE_URL}/inputs",
    headers=headers,
    timeout=30
)

print("HTTP Status:", response.status_code)
print("Response:", response.text)
