.DEFAULT_GOAL := help

help:
	@grep '^[a-zA-Z]' $(MAKEFILE_LIST) | \
	sort | \
	awk -F ':.*?## ' 'NF==2 {printf "\033[36m  %-25s\033[0m %s\n", $$1, $$2}'

test:
	uv run pytest tests -vv --tb=short -s

### Format (Check only) ###

fmt-chk-black:
	@echo "## black (check) ##"
	@-uv run black . --check
	@echo

fmt-chk-autoflake:
	@echo "## autoflake (check) ##"
	@-uv run autoflake -r . --exclude venv --expand-star-imports --remove-unused-variables --remove-all-unused-imports
	@echo

fmt-chk-isort:
	@echo "## isort (check) ##"
	@-uv run isort . -c
	@echo

fmt-chk: ## Format (check)
fmt-chk:  fmt-chk-black fmt-chk-isort fmt-chk-autoflake

### Format ###

fmt-black:
	@echo "## black ##"
	@-uv run black .
	@echo

fmt-autoflake:
	@echo "## autoflake ##"
	@-uv run autoflake -vri . --exclude venv --expand-star-imports --remove-unused-variables --remove-all-unused-imports
	@echo

fmt-isort:
	@echo "## isort ##"
	@-uv run isort .
	@echo

fmt: ## Format
fmt:  fmt-black fmt-isort fmt-autoflake

### Linting ###

lint-bandit:
	@echo "## bandit ##"
	@-uv run bandit -r . -c "pyproject.toml"
	@echo

lint-flake8:
	@echo "## flake8 ##"
	@-uv run flake8 .
	@echo

lint-pydoc:
	@echo "## pydocstyle ##"
	@-uv run pydocstyle .
	@echo

lint-yaml:
	@echo "## yamllint ##"
	@-uv run yamllint .
	@echo ""

lint-mypy:
	@echo "## mypy ##"
	@-uv run mypy .
	@echo ""

lint: ## Lint
lint:  lint-bandit lint-flake8 lint-pydoc lint-yaml lint-mypy