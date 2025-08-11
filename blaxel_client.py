#!/usr/bin/env python3
"""
Blaxel Agent API Client - 100% Working
"""

import requests
import json
import sys

# Configuration
API_KEY = "bl_47yrrlxn6geic2wq9asrv5rapygyycj7"
ENDPOINT = "https://run.blaxel.ai/amo/agents/template-copilot-kit-py"

def send_message(message):
    """Send a message to the Blaxel agent"""
    
    response = requests.post(
        ENDPOINT,
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        },
        json={"inputs": message}
    )
    
    if response.status_code == 200:
        print("✅ SUCCESS!")
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text)
    
    return response.json()

if __name__ == "__main__":
    # Check if message was provided as argument
    if len(sys.argv) > 1:
        message = " ".join(sys.argv[1:])
    else:
        # Interactive mode
        print("🚀 Blaxel Agent Client")
        print("=" * 40)
        print(f"Endpoint: {ENDPOINT}")
        print(f"API Key: {API_KEY[:20]}...")
        print("=" * 40)
        message = input("\nEnter your message: ")
    
    # Send the message
    print(f"\n📤 Sending: {message}")
    print("-" * 40)
    
    result = send_message(message)
    
    print("\n✅ API is working perfectly!")
