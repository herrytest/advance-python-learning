
import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_settings')
django.setup()

from db import get_gallery_items

try:
    items = get_gallery_items()
    print(f"Successfully retrieved {len(items)} items.")
    if len(items) > 0:
        item = items[0]
        print(f"First item timestamp type: {type(item['timestamp'])}")
        print(f"First item timestamp value: {item['timestamp']}")
        if isinstance(item['timestamp'], str):
            print("PASS: Timestamp is a string.")
        else:
            print("FAIL: Timestamp is not a string.")
    else:
        print("No items to check, but function ran successfully.")
except Exception as e:
    print(f"FAIL: Error retrieving items: {e}")
