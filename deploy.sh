#!/bin/bash
# Zendesk MCP Server Startup Script with .env loading for Linux/AWS

# Function to load .env file
load_env() {
    if [ -f .env ]; then
        echo "Loading environment from .env file..."
        # Export variables from .env file
        export $(grep -v '^#' .env | xargs)
    else
        echo ".env file not found, using default values..."
        # Set default values here
        export ZENDESK_BASE_URL="your_subdomain_here"
        export ZENDESK_EMAIL="your_email_here"
        export ZENDESK_API_TOKEN="your_api_token_here"
    fi
}

# Load environment variables
load_env

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

# Check if mcp-proxy is available
if ! command -v mcp-proxy &> /dev/null; then
    echo "Error: mcp-proxy not found. Please install the required dependencies."
    exit 1
fi

# Check if mcp-zendesk is available
if ! command -v mcp-zendesk &> /dev/null; then
    echo "Error: mcp-zendesk not found. Please install the package first."
    exit 1
fi

echo "Starting MCP server on port 8021..."
mcp-proxy --port 8021 --pass-environment -- mcp-zendesk

# Check exit status
if [ $? -ne 0 ]; then
    echo "Server exited with error. Press any key to continue..."
    read -n 1
fi
