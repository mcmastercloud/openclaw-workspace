import os
import json
import urllib.request
import urllib.error

def make_request(token, endpoint, method="GET", data=None):
    url = f"https://api.notion.com/v1/{endpoint.lstrip('/')}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }
    
    req = urllib.request.Request(url, headers=headers, method=method)
    if data:
        req.data = json.dumps(data).encode("utf-8")
        
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        return {"error": f"HTTP {e.code}", "details": e.read().decode('utf-8')}
    except Exception as e:
        return {"error": str(e)}

def update_block(token, block_id, payload):
    return make_request(token, f"blocks/{block_id}", method="PATCH", data=payload)
