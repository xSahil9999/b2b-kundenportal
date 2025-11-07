#!/bin/sh
set -e

echo "Waiting for database ${MYSQL_HOST:-db}:${MYSQL_PORT:-3306}..."
until nc -z ${MYSQL_HOST:-db} ${MYSQL_PORT:-3306}; do
  sleep 1
done

echo "Make migrations (if needed)"
python manage.py makemigrations accounts invoices tickets --noinput || true

echo "Apply migrations"
python manage.py migrate --noinput

echo "Collect static"
python manage.py collectstatic --noinput

echo "Starting server"
exec "$@"
