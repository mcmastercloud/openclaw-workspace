import os
import json
import sys

# Add scripts directory to path to import firefly_api
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'scripts'))
import firefly_api

def extract_firefly_accounts():
    """
    Fetches asset accounts from Firefly III and extracts Starling GUIDs from the notes.
    Saves the mapping to firefly-accounts.txt in the staging directory.
    """
    staging_dir = os.environ.get('FINANCE_STAGING_DIR')
    if not staging_dir:
        print("Error: FINANCE_STAGING_DIR environment variable not set.")
        sys.exit(1)

    output_path = os.path.join(staging_dir, 'firefly-accounts.txt')
    
    print(f"Fetching asset accounts from Firefly III...")
    # list_accounts returns the 'data' field from the response
    base_url = os.environ.get('FIREFLY_URL')
    token = os.environ.get('FIREFLY_TOKEN')
    response = firefly_api.list_accounts(base_url, token, type='asset')
    
    if 'error' in response:
        print(f"Error fetching accounts: {response['error']}")
        sys.exit(1)
        
    accounts = response.get('data', [])
    mappings = []
    
    import re
    uuid_pattern = re.compile(r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}')

    for acc in accounts:
        attributes = acc.get('attributes', {})
        name = attributes.get('name')
        account_id = acc.get('id')
        current_balance = attributes.get('current_balance', '0.00')
        notes = attributes.get('notes', '')
        
        if not notes:
            continue

        # Look for a UUID in the notes field
        match = uuid_pattern.search(notes.lower())
        if match:
            starling_guid = match.group(0)
            mappings.append(f"{account_id},{name},{starling_guid},{current_balance}")
    
    if mappings:
        with open(output_path, 'w') as f:
            f.write("\n".join(mappings) + "\n")
        print(f"Successfully wrote {len(mappings)} mappings to {output_path}")
    else:
        print("No accounts with Starling GUIDs found in Firefly III notes.")

if __name__ == "__main__":
    extract_firefly_accounts()
