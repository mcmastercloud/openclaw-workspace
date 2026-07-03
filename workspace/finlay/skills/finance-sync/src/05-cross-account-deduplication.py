import os
import json
import sys
from datetime import datetime

# McMaster Finance System: Step 05 - Cross-Account Deduplication
# This script identifies internal transfers via robust spendingCategory comparison.

def main(staging_dir):
    if not staging_dir:
        print("Error: Staging directory not provided.")
        sys.exit(1)

    accounts_file = os.path.join(staging_dir, 'starling-accounts.txt')
    if not os.path.exists(accounts_file):
        print("Error: starling-accounts.txt not found.")
        sys.exit(1)
        
    import csv
    with open(accounts_file, 'r') as f:
        lines = [row for row in csv.reader(f) if row]

    all_account_data = {}
    prec_map = {"personal": 1, "business": 2, "joint": 3, "space": 4}
    
    for row in lines:
        label, uid, name = row[0], row[1], row[2]
        file_path = os.path.join(staging_dir, f"{uid}-Starling.txt")
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                txs = json.load(f)
                for tx in txs:
                    tx.pop("HOLDING_IGNORE", None)
                    tx.pop("MATCHING_UID", None)
                
                p_val = prec_map.get(label.split(':')[0], 4)
                if ":space" in label: p_val = prec_map["space"]
                all_account_data[uid] = {"name": name, "transactions": txs, "precedence": p_val}

    print("Deduplicating Starling transfers via Spending Category...")
    
    def parse_dt(s):
        try: return datetime.strptime(s[:19], "%Y-%m-%dT%H:%M:%S")
        except: return None

    # Categories likely to contain internal transfers
    transfer_cats = ['TRANSFERS', 'PERSONAL_TRANSFERS', 'SAVING', 'INCOME', 'REVENUE']

    for uid, acc in all_account_data.items():
        for tx in acc["transactions"]:
            cat = tx.get('spendingCategory')
            if cat not in transfer_cats:
                continue

            amt = tx.get('amount', {}).get('minorUnits')
            direction = tx.get('direction')
            dt = parse_dt(tx.get('updatedAt') or tx.get('settlementTime') or tx.get('transactionTime'))
            if not dt: continue
            
            for other_uid, other_acc in all_account_data.items():
                if uid == other_uid: continue
                # Match logic: Same absolute amount, opposite direction, same date window (24h)
                for o_tx in other_acc["transactions"]:
                    if o_tx.get('amount', {}).get('minorUnits') == amt and \
                       o_tx.get('direction') != direction:
                        
                        o_dt = parse_dt(o_tx.get('updatedAt') or o_tx.get('settlementTime') or o_tx.get('transactionTime'))
                        if o_dt and abs((dt - o_dt).total_seconds()) <= 86400: # 24h
                            # Apply precedence rule
                            if acc["precedence"] > other_acc["precedence"]:
                                tx["HOLDING_IGNORE"] = True
                                tx["MATCHING_UID"] = o_tx.get('feedItemUid')
                            else:
                                o_tx["HOLDING_IGNORE"] = True
                                o_tx["MATCHING_UID"] = tx.get('feedItemUid')
                            break
                    if tx.get("HOLDING_IGNORE"): break
                if tx.get("HOLDING_IGNORE"): break
        
        with open(os.path.join(staging_dir, f"{uid}-Starling.txt"), 'w') as f:
            json.dump(acc["transactions"], f, indent=2)

    print(f"Deduplication complete. History files updated.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 05-cross-account-deduplication.py <staging_dir>")
        sys.exit(1)
    main(sys.argv[1])
