
import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = (
    "https://digital-policy-change-request-system-v1-f57-e259db36.crewai.com"
)

token = os.getenv("CREWAI_BEARER_TOKEN")

if not token:
    raise RuntimeError("CREWAI_BEARER_TOKEN is missing")

kickoff_id = "9e7c3b49-69e8-4fab-8555-71f4db743716"

headers = {
    "Authorization": f"Bearer {token}"
}

response = requests.get(
    f"{BASE_URL}/status/{kickoff_id}",
    headers=headers,
    timeout=30
)

print("HTTP Status:", response.status_code)

response.raise_for_status()

data = response.json()

print(json.dumps(data, indent=2, ensure_ascii=False))

print('==========================================')
print('==========================================')
print("\nTop-level JSON fields:")
print(list(data.keys()))

print("\nField names and data types:")
for key, value in data.items():
    print(f"{key}: {type(value).__name__}")

print('-------------------------------------------')
print('-------------------------------------------')

print("\nExecution state:")
print(data.get("state"))

print("\nResult dictionary keys:")
result = data.get("result")
print(list(result.keys()) if isinstance(result, dict) else result)

print("\nResult JSON dictionary keys:")
result_json = data.get("result_json")
print(
    list(result_json.keys())
    if isinstance(result_json, dict)
    else result_json
)

print("\nProgress dictionary keys:")
progress = data.get("progress")
print(list(progress.keys()) if isinstance(progress, dict) else progress)

print('++++++++++++++++++++++++++++++++++++++')
print('++++++++++++++++++++++++++++++++++++++')
raw = data.get("result", {}).get("raw")

print("Raw result type:", type(raw).__name__)
print("Raw result preview:")
print(str(raw)[:500])