# Deployment Guide for Zendesk MCP Server

This guide explains how to deploy the Zendesk MCP Server using virtual environment and load balancing.

## Prerequisites

- Python 3.10 or higher
- pip (Python package manager)
- Nginx (for load balancing)
- Zendesk API credentials (subdomain, email, and API token)

## Quick Start

### 1. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### 2. Install Dependencies

```bash
# Install the package in editable mode
pip install -e .
```


### 3. Environment Setup

Create a `.env` file in the project root with your Zendesk credentials. 

The following environment variables are required:

| Variable | Description | Example |
|----------|-------------|---------|
| `ZENDESK_BASE_URL` | Your Zendesk subdomain URL | `https://mycompany.zendesk.com` |
| `ZENDESK_EMAIL` | Your Zendesk email address | `admin@mycompany.com` |
| `ZENDESK_API_TOKEN` | Your Zendesk API token | `abc123def456...` |

Optional deployment configuration:

| Variable | Description | Default |
|----------|-------------|---------|
| `INSTANCES` | Number of MCP server instances | `3` |
| `BASE_PORT` | Starting port for instances | `8021` |
| `NGINX_PORT` | Nginx load balancer port | `80` |
| `HOST` | Host binding address | `0.0.0.0` |

```bash
# Build and start the service
docker-compose up -d
```


### 4. Deploy Load Balanced Setup

```bash
# Make deployment script executable
chmod +x deploy_load_balanced.sh

# Deploy with load balancing (default: 3 instances)
./deploy_load_balanced.sh
```

This will start:
- Multiple MCP server instances (default: 3) on ports 8021, 8022, 8023
- Nginx load balancer on port 80 (default)

You can customize the deployment:

```bash
# Custom number of instances and ports
INSTANCES=5 BASE_PORT=8021 NGINX_PORT=8080 ./deploy_load_balanced.sh
```




## Monitoring and Management

### Check Status

```bash
# Check if services are running
./check_load_balanced.sh
```

This will show:
- Nginx status
- MCP instance statuses
- Port usage
- Health check results

### Stop Services

```bash
# Stop all instances and nginx
./stop_load_balanced.sh
```

### Health Check

```bash
# Test the health endpoint
curl http://localhost/health
```

### Updates

```bash
# Pull latest changes
git pull origin main

# Reinstall package
pip install -e .

# Restart services
./stop_load_balanced.sh
./deploy_load_balanced.sh
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