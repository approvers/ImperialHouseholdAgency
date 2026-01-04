DEV_COMPOSE_FILE=./compose.developer.yml
DEV_COMPOSE_COMMAND=docker compose -f $(DEV_COMPOSE_FILE)
DEV_APP_SERVICE=developer_app

TEST_COMPOSE_FILE=./compose.test.yml
TEST_COMPOSE_COMMAND=docker compose -f $(TEST_COMPOSE_FILE)

# ===== Docker Related =====
.PHONY: up
up:
	$(DEV_COMPOSE_COMMAND) up --build --remove-orphans

.PHONY: down
down:
	$(DEV_COMPOSE_COMMAND) down

.PHONY: ensure_up
ensure_up:
	@if [ -z "$$($(DEV_COMPOSE_COMMAND) ps -q)" ]; then \
		echo "Docker containers are not running. Starting them up..."; \
		$(MAKE) up; \
	else \
		echo "Docker containers are already running."; \
	fi

.PHONY: bash
bash: ensure_up
	@$(DEV_COMPOSE_COMMAND) exec $(DEV_APP_SERVICE) bash

# ===== Environment Related =====
.PHONY: sync
sync:
	uv sync --dev

# ===== Code Quality Related =====
.PHONY: format
format:
	uv run ruff format

.PHONY: format_check
format_check:
	uv run ruff format --check

.PHONY: lint
lint:
	uv run ruff check --fix

.PHONY: lint_check
lint_check:
	uv run ruff check

.PHONY: type_check
type_check:
	uv run ty check .

.PHONY: test
test:
	uv run pytest -s -v

.PHONY: test_on_docker
test_on_docker:
	$(TEST_COMPOSE_COMMAND) up --exit-code-from test_app --abort-on-container-exit

# ===== Migration Related =====
.PHONY: migrate
migrate:
	uv run alembic upgrade head
