#!/bin/bash
set -e

/wait-for-it.sh $POSTGRES_HOST:$POSTGRES_PORT -t 60

/wait-for-it.sh $REDIS_HOST:$REDIS_PORT -t 60

cd /app

echo "Applying migrations..."
python manage.py migrate

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Creating superuser..."
python manage.py create_superuser_from_env

echo "Starting server..."
exec daphne -b 0.0.0.0 -p 8000 crud_website.asgi:application