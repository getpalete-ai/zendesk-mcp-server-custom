#!/bin/bash
# Zendesk MCP Server with Uvicorn Scaling

# Function to load .env file
load_env() {
    if [ -f .env ]; then
        echo "Loading environment from .env file..."
        export $(grep -v '^#' .env | xargs)
    else
        echo ".env file not found, using default values..."
        export ZENDESK_BASE_URL="your_subdomain_here"
        export ZENDESK_EMAIL="your_email_here"
        export ZENDESK_API_TOKEN="your_api_token_here"
    fi
}

# Load environment variables
load_env

# Configuration for scaling
WORKERS=${WORKERS:-4}  # Default to 4 workers, can be overridden via environment
HOST=${HOST:-"0.0.0.0"}
PORT=${PORT:-8021}
BACKLOG=${BACKLOG:-2048}
TIMEOUT_KEEP_ALIVE=${TIMEOUT_KEEP_ALIVE:-30}
LIMIT_CONCURRENCY=${LIMIT_CONCURRENCY:-1000}

echo
echo "=== Zendesk MCP Server - Uvicorn Scaling ==="
echo "Workers: $WORKERS"
echo "Host: $HOST"
echo "Port: $PORT"
echo "Backlog: $BACKLOG"
echo "Timeout Keep-Alive: $TIMEOUT_KEEP_ALIVE"
echo "Concurrency Limit: $LIMIT_CONCURRENCY"
echo
echo "Checking variable loading:"
echo "ZENDESK_BASE_URL=$ZENDESK_BASE_URL"
echo "ZENDESK_EMAIL=$ZENDESK_EMAIL"
echo "ZENDESK_API_TOKEN=$ZENDESK_API_TOKEN"
echo

# Check if virtual environment exists and activate it
if [ -d "venv" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
elif [ -d ".venv" ]; then
    echo "Activating virtual environment..."
    source .venv/bin/activate
else
    echo "No virtual environment found. Make sure to install dependencies globally or create a venv."
fi

# Check if uvicorn is available
if ! command -v uvicorn &> /dev/null; then
    echo "Error: uvicorn not found. Please install uvicorn: pip install uvicorn"
    exit 1
fi

# Check if our server module exists
if [ ! -f "mcp_zendesk/server.py" ]; then
    echo "Error: mcp_zendesk/server.py not found."
    exit 1
fi

echo "Starting MCP server with $WORKERS workers on $HOST:$PORT..."
echo "Note: Each worker can handle multiple concurrent requests via asyncio"
echo "Note: Connection pooling is enabled for better performance"

# Run uvicorn directly with our FastMCP server
uvicorn mcp_zendesk.server:app \
    --host $HOST \
    --port $PORT \
    --workers $WORKERS \
    --backlog $BACKLOG \
    --timeout-keep-alive $TIMEOUT_KEEP_ALIVE \
    --limit-concurrency $LIMIT_CONCURRENCY \
    --log-level info

# Check exit status
if [ $? -ne 0 ]; then
    echo "Server exited with error. Press any key to continue..."
    read -n 1
fi