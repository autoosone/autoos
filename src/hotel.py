from blaxel.langgraph import bl_model, bl_tools
from langgraph.prebuilt import create_react_agent


async def agent():
    prompt = (
        "You are a helpful assistant that can answer questions and help with tasks."
    )
    tools = await bl_tools(["explorer-mcp"])
    model = await bl_model("sandbox-openai")
    return create_react_agent(
        name="hotel-agent", model=model, tools=tools, prompt=prompt
    )
