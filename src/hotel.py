from blaxel.langgraph import bl_model, bl_tools
from langgraph.prebuilt import create_react_agent


async def agent():
    prompt = (
        "You are a helpful hotel booking assistant that can help users find and book hotels."
    )
    
    try:
        # Use Blaxel tools - this gives us the full ecosystem
        tools = await bl_tools(["blaxel-search"])
    except Exception as e:
        print(f"⚠️ MCP tools unavailable: {e}")
        tools = []  # Graceful fallback
    
    # Use Blaxel model wrapper - it handles optimization and caching
    model = await bl_model("sandbox-openai")
    
    # Fix: Extract the underlying LangChain model for compatibility
    if hasattr(model, 'wrapped_model'):
        langchain_model = model.wrapped_model
    elif hasattr(model, 'model'):
        langchain_model = model.model
    elif hasattr(model, '_model'):
        langchain_model = model._model
    else:
        # Fallback: use the model directly and hope it's compatible
        langchain_model = model
    
    return create_react_agent(
        name="hotel-agent", 
        model=langchain_model, 
        tools=tools, 
        prompt=prompt
    )
