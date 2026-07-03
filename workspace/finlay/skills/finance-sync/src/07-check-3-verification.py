import os
import json
import sys
import csv

# McMaster Finance System: Step 07 - Check 3 Balance Verification
# This script performs the final mathematical verification:
# Bank Balance == Firefly Balance + Sum(Delta Transactions)

def main(staging_dir):
    if not staging_dir:
        print("Error: Staging directory not provided.")
        sys.exit(1)

    # 1. Load Starling account data and balances
    starling_map = {}
    starling_accounts_file = os.path.join(staging_dir, 'starling-accounts.txt')
    with open(starling_accounts_file, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            # We switched to cleared balance (row[5]) to ignore pending items (2026-06-03 request)
            if len(row) >= 6:
                starling_map[row[1]] = {"name": row[2], "bank_balance": float(row[5])}

    # 2. Load Firefly account data and balances
    firefly_map = {}
    firefly_accounts_file = os.path.join(staging_dir, 'firefly-accounts.txt')
    with open(firefly_accounts_file, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            # Firefly balance only reflects settled ledger items.
            if len(row) >= 4:
                firefly_map[row[2]] = float(row[3])

    # 2.5 Load Space pending offsets (2026-06-03 request)
    offsets = {}
    offsets_file = os.path.join(staging_dir, 'space-pending-offsets.json')
    if os.path.exists(offsets_file):
        with open(offsets_file, 'r') as f:
            offsets = json.load(f)

    report_lines = ["Starling GUID,Account Name,Bank Balance,Ledger Balance,Delta Sum,Mismatch"]
    all_valid = True

    for guid, st_info in starling_map.items():
        name = st_info["name"]
        # MANDATORY: Use clearedBalance (bank_balance field now uses row[5]) as the benchmark.
        # This matches the ledger, as we are ignoring PENDING items in both Starling download and Delta.
        # For Spaces, we use totalSaved - captured pending offsets to simulate the cleared balance.
        bank_bal = st_info["bank_balance"]
        
        # Apply synthetic offset if it's a space (2026-06-03 request)
        if guid in offsets:
            offset_val = float(offsets[guid])
            # totalSaved (bank_bal) minus (negative pending OUT) = addition
            # e.g. 381.06 - (-9.99) = 391.05
            bank_bal = round(bank_bal - offset_val, 2)
            print(f"   Applied Space Offset: {name} Adjusted Bank Balance: {bank_bal} (Offset: {offset_val})")
            
        ledger_bal = firefly_map.get(guid, 0.0)

        # 3. Sum the Delta for this account
        delta_file = os.path.join(staging_dir, f"{guid}-Delta.txt")
        delta_sum = 0.0
        if os.path.exists(delta_file):
            with open(delta_file, 'r') as f:
                delta_txs = json.load(f)
                for tx in delta_txs:
                    # Logic: We sum ALL transactions in Delta (Settled and Pending)
                    # to match the bank's effectiveBalance.
                    minor = tx.get('amount', {}).get('minorUnits', 0)
                    direction = tx.get('direction')
                    val = float(minor) / 100.0
                    delta_sum += val if direction == 'IN' else -val

        # Logic: Bank - (Ledger + Delta) should be 0
        diff = round(bank_bal - (ledger_bal + delta_sum), 2)
        report_lines.append(f"{guid},{name},{bank_bal:.2f},{ledger_bal:.2f},{delta_sum:.2f},{diff:.2f}")

        if diff != 0:
            all_valid = False
            print(f"CHECK 3 FAILURE - {name}: Bank ({bank_bal:.2f}) != Ledger ({ledger_bal:.2f}) + Delta ({delta_sum:.2f}). Diff: {diff:.2f}")

    # Save results to a verification file
    results_path = os.path.join(staging_dir, 'CHECK_3_VERIFICATION.txt')
    with open(results_path, 'w') as f:
        f.write("\n".join(report_lines) + "\n")

    if all_valid:
        print("CHECK 3: PASS (Balance Reconciliation Validated - All Zero)")
    else:
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 07-check-3-verification.py <staging_dir>")
        sys.exit(1)
    main(sys.argv[1])
