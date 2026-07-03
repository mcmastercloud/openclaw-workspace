import os
import sys
import subprocess
from datetime import datetime

# McMaster Finance System: Step 00 - Sync Master
# Controls the full financial synchronisation pipeline from Step 01 to 10.
#
# Usage: python3 00-Sync-Master.py [FULL_RUN|DUMMY_RUN]
# - FULL_RUN: Executes Steps 01 to 10.
# - DUMMY_RUN: Executes Steps 01 to 09 (Verification only, no ledger load).

def log_to_file(staging_dir, message):
    log_path = os.path.join(staging_dir, 'sync_log.txt')
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_path, 'a') as f:
        f.write(f"[{timestamp}] {message}\n")
    print(message)

def run_step(step_num, script_name, staging_dir):
    script_path = os.path.join(os.path.dirname(__file__), script_name)
    log_to_file(staging_dir, f"STARTING STEP {step_num}: {script_name}")
    
    # Environment variable for children
    env = os.environ.copy()
    env['FINANCE_STAGING_DIR'] = staging_dir
    
    # Execute and capture output
    process = subprocess.Popen(
        [sys.executable, script_path],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )
    
    for line in process.stdout:
        clean_line = line.strip()
        if clean_line:
            log_to_file(staging_dir, f"  [{script_name}] {clean_line}")
            
    process.wait()
    
    if process.returncode != 0:
        log_to_file(staging_dir, f"CRITICAL FAILURE in Step {step_num}. Stopping execution.")
        return False
    
    log_to_file(staging_dir, f"COMPLETED STEP {step_num} successfully.")
    return True

def main():
    if len(sys.argv) < 2 or sys.argv[1] not in ['FULL_RUN', 'DUMMY_RUN']:
        print("Usage: python3 00-Sync-Master.py [FULL_RUN|DUMMY_RUN]")
        sys.exit(1)
        
    run_type = sys.argv[1]
    
    # 1. Prepare Staging Directory
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    staging_base = os.environ.get('FINANCE_STAGING_BASE_DIR', 'finance-staging')
    staging_dir = os.path.join(staging_base, timestamp)
    os.makedirs(staging_dir, exist_ok=True)
    
    log_to_file(staging_dir, f"--- NEW SYNC INITIATED: {run_type} ---")
    log_to_file(staging_dir, f"Staging Directory: {staging_dir}")

    # 2. Define Pipeline
    pipeline = [
        ("01", "01-starling-account-discovery.py"),
        ("02", "02-starling-transaction-download.py"),
        ("03", "03-firefly-account-discovery.py"),
        ("04", "04-firefly-cache-refresh.py"),
        ("05", "05-cross-account-deduplication.py"),
        ("06", "06-delta-reconciliation.py"),
        ("07", "07-check-3-verification.py"),
        ("08", "08-firefly-backup.py"),
        ("09", "09-prepare-upload-files.py")
    ]
    
    if run_type == "FULL_RUN":
        pipeline.append(("10", "10-firefly-delta-loader.py"))
        pipeline.append(("11", "11-ghostfolio-sync.py"))
        pipeline.append(("12", "12-notion-net-worth-update.py"))
    else:
        log_to_file(staging_dir, "MODE: DUMMY_RUN - Skipping ledger load, portfolio sync, and Notion update (Steps 10-12).")

    # 3. Execute Pipeline
    for step_num, script in pipeline:
        success = run_step(step_num, script, staging_dir)
        if not success:
            sys.exit(1)
            
    log_to_file(staging_dir, f"--- SYNC PIPELINE {run_type} FINISHED SUCCESSFULLY ---")

if __name__ == "__main__":
    main()
