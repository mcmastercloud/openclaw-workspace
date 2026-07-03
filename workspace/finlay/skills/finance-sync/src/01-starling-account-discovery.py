import os
import sys
import json
import csv
import requests

# McMaster Finance System: Step 01 - Starling Account Discovery
# This script maps all accounts and spaces, capturing current bank balances.

def main(staging_dir):
    output_path = os.path.join(staging_dir, 'starling-accounts.txt')

    # Mapping account slugs to environment variables
    account_configs = [
        ('personal', 'STARLING_CURRENT_ACCOUNT_TOKEN'),
        ('joint', 'STARLING_JOINT_ACCOUNT_TOKEN'),
        ('business', 'STARLING_BUSINESS_ACCOUNT_TOKEN')
    ]

    # Initialize file
    with open(output_path, mode='w', newline='') as f:
        pass

    for slug, env_var in account_configs:
        api_token = os.getenv(env_var)
        if not api_token:
            print(f"Warning: Environment variable {env_var} not found. Skipping.")
            continue

        headers = {
            "Authorization": f"Bearer {api_token}",
            "Accept": "application/json"
        }

        url = "https://api.starlingbank.com/api/v2/accounts"

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()

            accounts = data.get("accounts", [])
            
            with open(output_path, mode='a', newline='') as f:
                writer = csv.writer(f)
                for account in accounts:
                    account_uid = account.get("accountUid")
                    name = account.get("name")
                    cat_uid = account.get("defaultCategory")
                    
                    # Get Balance
                    bal_url = f"https://api.starlingbank.com/api/v2/accounts/{account_uid}/balance"
                    bal_resp = requests.get(bal_url, headers=headers)
                    cleared = 0.0
                    effective = 0.0
                    if bal_resp.status_code == 200:
                        bal_data = bal_resp.json()
                        cleared = bal_data.get('clearedBalance', {}).get('minorUnits', 0) / 100.0
                        effective = bal_data.get('effectiveBalance', {}).get('minorUnits', 0) / 100.0

                    # Format: slug, uid, name, effective, cat_uid, cleared, parent_uid
                    writer.writerow([slug, account_uid, name, effective, cat_uid, cleared, ""])
                    
                    # Fetch Savings Goals (Spaces)
                    spaces_url = f"https://api.starlingbank.com/api/v2/account/{account_uid}/savings-goals"
                    spaces_response = requests.get(spaces_url, headers=headers)
                    if spaces_response.status_code == 200:
                        spaces_data = spaces_response.json()
                        for space in spaces_data.get("savingsGoalList", []):
                            space_uid = space.get("savingsGoalUid")
                            space_name = f"{name} > {space.get('name')}"
                            # Spaces only have totalSaved which acts as cleared balance
                            s_bal = space.get('totalSaved', {}).get('minorUnits', 0) / 100.0
                            writer.writerow([f"{slug}:space", space_uid, space_name, s_bal, "", s_bal, account_uid])
                    
            print(f"Successfully discovered accounts for {slug}")

        except Exception as e:
            print(f"Failed to fetch accounts for {slug}: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 01-starling-account-discovery.py <staging_dir>")
        sys.exit(1)
    main(sys.argv[1])
