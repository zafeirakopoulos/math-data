#!/bin/bash

python /app/manage.py recreate_db
python /app/manage.py runserver