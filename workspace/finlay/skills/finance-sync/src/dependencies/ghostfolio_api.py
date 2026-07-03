import os
import json
import urllib.request
import urllib.error
from datetime import datetime

def make_request(base_url, token, endpoint, method="GET", data=None):
    url = f"{base_url.rstrip('/')}/api/v1/{endpoint.lstrip('/')}"
    # Use Access Token to get a Bearer token first
    auth_url = f"{base_url.rstrip('/')}/api/v1/auth/anonymous"
    auth_payload = json.dumps({"accessToken": token}).encode("utf-8")
    auth_req = urllib.request.Request(auth_url, data=auth_payload, headers={"Content-Type": "application/json"}, method="POST")
    
    try:
        with urllib.request.urlopen(auth_req) as auth_resp:
            bearer_token = json.loads(auth_resp.read().decode())["authToken"]
    except Exception as e:
        return {"error": f"Auth failed: {str(e)}"}

    headers = {
        "Authorization": f"Bearer {bearer_token}",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    
    req = urllib.request.Request(url, headers=headers, method=method)
    if data:
        req.data = json.dumps(data).encode("utf-8")
        
    try:
        with urllib.request.urlopen(req) as response:
            content = response.read().decode('utf-8')
            if not content:
                return {"success": True}
            return json.loads(content)
    except urllib.error.HTTPError as e:
        return {"error": f"HTTP {e.code}", "details": e.read().decode('utf-8')}
    except Exception as e:
        return {"error": str(e)}

def update_account(base_url, token, account, balance):
    account_id = account['id']
    payload = {
        "balance": balance,
        "comment": f"Synchronised by Finlay on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "currency": account.get('currency', 'GBP'),
        "id": account_id,
        "name": account.get('name'),
        "platformId": account.get('platformId')
    }
    # Correcting Endpoint for Ghostfolio Account Update (v1)
    return make_request(base_url, token, f"account/{account_id}", method="PUT", data=payload)

def get_accounts(base_url, token):
    return make_request(base_url, token, "account")
