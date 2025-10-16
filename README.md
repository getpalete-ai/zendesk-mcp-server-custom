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

Edit `.env` file with your actual Zendesk credentials (see [Environment Variables](#environment-variables))


### 2. Build and Run



```bash
# Build and start the service
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the service
docker-compose down
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


## Monitoring and Logs

### View Logs

```bash
# Docker Compose
docker-compose logs -f zendesk-mcp

# Docker
docker logs -f zendesk-mcp-server
```


### Updates

```bash
# Pull latest changes
git pull origin docker

# Rebuild and restart
docker-compose down
docker-compose build 
docker-compose up -d
```

## Support
- email: nicolas@getpalete.com & oussama@getpalete.com
