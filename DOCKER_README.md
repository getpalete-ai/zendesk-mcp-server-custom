# Docker Deployment Guide for Zendesk MCP Server

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

## Troubleshooting

### Common Issues

1. **Container won't start**: Check environment variables are set correctly
2. **Connection refused**: Verify the service is running on the correct port
3. **Authentication errors**: Verify Zendesk credentials are correct

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

### Horizontal Scaling

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
