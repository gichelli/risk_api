.PHONY: install test test-unit test-integration \
        smoke-test functional-test regression-test \
        e2e-test performance-test security-test \
        lint format run docker-build docker-run clean


IMAGE_NAME ?= risk-api
PORT ?= 8080


install:
	python3 -m pip install --upgrade pip
	pip install -e .


install-test:
	pip install -e ".[test]"


install-performance:
	pip install -e ".[performance]"


install-security:
	pip install -e ".[security]"



####################
# LOCAL DEVELOPMENT
####################

test:
	python3 -m pytest tests/unit


test-integration:
	python3 -m pytest tests/integration



####################
# DEV ENVIRONMENT
####################

smoke-test:
	python3 -m pytest tests/smoke



####################
# QA ENVIRONMENT
####################

functional-test:
	python3 -m pytest tests/functional


regression-test:
	python3 -m pytest tests/regression



####################
# STAGING ENVIRONMENT
####################

e2e-test:
	python3 -m pytest tests/e2e


performance-test:
	locust \
	-f tests/performace/locustfile.py \
	--headless \
	--users 10 \
	--spawn-rate 2 \
	--run-time 1m \
	--host $(STAGING_URL)


security-scan:
	python3 -m pytest tests/security