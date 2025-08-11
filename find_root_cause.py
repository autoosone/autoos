#!/usr/bin/env python3
"""
ULTIMATE BLAXEL API TEST - FIND THE EXACT ISSUE
"""

import requests
import json

print("=" * 60)
print("FINDING THE EXACT ROOT CAUSE")
print("=" * 60)

# Test configurations
API_KEYS = [
    "bl_47yrrlxn6geic2wq9asrv5rapygyycj7",  # Current key
    "bl_ogpdihxp6c503zffr81jyftlwc35ibdi",  # Old key from .env
]

HEADERS_VARIATIONS = [
    {"Authorization": "Bearer {key}"},
    {"X-Blaxel-Authorization": "Bearer {key}"},
    {"x-blaxel-authorization": "Bearer {key}"},
    {"Authorization": "{key}"},
    {"X-Blaxel-Authorization": "{key}"},
]

ENDPOINTS = [
    "https://run.blaxel.ai/amo/agents/template-copilot-kit-py",
    "https://run.blaxel.ai/amo/copilotkit",
]

# Test each combination
for endpoint in ENDPOINTS:
    print(f"\n🎯 Testing endpoint: {endpoint}")
    print("-" * 50)
    
    for key in API_KEYS:
        print(f"\n  API Key: {key[:20]}...")
        
        for header_template in HEADERS_VARIATIONS:
            headers = {"Content-Type": "application/json"}
            
            # Build the header
            for h_key, h_value in header_template.items():
                headers[h_key] = h_value.format(key=key)
            
            header_name = list(header_template.keys())[0]
            
            try:
                # Test POST
                response = requests.post(
                    endpoint,
                    headers=headers,
                    json={"inputs": "test"},
                    timeout=5
                )
                
                if response.status_code == 200:
                    print(f"    ✅ SUCCESS with {header_name}: {response.status_code}")
                    print(f"       Working combination found!")
                    print(f"       Endpoint: {endpoint}")
                    print(f"       API Key: {key}")
                    print(f"       Header: {header_name}: {headers[header_name]}")
                    print(f"       Response: {response.text[:100]}...")
                    
                    # Save working configuration
                    with open("WORKING_CONFIG.txt", "w") as f:
                        f.write(f"WORKING CONFIGURATION FOUND!\n")
                        f.write(f"========================\n")
                        f.write(f"Endpoint: {endpoint}\n")
                        f.write(f"API Key: {key}\n")
                        f.write(f"Header: {header_name}: {headers[header_name]}\n")
                        f.write(f"\nExample cURL:\n")
                        f.write(f'curl -X POST "{endpoint}" \\\n')
                        f.write(f'  -H "Content-Type: application/json" \\\n')
                        f.write(f'  -H "{header_name}: {headers[header_name]}" \\\n')
                        f.write(f'  -d \'{{\"inputs\": \"test\"}}\'\n')
                    
                    print("\n🎉 SOLUTION SAVED TO WORKING_CONFIG.txt")
                    exit(0)
                else:
                    print(f"    ❌ {header_name}: {response.status_code} - {response.text[:50]}...")
                    
            except Exception as e:
                print(f"    ❌ {header_name}: Exception - {str(e)[:50]}")

print("\n" + "=" * 60)
print("❌ NO WORKING COMBINATION FOUND")
print("=" * 60)
