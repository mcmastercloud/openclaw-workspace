import os
import sys
import json
import csv
import requests

def main():
    if len(sys.argv) < 4:
        print("Usage: python3 starling_discovery.py <ENV_VAR_NAME> <SLUG> <OUTPUT_PATH>")
        sys.exit(1)

    env_var_name = sys.argv[1]
    slug = sys.argv[2]
    output_path = sys.argv[3]

    api_token = os.getenv(env_var_name)
    if not api_token:
        print(f"Error: Environment variable {env_var_name} not found.")
        sys.exit(1)

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
                        s_bal = space.get('totalSaved', {}).get('minorUnits', 0) / 100.0
                        # For Spaces, col 5 is empty, and col 7 is parent account UID
                        writer.writerow([f"{slug}:space", space_uid, space_name, s_bal, "", s_bal, account_uid])
                
        print(f"Successfully wrote {len(accounts)} accounts and balances (including Spaces) to {output_path}")

    except Exception as e:
        print(f"Failed to fetch accounts: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
