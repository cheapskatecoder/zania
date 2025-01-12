#!/usr/bin/env bash

echo "Applying migrations..."
python manage.py migrate

echo "Starting Django server in the background..."
python manage.py runserver 0.0.0.0:8000 &

# Wait a bit for the server to come up
sleep 5

echo "Populating data via curl..."
/app/docker/create_products.sh

echo "All done! Keeping the container alive..."
# Keep container running indefinitely, or you could just do:
# exec python manage.py runserver 0.0.0.0:8000
tail -f /dev/null
