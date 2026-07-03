import os
import sys
import json
from datetime import datetime
from dependencies import notion_api, ghostfolio_api

# McMaster Finance System: Step 12 - Notion Net Worth Update
# Purpose: Pushes the consolidated Net Worth figure from Ghostfolio to Notion.

def main(staging_dir):
    if not staging_dir:
        print("Error: Staging directory not provided.")
        sys.exit(1)

    gf_url = os.environ.get('GHOSTFOLIO_URL')
    gf_token = os.environ.get('GHOSTFOLIO_API_TOKEN')
    notion_token = os.environ.get('NOTION_API_TOKEN')
    # Notion Callout Block ID identified within children of page
    callout_block_id = "3476a781-d358-814f-94be-fe22018be9b3"

    if not all([gf_url, gf_token, notion_token]):
        print("Error: Missing API configuration for Ghostfolio or Notion.")
        sys.exit(1)

    print("Initiating Notion Net Worth Update...")

    # 1. Fetch Total Net Worth from Ghostfolio
    gf_data = ghostfolio_api.get_accounts(gf_url, gf_token)
    if "error" in gf_data:
        print(f"Error fetching Ghostfolio data: {gf_data['error']}")
        sys.exit(1)

    total_net_worth = gf_data.get('totalValueInBaseCurrency', 0)
    formatted_total = f"£{total_net_worth:,.2f}"

    print(f"Consolidated Net Worth from Ghostfolio: {formatted_total}")

    # 2. Update Notion Callout Block
    # Payload for updating a callout block text
    payload = {
        "callout": {
            "rich_text": [
                {
                    "type": "text",
                    "text": {
                        "content": f"Total Net Worth: {formatted_total} (Updated: {datetime.now().strftime('%d %b %Y %H:%M')})"
                    },
                    "annotations": {
                        "bold": True
                    }
                }
            ]
        }
    }

    print(f"Updating Notion Block {callout_block_id}...")
    res = notion_api.update_block(notion_token, callout_block_id, payload)
    
    if "error" in res:
        print(f"Error updating Notion: {res['error']}")
        sys.exit(1)

    print("Notion Update Successfully Completed.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 12-notion-net-worth-update.py <staging_dir>")
        sys.exit(1)
    main(sys.argv[1])
