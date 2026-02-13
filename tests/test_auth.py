import unittest
import requests
import sys
import os

# Add parent directory to path to allow importing app if needed, 
# though we are mostly testing via requests to the running server.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class TestAuth(unittest.TestCase):
    BASE_URL = "http://127.0.0.1:5000"
    USERNAME = "admin"
    PASSWORD = "123456"

    def setUp(self):
        self.session = requests.Session()

    def test_login_success(self):
        """Test valid login credentials"""
        response = self.session.post(
            f"{self.BASE_URL}/", 
            data={"username": self.USERNAME, "password": self.PASSWORD}
        )
        self.assertEqual(response.status_code, 200)
        # Check if redirected to dashboard or content contains dashboard elements
        # Flask redirect might return 200 if follow_redirects is True (default in requests)
        self.assertIn("Dashboard", response.text)
        self.assertIn("Sign out", response.text)

    def test_login_failure(self):
        """Test invalid login credentials"""
        response = self.session.post(
            f"{self.BASE_URL}/", 
            data={"username": "wrong", "password": "wrong"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("Invalid Credentials", response.text)

    def test_logout(self):
        """Test logout functionality"""
        # Login first
        self.session.post(
            f"{self.BASE_URL}/", 
            data={"username": self.USERNAME, "password": self.PASSWORD}
        )
        
        # Logout
        response = self.session.get(f"{self.BASE_URL}/logout")
        self.assertEqual(response.status_code, 200)
        
        # Verify we are back at login page
        self.assertIn("Login", response.text)
        
        # Verify access to dashboard is restricted
        response = self.session.get(f"{self.BASE_URL}/dashboard")
        self.assertIn("Login", response.text) # Should redirect to login

if __name__ == '__main__':
    unittest.main()
