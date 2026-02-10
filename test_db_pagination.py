
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_settings')
django.setup()

try:
    from db import get_all_users
    print("Testing get_all_users...")
    result = get_all_users(page=1, page_size=10)
    print("Success!")
    print(f"Total: {result['total']}")
    print(f"Users count: {len(result['users'])}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
