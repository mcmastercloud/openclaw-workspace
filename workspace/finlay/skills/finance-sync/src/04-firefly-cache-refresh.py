import os
import json
import sys
import time
from datetime import datetime, timedelta

# McMaster Finance System: Step 04 - Firefly Cache Refresh (REVISED for Signage)
# This script downloads all transactions for matched asset accounts to provide a reconciliation base.
# It now correctly captures the transaction 'type' to ensure proper balance summation.

# Path handling for generic wrapper

from dependencies import firefly_api

def get_start_date(base_staging_dir, buffer_days=35):
    last_sync_path = os.path.join(base_staging_dir, 'LAST_SYNC_SUCCESS.txt')
    if os.path.exists(last_sync_path):
        try:
            with open(last_sync_path, 'r') as f:
                date_str = f.read().strip()
                # Handle both full ISO format and simple date format
                try:
                    last_date = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ')
                except ValueError:
                    last_date = datetime.strptime(date_str, '%Y-%m-%d')
                start_date = last_date - timedelta(days=buffer_days)
                return start_date.strftime('%Y-%m-%d')
        except Exception as e:
            print(f"Warning: Failed to parse LAST_SYNC_SUCCESS.txt: {e}")
    
    return '2020-01-01'

def main(staging_dir):
    if not staging_dir:
        print("Error: Staging directory not provided.")
        sys.exit(1)
    ff_url = os.environ.get('FIREFLY_URL')
    ff_token = os.environ.get('FIREFLY_TOKEN')

    if not all([staging_dir, ff_url, ff_token]):
        print("Error: FINANCE_STAGING_DIR, FIREFLY_URL, or FIREFLY_TOKEN not set.")
        sys.exit(1)

    ff_accounts_file = os.path.join(staging_dir, 'firefly-accounts.txt')
    if not os.path.exists(ff_accounts_file):
        print("Error: firefly-accounts.txt not found. Run Step 03 first.")
        sys.exit(1)

    # Dynamic Anchor Date
    base_staging = os.path.abspath(os.path.join(staging_dir, ".."))
    start_date = get_start_date(base_staging)
    
    # Use Tomorrow as the end date for safety (Belfast Timezone Alignment)
    # This ensures items posted just after midnight in the UK are included.
    from datetime import timedelta
    end_date = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
    print(f"Filtering Firefly transactions: {start_date} to {end_date}")

    with open(ff_accounts_file, 'r') as f:
        for line in f:
            parts = line.strip().split(',')
            if len(parts) < 3: continue
            ff_id, ff_name, s_guid = parts[0], parts[1], parts[2]
            
            print(f"Refreshing Firefly cache for {ff_name}...")
            all_txs = []
            page = 1
            while True:
                # Using both start and end to satisfy API range requirements
                resp = firefly_api.make_request(ff_url, ff_token, f"accounts/{ff_id}/transactions?page={page}&start={start_date}&end={end_date}")
                
                if "error" in resp:
                    print(f"   Error on page {page} for {ff_name}: {resp['error']}")
                    break
                    
                data = resp.get('data', [])
                if not data: break
                
                for group in data:
                    group_id = group.get('id')
                    for split in group.get('attributes', {}).get('transactions', []):
                        # Filter strictly for the leg belonging to THIS asset account
                        # A group/journal has multiple legs. We only care about the one matching ff_id.
                        if split.get('source_id') == ff_id or split.get('destination_id') == ff_id:
                            all_txs.append({
                                "firefly_transaction_id": group_id,
                                "amount": split.get('amount'),
                                "date": split.get('date'),
                                "external_id": split.get('external_id'),
                                "description": split.get('description'),
                                "type": split.get('type'),
                                "source_id": split.get('source_id'),
                                "destination_id": split.get('destination_id')
                            })
                
                total_pages = resp.get('meta', {}).get('pagination', {}).get('total_pages', 1)
                if page >= total_pages: break
                page += 1
            
            output_file = os.path.join(staging_dir, f"{s_guid}-Firefly.txt")
            with open(output_file, 'w') as out:
                json.dump(all_txs, out, indent=2)
            print(f"   Saved {len(all_txs)} transactions.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 04-firefly-cache-refresh.py <staging_dir>")
        sys.exit(1)
    main(sys.argv[1])
