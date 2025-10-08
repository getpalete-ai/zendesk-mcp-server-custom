#!/bin/bash
# automate-swarm.sh

set -e  # Exit on any error

ACTION=${1:-deploy}
REPLICAS=${2:-3}

case $ACTION in
    "build")
        echo "=== Building Docker Image ==="
        ./build-swarm.sh
        ;;
    "deploy")
        echo "=== Deploying with Docker Swarm ==="
        ./build-swarm.sh
        ./deploy-swarm.sh
        ;;
    "scale")
        echo "=== Scaling Service ==="
        ./scale-swarm.sh $REPLICAS
        ;;
    "stop")
        echo "=== Stopping Service ==="
        ./stop-swarm.sh
        ;;
    "restart")
        echo "=== Restarting Service ==="
        ./stop-swarm.sh
        sleep 5
        ./deploy-swarm.sh
        ;;
    "status")
        echo "=== Service Status ==="
        docker service ls
        docker service ps zendesk-stack_zendesk-mcp
        ;;
    "logs")
        echo "=== Service Logs ==="
        docker service logs zendesk-stack_zendesk-mcp
        ;;
    *)
        echo "Usage: $0 {build|deploy|scale|stop|restart|status|logs} [replicas]"
        echo "Examples:"
        echo "  $0 deploy          # Build and deploy"
        echo "  $0 scale 5         # Scale to 5 replicas"
        echo "  $0 stop            # Stop the service"
        echo "  $0 restart         # Restart the service"
        echo "  $0 status          # Check status"
        echo "  $0 logs            # View logs"
        exit 1
        ;;
esac
