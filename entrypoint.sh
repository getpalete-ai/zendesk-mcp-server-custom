#!/bin/bash
# entrypoint.sh

# Use environment variables or defaults
HOST=${SERVER_HOST:-0.0.0.0}
PORT=${SERVER_PORT:-8021}

echo "Starting Zendesk MCP server on $HOST:$PORT"

# Run the application
exec python -c "import sys; sys.path.append('/app'); from mcp_zendesk.server import app; import uvicorn; uvicorn.run(app, host='$HOST', port=$PORT)"

