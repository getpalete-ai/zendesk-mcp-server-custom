#!/bin/bash
# scale-swarm.sh

set -e  # Exit on any error

REPLICAS=${1:-3}

echo "=== Scaling Zendesk MCP Service ==="

# Check if service exists
if ! docker service ls | grep -q "zendesk-stack_zendesk-mcp"; then
    echo "Error: Service not found! Please deploy first with ./deploy-swarm.sh"
    exit 1
fi

echo "Scaling to $REPLICAS replicas..."
docker service scale zendesk-stack_zendesk-mcp=$REPLICAS

# Wait for scaling to complete
echo "Waiting for scaling to complete..."
timeout=60
counter=0
while [ $counter -lt $timeout ]; do
    running=$(docker service ps zendesk-stack_zendesk-mcp --filter "desired-state=running" --format "{{.CurrentState}}" | grep -c "Running" || true)
    if [ "$running" -eq "$REPLICAS" ]; then
        echo "✅ Scaling completed! ($running/$REPLICAS replicas running)"
        break
    fi
    echo "Waiting for scaling... ($running/$REPLICAS running)"
    sleep 5
    counter=$((counter + 5))
done

echo "Current service status:"
docker service ls
docker service ps zendesk-stack_zendesk-mcp
