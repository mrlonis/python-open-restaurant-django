#!/bin/bash
poetry run flake8 api project manage.py
poetry run pylint api project manage.py
docker compose up --build --pull always --remove-orphans -V --wait
poetry run python manage.py migrate
poetry run python manage.py test
