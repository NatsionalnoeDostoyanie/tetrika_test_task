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
	cd src/task1 && uv run --no-sync python solution.py

run-task2:
	cd src/task2 && uv run --no-sync python solution.py

run-task3:
	cd src/task3 && uv run --no-sync python solution.py

run-tests:
	uv run pytest
