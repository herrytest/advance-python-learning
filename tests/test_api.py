import unittest
import requests
import time

class TestAPI(unittest.TestCase):
    BASE_URL = "http://127.0.0.1:8000"

    def test_root_endpoint(self):
        """Test root endpoint accessibility"""
        response = requests.get(f"{self.BASE_URL}/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("User Management API", response.text)

    def test_user_crud_api(self):
        """Test User CRUD via API"""
        unique_id = int(time.time())
        new_user = {
            "name": f"APIUser_{unique_id}",
            "email": f"api_{unique_id}@example.com",
            "password": "password123",
            "role_id": 2
        }
        
        # Create
        response = requests.post(f"{self.BASE_URL}/api/users", json=new_user)
        self.assertIn(response.status_code, [201, 400]) # 400 if exists (unlikely with timestamp)
        
        if response.status_code == 201:
            user_id = response.json().get("id")
            
            # Read (Get All)
            response = requests.get(f"{self.BASE_URL}/api/users")
            self.assertEqual(response.status_code, 200)
            self.assertIn(new_user["email"], response.text)
            
            # Read (Get One)
            response = requests.get(f"{self.BASE_URL}/api/users/{user_id}")
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json().get("email"), new_user["email"])
            
            # Delete
            response = requests.delete(f"{self.BASE_URL}/api/users/{user_id}")
            self.assertEqual(response.status_code, 200)
            
            # Verify Deletion
            response = requests.get(f"{self.BASE_URL}/api/users/{user_id}")
            self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
