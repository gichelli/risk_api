.PHONY: install test lint format run docker-build

install:
	cd app/demo && pip install -e ".[dev]"

test:
	cd app/demo && pytest

lint:
	cd app/demo && ruff check .

format:
	cd app/demo && ruff format .

run:
	cd app/demo && gunicorn --bind 0.0.0.0:8080 src.app:app

docker-build:
	cd app/demo && docker build -t platform-demo .