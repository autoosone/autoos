"""
Flight Search Agent Module

This module implements an AI-powered flight search system using CrewAI framework.
It creates a crew of specialized agents to search for flights and provide booking information.
"""

# We have to apply nest_asyncio because crewai is not compatible with async
import nest_asyncio

nest_asyncio.apply()

from blaxel.models import bl_model
from blaxel.tools import bl_tools
from crewai import Agent, Crew, Task


async def agent():
    """
    Main flight search agent function that orchestrates the flight search process.

    Args:
        input (str): The search query containing flight search criteria

    Yields:
        str: The search results in a formatted string

    This function:
    1. Sets up the necessary tools and models
    2. Creates specialized agents for flight search and summarization
    3. Defines tasks for searching flights and finding booking providers
    4. Executes the crew workflow and yields the results
    """
    # Initialize tools and model for the agents
    tools = await bl_tools(["explorer-mcp"]).to_crewai()
    model = await bl_model("sandbox-openai").to_crewai()

    # Create the flight search agent
    flights_agent = Agent(
        role="Flights",
        goal="Search flights",
        backstory="I am an agent that can search for flights.",
        llm=model,
        tools=tools,
        allow_delegation=False,
    )

    # Create the summarization agent
    summarize_agent = Agent(
        role="Summarize",
        goal="Summarize content",
        backstory="I am an agent that can summarize text.",
        llm=model,
        allow_delegation=False,
    )

    # Example output format for flight search task
    output_search_example = """
    Here are our top 5 flights from San Francisco to New York on 21st September 2024:
    1. Delta Airlines: Departure: 21:35, Arrival: 03:50, Duration: 6 hours 15 minutes, Price: $125, Details: https://www.kayak.com/flights/sfo/jfk/2024-09-21/12:45/13:55/2:10/delta/airlines/economy/1
    """

    # Define the flight search task
    search_task = Task(
        description=(
            "Search flights according to criteria {request}. Current year: {current_year}"
        ),
        expected_output=output_search_example,
        agent=flights_agent,
    )

    # Example output format for booking providers task
    output_providers_example = """
    Here are our top 5 picks from San Francisco to New York on 21st September 2024:
    1. Delta Airlines:
        - Departure: 21:35
        - Arrival: 03:50
        - Duration: 6 hours 15 minutes
        - Price: $125
        - Booking: [Delta Airlines](https://www.kayak.com/flights/sfo/jfk/2024-09-21/12:45/13:55/2:10/delta/airlines/economy/1)
        ...
    """

    # Define the booking providers search task
    search_booking_providers_task = Task(
        description="Load every flight individually and find available booking providers",
        expected_output=output_providers_example,
        agent=flights_agent,
    )

    # Create and configure the crew
    crew = Crew(
        agents=[flights_agent, summarize_agent],
        tasks=[search_task, search_booking_providers_task],
        max_rpm=100,  # Maximum requests per minute
        verbose=True,  # Enable verbose output
        planning=True  # Enable planning mode
    )

    # Execute the crew workflow and yield results
    return crew
