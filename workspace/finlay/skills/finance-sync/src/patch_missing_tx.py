import os
import sys
import json
import requests
from datetime import datetime

# Script to inject a single missing £10.99 transaction into Firefly III
# Transaction: 2026-04-19, £10.99, Google Play Apps, external_id: d17430c4-bd69-4771-b7e3-d3317ae0d777

def patch_transaction():
    ff_url = os.environ.get('FIREFLY_URL')
    ff_token = os.environ.get('FIREFLY_TOKEN')
    
    # ff_id for "Starling Space: Entertainment" is '5' (from firefly-accounts.txt file previously read)
    ff_id = '5'
    
    transaction = {
        "transactions": [{
            "type": "withdrawal",
            "date": "2026-04-19T05:22:23Z",
            "amount": "10.99",
            "description": "Google Play Apps",
            "source_id": ff_id,
            "destination_name": "Google Play",
            "external_id": "d17430c4-bd69-4771-b7e3-d3317ae0d777",
            "notes": "Manual reconciliation patch for missing reconciliation sync item"
        }]
    }
    
    print(f"Posting missing transaction to Firefly URL: {ff_url}...")
    
    try:
        response = requests.post(
            f"{ff_url.rstrip('/')}/api/v1/transactions",
            headers={
                "Authorization": f"Bearer {ff_token}",
                "Content-Type": "application/json",
                "Accept": "application/json"
            },
            json=transaction
        )
        response.raise_for_status()
        print(f"Success! Transaction added. Response: {response.status_code}")
    except Exception as e:
        print(f"FAILED to post transaction: {e}")
        sys.exit(1)

if __name__ == "__main__":
    patch_transaction()