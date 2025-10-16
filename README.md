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

## Functionalities

This MCP server exposes the following Zendesk operations as tools:

**Ticket Management:**
- `get_tickets` - Retrieve list of recent tickets
- `get_ticket_details` / `get_tickets_details` - Get detailed information for specific ticket(s)
- `create_ticket` - Create new support tickets with subject, description, priority, and tags
- `update_ticket` - Modify ticket status, priority, tags, and custom fields
- `update_custom_status` - Update custom status (Escalade, Pending, Solved, Refund_pending). Present custom status are harcoded and project specific - to be adapted using `get_tickets_fields_map` )
- `search_tickets` - Search tickets using query strings with sorting options
- `get_ticket_comments` - Retrieve all comments from a specific ticket
- `add_ticket_comment` - Add public or private comments to tickets

**User Management:**
- `get_user` / `get_users` - Retrieve user details using user id(s)

**Configuration:**
- `get_tickets_fields_map` - Get mapping of available ticket fields and custom fields