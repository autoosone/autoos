from logging import getLogger
from time import sleep
from typing import Annotated, Optional

from blaxel import env
from blaxel.mcp.server import FastMCP
from html2text import html2text
from playwright.sync_api import sync_playwright

mcp = FastMCP("mcp-flight")
logger = getLogger(__name__)

@mcp.tool()
def browserbase(
    url: Annotated[
        str,
        "The URL to load",
    ],
) -> str:
    """Loads a URL using a headless webbrowser"""
    with sync_playwright() as playwright:
        browser = playwright.chromium.connect_over_cdp(
            "wss://connect.browserbase.com?apiKey="
            + env["BROWSERBASE_API_KEY"]
        )
        context = browser.contexts[0]
        page = context.pages[0]
        page.goto(url)

        # Wait for the flight search to finish
        sleep(25)

        content = html2text(page.content())
        browser.close()
        return content


@mcp.tool()
def kayak(
    departure: Annotated[
        str,
        "The departure city",
    ],
    destination: Annotated[
        str,
        "The arrival city",
    ],
    date: Annotated[
        str,
        "The date of the flight",
    ],
    return_date: Annotated[
        Optional[str],
        "The return date of the flight",
    ],
) -> str:
    """Generates a Kayak URL for flights between departure and destination on the specified date."""
    logger.info(f"Generating Kayak URL for {departure} to {destination} on {date}")
    URL = f"https://www.kayak.com/flights/{departure}-{destination}/{date}"
    if return_date:
        URL += f"/{return_date}"
    URL += "?currency=USD"
    return URL

if not env["BL_DEBUG"]:
    mcp.run(transport="ws")