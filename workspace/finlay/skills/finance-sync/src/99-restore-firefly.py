import os
import sys
import requests
import urllib3

# McMaster Finance System: Step 99 - Restore Firefly
# Purpose: This script provides an emergency manual trigger to restore a Firefly III database
# via the internal Docker Management API.
# NOTE: This script is NOT part of the automated daily sync cycle.

# Disable insecure request warnings for self-signed certs
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def main():
    if len(sys.argv) < 2:
        print("Error: No backup filename provided.")
        print("Usage: python3 99-restore-firefly.py <firefly_backup_YYYYMMDD_HHMMSS.tar.gz>")
        sys.exit(1)

    backup_filename = sys.argv[1]
    manager_url = os.environ.get('DOCKER1_MANAGER_URL')
    manager_token = os.environ.get('DOCKER1_MANAGER_TOKEN')
    
    if not manager_url or not manager_token:
        print("   ERROR: Docker Manager environment variables not set.")
        sys.exit(1)
    
    print(f"!!! EMERGENCY RESTORE INITIATED !!!")
    print(f"Target Backup: {backup_filename}")
    print(f"Initiating remote restore via Docker Manager API...")
    
    try:
        # Trigger the restore via API
        response = requests.post(
            manager_url,
            headers={
                "Authorization": f"Bearer {manager_token}",
                "Content-Type": "application/json"
            },
            json={"command": "restore-firefly", "file": backup_filename},
            verify=False
        )
        
        response.raise_for_status()
        result = response.json()
        
        print(f"   Success! Restore triggered. Response: {result}")
        print("Please verify the Firefly III interface to confirm ledger integrity.")

    except Exception as e:
        print(f"   ERROR: Restore failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
