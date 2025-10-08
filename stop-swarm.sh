#!/bin/bash
# stop-swarm.sh

set -e  # Exit on any error

echo "=== Stopping Zendesk MCP Stack ==="

# Check if stack exists
if ! docker stack ls | grep -q "zendesk-stack"; then
    echo "No stack found to stop!"
    exit 0
fi

echo "Stopping stack..."
docker stack rm zendesk-stack

# Wait for services to stop
echo "Waiting for services to stop..."
timeout=60
counter=0
while [ $counter -lt $timeout ]; do
    if ! docker stack ls | grep -q "zendesk-stack"; then
        echo "✅ Stack removed successfully!"
        break
    fi
    echo "Waiting for stack to stop..."
    sleep 5
    counter=$((counter + 5))
done

echo "Cleanup completed!"
