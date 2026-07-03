import os
import json
from dependencies.notion_api import make_request

# Placeholder for Token Retrieval
# Assuming a standard location or environment variable might be set for the migration
token = os.getenv("NOTION_API_TOKEN")
database_id = "383b2203-a808-4eea-9012-8207b5578fa2"

def fetch_diary_entries():
    endpoint = f"databases/{database_id}/query"
    payload = {
        "filter": {
            "property": "Date",
            "date": {
                "on_or_after": "2026-05-22",
                "on_or_before": "2026-05-30"
            }
        }
    }
    return make_request(token, endpoint, method="POST", data=payload)

if __name__ == "__main__":
    result = fetch_diary_entries()
    print(json.dumps(result, indent=2))
