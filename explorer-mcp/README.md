# Explorer-MCP Flight Data Service

A microservice providing flight data tools for the Trip Booking Agent.

This service exposes two MCP tools:
- `browserbase(url)`: loads a URL via a headless browser (Browserbase) and returns text content.
- `kayak(departure, destination, date[, return_date])`: generates a Kayak flight search URL.

## Prerequisites

- **Python:** 3.10 or later.
- **[UV](https://github.com/astral-sh/uv):** An extremely fast Python package and project manager, written in Rust.
- **[Blaxel CLI](https://docs.blaxel.ai/Get-started):** Ensure you have the Blaxel CLI installed. If not, install it globally:
  ```bash
  curl -fsSL https://raw.githubusercontent.com/beamlit/toolkit/main/install.sh | BINDIR=$HOME/.local/bin sh
  ```
- **Blaxel login:** Login to Blaxel platform
  ```bash
    bl login YOUR-WORKSPACE
  ```

**Environment Variable:** Create a `.env` file in this directory and set:
```bash
# Your Browserbase API key for headless browsing
BROWSERBASE_API_KEY=your_api_key_here
```

## Installation

Install dependencies for this service (from the root or this directory):

```bash
uv sync
```

## Running Locally

Start the MCP service in development mode with the inspector:

```bash
BL_DEBUG=true uv run mcp dev src/server.py
```

_Note:_ The MCP inspector UI will be available at http://localhost:16888 for interactive tool testing.

## Testing

When running in debug mode, use the inspector UI to invoke and inspect tools.

```
# Inspector is already started via the Running Locally step
```

## Deploying to Blaxel

To deploy this service only, run:

```bash
cd explorer-mcp
bl deploy --recursive=false
```

This will publish the MCP service to your Blaxel workspace.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
