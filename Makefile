.PHONY: install test lint format run docker-build docker-run clean


IMAGE_NAME ?= risk-api
PORT ?= 8080


install:
	python -m pip install --upgrade pip
	pip install -e ".[dev]"


test:
	python -m pytest


lint:
	ruff check .


format:
	ruff format .


run:
	gunicorn \
	--bind 0.0.0.0:$(PORT) \
	risk_api.app:app


docker-build:
	docker build \
	-t $(IMAGE_NAME):latest .


docker-run:
	docker run \
	--rm \
	-p $(PORT):8080 \
	$(IMAGE_NAME):latest


clean:
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -delete