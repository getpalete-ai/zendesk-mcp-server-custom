# Deployment Guide for Zendesk MCP Server

This guide explains how to deploy the Zendesk MCP Server using Docker.

## Prerequisites

- Docker and Docker Compose installed on your system
- Zendesk API credentials (subdomain, email, and API token)

## Quick Start

### 1. Environment Setup

Copy the example environment file and configure your Zendesk credentials:

```bash
cp env.example .env
```

Edit `.env` file with your actual Zendesk credentials:

```bash
ZENDESK_BASE_URL=https://your-subdomain.zendesk.com
ZENDESK_EMAIL=your-email@example.com
ZENDESK_API_TOKEN=your-api-token-here
```

### 2. Build and Run

#### Option A: Using Docker Compose (Recommended)

```bash
# Build and start the service
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the service
docker-compose down
```

#### Option B: Using Docker directly

```bash
# Build the image
docker build -t zendesk-mcp-server .

# Run the container
docker run -d \
  --name zendesk-mcp-server \
  -p 8021:8021 \
  --env-file .env \
  zendesk-mcp-server
```

### 3. Verify Deployment

Check if the service is running:

```bash
# Check container status
docker ps

# Check service health
curl http://localhost:8021/status
```

## Production Deployment

### Using Docker Swarm

For production deployment with automatic load balancing and orchestration:

```bash
# 1. Setup (run once) - prepares scripts and creates symlinks
chmod +x setup-swarm.sh
./setup-swarm.sh

# 2. Deploy with load balancing (builds image + deploys stack)
./deploy

# 3. Scale to multiple replicas (optional)
./scale 5

# 4. Check status
./status

# 5. View logs
./logs

# 6. Stop service
./stop
```

**What Each Step Does:**
- **Step 1**: Prepares scripts and creates convenient symlinks (run once)
- **Step 2**: Builds Docker image + deploys stack with 3 replicas + load balancing
- **Step 3**: Scales to more replicas (optional)
- **Steps 4-6**: Management commands

**Docker Swarm Features:**
- ✅ **Automatic load balancing** across replicas
- ✅ **Health checks** and automatic restarts
- ✅ **Rolling updates** with zero downtime
- ✅ **Resource limits** and reservations
- ✅ **Service discovery** between containers
- ✅ **Built-in scaling** and management

### Using Docker Compose with Nginx

For production deployment with load balancing and SSL termination:

```bash
# Start with nginx proxy
docker-compose --profile production up -d
```

This will start:
- Zendesk MCP Server on port 8021 (internal)
- Nginx reverse proxy on ports 80 and 443 (external)

### Environment Variables

The following environment variables are required:

| Variable | Description | Example |
|----------|-------------|---------|
| `ZENDESK_BASE_URL` | Your Zendesk subdomain URL | `https://mycompany.zendesk.com` |
| `ZENDESK_EMAIL` | Your Zendesk email address | `admin@mycompany.com` |
| `ZENDESK_API_TOKEN` | Your Zendesk API token | `abc123def456...` |

### Security Considerations

1. **Never commit `.env` files** to version control
2. **Use secrets management** in production (Docker secrets, Kubernetes secrets, etc.)
3. **Run as non-root user** (already configured in Dockerfile)
4. **Use HTTPS** in production with proper SSL certificates

## Monitoring and Logs

### View Logs

```bash
# Docker Compose
docker-compose logs -f zendesk-mcp

# Docker
docker logs -f zendesk-mcp-server
```

### Health Checks

The container includes health checks that verify the service is responding:

```bash
# Check health status
docker inspect --format='{{.State.Health.Status}}' zendesk-mcp-server
```

## Docker Swarm Management

### Available Commands

```bash
# Deploy service
./deploy

# Scale service
./scale 5

# Check status
./status

# View logs
./logs

# Stop service
./stop

# Restart service
./automate-swarm.sh restart
```

### Docker Swarm Commands

```bash
# Check swarm status
docker node ls

# Check service status
docker service ls

# Check service details
docker service ps zendesk-stack_zendesk-mcp

# View service logs
docker service logs zendesk-stack_zendesk-mcp

# Update service
docker service update zendesk-stack_zendesk-mcp
```

## Troubleshooting

### Common Issues

1. **Container won't start**: Check environment variables are set correctly
2. **Connection refused**: Verify the service is running on the correct port
3. **Authentication errors**: Verify Zendesk credentials are correct
4. **Swarm not initialized**: Run `docker swarm init` first
5. **Service not scaling**: Check if all replicas are healthy with `./status`

### Debug Mode

Run the container in interactive mode for debugging:

```bash
docker run -it --rm \
  --env-file .env \
  zendesk-mcp-server \
  /bin/bash
```

### Logs Analysis

```bash
# View recent logs
docker logs --tail 100 zendesk-mcp-server

# Follow logs in real-time
docker logs -f zendesk-mcp-server
```

## Scaling

### Docker Swarm Scaling (Recommended)

```bash
# Scale to 5 replicas with load balancing
./scale 5

# Check scaling status
./status

# View service details
docker service ps zendesk-stack_zendesk-mcp
```

### Docker Compose Scaling

To run multiple instances behind a load balancer:

```bash
# Scale the service
docker-compose up -d --scale zendesk-mcp=3
```

### Resource Limits

Add resource limits to your docker-compose.yml:

```yaml
services:
  zendesk-mcp:
    # ... other configuration
    deploy:
      resources:
        limits:
          memory: 512M
          cpus: '0.5'
        reservations:
          memory: 256M
          cpus: '0.25'
```

## Backup and Maintenance

### Backup Configuration

```bash
# Backup environment configuration
cp .env .env.backup

# Backup docker-compose configuration
cp docker-compose.yml docker-compose.yml.backup
```

### Updates

```bash
# Pull latest changes
git pull

# Rebuild and restart
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

## Support

For issues related to:
- **Docker deployment**: Check this guide and Docker documentation
- **Zendesk API**: Verify your credentials and API permissions
- **MCP Server**: Check the main project documentation
