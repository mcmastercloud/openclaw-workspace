import urllib.request
import json
import os

if os.path.exists('.env'):
    with open('.env') as f:
        for line in f:
            if '=' in line and not line.startswith('#'):
                k, v = line.strip().split('=', 1)
                os.environ[k] = v

token = os.environ.get('STARLING_TOKEN')

req = urllib.request.Request('https://api.starlingbank.com/api/v2/accounts', headers={'Authorization': f'Bearer {token}', 'Accept': 'application/json'})
with urllib.request.urlopen(req) as response:
    accounts = json.loads(response.read().decode()).get('accounts', [])

for account in accounts:
    print(json.dumps(account, indent=2))
    account_uid = account.get('accountUid')
    name = account.get('name')
    
    balance_req = urllib.request.Request(f'https://api.starlingbank.com/api/v2/accounts/{account_uid}/balance', headers={'Authorization': f'Bearer {token}', 'Accept': 'application/json'})
    with urllib.request.urlopen(balance_req) as balance_response:
        balance_data = json.loads(balance_response.read().decode())
        amount = balance_data.get('amount', {}).get('minorUnits', 0) / 100.0
        print(f"Account: {name} ({account_uid}) | Balance: £{amount}")
