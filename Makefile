.PHONY: format lint test clean

format:
	isort src/
	yapf -i -r src/ --exclude '**/.*'

lint:
	isort --check-only src/
	yapf --diff -r src/ --exclude '**/.*'
	mypy src/

test:
	pytest

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
