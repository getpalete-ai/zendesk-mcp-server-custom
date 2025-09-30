#!/bin/bash
# Stop all simple load balanced MCP instances

echo "Stopping simple load balanced MCP setup..."

# Stop MCP instances
echo "Stopping MCP instances..."
for pid_file in mcp_instance_*.pid; do
    if [ -f "$pid_file" ]; then
        pid=$(cat "$pid_file")
        if ps -p $pid > /dev/null 2>&1; then
            echo "Stopping instance with PID $pid..."
            kill $pid
        fi
        rm "$pid_file"
    fi
done

# Clean up any remaining mcp-proxy processes
pkill -f "mcp-proxy.*mcp-zendesk" 2>/dev/null

echo "All simple load balanced instances stopped."
