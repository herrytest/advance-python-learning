"""
Test script to verify Django ORM integration.
Run this after installing Django dependencies.
"""

import os
import sys

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("=" * 60)
print("Testing Django ORM Integration")
print("=" * 60)

try:
    # Test 1: Setup Django
    print("\n1. Setting up Django...")
    import os
    import django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_settings')
    django.setup()
    print("   ✓ Django setup successful")
    
    # Test 2: Import models
    print("\n2. Testing models import...")
    from models import Gallery, Category, User
    print("   ✓ Models imported successfully")
    
    # Test 3: Test database connection
    print("\n3. Testing database connection...")
    from django.db import connection
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
    print("   ✓ Database connection successful")
    
    # Test 4: Test Category model
    print("\n4. Testing Category model...")
    categories = Category.objects.all()
    print(f"   ✓ Found {categories.count()} categories")
    for cat in categories:
        print(f"     - {cat.name}")
    
    # Test 5: Test Gallery model
    print("\n5. Testing Gallery model...")
    gallery_count = Gallery.objects.count()
    print(f"   ✓ Found {gallery_count} gallery items")
    
    # Test 6: Test User model
    print("\n6. Testing User model...")
    user_count = User.objects.count()
    print(f"   ✓ Found {user_count} users")
    
    # Test 7: Test db.py functions
    print("\n7. Testing db.py functions...")
    from db import get_categories, get_gallery_count, get_all_users
    
    cats = get_categories()
    print(f"   ✓ get_categories() returned {len(cats)} categories")
    
    count = get_gallery_count()
    print(f"   ✓ get_gallery_count() returned {count}")
    
    users = get_all_users()
    print(f"   ✓ get_all_users() returned {len(users)} users")
    
    print("\n" + "=" * 60)
    print("✅ All tests passed! Django ORM is working correctly.")
    print("=" * 60)
    print("\nYou can now restart your Flask application:")
    print("  python3 app.py")
    print("=" * 60)
    
except ImportError as e:
    print(f"\n❌ Import Error: {e}")
    print("\nPlease install Django dependencies first:")
    print("  bash install_django.sh")
    print("  OR")
    print("  pip install Django==5.0.1 mysqlclient==2.2.1")
    sys.exit(1)
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
