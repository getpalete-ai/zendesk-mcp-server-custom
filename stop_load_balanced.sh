#!/bin/bash
# Stop all load balanced MCP instances and nginx

echo "Stopping load balanced MCP setup..."

# Stop nginx
echo "Stopping nginx..."
nginx -s quit 2>/dev/null || pkill nginx 2>/dev/null

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

# Clean up nginx config
rm -f nginx_mcp.conf

echo "All load balanced instances stopped."
