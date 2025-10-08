#!/bin/bash
# deploy-swarm.sh

set -e  # Exit on any error

echo "=== Automated Docker Swarm Deployment ==="

# Load environment variables
if [ -f .env ]; then
    echo "Loading environment from .env file..."
    export $(grep -v '^#' .env | xargs)
else
    echo "Error: .env file not found!"
    exit 1
fi

# Validate required environment variables
if [ -z "$ZENDESK_BASE_URL" ] || [ -z "$ZENDESK_EMAIL" ] || [ -z "$ZENDESK_API_TOKEN" ]; then
    echo "Error: Missing required environment variables!"
    echo "Please check your .env file"
    exit 1
fi

echo "Environment variables loaded successfully!"

# Initialize swarm if not already initialized
if ! docker info | grep -q "Swarm: active"; then
    echo "Initializing Docker Swarm..."
    docker swarm init
    echo "✅ Swarm initialized!"
else
    echo "✅ Swarm already active!"
fi

# Deploy the stack
echo "Deploying stack..."
docker stack deploy -c docker-stack.yml zendesk-stack

# Wait for services to start
echo "Waiting for services to start..."
sleep 15

# Check service status
echo "Checking service status..."
docker service ls

# Wait for all replicas to be running
echo "Waiting for all replicas to be running..."
timeout=60
counter=0
while [ $counter -lt $timeout ]; do
    running=$(docker service ps zendesk-stack_zendesk-mcp --filter "desired-state=running" --format "{{.CurrentState}}" | grep -c "Running" || true)
    if [ "$running" -eq 3 ]; then
        echo "✅ All replicas are running!"
        break
    fi
    echo "Waiting for replicas... ($running/3 running)"
    sleep 5
    counter=$((counter + 5))
done

# Test the service
echo "Testing service..."
if curl -f http://localhost:8021/status > /dev/null 2>&1; then
    echo "✅ Service is responding!"
else
    echo "❌ Service is not responding!"
    exit 1
fi

echo
echo "🎉 Deployment completed successfully!"
echo "Service available at: http://localhost:8021"
echo "Health check: http://localhost:8021/status"
echo
echo "Management commands:"
echo "  Scale: ./scale-swarm.sh 5"
echo "  Stop:  ./stop-swarm.sh"
echo "  Logs:  docker service logs zendesk-stack_zendesk-mcp"
