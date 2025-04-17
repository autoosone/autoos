from blaxel.models import bl_model
from blaxel.tools import bl_tools
from langgraph.prebuilt import create_react_agent


async def agent():
    prompt = "You are a helpful assistant that can answer questions and help with tasks."
    tools = await bl_tools(["blaxel-search"]).to_langchain()
    model = await bl_model("sandbox-openai").to_langchain()
    return create_react_agent(name="hotel-agent", model=model, tools=tools, prompt=prompt)
