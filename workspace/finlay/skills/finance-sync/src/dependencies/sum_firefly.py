import os, requests, json
def load_env():
    with open('/home/openclaw/.openclaw/agents/finlay/workspace/.env') as f:
        for line in f:
            if '=' in line and not line.startswith('#'):
                k, v = line.strip().split('=', 1)
                os.environ[k] = v

load_env()
ff_url = os.getenv('FIREFLY_URL', 'http://192.168.50.201:8081')
ff_token = os.getenv('FIREFLY_TOKEN')
ff_headers = {"Authorization": f"Bearer {ff_token}", "Accept": "application/json"}

def get_totals(account_id):
    deposits = 0.0
    withdrawals = 0.0
    page = 1
    while True:
        resp = requests.get(f"{ff_url}/api/v1/accounts/{account_id}/transactions?page={page}", headers=ff_headers)
        data = resp.json()
        if 'data' not in data or not data['data']:
            break
        for item in data['data']:
            for tx in item['attributes']['transactions']:
                amount = float(tx['amount'])
                if tx['type'] == 'deposit' and tx['destination_id'] == str(account_id):
                    deposits += amount
                elif tx['type'] == 'withdrawal' and tx['source_id'] == str(account_id):
                    withdrawals += amount
                elif tx['type'] == 'transfer':
                    if tx['destination_id'] == str(account_id):
                        deposits += amount
                    elif tx['source_id'] == str(account_id):
                        withdrawals += amount
        
        if page >= data['meta']['pagination']['total_pages']:
            break
        page += 1
    return deposits, withdrawals

d, w = get_totals(1)
print(f"Deposits: {d}, Withdrawals: {w}, Net: {d-w}")
