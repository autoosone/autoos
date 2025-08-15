#!/usr/bin/env python3
"""
🚀 PRODUCTION-READY BLAXEL PROXY SERVER
Handles CORS, authentication, and provides browser-friendly access to Blaxel agents
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import httpx
import os
import json
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
BLAXEL_API_KEY = os.getenv("BLAXEL_API_KEY", "YOUR_API_KEY_HERE")  # Set in environment variables
BLAXEL_BASE_URL = "https://run.blaxel.ai"
WORKSPACE = "amo"
AGENT = "template-copilot-kit-py"

app = FastAPI(
    title="Blaxel Proxy Server",
    description="Production-ready proxy for Blaxel agents with CORS support",
    version="1.0.0"
)

# Add CORS middleware for browser access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Root endpoint with service info"""
    return {
        "service": "Blaxel Proxy Server",
        "status": "running",
        "version": "1.0.0",
        "endpoints": {
            "agent": f"/proxy/agents/{WORKSPACE}/{AGENT}",
            "health": "/health",
            "test": "/test"
        },
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health")
async def health():
    """Health check endpoint"""
    try:
        # Test connection to Blaxel
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{BLAXEL_BASE_URL}/{WORKSPACE}/agents/{AGENT}",
                headers={
                    "Authorization": f"Bearer {BLAXEL_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={"inputs": "healthcheck"},
                timeout=10.0
            )
            
        return {
            "status": "healthy",
            "blaxel_connection": "ok" if response.status_code == 200 else "error",
            "blaxel_status": response.status_code,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

@app.post("/proxy/agents/{workspace}/{agent}")
async def proxy_to_blaxel(workspace: str, agent: str, request: Request):
    """
    Proxy requests to Blaxel agents with authentication
    """
    try:
        # Get request body
        request_data = await request.json()
        
        # Validate request format
        if "inputs" not in request_data:
            raise HTTPException(
                status_code=400, 
                detail="Missing 'inputs' field in request body. Use {'inputs': 'your message'}"
            )
        
        # Get thread ID from headers if present
        thread_id = request.headers.get("X-Blaxel-Thread-Id")
        
        # Prepare headers for Blaxel
        blaxel_headers = {
            "Authorization": f"Bearer {BLAXEL_API_KEY}",
            "Content-Type": "application/json"
        }
        
        if thread_id:
            blaxel_headers["X-Blaxel-Thread-Id"] = thread_id
        
        # Make request to Blaxel
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{BLAXEL_BASE_URL}/{workspace}/agents/{agent}",
                headers=blaxel_headers,
                json=request_data,
                timeout=30.0
            )
            
        # Return response
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Blaxel API error: {response.text}"
            )
            
    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="Blaxel API timeout")
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON in request body")
    except Exception as e:
        logger.error(f"Proxy error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Proxy server error: {str(e)}")

@app.get("/test")
async def test_page():
    """Serve a test page for browser testing"""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Blaxel Agent Test</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
            .container { background: #f5f5f5; padding: 20px; border-radius: 8px; margin: 10px 0; }
            .success { color: green; }
            .error { color: red; }
            button { background: #007cba; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; }
            button:hover { background: #005a87; }
            #response { background: white; padding: 15px; border-radius: 4px; margin-top: 10px; min-height: 50px; }
        </style>
    </head>
    <body>
        <h1>🚀 Blaxel Agent Test Interface</h1>
        
        <div class="container">
            <h3>Test Agent Communication</h3>
            <input type="text" id="messageInput" placeholder="Enter your message..." style="width: 300px; padding: 8px;">
            <button onclick="testAgent()">Send Message</button>
            <div id="response"></div>
        </div>
        
        <div class="container">
            <h3>Test with Thread ID (Stateful)</h3>
            <input type="text" id="threadInput" placeholder="Thread ID (optional)" style="width: 200px; padding: 8px;">
            <input type="text" id="threadMessageInput" placeholder="Enter your message..." style="width: 300px; padding: 8px;">
            <button onclick="testWithThread()">Send with Thread</button>
            <div id="threadResponse"></div>
        </div>
        
        <script>
            async function testAgent() {
                const message = document.getElementById('messageInput').value;
                const responseDiv = document.getElementById('response');
                
                if (!message) {
                    responseDiv.innerHTML = '<span class="error">Please enter a message</span>';
                    return;
                }
                
                responseDiv.innerHTML = 'Sending...';
                
                try {
                    const response = await fetch('/proxy/agents/amo/template-copilot-kit-py', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ inputs: message })
                    });
                    
                    const data = await response.json();
                    
                    if (response.ok) {
                        responseDiv.innerHTML = `<span class="success">✅ Success:</span><br><pre>${JSON.stringify(data, null, 2)}</pre>`;
                    } else {
                        responseDiv.innerHTML = `<span class="error">❌ Error:</span><br><pre>${JSON.stringify(data, null, 2)}</pre>`;
                    }
                } catch (error) {
                    responseDiv.innerHTML = `<span class="error">❌ Network Error:</span><br>${error.message}`;
                }
            }
            
            async function testWithThread() {
                const threadId = document.getElementById('threadInput').value || `test-${Date.now()}`;
                const message = document.getElementById('threadMessageInput').value;
                const responseDiv = document.getElementById('threadResponse');
                
                if (!message) {
                    responseDiv.innerHTML = '<span class="error">Please enter a message</span>';
                    return;
                }
                
                responseDiv.innerHTML = 'Sending...';
                
                try {
                    const headers = {
                        'Content-Type': 'application/json',
                        'X-Blaxel-Thread-Id': threadId
                    };
                    
                    const response = await fetch('/proxy/agents/amo/template-copilot-kit-py', {
                        method: 'POST',
                        headers: headers,
                        body: JSON.stringify({ inputs: message })
                    });
                    
                    const data = await response.json();
                    
                    if (response.ok) {
                        responseDiv.innerHTML = `<span class="success">✅ Success (Thread: ${threadId}):</span><br><pre>${JSON.stringify(data, null, 2)}</pre>`;
                    } else {
                        responseDiv.innerHTML = `<span class="error">❌ Error:</span><br><pre>${JSON.stringify(data, null, 2)}</pre>`;
                    }
                } catch (error) {
                    responseDiv.innerHTML = `<span class="error">❌ Network Error:</span><br>${error.message}`;
                }
            }
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

if __name__ == "__main__":
    import uvicorn
    
    port = int(os.getenv("PORT", 8888))
    host = os.getenv("HOST", "0.0.0.0")
    
    print(f"🚀 Starting Blaxel Proxy Server on {host}:{port}")
    print(f"📡 Proxying to: {BLAXEL_BASE_URL}/{WORKSPACE}/agents/{AGENT}")
    print(f"🌐 Test interface: http://localhost:{port}/test")
    
    uvicorn.run(app, host=host, port=port)
