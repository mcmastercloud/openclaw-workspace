import subprocess
import sys
import os

def run_step(step_name, staging_dir, run_mode="DUMMY_RUN"):
    script_map = {
        "01-discovery": "01-starling-account-discovery.py",
        "02-download": "02-starling-transaction-download.py",
        "03-firefly-discovery": "03-firefly-account-discovery.py",
        "04-firefly-refresh": "04-firefly-cache-refresh.py",
        "05-deduplication": "05-cross-account-deduplication.py",
        "06-reconciliation": "06-delta-reconciliation.py",
        "07-verification": "07-check-3-verification.py",
        "08-backup": "08-firefly-backup.py",
        "09-prepare-upload": "09-prepare-upload-files.py",
        "10-delta-loader": "10-firefly-delta-loader.py",
        "11-ghostfolio-sync": "11-ghostfolio-sync.py",
        "12-notion-net-worth-update": "12-notion-net-worth-update.py"
    }
    
    script_name = script_map[step_name]
    script_path = os.path.join(os.path.dirname(__file__), 'src', script_name)
    interpreter = "/home/node/.openclaw/workspace/finlay/.venv/bin/python3"
    
    print(f"Executing: {script_name}...")
    
    # Run the step directly with the staging directory
    result = subprocess.run([interpreter, script_path, staging_dir], capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"Error in {step_name}: {result.stdout} {result.stderr}")
        return False
        
    if run_mode == "DUMMY_RUN" and step_name == "09-prepare-upload":
        print("DUMMY_RUN: Reached upload step. Flagging as WAITING_FOR_REVIEW.")
        return "WAITING_FOR_REVIEW"
        
    return True

if __name__ == "__main__":
    # TaskFlow bridge logic will be added here
    print("Bridge ready for TaskFlow engagement.")
