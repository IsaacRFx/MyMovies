#!/bin/bash

cd /home/appuser/app/movies/

python manage.py migrate

exec "$@"