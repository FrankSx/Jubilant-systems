.PHONY: help install test lint clean docker-build docker-run generate

help:
	@echo "Adversarial ML Testing Suite - Available commands:"
	@echo "  make install      - Install dependencies"
	@echo "  make test         - Run all tests"
	@echo "  make lint         - Run linting"
	@echo "  make generate     - Generate adversarial content"
	@echo "  make docker-build - Build Docker image"
	@echo "  make docker-run   - Run in Docker container"
	@echo "  make clean        - Clean generated files"

install:
	pip install -r requirements.txt
	pip install -e .

test:
	pytest tests/ -v --cov=. --cov-report=term-missing

lint:
	flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

generate:
	python -m adversarial_ml_tester generate -c 100 -o output/profiles.json --verbose

docker-build:
	docker build -t adversarial-ml-tester:latest .

docker-run:
	docker run --rm -v $(PWD)/output:/app/output adversarial-ml-tester:latest generate -c 100

clean:
	rm -rf __pycache__ .pytest_cache *.pyc
	rm -rf output/*.json reports/*.html
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
