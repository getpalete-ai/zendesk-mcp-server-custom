# server.py
import sys
import os
import json
from typing import Dict, List, Optional, Any, Union
import httpx
from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("Zendesk MCP")

# Environment variables for Zendesk configuration
ZENDESK_BASE_URL = os.environ.get("ZENDESK_BASE_URL")
ZENDESK_EMAIL = os.environ.get("ZENDESK_EMAIL")
ZENDESK_API_TOKEN = os.environ.get("ZENDESK_API_TOKEN")

# Check if environment variables are set
if not all([ZENDESK_BASE_URL, ZENDESK_EMAIL, ZENDESK_API_TOKEN]):
    print("Warning: Zendesk environment variables not fully configured. Set ZENDESK_BASE_URL, ZENDESK_EMAIL and ZENDESK_API_TOKEN.", file=sys.stderr)

# Helper function for API requests
async def make_zendesk_request(method: str, endpoint: str, data: Dict = None) -> Dict:
    """
    Make a request to the Zendesk API.
    
    Args:
        method: HTTP method (GET, POST, PUT, DELETE)
        endpoint: API endpoint (without base URL)
        data: Data to send (for POST/PUT)
    
    Returns:
        Response from Zendesk API as dictionary
    """
    url = f"{ZENDESK_BASE_URL}{endpoint}"
    auth = (f"{ZENDESK_EMAIL}/token", ZENDESK_API_TOKEN)
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    async with httpx.AsyncClient() as client:
        try:
            if method.upper() == "GET":
                response = await client.get(url, auth=auth, headers=headers)
            elif method.upper() == "POST":
                response = await client.post(url, auth=auth, headers=headers, json=data)
            elif method.upper() == "PUT":
                response = await client.put(url, auth=auth, headers=headers, json=data)
            elif method.upper() == "DELETE":
                response = await client.delete(url, auth=auth, headers=headers)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            error_message = f"HTTP Status Error: {e.response.status_code}"
            try:
                error_data = e.response.json()
                error_message = f"{error_message} - {json.dumps(error_data)}"
            except:
                error_message = f"{error_message} - {e.response.text}"
            
            return {
                "error": True,
                "status_code": e.response.status_code,
                "message": error_message
            }
        except Exception as e:
            return {
                "error": True,
                "message": str(e)
            }



# === TOOLS ===

@mcp.tool()
async def get_ticket_comments(ticket_id: str) -> list[Dict]:
    """
    Get comments of a specific Zendesk ticket.
    """
    result = await make_zendesk_request("GET", f"/api/v2/tickets/{ticket_id}/comments.json")
    
    if "error" in result:
        return f"Error retrieving ticket comments: {result.get('message', 'Unknown error')}"
    
    # Format the ticket comments in a readable way
    comments = result.get("comments", [])
    for comment in comments:
        print("---------")
        for field in comment:
            print(field,":",comment[field])
    return comments


@mcp.tool()
async def get_users(user_ids: list) -> dict:
    """
    Get details of a specific Zendesk user.
    user_ids: List of user IDs
    """
    user_ids_str = ",".join(str(user_id) for user_id in user_ids)
    result = await make_zendesk_request("GET", f"/api/v2/users/show_many.json?ids={user_ids_str}")
    users:List[Dict] = result.get("users", [])
    for user in users:
        print("---------")
        for field in user:
            print(field,":",user[field])
    
    dict_users = {user.pop("id"): user for user in users}
    return dict_users


@mcp.tool()
async def get_ticket_details(ticket_id: str) -> dict:
    """
    Get details of a specific Zendesk ticket.
    
    Args:
        ticket_id: The Zendesk ticket ID
    """
    result = await make_zendesk_request("GET", f"/api/v2/tickets/{ticket_id}.json")
    
    if "error" in result:
        return f"Error retrieving ticket: {result.get('message', 'Unknown error')}"
    
    # Format the ticket in a readable way
    ticket = result.get("ticket", {})
    # fields_to_expose=["id",
    #                   "subject",
    #                   "description",
    #                   "status",
    #                   "priority",
    #                   "requester_id",
    #                   "assignee_id",
    #                   "created_at",
    #                   "updated_at",
    #                   "tags"]
    # fields_if_non_null=["external_id","due_at","custom_fields"]
    # output_str=''
    # for field in fields_to_expose:
    #     if field in ticket:
    #         output_str += f"{field}: {ticket[field]} \n"
    # for field in fields_if_non_null:
    #     if field in ticket and ticket[field] is not None:
    #         output_str += f"{field}: {ticket[field]} \n"

    # formatted_ticket = {
    #     "id": ticket.get("id"),
    #     "subject": ticket.get("subject"),
    #     "description": ticket.get("description"),
    #     "status": ticket.get("status"),
    #     "priority": ticket.get("priority"),
    #     "requester_id": ticket.get("requester_id"),
    #     "assignee_id": ticket.get("assignee_id"),
    #     "created_at": ticket.get("created_at"),
    #     "updated_at": ticket.get("updated_at"),
    #     "tags": ticket.get("tags", [])
    # }
    return ticket

