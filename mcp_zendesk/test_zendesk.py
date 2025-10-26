from dotenv import load_dotenv
import os

# Debug: Check current working directory and .env file
print(f"Current working directory: {os.getcwd()}")
print(f".env file exists: {os.path.exists('.env')}")

# Load environment variables BEFORE importing server module
result = load_dotenv(dotenv_path=".env", override=True)
print(f"load_dotenv result: {result}")

# Try alternative paths if .env not found
if not result:
    print("Trying alternative .env paths...")
    alternative_paths = [
        "../.env",
        "../../.env", 
        "/home/ec2-user/zendesk-mcp-server-custom/.env",
        os.path.join(os.path.dirname(__file__), "..", ".env")
    ]
    
    for path in alternative_paths:
        print(f"Trying path: {path}")
        if os.path.exists(path):
            result = load_dotenv(dotenv_path=path, override=True)
            print(f"Found .env at {path}, load result: {result}")
            break

from mcp_zendesk.server import make_zendesk_request, update_ticket, get_ticket_details, get_ticket_comments
from mcp_zendesk.server import get_tickets_details
import asyncio

ZENDESK_BASE_URL = os.environ.get("ZENDESK_BASE_URL")
ZENDESK_EMAIL = os.environ.get("ZENDESK_EMAIL")
ZENDESK_API_TOKEN = os.environ.get("ZENDESK_API_TOKEN")


print("ZENDESK_BASE_URL: ", ZENDESK_BASE_URL)
print("ZENDESK_EMAIL: ", ZENDESK_EMAIL)
print("ZENDESK_API_TOKEN: ", ZENDESK_API_TOKEN)

# Debug: Check if .env file exists and show its contents
env_file_path = ".env"
if os.path.exists(env_file_path):
    print(f"\n.env file contents:")
    try:
        with open(env_file_path, 'r') as f:
            content = f.read()
            print(content)
    except Exception as e:
        print(f"Error reading .env file: {e}")
else:
    print(f"\n.env file not found at {env_file_path}")
    print("Available files in current directory:")
    for file in os.listdir("."):
        print(f"  {file}")

# Test Functions
async def test_get_ticket_fields():
    """Test getting ticket fields and create field mapping"""
    print("Testing: Get Ticket Fields")
    result = await make_zendesk_request("GET", "/api/v2/ticket_fields.json")
    for field in result["ticket_fields"]:
        print(field["title"], ":", field["id"])
    
    field_map = {field["title"]: field["id"] for field in result["ticket_fields"]}
    print("Field Map:", field_map)
    return field_map

async def test_get_many_users():
    """Test getting multiple users by IDs"""
    print("Testing: Get Many Users")
    user_ids = input("Enter user IDs (comma-separated, e.g., 10470154166941,10471965582365): ")
    result = await make_zendesk_request("GET", f"/api/v2/users/show_many.json?ids={user_ids}")
    for user in result["users"]:
        print("---------")
        for field in user:
            print(field, ":", user[field])

async def test_get_tickets_paginated():
    """Test getting tickets with pagination"""
    print("Testing: Get Tickets (Paginated)")
    page = input("Enter page number (default: 3): ") or "3"
    per_page = input("Enter per_page (default: 1000): ") or "1000"
    result = await make_zendesk_request("GET", "/api/v2/tickets", data={"page": int(page), "per_page": int(per_page)})

    print(f"Number of tickets: {len(result['tickets'])}")
    print(f"Next page: {result.get('next_page')}")
    return result["tickets"]

async def test_get_tickets_show_many():
    """Test getting multiple tickets by IDs"""
    print("Testing: Get Tickets (Show Many)")
    ticket_ids = input("Enter ticket IDs (comma-separated, e.g., 49218,49306): ")
    result = await make_zendesk_request("GET", f"/api/v2/tickets/show_many.json?ids={ticket_ids}")
    print(f"Number of tickets: {len(result['tickets'])}")
    for ticket in result["tickets"]:
        for field in ticket:
            print(field, ":", ticket[field])
        print("---------")

