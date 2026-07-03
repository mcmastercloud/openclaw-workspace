import os
import json
import sys
import time
from datetime import datetime

# Path handling
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'scripts'))
import starling_api
import firefly_api

def load_env():
    env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))), '.env')
    try:
        with open(env_path, 'r') as f:
            for line in f:
                if line.strip() and not line.startswith('#'):
                    try:
                        key, val = line.strip().split('=', 1)
                        os.environ[key] = val
                    except ValueError:
                        pass
    except Exception as e:
        print(f"Warning: Could not load .env file: {e}")

def api_call_retry(func, *args, **kwargs):
    retries = 3
    for i in range(retries):
        result = func(*args, **kwargs)
        resp = result[0] if isinstance(result, tuple) else result
        if isinstance(resp, dict) and "error" in resp and "429" in str(resp.get("error")):
            time.sleep(5)
            continue
        return result
    return func(*args, **kwargs)

def sync_firefly_cache():
    """Refreshes the Firefly transaction files for matched accounts."""
    load_env()
    staging_dir = os.environ.get('FINANCE_STAGING_DIR')
    ff_url = os.environ.get('FIREFLY_URL')
    ff_token = os.environ.get('FIREFLY_TOKEN')

    ff_accounts_file = os.path.join(staging_dir, 'firefly-accounts.txt')
    with open(ff_accounts_file, 'r') as f:
        for line in f:
            parts = line.strip().split(',')
            ff_id, ff_name, s_guid = parts[0], parts[1], parts[2]
            print(f"Refreshing Firefly cache for {ff_name}...")
            all_ff = []
            page = 1
            while True:
                # Use make_request directly with paged endpoint
                resp = api_call_retry(firefly_api.make_request, ff_url, ff_token, f"accounts/{ff_id}/transactions?page={page}")
                
                # Check for empty response or non-dict
                if not isinstance(resp, dict):
                    print(f"Non-dict response on page {page} for {ff_name}: {resp}")
                    break
                    
                if "error" in resp: 
                    print(f"Error on page {page} for {ff_name}: {resp['error']}")
                    break
                data = resp.get('data', [])
                if not data: break
                for group in data:
                    for split in group.get('attributes', {}).get('transactions', []):
                        all_ff.append({
                            "firefly_transaction_id": group.get('id'),
                            "amount": split.get('amount'),
                            "date": split.get('date'),
                            "external_id": split.get('external_id'),
                            "description": split.get('description')
                        })
                if page >= resp.get('meta', {}).get('pagination', {}).get('total_pages', 1): break
                page += 1
            with open(os.path.join(staging_dir, f"{s_guid}-Firefly.txt"), 'w') as f:
                json.dump(all_ff, f, indent=2)

if __name__ == "__main__":
    sync_firefly_cache()
