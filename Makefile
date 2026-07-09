.PHONY: install test lint format run docker-build docker-run

APP_DIR=app/risk_api
IMAGE_NAME=risk-api

install:
	cd $(APP_DIR) && python -m pip install -e ".[dev]"

test:
	cd $(APP_DIR) && python -m pytest

lint:
	cd $(APP_DIR) && ruff check .

format:
	cd $(APP_DIR) && ruff format .

run:
	cd $(APP_DIR) && gunicorn --bind 0.0.0.0:8080 src.app:app

docker-build:
	docker build -t $(IMAGE_NAME):latest $(APP_DIR)

docker-run:
	docker run --rm -p 8080:8080 $(IMAGE_NAME):latest