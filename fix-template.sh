#!/bin/bash

# Fix script for template-copilot-kit-py
echo "🔧 Fixing template-copilot-kit-py bugs..."

# Fix 1: Correct the import statement
echo "  [1/3] Fixing import from blaxel.crewai to blaxel.langgraph..."
sed -i 's/from blaxel.crewai import bl_model/from blaxel.langgraph import bl_model/' src/agent.py

# Fix 2: Correct the async/await syntax
echo "  [2/3] Fixing async/await syntax on line 43..."
sed -i 's/model = await bl_model("sandbox-openai").to_langchain()/model = (await bl_model("sandbox-openai")).to_langchain()/' src/agent.py

# Fix 3: Comment out the broken MCP server
echo "  [3/3] Disabling broken explorer-mcp server..."
sed -i 's/^\[function.explorer-mcp\]/#[function.explorer-mcp]/' blaxel.toml
sed -i 's/^path = "explorer-mcp"/#path = "explorer-mcp"/' blaxel.toml
sed -i 's/^port = 1339/#port = 1339/' blaxel.toml

echo "✅ Fixes applied! Now you can run: bl serve --hotreload"
