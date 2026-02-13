import requests
import os

# Configuration
BASE_URL = "http://127.0.0.1:5000"
USERNAME = "admin"
PASSWORD = "123456"
# Use a known existing image
IMAGE_PATH = "/home/hiren/python-learn/myproject/static/hair_assets/male/1.png"

def test_upload():
    session = requests.Session()
    
    # 1. Login
    print("Logging in...")
    login_url = f"{BASE_URL}/"
    response = session.post(login_url, data={"username": USERNAME, "password": PASSWORD})
    
    if "Dashboard" not in response.text and response.url != f"{BASE_URL}/dashboard":
        # Check if we were redirected to dashboard
        if response.status_code == 200 and "Login" in response.text:
            print("FAILED: Login failed")
            return
    
    print("Login successful.")

    # 2. Upload
    print(f"Uploading {IMAGE_PATH}...")
    upload_url = f"{BASE_URL}/upload"
    
    if not os.path.exists(IMAGE_PATH):
        print(f"ERROR: Image not found at {IMAGE_PATH}")
        return

    with open(IMAGE_PATH, 'rb') as f:
        files = {'image': ('test_image.png', f, 'image/png')}
        # data = {'category_id': 1} # Default
        
        # We need to simulate the AJAX request or form submit
        response = session.post(upload_url, files=files)
    
    if response.status_code == 200:
        if "Detected Text" in response.text or "EasyOCR" in response.text or "upload.html" in response.url:
             print("SUCCESS: Upload processed.")
             if "Detected Text" in response.text:
                 print("OCR Output found in response.")
             else:
                 print("Check if OCR output is displayed in the page.")
        else:
            print("WARNING: Upload succeeded but unexpected response content.")
            # print(response.text[:500])
    else:
        print(f"FAILED: Upload returned status {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    test_upload()
