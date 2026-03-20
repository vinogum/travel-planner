.PHONY: run migrate env setup lint test shell superuser \
       up down build logs restart

# ── Local ─────────────────────────────────────────────

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

# ── Docker ────────────────────────────────────────────

up:
	docker compose up -d

down:
	docker compose down

build:
	docker compose up -d --build

logs:
	docker compose logs -f

restart:
	docker compose restart
