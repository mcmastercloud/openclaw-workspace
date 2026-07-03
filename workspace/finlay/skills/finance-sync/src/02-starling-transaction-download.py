import os
import sys
import json
import csv
from datetime import datetime, timedelta

# McMaster Finance System: Step 02 - Starling Transaction Download
# This script downloads SETTLED transaction history for all discovered accounts and spaces.

# Path handling for generic wrapper

from dependencies import starling_api

def get_start_date(base_staging_dir, buffer_days=7):
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
                return start_date.strftime('%Y-%m-%dT00:00:00Z')
        except Exception as e:
            print(f"Warning: Failed to parse LAST_SYNC_SUCCESS.txt: {e}")
    
    return '2020-01-01T00:00:00Z'

def main(staging_dir):
    accounts_file = os.path.join(staging_dir, 'starling-accounts.txt')
    if not os.path.exists(accounts_file):
        print("Error: starling-accounts.txt not found. Run Step 01 first.")
        sys.exit(1)

    # Identification logic for current run staging directory
    base_staging = os.path.abspath(os.path.join(staging_dir, ".."))
    start_date = get_start_date(base_staging)
    print(f"Filtering Starling transactions since: {start_date}")

    # 1. Clean existing Starling history
    print(f"Cleaning existing Starling history in {staging_dir}...")
    import glob
    for f in glob.glob(os.path.join(staging_dir, "*-Starling.txt")):
        os.remove(f)

    space_pending_offsets = {}

    with open(accounts_file, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if not row: continue
            # Format: slug, uid, name, effective, cat_uid, cleared, parent_uid
            slug, uid, name, _, cat_uid, _, parent_uid = row
            
            token_prefix = slug.split(':')[0].upper()
            if token_prefix == 'PERSONAL': env_key = 'STARLING_CURRENT_ACCOUNT_TOKEN'
            elif token_prefix == 'JOINT': env_key = 'STARLING_JOINT_ACCOUNT_TOKEN'
            elif token_prefix == 'BUSINESS': env_key = 'STARLING_BUSINESS_ACCOUNT_TOKEN'
            else: continue
            
            token = os.getenv(env_key)
            if not token:
                print(f"Warning: No token for {name}. skipping.")
                continue

            print(f"Downloading history for {name}...")
            
            # Identify the correct feed fetch strategy
            fetch_uid = uid if parent_uid else cat_uid
            fetch_account = parent_uid if parent_uid else uid
            
            if not fetch_uid:
                print(f"Skipping {name} (Missing category/goal UID)")
                continue

            # Fetch the feed
            raw_data = starling_api.list_transactions(token, fetch_account, fetch_uid, start_date=start_date)
            all_items = raw_data.get('feedItems', [])
            
            relevant_items = []
            pending_total_minor = 0
            for item in all_items:
                status = item.get('status')
                if status == 'SETTLED':
                    relevant_items.append(item)
                elif status == 'PENDING':
                    # Capture pending amount to offset Space balances (2026-06-03 fix)
                    minor = item.get('amount', {}).get('minorUnits', 0)
                    direction = item.get('direction')
                    if direction == 'OUT':
                        pending_total_minor -= minor
                    else:
                        pending_total_minor += minor
            
            if parent_uid and pending_total_minor != 0:
                space_pending_offsets[uid] = pending_total_minor / 100.0
            
            output_file = os.path.join(staging_dir, f"{uid}-Starling.txt")
            with open(output_file, 'w') as out:
                json.dump(relevant_items, out, indent=2)
                
            print(f"   Done. {len(relevant_items)} items saved")

    # Save offsets for Step 07
    with open(os.path.join(staging_dir, 'space-pending-offsets.json'), 'w') as f:
        json.dump(space_pending_offsets, f)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 02-starling-transaction-download.py <staging_dir>")
        sys.exit(1)
    main(sys.argv[1])
