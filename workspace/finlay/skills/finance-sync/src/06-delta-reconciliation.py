import os
import json
import sys
from datetime import datetime

# McMaster Finance System: Step 06 - Delta Reconciliation
# This script compares bank and ledger history to identify what is truly missing (The Delta).

def main(staging_dir):
    if not staging_dir:
        print("Error: Staging directory not provided.")
        sys.exit(1)

    accounts_file = os.path.join(staging_dir, 'starling-accounts.txt')
    if not os.path.exists(accounts_file):
        print("Error: starling-accounts.txt not found.")
        sys.exit(1)

    # 1. Clear existing Delta files
    import glob
    for f in glob.glob(os.path.join(staging_dir, "*-Delta.txt")):
        os.remove(f)

    import csv
    with open(accounts_file, 'r') as f:
        reader = csv.reader(f)
        accounts = [row for row in reader if row]

    # 2. Index everything currently in Firefly
    global_firefly_ext_ids = set()
    global_firefly_fuzzy = {} # amount -> [list of ISO dates]
    
    for acc in accounts:
        guid = acc[1]
        firefly_cache = os.path.join(staging_dir, f"{guid}-Firefly.txt")
        if os.path.exists(firefly_cache):
            with open(firefly_cache, 'r') as f:
                txs = json.load(f)
                for tx in txs:
                    eid = tx.get('external_id')
                    if eid: global_firefly_ext_ids.add(eid)
                    
                    amt = tx.get('amount')
                    date = tx.get('date')
                    if amt and date:
                        try:
                            f_amt = abs(round(float(amt), 2))
                            if f_amt not in global_firefly_fuzzy: global_firefly_fuzzy[f_amt] = []
                            global_firefly_fuzzy[f_amt].append(date)
                        except: pass
    
    print(f"Loaded {len(global_firefly_ext_ids)} unique IDs and indexed {len(global_firefly_fuzzy)} distinct amounts from Firefly.")

    def parse_dt(dt_str):
        if not dt_str: return None
        try: return datetime.strptime(dt_str[:19], "%Y-%m-%dT%H:%M:%S")
        except: return None

    # 3. Process every account history to produce Delta
    anchor_date = datetime(2026, 1, 1)
    
    for acc in accounts:
        guid = acc[1]
        name = acc[2]
        starling_history = os.path.join(staging_dir, f"{guid}-Starling.txt")
        if not os.path.exists(starling_history): continue

        with open(starling_history, 'r') as f:
            st_txs = json.load(f)
        
        delta_txs = []
        for st_tx in st_txs:
            # Anchor Date Check
            st_date_str = st_tx.get('updatedAt') or st_tx.get('settlementTime') or st_tx.get('transactionTime')
            st_dt = parse_dt(st_date_str)
            if not st_dt or st_dt < anchor_date:
                continue
            
            # RULE (Correction 2026-05-20): We UNCONDITIONALLY add missing items 
            # to the Delta file, regardless of HOLDING_IGNORE or IGNORE_REASON.
            # This ensures that PENDING items are available for Step 07 math.
            # Step 10 (Loader) will perform the final 'is this item ready to post?' check.

            st_uid = st_tx.get('feedItemUid')
            matching_uid = st_tx.get('MATCHING_UID') # Non-None only for Linked Starling Transfers
            
            # Exclusion 1: UID Match (Direct or Linked Starling Transfer leg)
            is_in_firefly = (st_uid in global_firefly_ext_ids) or \
                             (matching_uid and matching_uid in global_firefly_ext_ids)

            # Exclusion 2: Fuzzy magnitude/date match (ONLY for transfers where legs weren't linked by Starling)
            if not is_in_firefly:
                # Determine if this Starling record is a transfer candidate
                source = st_tx.get('source')
                sub_type = st_tx.get('sourceSubType')
                transfer_sources = ['INTERNAL_TRANSFER', 'SAVINGS_GOAL_TRANSFER', 'TRANSFER_SAME_CURRENCY']
                is_transfer = source in transfer_sources or sub_type in transfer_sources

                if is_transfer:
                    st_date_str = st_tx.get('updatedAt') or st_tx.get('settlementTime') or st_tx.get('transactionTime')
                    st_minor = st_tx.get('amount', {}).get('minorUnits', 0)
                    if st_date_str and st_minor:
                        st_amt = abs(round(float(st_minor) / 100.0, 2))
                        st_dt = parse_dt(st_date_str)
                        
                        if st_amt in global_firefly_fuzzy and st_dt:
                            for ff_date_str in global_firefly_fuzzy[st_amt]:
                                ff_dt = parse_dt(ff_date_str)
                                if ff_dt and abs((st_dt - ff_dt).total_seconds()) <= 86400: # 24h window
                                    is_in_firefly = True
                                    break

            # If it's truly not in Firefly, it belongs in Delta
            if not is_in_firefly:
                delta_txs.append(st_tx)

        # Save Delta
        with open(os.path.join(staging_dir, f"{guid}-Delta.txt"), 'w') as f:
            json.dump(delta_txs, f, indent=2)
        print(f"Reconciled {name}: {len(delta_txs)} transactions in Delta.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 06-delta-reconciliation.py <staging_dir>")
        sys.exit(1)
    main(sys.argv[1])
