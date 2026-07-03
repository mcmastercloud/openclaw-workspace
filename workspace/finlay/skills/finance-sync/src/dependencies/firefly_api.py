import os
import json
import sys
import urllib.request
import urllib.parse
import urllib.error

def make_request(base_url, token, endpoint, method="GET", data=None):
    url = f"{base_url.rstrip('/')}/api/v1/{endpoint.lstrip('/')}"
    headers = {
        "Authorization": f"Bearer {token}",
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

def list_accounts(base_url, token, type=None):
    endpoint = "accounts"
    if type:
        endpoint += f"?type={type}"
    return make_request(base_url, token, endpoint)

def create_transaction(base_url, token, data):
    return make_request(base_url, token, "transactions", method="POST", data=data)

if __name__ == "__main__":
    if len(sys.argv) < 4:
        # CLI usage: firefly_api.py <BASE_URL> <TOKEN> <command> [args...]
        sys.exit(1)
        
    base_url = sys.argv[1]
    token = sys.argv[2]
    cmd = sys.argv[3]
    
    if cmd == "list_accounts":
        type_filter = sys.argv[4] if len(sys.argv) > 4 else None
        print(json.dumps(list_accounts(base_url, token, type_filter), indent=2))
    elif cmd == "create_transaction":
        if sys.argv[4] == "-":
            data = json.load(sys.stdin)
        else:
            with open(sys.argv[4], 'r') as f:
                data = json.load(f)
        print(json.dumps(create_transaction(base_url, token, data), indent=2))
    elif cmd == "make_request":
        method = "GET"
        data = None
        endpoint = sys.argv[4]
        remaining = sys.argv[4:]
        if "-X" in remaining:
            idx = remaining.index("-X")
            method = remaining[idx+1]
        if "-d" in remaining:
            idx = remaining.index("-d")
            data = json.loads(remaining[idx+1])
        print(json.dumps(make_request(base_url, token, endpoint, method=method, data=data), indent=2))
