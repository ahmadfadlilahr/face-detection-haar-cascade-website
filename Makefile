# Makefile for development tasks
# Copyright (c) 2025, Ahmad Fadlilah (https://github.com/ahmadfadlilah)

.PHONY: help clean test lint format install dev-install

help:
	@echo "Available commands:"
	@echo "  clean      - Remove build artifacts"
	@echo "  test       - Run test suite"
	@echo "  lint       - Run linter (flake8)"
	@echo "  format     - Format code (black)"
	@echo "  install    - Install package"
	@echo "  dev-install - Install package in development mode"

clean:
	rm -rf build/ dist/ *.egg-info/ __pycache__/ .pytest_cache/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

test:
	pytest

lint:
	flake8 src tests

format:
	black src tests

install:
	pip install .

dev-install:
	pip install -e .
