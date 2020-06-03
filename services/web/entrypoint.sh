#!/bin/sh

python manage.py create_db

exec "$@"