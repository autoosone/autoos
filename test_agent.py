import requests

# Using your personal API key from the screenshot
API_KEY = "bl_0nquezyion6lgl8e6g5vdf8znodyrzzx"

print("Testing Blaxel Agent with Personal API Key...")
print("-" * 50)

response = requests.post(
    "https://run.blaxel.ai/amo/agents/template-copilot-kit-py",
    headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    },
    json={
        "inputs": "Hello, find hotels in Paris"
    }
)

print(f"Status Code: {response.status_code}")
print(f"Response: {response.text[:500] if response.text else 'Empty response'}")

# Also test the CopilotKit endpoint
print("\n" + "=" * 50)
print("Testing CopilotKit Endpoint...")
print("-" * 50)

response2 = requests.post(
    "https://run.blaxel.ai/amo/agents/template-copilot-kit-py/copilotkit",
    headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    },
    json={
        "message": "Hello",
        "actions": []
    }
)

print(f"Status Code: {response2.status_code}")
print(f"Response: {response2.text[:500] if response2.text else 'Empty response'}")
