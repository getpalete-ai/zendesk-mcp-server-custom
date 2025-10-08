#!/bin/bash
# setup-swarm.sh

echo "=== Setting up Docker Swarm Automation ==="

# Make all scripts executable
echo "Making scripts executable..."
chmod +x build-swarm.sh deploy-swarm.sh scale-swarm.sh stop-swarm.sh automate-swarm.sh

# Create convenient symlinks
echo "Creating symlinks..."
ln -sf automate-swarm.sh deploy
ln -sf automate-swarm.sh scale
ln -sf automate-swarm.sh stop
ln -sf automate-swarm.sh status
ln -sf automate-swarm.sh logs

echo "✅ Setup completed!"
echo
echo "Available commands:"
echo "  ./deploy          # Deploy the service"
echo "  ./scale 5         # Scale to 5 replicas"
echo "  ./stop            # Stop the service"
echo "  ./status          # Check status"
echo "  ./logs            # View logs"
echo
echo "Or use the full automation script:"
echo "  ./automate-swarm.sh deploy"
echo "  ./automate-swarm.sh scale 5"
echo "  ./automate-swarm.sh stop"
