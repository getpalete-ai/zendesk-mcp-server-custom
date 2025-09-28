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

from server import make_zendesk_request
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

async def main():
    result = await make_zendesk_request("GET", "/api/v2/ticket_fields.json")
    # for field in result["ticket_fields"]:
    #     print(field["title"],":",field["id"])
    print(result)
    # field_map={field["title"]: field["id"] for field in result["ticket_fields"]}
    # print(field_map)

    # result = await make_zendesk_request("GET", "/api/v2/users/show_many.json?ids=10470154166941,10471965582365")
    # for user in result["users"]:
    #     print("---------")
    #     for field in user:
    #         print(field,":",user[field])

    # input("Press Enter to continue...")

    print("---------")
    result = await make_zendesk_request("GET", "/api/v2/tickets/49306.json")
    for field in result["ticket"]:
        print(field,":",result["ticket"][field])
    
    # ticket_data = {
    #     "ticket": {
    #         "comment": {
    #             "body": "test of reply to ticket",
    #             "public": True
    #         }
    #     }
    # # }
    # result = await make_zendesk_request("GET", "/api/v2/users.json?ids=")
    
    # if "error" in result:
    #     return f"Error retrieving users: {result.get('message', 'Unknown error')}"
    
    # # Format the users in a readable way
    # users = result.get("users", [])
    # user_summaries = {}
    
    # for user in users:
    #     user_summaries[user.get("id")] = {
    #         "name": user.get("name"),
    #         "email": user.get("email"),
    #         "role": user.get("role")
    #     }
    # print(user_summaries)
    # print("---------")
    # result = await make_zendesk_request("GET", "/api/v2/tickets/49218/comments.json")
    # comments = result.get("comments", [])
    # author_ids = [comment.get("author_id") for comment in comments]
    # author_ids_str = ",".join(str(author_id) for author_id in author_ids)
    # result = await make_zendesk_request("GET", f"/api/v2/users/show_many.json?ids={author_ids_str}")
    # users = result.get("users", [])
    # user_summaries = {str(user.get("id")): user for user in users}
    # for comment in comments:
    #     author_id = comment.get("author_id")
    #     print(author_id,"--->",user_summaries[str(author_id)]["role"],"--->")
    #     print(comment)
    #     print("---------")
    # output = await make_zendesk_request("PUT", "/api/v2/tickets/48935.json", ticket_data)
    # print(output)

    # result = await make_zendesk_request("PUT", "/api/v2/tickets/3d.json", {"ticket": {"custom_fields": [
    #   {"id": field_map["Merchant Name"], "value": "test_Merchant"}]}})
    # for ticket in result["tickets"]:
        

    # result= await make_zendesk_request("GET", "/api/v2/organizations.json")
    # for org in result["organizations"]:
    #     for field in org:
    #         print(field,":",org[field])
    #     print("---------")


if __name__ == "__main__":
    asyncio.run(main())
