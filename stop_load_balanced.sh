#!/bin/bash
# Stop all load balanced MCP instances and nginx

echo "Stopping load balanced MCP setup..."

# Stop nginx
echo "Stopping nginx..."
if [ -f "nginx.pid" ]; then
    nginx_pid=$(cat "nginx.pid")
    if ps -p $nginx_pid > /dev/null 2>&1; then
        echo "Stopping nginx with PID $nginx_pid..."
        kill $nginx_pid
    fi
    rm "nginx.pid"
fi
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

# Clean up nginx config and directories
rm -f nginx_mcp.conf
rm -rf nginx_logs nginx_temp

echo "All load balanced instances stopped."
