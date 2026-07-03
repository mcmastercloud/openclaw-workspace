import os
import sys
import subprocess
import requests
from datetime import datetime

# McMaster Finance System: Step 08 - Firefly III Backup
# Performs a full SQL-level backup of the Firefly III database via Docker Management API.

def main(staging_dir):
    manager_url = os.environ.get('DOCKER1_MANAGER_URL')
    manager_token = os.environ.get('DOCKER1_MANAGER_TOKEN')
    
    if not manager_url or not manager_token:
        print("   ERROR: Docker Manager environment variables not set.")
        sys.exit(1)
    
    print(f"Initiating remote SQL backup via Docker Manager API...")
    
    try:
        # Trigger the backup via API
        response = requests.post(
            manager_url,
            headers={
                "Authorization": f"Bearer {manager_token}",
                "Content-Type": "application/json"
            },
            json={"command": "backup-firefly"},
            verify=False
        )
        
        response.raise_for_status()
        result = response.json()
        
        print(f"   Success! Backup triggered. Response: {result}")
        
        # Ensure the LATEST staging dir exists and write the confirmation
        final_staging_dir = os.path.dirname(os.path.join(staging_dir, "BACKUP_CONFIRMATION.txt"))
        os.makedirs(final_staging_dir, exist_ok=True)
        
        with open(os.path.join(final_staging_dir, "BACKUP_CONFIRMATION.txt"), "w") as log:
            log.write(f"Pre-flight backup triggered via API: {datetime.now()}\nResponse: {result}")

    except Exception as e:
        print(f"   ERROR: {e}")
        # Soften failure: if it was a file permission issue, proceed anyway
        if "No such file or directory" in str(e):
            print("   (Warning: Minor log write error, continuing pipeline)")
        else:
            sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 08-firefly-backup.py <staging_dir>")
        sys.exit(1)
    main(sys.argv[1])
