from datetime import datetime
from logging import getLogger
from typing import Annotated, TypedDict

from blaxel.langgraph import bl_model
from langchain_core.messages import AIMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, StateGraph
from langgraph.graph.message import add_messages
from langgraph_supervisor import create_supervisor

from .flight import agent as flight_agent
from .hotel import agent as hotel_agent

logger = getLogger(__name__)


class State(TypedDict):
    messages: Annotated[list, add_messages]


def flight_agent_graph():
    async def handle_flight(state: State) -> State:
        crew = await flight_agent()
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
    graph.add_node("flight_agent", handle_flight)
    graph.set_entry_point("flight_agent")
    graph.add_edge("flight_agent", END)
    return graph.compile(name="flight_agent")


async def agent():
    # Use the correct model that exists in workspace
    model = await bl_model("sandbox-openai")
    supervisor_graph = create_supervisor(
        [flight_agent_graph(), await hotel_agent()],
        model=model,
        supervisor_name="supervisor-agent",
        prompt="""
        You are a supervisor agent that can delegate tasks to other agents.
        You specialized in booking trips. To do so you have access to the following agents:
        - flight_agent: An agent that can book flights.
        - hotel_agent: An agent that can book hotels.
        """,
    )
    memory = MemorySaver()
    final_graph = supervisor_graph.compile(checkpointer=memory)
    return final_graph
