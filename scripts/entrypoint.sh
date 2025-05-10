#!/bin/bash
set -e

echo "Applying database migrations..."
poetry run python manage.py migrate

echo "Loading fixtures..."
python manage.py loaddata sample_cv.json

echo "Starting server..."
exec "$@"