async def test_get_custom_statuses():
    """Test getting custom statuses"""
    print("Testing: Get Custom Statuses")
    result = await make_zendesk_request("GET", "/api/v2/custom_statuses.json")
    for custom_status in result["custom_statuses"]:
        for field in custom_status:
            print(field, ":", custom_status[field])
        print("---------")

async def test_update_ticket_status():
    """Test updating ticket custom status"""
    print("Testing: Update Ticket Status")
    ticket_id = input("Enter ticket ID: ")
    status_id = input("Enter custom status ID: ")
    result = await make_zendesk_request("PUT", f"/api/v2/tickets/{ticket_id}.json", {"ticket": {"custom_status_id": status_id}})
    print(result)

async def test_get_tickets_details():
    """Test getting tickets details using server function"""
    print("Testing: Get Tickets Details")
    ticket_ids_input = input("Enter ticket IDs (comma-separated): ")
    ticket_ids = [int(id.strip()) for id in ticket_ids_input.split(",")]
    
    result = await get_tickets_details(ticket_ids)
    print(f"Number of tickets: {len(result)}")

async def test_analyze_ticket_field_types():
    """Test analyzing ticket field types"""
    print("Testing: Analyze Ticket Field Types")
    result = await make_zendesk_request("GET", "/api/v2/ticket_fields.json")
    all_types = []
    for field in result["ticket_fields"]:
        all_types.append(field["type"])
        for key in field:
            print(key, ":", field[key])
        print("---------")
    print("All field types:", set(all_types))

async def test_update_ticket_custom_fields():
    """Test updating ticket custom fields"""
    print("Testing: Update Ticket Custom Fields")
    ticket_id = input("Enter ticket ID: ")
    field_name = input("Enter custom field name: ")
    field_value = input("Enter field value: ")
    result = await update_ticket(ticket_id, custom_fields={field_name: field_value})
    print(result)


async def test_get_ticket_details():
    """Test getting ticket details"""
    print("Testing: Get Ticket Details")
    ticket_id = input("Enter ticket ID: ")
    ticket_data = await get_ticket_details(ticket_id)
    print("Ticket data:", ticket_data)

async def test_get_ticket_comments():
    """Test getting ticket comments"""
    print("Testing: Get Ticket Comments")
    ticket_id = input("Enter ticket ID: ")
    comments = await get_ticket_comments(ticket_id)
    print("Comments:", comments)

async def test_add_ticket_comment():
    """Test adding a comment to a ticket"""
    print("Testing: Add Ticket Comment")
    ticket_id = input("Enter ticket ID: ")
    comment_body = input("Enter comment body: ")
    is_public = input("Is comment public? (y/n): ").lower() == 'y'
    
    ticket_data = {
        "ticket": {
            "comment": {
                "body": comment_body,
                "public": is_public
            }
        }
    }
    result = await make_zendesk_request("PUT", f"/api/v2/tickets/{ticket_id}.json", ticket_data)
    print(result)

async def test_get_users_by_ids():
    """Test getting users by IDs"""
    print("Testing: Get Users by IDs")
    user_ids = input("Enter user IDs (comma-separated): ")
    result = await make_zendesk_request("GET", f"/api/v2/users/show_many.json?ids={user_ids}")
    
    if "error" in result:
        print(f"Error retrieving users: {result.get('message', 'Unknown error')}")
        return
    
    users = result.get("users", [])
    user_summaries = {}
    
    for user in users:
        user_summaries[user.get("id")] = {
            "name": user.get("name"),
            "email": user.get("email"),
            "role": user.get("role")
        }
    print("User summaries:", user_summaries)

async def test_get_ticket_comments_with_authors():
    """Test getting ticket comments with author details"""
    print("Testing: Get Ticket Comments with Authors")
    ticket_id = input("Enter ticket ID: ")
    result = await make_zendesk_request("GET", f"/api/v2/tickets/{ticket_id}/comments.json")
    comments = result.get("comments", [])
    author_ids = [comment.get("author_id") for comment in comments]
    author_ids_str = ",".join(str(author_id) for author_id in author_ids)
    result = await make_zendesk_request("GET", f"/api/v2/users/show_many.json?ids={author_ids_str}")
    users = result.get("users", [])
    user_summaries = {str(user.get("id")): user for user in users}
    for comment in comments:
        author_id = comment.get("author_id")
        print(f"Author ID: {author_id} -> Role: {user_summaries[str(author_id)]['role']}")
        print(comment)
        print("---------")

