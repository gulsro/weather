#!/bin/bash

ls -la

echo "Checking for pending migrations..."
python manage.py makemigrations

echo "Applying migrations..."
python manage.py migrate

# echo "creating static folder"
# mkdir "/app/staticfiles/"

# echo "migrating static files"
# python manage.py collectstatic --noinput

echo "Starting Django server..."
exec python manage.py runserver 0.0.0.0:8000