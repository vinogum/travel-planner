.PHONY: run migrate env setup lint test shell superuser

run:
	uv run python manage.py runserver

migrate:
	uv run python manage.py makemigrations
	uv run python manage.py migrate

env:
	cp -n .env.example .env || true

setup: env
	uv sync
	uv run python manage.py migrate

lint:
	uv run ruff check . --fix
	uv run ruff format .

test:
	uv run python manage.py test

shell:
	uv run python manage.py shell

superuser:
	uv run python manage.py createsuperuser
