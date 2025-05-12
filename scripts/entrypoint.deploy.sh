#!/bin/bash
set -e

echo "Applying database migrations..."
poetry run python manage.py migrate

echo "Loading fixtures..."
poetry run python manage.py loaddata sample_cv.json

echo "Starting Gunicorn server..."
poetry run gunicorn CVProject.wsgi:application --bind 0.0.0.0:8000
