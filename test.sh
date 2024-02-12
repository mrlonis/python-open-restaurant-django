#!/bin/bash
docker compose up --build --pull always --remove-orphans -V --wait
poetry run python manage.py migrate
poetry run python manage.py test
