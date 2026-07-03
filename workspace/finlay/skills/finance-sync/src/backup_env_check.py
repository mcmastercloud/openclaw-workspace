import os
import requests

def test_api():
    manager_url = os.environ.get('DOCKER1_MANAGER_URL')
    manager_token = os.environ.get('DOCKER1_MANAGER_TOKEN')
    print(f"URL: {manager_url}")
    print(f"Token present: {bool(manager_token)}")
    try:
        response = requests.post(
            manager_url,
            headers={
                "Authorization": f"Bearer {manager_token}",
                "Content-Type": "application/json"
            },
            json={"command": "list-backups"},
            verify=False
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_api()
