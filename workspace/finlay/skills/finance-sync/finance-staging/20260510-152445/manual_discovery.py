import os, sys, csv
sys.path.append('/home/openclaw/.openclaw/agents/finlay/workspace/scripts')
import starling_api

accounts_to_check = [
    ('personal', os.environ['STARLING_PERSONAL_ACCOUNT_TOKEN']),
    ('joint', os.environ['STARLING_JOINT_ACCOUNT_TOKEN']),
    ('business', os.environ['STARLING_BUSINESS_ACCOUNT_TOKEN'])
]

with open(os.path.join(os.environ['FINANCE_STAGING_DIR'], 'starling-accounts.txt'), 'w', newline='') as f:
    writer = csv.writer(f)
    for slug, token in accounts_to_check:
        try:
            accs = starling_api.list_accounts(token)
            for acc in accs.get('accounts', []):
                uid = acc['accountUid']
                cat_uid = acc['defaultCategory']
                name = acc['name']
                bal = starling_api.get_balance(token, uid)
                # Structure: clearedBalance -> minorUnits
                cleared = bal.get('clearedBalance', {}).get('minorUnits', 0) / 100.0
                effective = bal.get('effectiveBalance', {}).get('minorUnits', 0) / 100.0
                writer.writerow([slug, uid, name, effective, cat_uid, cleared])
                
                # Fetch Savings Goals (Spaces)
                spaces_data, _ = starling_api.make_request(token, f"account/{uid}/savings-goals")
                for s in spaces_data.get('savingsGoalList', []):
                    s_uid = s['savingsGoalUid']
                    s_name = f"{name} > {s['name']}"
                    s_bal = s.get('totalSaved', {}).get('minorUnits', 0) / 100.0
                    writer.writerow([f"{slug}:space", s_uid, s_name, s_bal, "", s_bal])

        except Exception as e:
            print(f"Error processing {slug}: {e}")
