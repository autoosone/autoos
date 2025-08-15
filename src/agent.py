from datetime import datetime
from logging import getLogger
from typing import Annotated, TypedDict

from blaxel.langgraph import bl_model
from langchain_core.messages import AIMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, StateGraph
from langgraph.graph.message import add_messages
from langgraph_supervisor import create_supervisor

from .vehicle import agent as vehicle_agent
from .dealer import agent as dealer_agent

logger = getLogger(__name__)


class State(TypedDict):
    messages: Annotated[list, add_messages]


def vehicle_agent_graph():
    async def handle_vehicle(state: State) -> State:
        crew = await vehicle_agent()
        inputs = {
            "request": state["messages"][-1].content,
            "current_year": datetime.now().year,
        }
        result = crew.kickoff(
            inputs=inputs,
        )
        state["messages"].append(AIMessage(content=result.raw))
        return state

    graph = StateGraph(State)
    graph.add_node("vehicle_agent", handle_vehicle)
    graph.set_entry_point("vehicle_agent")
    graph.add_edge("vehicle_agent", END)
    return graph.compile(name="vehicle_agent")


async def agent():
    # Use the correct model that exists in workspace
    model = await bl_model("sandbox-openai")
    supervisor_graph = create_supervisor(
        [vehicle_agent_graph(), await dealer_agent()],
        model=model,
        supervisor_name="automotive-supervisor",
        prompt="""
        You are an automotive marketplace supervisor agent that helps users find their perfect vehicle.
        
        You can delegate tasks to specialized agents:
        - Vehicle Agent: Search for vehicles, compare specs, check pricing, analyze features
        - Dealer Agent: Find nearby dealers, check inventory, schedule test drives, get contact info
        
        Key capabilities:
        - Search vehicles by make, model, year, price range, and features
        - Compare multiple vehicles side by side
        - Find dealers with specific inventory
        - Calculate monthly payments and financing options
        - Schedule test drives and appointments
        - Provide market analysis and pricing insights
        
        Always be helpful, informative, and guide users through their car buying journey.
        Focus on understanding their needs (budget, lifestyle, preferences) to make personalized recommendations.
        """,
    )
    return supervisor_graph.compile(checkpointer=MemorySaver())
