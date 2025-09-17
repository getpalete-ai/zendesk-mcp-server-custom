# Zendesk MCP Server

A Model Context Protocol (MCP) server for Zendesk integration. This server provides tools for interacting with Zendesk, including ticket management, user operations, and search functionality.

## Features

- **Ticket Management**: Create, read, update, and comment on support tickets
- **User Management**: View user information and details
- **Search**: Advanced ticket search with flexible query options
- **Resources**: Access Zendesk tickets, users, groups, and ticket fields
- **Prompts**: Templates for creating tickets, crafting responses, and analyzing data

## Installation

```bash
pip install mcp-zendesk
```

## Configuration

Set the following environment variables:

```bash
export ZENDESK_BASE_URL="https://your-subdomain.zendesk.com"
export ZENDESK_EMAIL="your_email@example.com"
export ZENDESK_API_TOKEN="your_api_token"
```

To get an API token, visit Admin > Channels > API in your Zendesk Support admin interface.

## Usage

### Starting the server directly

```bash
mcp-zendesk
```

### Using with Claude Desktop

Add the following to your `claude_desktop_config.json` file:

```json
"mcp-zendesk": {
  "command": "uvx",
  "args": [
    "mcp-zendesk"
  ],
  "env": {
    "ZENDESK_BASE_URL": "https://your-subdomain.zendesk.com",
    "ZENDESK_EMAIL": "your_email@example.com",
    "ZENDESK_API_TOKEN": "your_api_token"
  }
}
```

Replace the environment variables with your actual Zendesk credentials.

## Available Tools

* **get_ticket**: Get details of a specific Zendesk ticket
* **create_ticket**: Create a new ticket with subject, description, priority, and tags
* **update_ticket**: Update status, priority, or add comments to existing tickets
* **search_tickets**: Search tickets with custom queries and sorting options
* **get_user**: Get details of a specific Zendesk user
* **add_ticket_comment**: Add public or private comments to tickets

## Available Resources

* **zendesk://tickets**: List of all recent Zendesk tickets
* **zendesk://users**: List of all Zendesk users
* **zendesk://ticket-fields**: List of all ticket fields (default and custom)
* **zendesk://groups**: List of support groups in the Zendesk account

## Available Prompts

* **create_ticket**: Template for creating a new ticket with appropriate details
* **ticket_response**: Template for drafting professional responses to tickets
* **ticket_analysis**: Template for analyzing ticket data and trends

## Example Queries

Once connected to Claude, you can ask questions like:

- "Show me all open tickets with high priority"
- "Create a new ticket for a customer who can't log into their account"
- "Find all tickets submitted by user@example.com"
- "What's the status of ticket #12345?"
- "Add a reply to ticket #12345 explaining how to reset a password"

## Version

0.0.1