@mcp.tool()
async def create_ticket(subject: str, description: str, priority: Optional[str] = None, 
                       tags: Optional[str] = None) -> str:
    """
    Create a new ticket in Zendesk.
    
    Args:
        subject: Subject line for the ticket
        description: Detailed description of the issue
        priority: Ticket priority (low, normal, high, urgent)
        tags: Comma-separated list of tags
    """
    # Prepare the ticket data
    ticket_data = {
        "ticket": {
            "subject": subject,
            "comment": {"body": description},
            "priority": priority if priority else "normal"
        }
    }
    
    # Add tags if provided
    if tags:
        ticket_data["ticket"]["tags"] = [tag.strip() for tag in tags.split(",")]
    
    result = await make_zendesk_request("POST", "/api/v2/tickets.json", ticket_data)
    
    if "error" in result:
        return f"Error creating ticket: {result.get('message', 'Unknown error')}"
    
    ticket = result.get("ticket", {})
    return f"Ticket created successfully! Ticket ID: {ticket.get('id')}, Subject: '{ticket.get('subject')}'"

@mcp.tool()
async def get_tickets_fields_map() -> dict:
    """
    Get a list of ticket fields in the Zendesk account.
    """
    result = await make_zendesk_request("GET", "/api/v2/ticket_fields.json")
    for field in result["ticket_fields"]:
        print(field["title"],":",field["id"])
    field_map={field["id"]:field["title"] for field in result["ticket_fields"]}
    return field_map

@mcp.tool()
async def update_ticket(ticket_id: int, status: Optional[str] = None, 
                       priority: Optional[str] = None, comment: Optional[dict] = None) -> str:
    """
    Update an existing Zendesk ticket.
    
    Args:
        ticket_id: The ID of the ticket to update
        status: New status (open, pending, solved, closed)
        priority: New priority (low, normal, high, urgent)
        comment: Comment to add to the ticket in a dictionary format, such as {"body": "comment", "public": true/false}
        tags: 
    """
    # Prepare the update data
    ticket_data = {"ticket": {}}
    
    if status:
        ticket_data["ticket"]["status"] = status
    if priority:
        ticket_data["ticket"]["priority"] = priority
    if comment:
        ticket_data["ticket"]["comment"] = comment
    
    
    # Only proceed if we have something to update
    if not any([status, priority, comment]):
        return "No update parameters provided. Ticket remains unchanged."
    
    result = await make_zendesk_request("PUT", f"/api/v2/tickets/{ticket_id}.json", ticket_data)
    
    if "error" in result:
        return f"Error updating ticket: {result.get('message', 'Unknown error')}"
    
    return f"Ticket {ticket_id} updated successfully!"

@mcp.tool()
async def search_tickets(query: str, sort_by: Optional[str] = "created_at", 
                        sort_order: Optional[str] = "desc") -> str:
    """
    Search for Zendesk tickets using a query string.
    
    Args:
        query: Search query string (e.g., "status:open priority:high")
        sort_by: Field to sort by (created_at, updated_at, priority, status)
        sort_order: Sort order (asc, desc)
    """
    # URL encode the query parameter
    import urllib.parse
    encoded_query = urllib.parse.quote(query)
    
    result = await make_zendesk_request(
        "GET", 
        f"/api/v2/search.json?query={encoded_query}&sort_by={sort_by}&sort_order={sort_order}"
    )
    
    if "error" in result:
        return f"Error searching tickets: {result.get('message', 'Unknown error')}"
    
    # Format results in a readable way
    tickets = result.get("results", [])
    if not tickets:
        return "No tickets found matching your query."
    
    ticket_summaries = []
    for ticket in tickets:
        if ticket.get("type") != "ticket":
            continue
            
        ticket_summaries.append({
            "id": ticket.get("id"),
            "subject": ticket.get("subject"),
            "status": ticket.get("status"),
            "priority": ticket.get("priority"),
            "created_at": ticket.get("created_at")
        })
    
    summary = f"Found {len(ticket_summaries)} tickets:\n\n"
    summary += json.dumps(ticket_summaries, indent=2)
    return summary

@mcp.tool()
async def get_user(user_id: int) -> str:
    """
    Get details of a specific Zendesk user.
    
    Args:
        user_id: The Zendesk user ID
    """
    result = await make_zendesk_request("GET", f"/api/v2/users/{user_id}.json")
    
    if "error" in result:
        return f"Error retrieving user: {result.get('message', 'Unknown error')}"
    
    # Format the user in a readable way
    user = result.get("user", {})
    formatted_user = {
        "id": user.get("id"),
        "name": user.get("name"),
        "email": user.get("email"),
        "phone": user.get("phone"),
        "role": user.get("role"),
        "created_at": user.get("created_at"),
        "time_zone": user.get("time_zone"),
        "tags": user.get("tags", [])
    }
    return json.dumps(formatted_user, indent=2)

