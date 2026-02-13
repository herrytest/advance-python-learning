import unittest
import requests
import time

class TestUsersFlask(unittest.TestCase):
    BASE_URL = "http://127.0.0.1:5000"
    USERNAME = "admin"
    PASSWORD = "123456"

    def setUp(self):
        self.session = requests.Session()
        # Login first
        self.session.post(
            f"{self.BASE_URL}/", 
            data={"username": self.USERNAME, "password": self.PASSWORD}
        )

    def test_create_user(self):
        """Test creating a user via Flask form"""
        new_user = {
            "action": "create",
            "name": f"TestUser_{int(time.time())}",
            "email": f"test_{int(time.time())}@example.com",
            "password": "password123"
        }
        
        response = self.session.post(f"{self.BASE_URL}/users", data=new_user)
        if response.status_code != 200:
            print(f"\nDEBUG ERROR RESPONSE: {response.status_code}\n{response.text[:1000]}")
        self.assertEqual(response.status_code, 200)
        
        # Check for success message
        self.assertIn("User created successfully!", response.text)
        
        # Verify user is in the list
        self.assertIn(new_user["name"], response.text)
        self.assertIn(new_user["email"], response.text)

    def test_create_duplicate_user(self):
        """Test creating a user with existing email (should fail)"""
        # Create a user first
        unique_id = int(time.time())
        email = f"duplicate_{unique_id}@example.com"
        
        user_data = {
            "action": "create",
            "name": "Duplicate User",
            "email": email,
            "password": "password123"
        }
        
        # First creation
        self.session.post(f"{self.BASE_URL}/users", data=user_data)
        
        # Second creation (should fail)
        response = self.session.post(f"{self.BASE_URL}/users", data=user_data)
        if response.status_code != 200:
            print(f"\nDEBUG ERROR RESPONSE: {response.status_code}\n{response.text[:1000]}")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Name or Email already exists!", response.text)

if __name__ == '__main__':
    unittest.main()
