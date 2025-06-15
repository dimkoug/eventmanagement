#!/bin/sh

echo "runnning"
python manage.py runserver 0.0.0.0:8000
#python manage.py collectstatic --noinput && gunicorn todoproject.wsgi:application -b 0.0.0.0:8000