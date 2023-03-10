# python-open-restaurant-django

Demo API using Django with one route that takes a datetime string and returns open restaurants, if any.

The Django project was initialized using the command:

```sh
django-admin startproject project .
```

The api application was created using the command:

```sh
python manage.py startapp api
```

## Table of Contents

- [python-open-restaurant-django](#python-open-restaurant-django)
  - [Table of Contents](#table-of-contents)
  - [Pre-requisites](#pre-requisites)
    - [.env File](#env-file)
    - [Required Build Packages](#required-build-packages)
    - [Docker](#docker)
  - [Migrate the Database](#migrate-the-database)
  - [Linting](#linting)
  - [Testing](#testing)

## Pre-requisites

### .env File

Create a .env file in the root directory of your project based off of the `.env.sample` file.

### Required Build Packages

```shell
sudo apt-get install gcc libpq-dev python3-dev
```

### Docker

Install Docker and run the following command to startup the database/api in Docker:

```sh
docker compose up --build --pull postgresql --remove-orphans -V --wait
```

## Migrate the Database

```shell
poetry run python manage.py migrate
```

## Linting

To lint the project, run the following commands:

```shell
poetry run flake8 api project manage.py
poetry run pylint api project manage.py
```

## Testing

To run the tests, be sure you have ran the [Docker Compose Command](#docker), then run the following command:

```sh
poetry run python manage.py test
```
