.PHONY: help install test clean lint format type-check quality run dev setup-db sample-data

# Default target
help:
	@echo "Available commands:"
	@echo "  help         Show this help message"
	@echo "  install      Install dependencies"
	@echo "  setup-db     Initialize database and load sample data"
	@echo "  sample-data  Load sample quotes into database"
	@echo "  run          Run the development server"
	@echo "  dev          Setup development environment and run server"
	@echo "  test         Run tests"
	@echo "  test-cov     Run tests with coverage"
	@echo "  lint         Run flake8 linting"
	@echo "  format       Format code with black and isort"
	@echo "  type-check   Run mypy type checking"
	@echo "  quality      Run all quality checks (format, lint, type-check, test)"
	@echo "  clean        Clean up cache files and artifacts"

# Installation
install:
	pip install -r requirements.txt

# Database setup
setup-db:
	python manage_db.py init
	python manage_db.py sample

sample-data:
	python manage_db.py sample

# Development
run:
	python app.py

dev: install setup-db run

# Testing
test:
	pytest

test-cov:
	pytest --cov=app --cov-report=term-missing --cov-report=html

# Code quality
lint:
	flake8 .

format:
	black .
	isort .

type-check:
	mypy .

quality: format lint test

# Cleanup
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .coverage htmlcov/ .pytest_cache/ .mypy_cache/

# Docker commands (if using Docker)
docker-build:
	docker build -t futurama-quotes .

docker-run:
	docker run -p 5000:5000 futurama-quotes

# Production deployment helpers
prod-deps:
	pip install gunicorn

prod-run:
	gunicorn "app:create_app()" --bind 0.0.0.0:8000 --workers 4