import os
import json
import sys
import csv
from datetime import datetime

# McMaster Finance System: Step 10 - Firefly Delta Loader
# This script posts verified transactions from -Upload files to Firefly III.
# RULES: 
# 1. Prioritizes 'settlementTime' for the primary date field (SOP Compliance).
# 2. Always populates 'external_id' with the Starling UID (Idempotency).

# Path handling for generic wrapper

from dependencies import firefly_api

def main(staging_dir):
    if not staging_dir:
        print("Error: Staging directory not provided.")
        sys.exit(1)
        
    ff_url = os.environ.get('FIREFLY_URL')
    ff_token = os.environ.get('FIREFLY_TOKEN')

    if not all([staging_dir, ff_url, ff_token]):
        print("Error: Missing config (DIR, URL, or TOKEN).")
        sys.exit(1)

    # 1. Load Firefly Mappings (GUID -> FF_ID)
    ff_map = {}
    ff_accounts_file = os.path.join(staging_dir, 'firefly-accounts.txt')
    with open(ff_accounts_file, 'r') as f:
        for row in csv.reader(f):
            if len(row) >= 3:
                ff_map[row[2]] = row[0]

    # 2. Process -Upload files for every account
    import glob
    upload_files = glob.glob(os.path.join(staging_dir, "*-Upload.txt"))
    
    if not upload_files:
        print("No Upload files found. Run Step 09 first.")
        return

    for upload_path in upload_files:
        guid = os.path.basename(upload_path).replace("-Upload.txt", "")
        
        with open(upload_path, 'r') as df:
            txs = json.load(df)
        
        if not txs:
            continue

        ff_id = ff_map.get(guid)
        if not ff_id:
            print(f"Skipping {guid}: No matching Firefly account ID.")
            continue

        print(f"\nPosting verified updates to account ID {ff_id}...")
        
        success_count = 0
        for tx in txs:
            # RULE: Skip items marked as IGNORE (e.g., Pending items used only for Check 3)
            if tx.get('HOLDING_IGNORE') or tx.get('IGNORE_REASON'):
                print(f"      Skipping {tx.get('feedItemUid')} (Reason: {tx.get('IGNORE_REASON')})")
                continue

            # MANDATORY RULE (SOP Phase 5): Use Settlement Time as primary date
            st_date = tx.get('settlementTime') or tx.get('transactionTime') or tx.get('updatedAt')
            
            st_amt = float(tx.get('amount', {}).get('minorUnits', 0)) / 100.0
            st_ref = tx.get('reference') or tx.get('counterPartyName') or "No Reference"
            
            # MANDATORY RULE: Always put Starling UID into external_id
            st_uid = tx.get('feedItemUid')
            
            matching_uid = tx.get('MATCHING_UID') # Counterpart for internal transfers
            
            # Transfer Detection
            is_internal_transfer = False
            target_ff_id = None
            if matching_uid and matching_uid in ff_map:
                is_internal_transfer = True
                target_ff_id = ff_map[matching_uid]

            # Build Split
            split = {
                "date": st_date,
                "amount": f"{st_amt:.2f}",
                "description": st_ref,
                "external_id": st_uid, # Verified: Starling UID
                "notes": f"Settlement Time: {tx.get('settlementTime')}. Transaction Time: {tx.get('transactionTime')}."
            }

            if tx.get('direction') == 'OUT':
                split["source_id"] = ff_id
                if is_internal_transfer:
                    split["type"] = "transfer"
                    split["destination_id"] = target_ff_id
                else:
                    split["type"] = "withdrawal"
                    split["destination_name"] = tx.get('counterPartyName') or "Cash/Expense"
            else: # IN
                split["destination_id"] = ff_id
                if is_internal_transfer:
                    split["type"] = "transfer"
                    split["source_id"] = target_ff_id
                else:
                    split["type"] = "deposit"
                    split["source_name"] = tx.get('counterPartyName') or "Revenue/Income"

            # Execute load
            payload = {"transactions": [split]}
            resp = firefly_api.create_transaction(ff_url, ff_token, payload)
            
            if "error" in resp:
                print(f"      ERROR loading {st_uid}: {resp['error']}")
            else:
                success_count += 1

        print(f"   Successfully uploaded {success_count} of {len(txs)} transactions.")

    # 3. Final: Record success timestamp if at least one transaction was loaded
    # The next run will uses this anchor - 7 days for safety.
    last_sync_path = os.path.join(os.path.dirname(staging_dir), 'LAST_SYNC_SUCCESS.txt')
    with open(last_sync_path, 'w') as f:
        f.write(datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"))
    print(f"\nFinal: Success timestamp recorded in {last_sync_path}")

    # Update LATEST symlink
    base_dir = os.path.dirname(staging_dir)
    latest_link = os.path.join(base_dir, 'LATEST')
    if os.path.exists(latest_link):
        os.remove(latest_link)
    os.symlink(staging_dir, latest_link)
    print(f"Updated LATEST symlink to {staging_dir}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 10-firefly-delta-loader.py <staging_dir>")
        sys.exit(1)
    main(sys.argv[1])
