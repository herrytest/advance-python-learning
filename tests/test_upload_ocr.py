import unittest
import requests
import os
import sys

class TestUploadOCR(unittest.TestCase):
    BASE_URL = "http://127.0.0.1:5000"
    USERNAME = "admin"
    PASSWORD = "123456"
    
    # Path to test image (relative to project root where we run tests)
    IMAGE_PATH = os.path.join("tests", "data", "test_image.png")

    def setUp(self):
        self.session = requests.Session()
        # Login first
        self.session.post(
            f"{self.BASE_URL}/", 
            data={"username": self.USERNAME, "password": self.PASSWORD}
        )

    def test_upload_image(self):
        """Test uploading an image and checking for OCR response"""
        if not os.path.exists(self.IMAGE_PATH):
            self.fail(f"Test image not found at {self.IMAGE_PATH}")

        with open(self.IMAGE_PATH, 'rb') as f:
            files = {'image': ('test_image_ocr.png', f, 'image/png')}
            response = self.session.post(f"{self.BASE_URL}/upload", files=files)
            
        self.assertEqual(response.status_code, 200)
        # Check if the page contains evidence of successful upload/processing
        # This depends on what the template renders, but usually 'Detected Text' or similar
        self.assertTrue(
            "Detected Text" in response.text or "EasyOCR" in response.text,
            "Response did not contain expected OCR output markers"
        )
        
    def test_upload_no_file(self):
        """Test uploading without a file"""
        response = self.session.post(f"{self.BASE_URL}/upload")
        # Flask usually returns 400 Bad Request if a required file part is missing
        # However, our code might handle it differently. Let's check.
        # If it just re-renders the template, it's 200.
        # But requests usually raise errors if file logic fails.
        # For now, just ensure it doesn't crash (500).
        self.assertNotEqual(response.status_code, 500)

if __name__ == '__main__':
    unittest.main()
