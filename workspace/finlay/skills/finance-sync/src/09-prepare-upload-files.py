import os
import json
import sys
import csv

# McMaster Finance System: Step 09 - Prepare Upload Files
# This script reads the Delta files and creates corresponding -Upload files.
# It strictly excludes any transaction where HOLDING_IGNORE = true.

def main(staging_dir):
    # 1. Discover all Delta files in the staging area
    import glob
    delta_files = glob.glob(os.path.join(staging_dir, "*-Delta.txt"))
    
    if not delta_files:
        print("No Delta files found. Run Step 06 first.")
        sys.exit(1)

    for delta_path in delta_files:
        filename = os.path.basename(delta_path)
        guid = filename.replace("-Delta.txt", "")
        upload_path = os.path.join(staging_dir, f"{guid}-Upload.txt")
        
        with open(delta_path, 'r') as f:
            try:
                txs = json.load(f)
            except:
                print(f"Error reading {delta_path}")
                continue
        
        # Filter for non-ignored transactions
        # (Exclude PENDING items and Low-Precedence Transfer Legs)
        upload_txs = []
        for tx in txs:
            if tx.get('HOLDING_IGNORE') or tx.get('IGNORE_REASON'):
                continue
            upload_txs.append(tx)
        
        # Save to -Upload file
        with open(upload_path, 'w') as out:
            json.dump(upload_txs, out, indent=2)
            
        print(f"Created {os.path.basename(upload_path)}: {len(upload_txs)} transactions to be posted.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 09-prepare-upload-files.py <staging_dir>")
        sys.exit(1)
    main(sys.argv[1])
