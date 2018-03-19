#!/bin/sh

#Collect static resources
echo "Collecting static assets"
python manage.py collectstatic --settings=$PROJECT_SETTINGS --noinput

# Start server
echo "Starting server"
python manage.py runserver --settings=$PROJECT_SETTINGS 0.0.0.0:8000
