import os, sys, csv
sys.path.append('/home/openclaw/.openclaw/agents/finlay/workspace/scripts')
import firefly_api

base_url = os.environ['FIREFLY_URL']
token = os.environ['FIREFLY_TOKEN']
output_path = os.path.join(os.environ['FINANCE_STAGING_DIR'], 'firefly-accounts.txt')

resp = firefly_api.list_accounts(base_url, token, type='asset')
accounts = resp.get('data', [])

with open(output_path, 'w', newline='') as f:
    writer = csv.writer(f)
    for acc in accounts:
        attrs = acc.get('attributes', {})
        # Firefly accounts have an 'external_id' where we store the Starling GUID
        writer.writerow([
            acc.get('id'),
            attrs.get('name'),
            attrs.get('external_id'),
            attrs.get('current_balance', 0.0)
        ])
