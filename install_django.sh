#!/bin/bash
# Install Django and mysqlclient dependencies

echo "Installing Django ORM dependencies..."
pip install Django==5.0.1 mysqlclient==2.2.1

echo ""
echo "Installation complete!"
echo ""
echo "To test the Django ORM setup, run:"
echo "  python -c 'import django_settings; from models import Gallery, Category, User; print(\"Django ORM setup successful!\")'"
