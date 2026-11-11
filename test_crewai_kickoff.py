
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

payload = {
    "inputs": {
        "transcript": (
            "The insurance company needs a digital policy "
            "change request system. Customers must submit "
            "requests online. Staff must review and approve "
            "requests. The system must maintain an audit trail."
        )
    }
}

response = requests.post(
    f"{BASE_URL}/kickoff",
    headers=headers,
    json=payload,
    timeout=30
)

print("HTTP Status:", response.status_code)
print("Response:", response.text)

response.raise_for_status()
