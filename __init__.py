"""
Initialize Django ORM for use with Flask application.
This module sets up Django's ORM without running a full Django project.
"""

import os
import django
from django.conf import settings

# Configure Django settings
if not settings.configured:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_settings')
    django.setup()
