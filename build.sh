#!/usr/bin/env bash
set -o errexit

echo "=== Starting Build Process ==="

# Install dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py migrate --no-input

# Load initial products
echo "=== Loading initial products ==="
python manage.py load_products

# Collect static files
python manage.py collectstatic --no-input

echo "=== Build Complete ==="
