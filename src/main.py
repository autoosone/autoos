
import os
from contextlib import asynccontextmanager
from logging import getLogger

from copilotkit import CopilotKitRemoteEndpoint, LangGraphAgent
from copilotkit.crewai import CrewAIAgent
from copilotkit.integrations.fastapi import add_fastapi_endpoint
from fastapi import FastAPI
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

from .agent import agent
from .vehicle import agent as vehicle_agent
from .dealer import agent as dealer_agent
from .server.error import init_error_handlers
from .server.middleware import init_middleware

logger = getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Use system PORT variable
    port = os.environ.get("PORT", "8080")
    logger.info(f"Server running on port {port}")
    try:
        # Initialize the SDK
        sdk = await get_sdk()

        # Store in app state
        app.state.sdk = sdk

        # Add CopilotKit endpoint with error handling
        try:
            add_fastapi_endpoint(app, sdk, "/copilotkit")
            logger.info("CopilotKit endpoint added successfully")
        except Exception as copilot_error:
            logger.error(f"Failed to add CopilotKit endpoint: {str(copilot_error)}")
            # Continue without CopilotKit endpoint - base agent still works

        yield
        logger.info("Server shutting down")
    except Exception as e:
        logger.error(f"Error during startup: {str(e)}", exc_info=True)
        raise


# Create the SDK after the graph is initialized
async def get_sdk():
    supervisor = await agent()
    vehicle = await vehicle_agent()
    dealer = await dealer_agent()
    sdk = CopilotKitRemoteEndpoint(
        agents=[
            LangGraphAgent(
                name="automotive-supervisor", 
                description="Find your perfect vehicle", 
                graph=supervisor
            ),
            LangGraphAgent(
                name="vehicle-agent", 
                description="Search and analyze vehicles", 
                graph=vehicle
            ),
            LangGraphAgent(
                name="dealer-agent", 
                description="Find dealers and schedule test drives", 
                graph=dealer
            ),
        ],
    )
    return sdk


app = FastAPI(lifespan=lifespan)
init_error_handlers(app)
init_middleware(app)

# Add a simple root endpoint for testing
@app.get("/")
async def root():
    return {"message": "CopilotKit Agent is running", "status": "healthy"}

# Add a POST endpoint that matches the Blaxel agent interface  
@app.post("/")
async def agent_endpoint(request: dict):
    # CRITICAL FIX: Check for "inputs" not "input"
    if "inputs" in request:
        return {"message": "Agent received input", "input": request, "available_endpoints": ["/copilotkit"]}
    else:
        return {"error": "Missing 'inputs' field in request body"}, 400

# Add health endpoints for monitoring
@app.get("/healthz")
async def health():
    return {"status": "ok", "service": "copilotkit-agent", "timestamp": os.environ.get("DEPLOYMENT_ID", "local")}

# Add manual CopilotKit endpoint as fallback
@app.post("/copilotkit")
async def copilotkit_fallback():
    """Fallback CopilotKit endpoint if automatic mounting fails"""
    try:
        sdk = app.state.sdk
        return {
            "agents": [
                {
                    "name": "automotive-supervisor",
                    "description": "Find your perfect vehicle"
                },
                {
                    "name": "vehicle-agent", 
                    "description": "Search and analyze vehicles"
                },
                {
                    "name": "dealer-agent",
                    "description": "Find dealers and schedule test drives"
                }
            ],
            "status": "available",
            "sdkVersion": "1.0.0"
        }
    except Exception as e:
        logger.error(f"CopilotKit fallback error: {str(e)}")
        return {"error": "CopilotKit endpoint unavailable", "details": str(e)}

FastAPIInstrumentor.instrument_app(app, exclude_spans=["receive", "send"])


# Add main entry point for proper port binding
if __name__ == "__main__":
    import uvicorn
    
    # Use Blaxel-injected environment variables
    host = os.getenv('BL_SERVER_HOST', '0.0.0.0')
    port = int(os.getenv('BL_SERVER_PORT', 80))
    
    uvicorn.run(app, host=host, port=port)
