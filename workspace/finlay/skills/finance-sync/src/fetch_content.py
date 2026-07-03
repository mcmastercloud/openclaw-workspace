import os
import json
import sys
from dependencies.notion_api import make_request

# Use environment variable for token
token = os.getenv("NOTION_API_TOKEN")
database_id = "383b2203-a808-4eea-9012-8207b5578fa2"

def fetch_page_content(page_id):
    endpoint = f"blocks/{page_id}/children"
    return make_request(token, endpoint, method="GET")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 fetch_content.py <page_id>")
        sys.exit(1)
    page_id = sys.argv[1]
    result = fetch_page_content(page_id)
    print(json.dumps(result, indent=2))
