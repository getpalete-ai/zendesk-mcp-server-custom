from dotenv import load_dotenv
import os

# Load environment variables BEFORE importing server module
load_dotenv(dotenv_path=".env", override=True)

from server import make_zendesk_request
import asyncio

ZENDESK_BASE_URL = os.environ.get("ZENDESK_BASE_URL")
ZENDESK_EMAIL = os.environ.get("ZENDESK_EMAIL")
ZENDESK_API_TOKEN = os.environ.get("ZENDESK_API_TOKEN")


print("ZENDESK_BASE_URL: ", ZENDESK_BASE_URL)
print("ZENDESK_EMAIL: ", ZENDESK_EMAIL)
print("ZENDESK_API_TOKEN: ", ZENDESK_API_TOKEN)

async def main():
    # result = await make_zendesk_request("GET", "/api/v2/ticket_fields.json")
    # for field in result["ticket_fields"]:
    #     print(field["title"],":",field["id"])

    # field_map={field["title"]: field["id"] for field in result["ticket_fields"]}

    # result = await make_zendesk_request("GET", "/api/v2/users/show_many.json?ids=10470154166941,30475703687709")
    # for user in result["users"]:
    #     print("---------")
    #     for field in user:
    #         print(field,":",user[field])

    # input("Press Enter to continue...")

    # print("---------")
    # result = await make_zendesk_request("GET", "/api/v2/tickets/48935.json")
    # for field in result["ticket"]:
    #     print(field,":",result["ticket"][field])
    
    # ticket_data = {
    #     "ticket": {
    #         "comment": {
    #             "body": "test of reply to ticket",
    #             "public": True
    #         }
    #     }
    # }
    print("---------")
    result = await make_zendesk_request("GET", "/api/v2/tickets/48935/comments.json")
    comments = result.get("comments", [])
    for comment in comments:
        print("---------")
        for field in comment:
            print(field,":",comment[field])
    # output = await make_zendesk_request("PUT", "/api/v2/tickets/48935.json", ticket_data)
    # print(output)

    # result = await make_zendesk_request("PUT", "/api/v2/tickets/3d.json", {"ticket": {"custom_fields": [
    #   {"id": field_map["Merchant Name"], "value": "test_Merchant"}]}})
    # for ticket in result["tickets"]:
        


if __name__ == "__main__":
    asyncio.run(main())
