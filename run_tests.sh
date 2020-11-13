#!/bin/sh
export DJANGO_SETTINGS_MODULE=api.settings.development
black footballleagues api 
coverage run manage.py test --noinput footballleagues -v 2
coverage html