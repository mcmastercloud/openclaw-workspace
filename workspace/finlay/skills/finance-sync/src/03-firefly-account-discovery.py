import os
import sys
import csv

# Path handling for generic wrapper

from dependencies import firefly_api

def main(staging_dir):
    ff_url = os.environ.get('FIREFLY_URL')
    ff_token = os.environ.get('FIREFLY_TOKEN')

    output_path = os.path.join(staging_dir, 'firefly-accounts.txt')
    resp = firefly_api.list_accounts(ff_url, ff_token, type='asset')
    accounts = resp.get('data', [])
    mappings = []
    
    for acc in accounts:
        attrs = acc.get('attributes', {})
        notes = str(attrs.get('notes', ''))
        if 'Starling' in notes:
            # Simple GUID extraction
            import re
            match = re.search(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}", notes.lower())
            if match:
                mappings.append(f"{acc['id']},{attrs['name']},{match.group(0)},{attrs['current_balance']}")

    if mappings:
        with open(output_path, 'w') as f:
            f.write("\n".join(mappings) + "\n")
        print(f"Wrote {len(mappings)} Firefly mappings.")
    else:
        print("Discovery Failed.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 03-firefly-account-discovery.py <staging_dir>")
        sys.exit(1)
    main(sys.argv[1])
