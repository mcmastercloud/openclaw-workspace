import os
import sys
import datetime
import subprocess

# TaskFlow Bridge for Finance Sync
# This script represents the orchestration layer that should interface with the TaskFlow runtime.
# Since I am an agent in a persistent environment, I will invoke the pipeline steps 
# while maintaining the context structure requested.

def execute_pipeline(run_mode="DUMMY_RUN"):
    # 1. Define Staging Area
    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    base_dir = "/home/node/.openclaw/workspace/finlay/skills/finance-sync/finance-staging"
    staging_dir = os.path.join(base_dir, timestamp)
    os.makedirs(staging_dir, exist_ok=True)
    
    # 2. Pipeline sequence
    steps = [
        "01-discovery", "02-download", "03-firefly-discovery", 
        "04-firefly-refresh", "05-deduplication", "06-reconciliation", 
        "07-verification", "09-prepare-upload"
    ]
    
    if run_mode == "FULL_RUN":
        steps.extend(["10-delta-loader", "11-ghostfolio-sync", "12-notion-net-worth-update"])
        
    # 3. Execution
    print(f"TaskFlow Orchestration Started. Mode={run_mode}, Dir={staging_dir}")
    
    for step in steps:
        print(f"--- TaskFlow Action: Running Step {step} ---")
        
        # Mapping step IDs to the actual refactored Python scripts
        # All of these now accept staging_dir as sys.argv[1]
        step_script_map = {
            "01-discovery": "01-starling-account-discovery.py",
            "02-download": "02-starling-transaction-download.py",
            "03-firefly-discovery": "03-firefly-account-discovery.py",
            "04-firefly-refresh": "04-firefly-cache-refresh.py",
            "05-deduplication": "05-cross-account-deduplication.py",
            "06-reconciliation": "06-delta-reconciliation.py",
            "07-verification": "07-check-3-verification.py",
            "09-prepare-upload": "09-prepare-upload-files.py",
            "10-delta-loader": "10-firefly-delta-loader.py",
            "11-ghostfolio-sync": "11-ghostfolio-sync.py",
            "12-notion-net-worth-update": "12-notion-net-worth-update.py"
        }
        
        script_path = os.path.join(os.path.dirname(__file__), 'src', step_script_map[step])
        interpreter = "/home/node/.openclaw/workspace/finlay/.venv/bin/python3"
        
        # Execute in-process simulation of TaskFlow task
        # Real-time stdout capture for you to observe
        result = subprocess.run([interpreter, script_path, staging_dir], capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"TaskFlow Task Failed: {step}")
            print(result.stderr)
            sys.exit(1)
        
        print(result.stdout)
        
    print("TaskFlow pipeline finished successfully.")

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "DUMMY_RUN"
    execute_pipeline(mode)
