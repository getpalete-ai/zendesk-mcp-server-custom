#!/bin/bash
# entrypoint.sh

# Use environment variables or defaults
HOST=${SERVER_HOST:-0.0.0.0}
PORT=${SERVER_PORT:-8021}

echo "Starting Zendesk MCP server with mcp-proxy on $HOST:$PORT"

# Run with mcp-proxy instead of uvicorn
exec mcp-proxy --host $HOST --port $PORT --pass-environment -- mcp-zendesk

