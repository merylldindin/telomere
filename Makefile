TOML_FILES = `(find . -iname "*.toml" -not -path "./.venv/*")`
PYTHON_FILES = `(find . -iname "*.py" -not -path "./.venv/*")`

LOCAL_PORT = 8000

DOCKER_IMAGE = "merylldindin/telomere"

setup: ## Install developer experience
	yarn install
	yarn setup

setup-hard: ## Install developer experience with no cache
	rm -rf node_modules/
	yarn cache clean
	make setup

install: ## Install package dependencies
	poetry install --sync --no-root --with dev

install-hard: ## Install package dependencies from scratch
	rm -rf .venv/
	poetry lock --no-update
	make install

poetry-update: ## Upgrade poetry and dependencies
	poetry self update
	poetry run pip install --upgrade pip wheel setuptools
	poetry update

toml-sort: ## Sort pyproject.toml
	poetry run toml-sort --all --in-place $(TOML_FILES)

black: ## Run Black
	poetry run black --quiet --check $(PYTHON_FILES)

black-fix: ## Run Black with automated fix
	poetry run black --quiet $(PYTHON_FILES)

isort: ## Run Isort
	poetry run isort --check-only $(PYTHON_FILES)

isort-fix: ## Run Isort with automated fix
	poetry run isort $(PYTHON_FILES)

mypy: ## Run Mypy
	poetry run mypy $(PYTHON_FILES)

ruff: ## Run Ruff
	poetry run ruff $(PYTHON_FILES)

ruff-fix: ## Run Ruff with automated fix
	poetry run ruff --fix $(PYTHON_FILES)

pytest: ## Run Pytest
	poetry run pytest tests/

pytest-coverage: ## Run coverage report
	poetry run coverage run -m pytest tests/
	poetry run coverage report

start: ## Start telomere FastAPI application
	poetry run uvicorn --reload --log-level info --port $(LOCAL_PORT) main:telomere

build: ## Build Docker image
	docker buildx build --platform=linux/amd64 -t $(DOCKER_IMAGE) .

serve: ## Run Docker image
	make build
	docker run -it -p $(LOCAL_PORT):5000 $(DOCKER_IMAGE)

push: ## Push Docker image to Dockerhub
	make build
	docker push $(DOCKER_IMAGE)

help: ## Description of the Makefile commands
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-25s\033[0m %s\n", $$1, $$2}'
