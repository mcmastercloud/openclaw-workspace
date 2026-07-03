import os
import json
import sys
import re
import time
from datetime import datetime

# Add scripts directory to path to import generic api wrappers
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'scripts'))
import starling_api
import firefly_api

def load_env():
    env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))), '.env')
    try:
        with open(env_path, 'r') as f:
            for line in f:
                if line.strip() and not line.startswith('#'):
                    try:
                        key, val = line.strip().split('=', 1)
                        os.environ[key] = val
                    except ValueError:
                        pass
    except Exception as e:
        print(f"Warning: Could not load .env file: {e}")

def run_discovery():
    load_env()
    staging_dir = os.environ.get('FINANCE_STAGING_DIR')
    if not staging_dir:
        print("Error: FINANCE_STAGING_DIR environment variable not set.")
        sys.exit(1)

    starling_accounts_file = os.path.join(staging_dir, 'starling-accounts.txt')
    if not os.path.exists(starling_accounts_file):
        print("Error: starling-accounts.txt not found.")
        sys.exit(1)
        
    with open(starling_accounts_file, 'r') as f:
        starling_results = [line.strip() for line in f if line.strip()]

    all_account_data = {}
    prec_map = {"personal": 1, "business": 2, "joint": 3, "space": 4}
    
    for line in starling_results:
        parts = line.split(',')
        if len(parts) < 6: continue
        label, uid, name = parts[0], parts[1], parts[2]
        
        file_path = os.path.join(staging_dir, f"{uid}-Starling.txt")
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                txs = json.load(f)
                for tx in txs:
                    tx.pop("HOLDING_IGNORE", None)
                    tx.pop("IGNORE_REASON", None)
                    tx.pop("MATCHING_UID", None)
                
                p_val = prec_map.get(label.split(':')[0], 4)
                if ":space" in label: p_val = prec_map["space"]
                
                all_account_data[uid] = {"name": name, "transactions": txs, "precedence": p_val}

    print("Step 4: Deduplicating transfers (Fuzzy Date + Amount)...")
    transfer_sources = ['INTERNAL_TRANSFER', 'SAVINGS_GOAL_TRANSFER', 'TRANSFER_SAME_CURRENCY', 'FASTER_PAYMENTS_OUT', 'FASTER_PAYMENTS_IN']
    
    for uid, acc in all_account_data.items():
        for tx in acc["transactions"]:
            amt = tx.get('amount', {}).get('minorUnits')
            # Extract date part only (YYYY-MM-DD) for fuzzy matching
            full_date = tx.get('updatedAt') or tx.get('settlementTime') or tx.get('transactionTime')
            if not full_date: continue
            date_only = full_date[:10]
            direction = tx.get('direction')
            
            match_found = False
            for other_uid, other_acc in all_account_data.items():
                if uid == other_uid: continue
                for o_tx in other_acc["transactions"]:
                    if o_tx.get('amount', {}).get('minorUnits') == amt and \
                       o_tx.get('direction') != direction:
                        
                        o_full_date = o_tx.get('updatedAt') or o_tx.get('settlementTime') or o_tx.get('transactionTime')
                        if o_full_date and o_full_date[:10] == date_only:
                            if acc["precedence"] > other_acc["precedence"]:
                                tx["HOLDING_IGNORE"] = True
                                tx["IGNORE_REASON"] = f"Handled by {other_acc['name']} (Fuzzy Match)"
                                tx["MATCHING_UID"] = o_tx.get('feedItemUid')
                                # print(f"Fuzzy Match {amt} ({date_only}): Leg in {acc['name']} -> {other_acc['name']}")
                            match_found = True
                            break
                if match_found: break
        
        with open(os.path.join(staging_dir, f"{uid}-Starling.txt"), 'w') as f:
            json.dump(acc["transactions"], f, indent=2)

    print(f"Deduplication complete. Files updated in {staging_dir}")

if __name__ == "__main__":
    run_discovery()
