#!/bin/bash
# build-swarm.sh

set -e  # Exit on any error

echo "=== Automated Docker Swarm Build ==="

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "Error: Docker is not running!"
    exit 1
fi

# Check if .env file exists
if [ ! -f .env ]; then
    echo "Error: .env file not found!"
    echo "Please create .env file with your Zendesk credentials"
    exit 1
fi

# Build the Docker image
echo "Building Docker image..."
docker build -t zendesk-mcp-server:latest .

# Verify image was created
if docker images | grep -q "zendesk-mcp-server"; then
    echo "✅ Image built successfully!"
else
    echo "❌ Image build failed!"
    exit 1
fi

echo "Build completed successfully!"
