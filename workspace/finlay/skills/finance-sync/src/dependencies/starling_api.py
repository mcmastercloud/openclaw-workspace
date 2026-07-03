import os
import json
import sys
import urllib.request
import urllib.parse
import urllib.error

def make_request(token, endpoint, method="GET", data=None):
    if endpoint.startswith("http"):
        url = endpoint
    else:
        url = f"https://api.starlingbank.com/api/v2/{endpoint.lstrip('/')}"
        
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
        "User-Agent": "OpenClaw-Finlay"
    }
    
    req = urllib.request.Request(url, headers=headers, method=method)
    if data:
        req.add_header("Content-Type", "application/json")
        req.data = json.dumps(data).encode("utf-8")
        
    try:
        with urllib.request.urlopen(req) as response:
            resp_data = json.loads(response.read().decode('utf-8'))
            next_link = None
            link_header = response.getheader('Link')
            if link_header:
                links = link_header.split(',')
                for link in links:
                    if 'rel="next"' in link:
                        next_link = link.split(';')[0].strip(' <>')
            return resp_data, next_link
    except urllib.error.HTTPError as e:
        return {"error": f"HTTP {e.code}", "details": e.read().decode('utf-8')}, None
    except Exception as e:
        return {"error": str(e)}, None

def list_accounts(token):
    data, _ = make_request(token, "accounts")
    return data

def get_balance(token, account_uid):
    data, _ = make_request(token, f"accounts/{account_uid}/balance")
    return data

def list_transactions(token, account_uid, category_uid, start_date=None):
    endpoint = f"feed/account/{account_uid}/category/{category_uid}"
    if start_date:
        endpoint += f"?changesSince={start_date}"
    
    all_items = []
    current_url = endpoint
    seen_urls = set()
    
    while current_url and current_url not in seen_urls:
        seen_urls.add(current_url)
        data, next_url = make_request(token, current_url)
        
        if not isinstance(data, dict) or "error" in data:
            break
            
        items = data.get('feedItems', [])
        all_items.extend(items)
        current_url = next_url
            
    return {"feedItems": all_items}

if __name__ == "__main__":
    if len(sys.argv) < 3:
        # CLI usage: starling_api.py <ACCOUNT_TYPE|TOKEN> <command> [args...]
        sys.exit(1)
        
    first_arg = sys.argv[1]
    
    # Check if first arg is a known account type to load Token from .env
    if first_arg in ['current', 'joint', 'business']:
        if os.path.exists('.env'):
            with open('.env') as f:
                for line in f:
                    if '=' in line and not line.startswith('#'):
                        k, v = line.strip().split('=', 1)
                        os.environ[k] = v
        
        env_map = {
            'current': 'STARLING_PERSONAL_ACCOUNT_TOKEN',
            'joint': 'STARLING_JOINT_ACCOUNT_TOKEN',
            'business': 'STARLING_BUSINESS_ACCOUNT_TOKEN'
        }
        token = os.environ.get(env_map[first_arg])
        if not token:
            print(f"Error: Token for {first_arg} not found in .env")
            sys.exit(1)
    else:
        # Fallback: assume first_arg is the literal token
        token = first_arg
        
    cmd = sys.argv[2]
    
    if cmd == "list_accounts":
        print(json.dumps(list_accounts(token), indent=2))
    elif cmd == "get_balance":
        print(json.dumps(get_balance(token, sys.argv[3]), indent=2))
    elif cmd == "list_transactions":
        start_date = sys.argv[5] if len(sys.argv) > 5 else None
        print(json.dumps(list_transactions(token, sys.argv[3], sys.argv[4], start_date), indent=2))
    elif cmd == "make_request":
        # Raw request: starling_api.py <token> make_request <endpoint> [method] [json_data]
        method = sys.argv[4] if len(sys.argv) > 4 else "GET"
        data = json.loads(sys.argv[5]) if len(sys.argv) > 5 else None
        resp, _ = make_request(token, sys.argv[3], method=method, data=data)
        print(json.dumps(resp, indent=2))
