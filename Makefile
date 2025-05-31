.PHONY: install-base install-full lint format-code run-task1 run-task2 run-task3 run-tests

install-base:
	uv sync --no-dev

install-full:
	uv sync --all-groups

lint:
	uv run --no-sync mypy .

format-code:
	uv run --no-sync autoflake . && uv run --no-sync isort . && uv run --no-sync black .

run-task1:
	uv run --no-sync src/task1/solution.py

run-task2:
	uv run --no-sync src/task2/solution.py

run-task3:
	uv run --no-sync src/task3/solution.py

run-tests:
	uv run pytest