async def test_update_ticket_with_comment():
    """Test updating ticket with comment"""
    print("Testing: Update Ticket with Comment")
    ticket_id = input("Enter ticket ID: ")
    comment_body = input("Enter comment body: ")
    is_public = input("Is comment public? (y/n): ").lower() == 'y'
    
    ticket_data = {
        "ticket": {
            "comment": {
                "body": comment_body,
                "public": is_public
            }
        }
    }
    output = await make_zendesk_request("PUT", f"/api/v2/tickets/{ticket_id}.json", ticket_data)
    print(output)

async def test_update_ticket_custom_field_by_id():
    """Test updating ticket custom field by field ID"""
    print("Testing: Update Ticket Custom Field by ID")
    # First get field map
    field_map = await test_get_ticket_fields()
    ticket_id = input("Enter ticket ID: ")
    field_name = input("Enter field name (from the field map above): ")
    field_value = input("Enter field value: ")
    
    if field_name in field_map:
        result = await make_zendesk_request("PUT", f"/api/v2/tickets/{ticket_id}.json", {
            "ticket": {
                "custom_fields": [
                    {"id": field_map[field_name], "value": field_value}
                ]
            }
        })
        print(result)
    else:
        print(f"Field '{field_name}' not found in field map")

async def test_get_organizations():
    """Test getting organizations"""
    print("Testing: Get Organizations")
    result = await make_zendesk_request("GET", "/api/v2/organizations.json")
    for org in result["organizations"]:
        for field in org:
            print(field, ":", org[field])
        print("---------")

def display_menu():
    """Display the test menu"""
    print("\n" + "="*50)
    print("ZENDESK MCP SERVER TEST MENU")
    print("="*50)
    print("1.  Get Ticket Fields")
    print("2.  Get Many Users")
    print("3.  Get Tickets (Paginated)")
    print("4.  Get Tickets (Show Many)")
    print("5.  Get Custom Statuses")
    print("6.  Update Ticket Status")
    print("7.  Get Tickets Details")
    print("8.  Analyze Ticket Field Types")
    print("9.  Update Ticket Custom Fields")
    print("11. Get Ticket Details")
    print("12. Get Ticket Comments")
    print("13. Add Ticket Comment")
    print("14. Get Users by IDs")
    print("15. Get Ticket Comments with Authors")
    print("16. Update Ticket with Comment")
    print("17. Update Ticket Custom Field by ID")
    print("18. Get Organizations")
    print("0.  Exit")
    print("="*50)

async def main():
    """Main function with menu system"""
    while True:
        display_menu()
        choice = input("\nPlease choose a test (0-18): ").strip()
        
        if choice == "0":
            print("Exiting...")
            break
        elif choice == "1":
            await test_get_ticket_fields()
        elif choice == "2":
            await test_get_many_users()
        elif choice == "3":
            await test_get_tickets_paginated()
        elif choice == "4":
            await test_get_tickets_show_many()
        elif choice == "5":
            await test_get_custom_statuses()
        elif choice == "6":
            await test_update_ticket_status()
        elif choice == "7":
            await test_get_tickets_details()
        elif choice == "8":
            await test_analyze_ticket_field_types()
        elif choice == "9":
            await test_update_ticket_custom_fields()

        elif choice == "11":
            await test_get_ticket_details()
        elif choice == "12":
            await test_get_ticket_comments()
        elif choice == "13":
            await test_add_ticket_comment()
        elif choice == "14":
            await test_get_users_by_ids()
        elif choice == "15":
            await test_get_ticket_comments_with_authors()
        elif choice == "16":
            await test_update_ticket_with_comment()
        elif choice == "17":
            await test_update_ticket_custom_field_by_id()
        elif choice == "18":
            await test_get_organizations()
        else:
            print("Invalid choice. Please try again.")
        
        input("\nPress Enter to continue...")


if __name__ == "__main__":
    asyncio.run(main())
