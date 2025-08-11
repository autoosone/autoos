import asyncio
import os
from logging import getLogger
from typing import Annotated, Optional

from mcp.server.fastmcp import FastMCP

# Create MCP server
mcp = FastMCP("explorer")
logger = getLogger(__name__)

@mcp.tool()
async def web_search(
    query: Annotated[str, "The search query"]
) -> str:
    """Search the web for information"""
    logger.info(f"Web search for: {query}")
    return f"Search results for '{query}': Found relevant information about {query}. Here are some key findings..."

@mcp.tool()
async def hotel_search(
    location: Annotated[str, "The location to search for hotels"],
    checkin: Annotated[str, "Check-in date"] = "2024-01-01",
    checkout: Annotated[str, "Check-out date"] = "2024-01-02"
) -> str:
    """Search for hotels in a specific location"""
    logger.info(f"Hotel search for {location}")
    return f"Hotels in {location} from {checkin} to {checkout}:\n• Hilton - $200/night\n• Marriott - $180/night\n• Holiday Inn - $150/night"

@mcp.tool()
async def flight_search(
    departure: Annotated[str, "Departure city"],
    destination: Annotated[str, "Destination city"], 
    date: Annotated[str, "Flight date"]
) -> str:
    """Search for flights between cities"""
    logger.info(f"Flight search from {departure} to {destination} on {date}")
    return f"Flights from {departure} to {destination} on {date}:\n• United - $450\n• Delta - $475\n• American - $420"

@mcp.tool()
async def get_weather(
    city: Annotated[str, "The city to get weather for"]
) -> str:
    """Get current weather for a city"""
    logger.info(f"Weather request for {city}")
    return f"Weather in {city}: Sunny, 72°F (22°C), light breeze"

if __name__ == "__main__":
    # Run the MCP server
    mcp.run()
