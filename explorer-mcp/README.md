# Template MCP Hello World Python

A template implementation of a MCP Hello World Python.

## Prerequisites

- **Python:** 3.12 or later.
- **[UV](https://github.com/astral-sh/uv):** An extremely fast Python package and project manager, written in Rust.
- **[Blaxel CLI](https://docs.blaxel.ai/Get-started):** Ensure you have the Blaxel CLI installed. If not, install it globally:
  ```bash
  curl -fsSL https://raw.githubusercontent.com/beamlit/toolkit/main/install.sh | BINDIR=$HOME/.local/bin sh
  ```
- **Blaxel login:** Login to Blaxel platform
  ```bash
    bl login YOUR-WORKSPACE
  ```
  
- Optional - **NodeJS:** 20.11.0 or later. We use a npm package for the hot reload feature "bl serve --hotrealod".

## Installation

- **Clone the repository and install the dependencies**:

  ```bash
  git clone https://github.com/beamlit/template-mcp-helloworld-python.git
  cd template-mcp-helloworld-python
  uv sync
  ```

## Running the Server Locally

Start the development server with hot reloading using the Blaxel CLI command:

```bash
bl serve --hotrealod
```

_Note:_ This command starts the server and enables hot reload so that changes to the source code are automatically reflected.

## Testing your agent

This command allow you to launch MCP inspector locally, which help a lot for debug through the UI.

```bash
BL_DEBUG=true uv run mcp dev src/server.py
```

## Deploying to Blaxel

When you are ready to deploy your application, run:

```bash
bl deploy
```

This command uses your code and the configuration files under the `.blaxel` directory to deploy your application.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
