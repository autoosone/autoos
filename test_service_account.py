import requests

response = requests.post(
    "https://run.blaxel.ai/amo/agents/template-copilot-kit-py",
    headers={
        "Content-Type": "application/json",
        "Authorization": "Bearer bl_47yrrlxn6geic2wq9asrv5rapygyycj7",
        "X-Blaxel-Thread-Id": "your-thread-id" // Optional
    },
    json={
        "inputs": "Hello, world!"
    }
)

data = response.text
print(data)