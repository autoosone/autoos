"""
Flight Search Agent Module

This module implements a flight search agent using Blaxel LangGraph integration.
"""

from blaxel.langgraph import bl_model, bl_tools
from langgraph.prebuilt import create_react_agent


async def flight_agent_graph():
    """
    Creates a flight search agent graph using Blaxel + LangGraph.
    
    Returns:
        A LangGraph agent that can help with flight searches using Blaxel tools
    """
    prompt = (
        "You are a helpful flight booking assistant that can help users find and book flights. "
        "You can search for flights, compare prices, and provide booking recommendations."
    )
    
    try:
        # Use Blaxel tools for web search and flight APIs
        tools = await bl_tools(["blaxel-search"])
    except Exception as e:
        print(f"⚠️ MCP tools unavailable: {e}")
        tools = []  # Graceful fallback
    
    # Use Blaxel model wrapper for optimized performance
    model = await bl_model("sandbox-openai")
    
    # Fix: Extract the underlying LangChain model for compatibility
    if hasattr(model, 'wrapped_model'):
        langchain_model = model.wrapped_model
    elif hasattr(model, 'model'):
        langchain_model = model.model
    elif hasattr(model, '_model'):
        langchain_model = model._model
    else:
        # Fallback: use the model directly
        langchain_model = model
    
    return create_react_agent(
        name="flight-agent",
        model=langchain_model, 
        tools=tools, 
        prompt=prompt
    )


# Keep the async function for backward compatibility
async def agent():
    """
    Async wrapper for the flight agent.
    
    Returns:
        Flight search agent graph using Blaxel integration
    """
    return await flight_agent_graph()
