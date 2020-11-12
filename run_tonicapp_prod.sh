#!/bin/sh
export DJANGO_SETTINGS_MODULE=api.settings.production

echo "Django Database Migration process"
python manage.py makemigrations footballleagues
python manage.py migrate

echo "Collecting Django static files"
python manage.py collectstatic --noinput

echo "Run Server"
python manage.py runserver $1

"$@"