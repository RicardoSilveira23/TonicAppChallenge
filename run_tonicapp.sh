#!/bin/sh
export DJANGO_SETTINGS_MODULE=api.settings.development

python manage.py makemigrations
python manage.py migrate
python manage.py runserver $1