@mcp.tool()
async def add_ticket_comment(ticket_id: int, comment: str, public: bool = True) -> str:
    """
    Add a comment to an existing Zendesk ticket.
    
    Args:
        ticket_id: The ID of the ticket to comment on
        comment: The comment text to add
        public: Whether the comment should be public (visible to requesters)
    """
    ticket_data = {
        "ticket": {
            "comment": {
                "body": comment,
                "public": public
            }
        }
    }
    
    result = await make_zendesk_request("PUT", f"/api/v2/tickets/{ticket_id}.json", ticket_data)
    
    if "error" in result:
        return f"Error adding comment: {result.get('message', 'Unknown error')}"
    
    status = "public" if public else "private"
    return f"Added {status} comment to ticket {ticket_id} successfully!"



# === RESOURCES ===

@mcp.resource("zendesk://tickets")
async def get_tickets() -> str:
    """Get a list of recent Zendesk tickets."""
    result = await make_zendesk_request("GET", "/api/v2/tickets.json")
    
    if "error" in result:
        return f"Error retrieving tickets: {result.get('message', 'Unknown error')}"
    
    # Format the tickets in a readable way
    tickets = result.get("tickets", [])
    ticket_summaries = []
    
    for ticket in tickets:
        ticket_summaries.append({
            "id": ticket.get("id"),
            "subject": ticket.get("subject"),
            "status": ticket.get("status"),
            "priority": ticket.get("priority"),
            "created_at": ticket.get("created_at")
        })
    
    return json.dumps(ticket_summaries, indent=2)

@mcp.resource("zendesk://users")
async def get_users() -> str:
    """Get a list of Zendesk users."""
    result = await make_zendesk_request("GET", "/api/v2/users.json")
    
    if "error" in result:
        return f"Error retrieving users: {result.get('message', 'Unknown error')}"
    
    # Format the users in a readable way
    users = result.get("users", [])
    user_summaries = []
    
    for user in users:
        user_summaries.append({
            "id": user.get("id"),
            "name": user.get("name"),
            "email": user.get("email"),
            "role": user.get("role")
        })
    
    return json.dumps(user_summaries, indent=2)

@mcp.resource("zendesk://ticket-fields")
async def get_ticket_fields() -> list[Dict]:
    """Get a list of ticket fields in the Zendesk account."""
    result = await make_zendesk_request("GET", "/api/v2/ticket_fields.json")
    
    if "error" in result:
        return f"Error retrieving ticket fields: {result.get('message', 'Unknown error')}"
    
    # Format the ticket fields in a readable way
    fields = result.get("ticket_fields", [])
    field_summaries = []
    
    for field in fields:
        field_summaries.append({
            "id": field.get("id"),
            "title": field.get("title"),
            "type": field.get("type"),
            "description": field.get("description"),
            "required": field.get("required"),
            "custom_field": field.get("custom_field", False)
        })
    
    return field_summaries

@mcp.resource("zendesk://groups")
async def get_groups() -> str:
    """Get a list of groups in the Zendesk account."""
    result = await make_zendesk_request("GET", "/api/v2/groups.json")
    
    if "error" in result:
        return f"Error retrieving groups: {result.get('message', 'Unknown error')}"
    
    # Format the groups in a readable way
    groups = result.get("groups", [])
    group_summaries = []
    
    for group in groups:
        group_summaries.append({
            "id": group.get("id"),
            "name": group.get("name"),
            "description": group.get("description"),
            "created_at": group.get("created_at")
        })
    
    return json.dumps(group_summaries, indent=2)

# === PROMPTS ===

@mcp.prompt("create_ticket")
def create_ticket_prompt(subject: str = None, description: str = None, priority: str = None) -> str:
    """
    A prompt template for creating a new ticket in Zendesk.
    
    Args:
        subject: Subject line for the ticket
        description: Detailed description of the issue
        priority: Ticket priority (low, normal, high, urgent)
    """
    if all([subject, description]):
        priority_text = f", priority: {priority}" if priority else ""
        return f"Please help me create a new Zendesk ticket with these details:\n\nSubject: {subject}\nDescription: {description}{priority_text}\n\nCan you also suggest any tags that might be relevant for this ticket?"
    else:
        return "I need to create a new support ticket in Zendesk. Please help me with the required details and best practices for writing effective ticket subjects and descriptions."

@mcp.prompt("ticket_response")
def ticket_response_prompt(ticket_id: str = None, summary: str = None) -> str:
    """
    A prompt template for drafting a response to a support ticket.
    
    Args:
        ticket_id: ID of the ticket being responded to
        summary: Brief summary of the issue
    """
    if all([ticket_id, summary]):
        return f"Please help me draft a professional and helpful response to Zendesk ticket #{ticket_id}. The customer issue is: {summary}\n\nDraft a response that is empathetic, clear, and provides actionable next steps."
    else:
        return "I need to respond to a support ticket in Zendesk. Can you help me draft a professional, empathetic response that follows best practices for customer support communication?"

@mcp.prompt("ticket_analysis")
def ticket_analysis_prompt() -> str:
    """A prompt template for analyzing ticket data and trends."""
    return "I'd like to analyze our Zendesk ticket data to identify trends and areas for improvement. Can you help me understand what metrics and patterns to look for, and how to interpret the results to improve our customer support process?"
if __name__ == "__main__":
    print("Starting Zendesk MCP server...", file=sys.stderr)
    mcp.run()
