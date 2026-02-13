import requests
import sys

BASE_URL = "http://127.0.0.1:8000"

def test_api():
    print(f"Testing FastAPI at {BASE_URL}...")
    
    # 1. Root
    try:
        resp = requests.get(f"{BASE_URL}/")
        print(f"Root: {resp.status_code} - {resp.json()}")
    except Exception as e:
        print(f"FATAL: Cannot connect to FastAPI: {e}")
        sys.exit(1)

    # 2. Create User
    new_user = {
        "name": "APITestUser",
        "email": "apitest@example.com",
        "password": "apipassword",
        "role_id": 2
    }
    print(f"Creating user: {new_user['email']}")
    resp = requests.post(f"{BASE_URL}/api/users", json=new_user)
    print(f"Create User: {resp.status_code}")
    
    user_id = None
    if resp.status_code == 201:
        user_id = resp.json().get("id")
        print(f"User created with ID: {user_id}")
    elif resp.status_code == 400:
        print("User likely already exists. Trying to find it...")
    
    # 3. Get All Users
    print("Getting all users...")
    resp = requests.get(f"{BASE_URL}/api/users")
    print(f"Get Users: {resp.status_code}")
    if resp.status_code == 200:
        users = resp.json().get("items", [])
        print(f"Found {len(users)} users.")
        
        # If we didn't create a new user (because it existed), find it
        if not user_id:
            for u in users:
                if u['email'] == new_user['email']:
                    user_id = u['id']
                    print(f"Found existing user ID: {user_id}")
                    break
    
    # 4. Get User By ID
    if user_id:
        print(f"Getting user {user_id}...")
        resp = requests.get(f"{BASE_URL}/api/users/{user_id}")
        print(f"Get User: {resp.status_code}")
        if resp.status_code == 200:
            print(f"User Name: {resp.json().get('name')}")

    # 5. Delete User
    if user_id:
        print(f"Deleting user {user_id}...")
        resp = requests.delete(f"{BASE_URL}/api/users/{user_id}")
        print(f"Delete User: {resp.status_code}")
        if resp.status_code == 200:
            print("User deleted.")
    else:
        print("Skipping delete (no user ID).")

if __name__ == "__main__":
    test_api()
