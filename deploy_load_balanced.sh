#!/bin/bash
# Zendesk MCP Server - Load Balanced with Multiple Instances

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

# Configuration for load balancing
INSTANCES=${INSTANCES:-3}  # Number of mcp-proxy instances
BASE_PORT=${BASE_PORT:-8021}
NGINX_PORT=${NGINX_PORT:-80}
HOST=${HOST:-"0.0.0.0"}

echo
echo "=== Zendesk MCP Server - Load Balanced ==="
echo "Instances: $INSTANCES"
echo "Base Port: $BASE_PORT"
echo "Nginx Port: $NGINX_PORT"
echo "Host: $HOST"
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

echo "Starting $INSTANCES MCP server instances with nginx load balancer..."

# Create local directories for nginx
mkdir -p nginx_logs

# Create nginx configuration with dynamic upstream servers
cat > nginx_mcp.conf << EOF
events {
    worker_connections 1024;
}

http {
    upstream mcp_backend {
        # Load balance across MCP instances (dynamically generated)
EOF

# Add server entries for each instance
for i in $(seq 1 $INSTANCES); do
    PORT=$((BASE_PORT + i - 1))
    echo "        server $HOST:$PORT;" >> nginx_mcp.conf
done

# Complete the nginx configuration
cat >> nginx_mcp.conf << EOF
    }

    server {
        listen $NGINX_PORT;
        server_name localhost;

        # Health check endpoint
        location /health {
            access_log off;
            return 200 "healthy\n";
            add_header Content-Type text/plain;
        }

        # Load balance all MCP requests
        location / {
            proxy_pass http://mcp_backend;
            proxy_set_header Host \$host;
            proxy_set_header X-Real-IP \$remote_addr;
            proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto \$scheme;
            
            # WebSocket support for SSE
            proxy_http_version 1.1;
            proxy_set_header Upgrade \$http_upgrade;
            proxy_set_header Connection "upgrade";
            
            # SSE specific settings
            proxy_buffering off;
            proxy_cache off;
            proxy_read_timeout 24h;
            
            # Timeouts
            proxy_connect_timeout 30s;
            proxy_send_timeout 30s;
            proxy_read_timeout 30s;
        }
    }
}
EOF


# Start MCP instances
echo "Starting MCP instances..."
for i in $(seq 1 $INSTANCES); do
    PORT=$((BASE_PORT + i - 1))
    echo "Starting instance $i on port $PORT..."
    
    # Start in background
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

# Start nginx with our configuration
echo "Starting nginx load balancer on port $NGINX_PORT..."

# Check if nginx is already running and stop it
if [ -f "nginx.pid" ]; then
    nginx_pid=$(cat "nginx.pid")
    if ps -p $nginx_pid > /dev/null 2>&1; then
        echo "Stopping existing nginx..."
        sudo kill $nginx_pid
        sleep 2
    fi
fi

# Start nginx with sudo to avoid permission issues
sudo nginx -c $(pwd)/nginx_mcp.conf &

# Store nginx PID for cleanup
echo $! > "nginx.pid"

# Give nginx a moment to start
sleep 3

echo
echo "Load balanced setup complete!"
echo "MCP instances: $(seq -s ', ' $BASE_PORT $((BASE_PORT + INSTANCES - 1)))"
echo "Nginx load balancer: http://$HOST:$NGINX_PORT"
echo "Health check: http://$HOST:$NGINX_PORT/health"
echo
echo "To stop all instances, run: ./stop_load_balanced.sh"

# Wait for all background processes
wait
