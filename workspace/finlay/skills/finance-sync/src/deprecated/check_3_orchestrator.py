import os
import json
import sys

def run_check_3():
    staging_dir = os.environ.get('FINANCE_STAGING_DIR')
    if not staging_dir:
        print("Error: FINANCE_STAGING_DIR environment variable not set.")
        sys.exit(1)

    log_path = os.path.join(staging_dir, 'sync_log.txt')
    results_path = os.path.join(staging_dir, 'CHECK_3_Balances.txt')

    # 1. Load Mappings and Balances
    # starling-accounts.txt format: label,uid,name,eff_bal,cat_uid,clr_bal
    starling_map = {}
    starling_accounts_file = os.path.join(staging_dir, 'starling-accounts.txt')
    with open(starling_accounts_file, 'r') as f:
        for line in f:
            parts = line.strip().split(',')
            if len(parts) >= 6:
                starling_map[parts[1]] = {"name": parts[2], "cleared_bal": float(parts[5])}

    # firefly-accounts.txt format: id,name,starling_guid,balance
    firefly_map = {}
    firefly_accounts_file = os.path.join(staging_dir, 'firefly-accounts.txt')
    with open(firefly_accounts_file, 'r') as f:
        for line in f:
            parts = line.strip().split(',')
            if len(parts) >= 4:
                firefly_map[parts[2]] = float(parts[3])

    report_lines = ["GUID,Account Name,Starling Cleared,Firefly Balance,Delta Sum,Mismatch"]
    all_valid = True

    for guid, st_info in starling_map.items():
        name = st_info["name"]
        st_bal = st_info["cleared_bal"]
        ff_bal = firefly_map.get(guid, 0.0)

        # 2. Calculate Sum of Delta File
        delta_file = os.path.join(staging_dir, f"{guid}-Delta.txt")
        delta_sum = 0.0
        if os.path.exists(delta_file):
            with open(delta_file, 'r') as f:
                delta_txs = json.load(f)
                for tx in delta_txs:
                    minor = tx.get('amount', {}).get('minorUnits', 0)
                    direction = tx.get('direction')
                    val = float(minor) / 100.0
                    delta_sum += val if direction == 'IN' else -val

        # Logic: Starling - (Firefly + Delta) should be 0
        diff = round(st_bal - (ff_bal + delta_sum), 2)
        
        report_lines.append(f"{guid},{name},{st_bal:.2f},{ff_bal:.2f},{delta_sum:.2f},{diff:.2f}")

        if diff != 0:
            all_valid = False
            error_msg = f"CHECK 3 FAILURE - {name}: Starling ({st_bal:.2f}) != Firefly ({ff_bal:.2f}) + Delta ({delta_sum:.2f}). Diff: {diff:.2f}"
            with open(log_path, 'a') as log:
                log.write(error_msg + "\n")
            print(error_msg)

    with open(results_path, 'w') as f:
        f.write("\n".join(report_lines) + "\n")

    if all_valid:
        success_msg = "CHECK 3 - Balance Reconciliation Validated (All Zero)"
        with open(log_path, 'a') as log:
            log.write(success_msg + "\n")
        print(success_msg)
    else:
        sys.exit(1)

if __name__ == "__main__":
    run_check_3()
