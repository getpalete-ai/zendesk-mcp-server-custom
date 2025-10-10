#!/bin/bash
# entrypoint.sh - Load balanced MCP server

# Configuration
INSTANCES=${INSTANCES:-3}
BASE_PORT=${BASE_PORT:-8021}
HOST=${SERVER_HOST:-0.0.0.0}

echo "Starting $INSTANCES MCP server instances..."

# Start MCP instances on different ports
for i in $(seq 1 $INSTANCES); do
    PORT=$((BASE_PORT + i - 1))
    echo "Starting instance $i on port $PORT..."
    
    # Start mcp-proxy in background
    mcp-proxy \
        --host $HOST \
        --port $PORT \
        --pass-environment \
        -- mcp-zendesk &
    
    # Store PID for cleanup
    echo $! > "mcp_instance_$i.pid"
    
    # Small delay between instances
    sleep 2
done

echo "All MCP instances started. Waiting for connections..."
wait

