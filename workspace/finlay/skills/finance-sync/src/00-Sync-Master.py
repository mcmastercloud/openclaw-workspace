import os
import sys
import subprocess
from datetime import datetime

# McMaster Finance System: TaskFlow Orchestrator
# Uses Managed TaskFlow for durable, resumable execution
# Usage: python3 00-Sync-Master.py [FULL_RUN|DUMMY_RUN]

PYTHON_PATH = "/home/node/.openclaw/workspace/finlay/.venv/bin/python3"

def run_pipeline(run_type, staging_dir):
    print(f"Starting pipeline: {run_type} in {staging_dir}")

    steps = [
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
        steps.extend([
            ("10", "10-firefly-delta-loader.py"),
            ("11", "11-ghostfolio-sync.py"),
            ("12", "12-notion-net-worth-update.py")
        ])

    for step_num, script in steps:
        print(f"Running Step {step_num}: {script}")
        
        # Execute script and pipe output
        script_path = os.path.join(os.path.dirname(__file__), script)
        
        # Pass staging_dir as a command-line argument explicitly
        process = subprocess.Popen([PYTHON_PATH, script_path, staging_dir], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        stdout, _ = process.communicate()
        print(stdout.decode())
        
        if process.returncode != 0:
            print(f"Failed at {script}")
            sys.exit(1)
        
    print("Pipeline complete")

if __name__ == "__main__":
    if len(sys.argv) < 2: sys.exit(1)
    
    # Generate a single timestamp for the entire run
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    # Base directory is skills/finance-sync/finance-staging
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "finance-staging"))
    staging_dir = os.path.join(base_dir, timestamp)
    
    # Ensure the directory exists
    os.makedirs(staging_dir, exist_ok=True)
    
    # Pass the specific timestamped directory to the pipeline
    run_pipeline(sys.argv[1], staging_dir)
