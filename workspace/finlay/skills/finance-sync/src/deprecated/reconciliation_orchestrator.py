import os
import json
import sys
from datetime import datetime, timedelta

def run_reconciliation():
    staging_dir = os.environ.get('FINANCE_STAGING_DIR')
    if not staging_dir:
        print("Error: FINANCE_STAGING_DIR environment variable not set.")
        sys.exit(1)

    # 1. Load Mappings
    starling_accounts_file = os.path.join(staging_dir, 'starling-accounts.txt')
    if not os.path.exists(starling_accounts_file):
        print("Error: starling-accounts.txt not found.")
        sys.exit(1)

    # Clean up existing Delta files before re-running
    print(f"Cleaning up existing Delta files in {staging_dir}...")
    import glob
    for f_path in glob.glob(os.path.join(staging_dir, "*-Delta.txt")):
        os.remove(f_path)

    with open(starling_accounts_file, 'r') as f:
        # Expected format: label,uid,name,eff_bal,cat_uid,clr_bal
        accounts = [line.strip().split(',') for line in f if line.strip()]

    # 2. Gather ALL External IDs and Fuzzy Keys from Firefly
    # Fuzzy Key Map: amount -> [list of ISO date strings]
    global_firefly_ext_ids = set()
    global_firefly_fuzzy_data = {} # Map amount to dates
    
    for acc in accounts:
        if len(acc) < 2: continue
        guid = acc[1]
        firefly_file = os.path.join(staging_dir, f"{guid}-Firefly.txt")
        if os.path.exists(firefly_file):
            with open(firefly_file, 'r') as f:
                ff_txs = json.load(f)
                for tx in ff_txs:
                    # UID Matching
                    ext_id = tx.get('external_id')
                    if ext_id:
                        global_firefly_ext_ids.add(ext_id)
                    
                    # Fuzzy Metadata
                    f_date_str = tx.get('date')
                    f_amt_str = tx.get('amount')
                    if f_date_str and f_amt_str:
                        try:
                            # Normalize amount to float
                            f_amt = abs(round(float(f_amt_str), 2))
                            if f_amt not in global_firefly_fuzzy_data:
                                global_firefly_fuzzy_data[f_amt] = []
                            # Store the normalized date (stripping microseconds/TZ for easier partial comparison if needed)
                            # But we'll parse it properly during check
                            global_firefly_fuzzy_data[f_amt].append(f_date_str)
                        except: pass
    
    print(f"Loaded {len(global_firefly_ext_ids)} unique IDs and indexed {len(global_firefly_fuzzy_data)} distinct amounts from Firefly.")

    def parse_dt(dt_str):
        if not dt_str: return None
        # Handle formats like '2024-06-27T23:15:15.169Z' or '2024-06-28T00:15:15+01:00'
        # Basic parsing: take the first 19 chars 'YYYY-MM-DDTHH:MM:SS'
        try:
            return datetime.strptime(dt_str[:19], "%Y-%m-%dT%H:%M:%S")
        except:
            return None

    # 3. Reconcile each account
    for acc in accounts:
        if len(acc) < 2: continue
        guid = acc[1]
        name = acc[2]

        starling_file = os.path.join(staging_dir, f"{guid}-Starling.txt")
        if not os.path.exists(starling_file):
            continue

        with open(starling_file, 'r') as f:
            starling_txs = json.load(f)
        
        delta_txs = []
        for st_tx in starling_txs:
            st_uid = st_tx.get('feedItemUid')
            matching_uid = st_tx.get('MATCHING_UID')
            
            # UID Match Check
            is_in_firefly = (st_uid in global_firefly_ext_ids) or (matching_uid and matching_uid in global_firefly_ext_ids)
            
            # Fuzzy Match Check (Amount + 24h Date Window)
            if not is_in_firefly:
                st_date_str = st_tx.get('updatedAt') or st_tx.get('settlementTime') or st_tx.get('transactionTime')
                st_minor = st_tx.get('amount', {}).get('minorUnits', 0)
                if st_date_str and st_minor:
                    st_amt = abs(round(float(st_minor) / 100.0, 2))
                    st_dt = parse_dt(st_date_str)
                    
                    if st_amt in global_firefly_fuzzy_data and st_dt:
                        # Check all recorded Firefly dates for this amount
                        for ff_date_str in global_firefly_fuzzy_data[st_amt]:
                            ff_dt = parse_dt(ff_date_str)
                            if ff_dt:
                                # Calculate absolute difference
                                diff = abs((st_dt - ff_dt).total_seconds())
                                if diff <= 86400: # 24 hour window to handle TZ shifts
                                    is_in_firefly = True
                                    # print(f"Fuzzy Matched {st_amt} ({st_date_str}) with FF ({ff_date_str}) - Diff: {diff}s")
                                    break

            if not is_in_firefly:
                delta_txs.append(st_tx)

        # Write Delta File
        delta_file = os.path.join(staging_dir, f"{guid}-Delta.txt")
        with open(delta_file, 'w') as f:
            json.dump(delta_txs, f, indent=2)

        print(f"Reconciled {name}: {len(delta_txs)} transactions in Delta. Saved to {guid}-Delta.txt")

if __name__ == "__main__":
    run_reconciliation()
