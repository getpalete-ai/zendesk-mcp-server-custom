#!/bin/bash
# Check status of load balanced MCP setup

echo "=== Load Balanced MCP Status ==="
echo

# Check nginx
if pgrep nginx > /dev/null; then
    echo "✓ Nginx is running"
else
    echo "✗ Nginx is not running"
fi

# Check MCP instances
echo
echo "=== MCP Instances ==="
for pid_file in mcp_instance_*.pid; do
    if [ -f "$pid_file" ]; then
        pid=$(cat "$pid_file")
        if ps -p $pid > /dev/null 2>&1; then
            echo "✓ Instance with PID $pid is running"
        else
            echo "✗ Instance with PID $pid is not running"
        fi
    fi
done

echo
echo "=== Port Usage ==="
netstat -tlnp 2>/dev/null | grep -E ":(802[0-9]|803[0-9]|80)" || echo "No services found on expected ports"

echo
echo "=== Process List ==="
ps aux | grep -E "(mcp-proxy|nginx)" | grep -v grep || echo "No MCP or nginx processes found"

echo
echo "=== Health Check ==="
if command -v curl &> /dev/null; then
    echo "Testing health endpoint..."
    curl -s http://localhost/health || echo "Health check failed"
else
    echo "curl not available for health check"
fi
