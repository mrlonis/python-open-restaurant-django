#!/bin/bash
docker compose up --build --pull postgresql --remove-orphans -V --wait
poetry run python manage.py migrate
poetry run python manage.py test
