.PHONY: help setup demo test lint fmt type verify clean

VENV ?= .venv
PY ?= $(VENV)/bin/python
PIP ?= $(VENV)/bin/pip

help:
	@echo "Targets:"
	@echo "  setup  - create venv + install deps"
	@echo "  demo   - run end-to-end demo (writes artifacts/)"
	@echo "  test   - run unit + integration tests"
	@echo "  lint   - ruff check"
	@echo "  fmt    - ruff format"
	@echo "  type   - mypy type checks"
	@echo "  verify - fmt-check + lint + type + test + smoke"
	@echo "  clean  - remove artifacts and caches"

$(VENV)/bin/activate:
	python3 -m venv $(VENV)

setup: $(VENV)/bin/activate
	@set -e; \
	if command -v uv >/dev/null 2>&1; then \
		uv pip install -e ".[dev]" --python $(PY); \
	else \
		$(PIP) install -U pip; \
		$(PIP) install -e ".[dev]"; \
	fi

demo:
	$(PY) -m okml demo

test:
	$(PY) -m pytest

lint:
	$(PY) -m ruff check .

fmt:
	$(PY) -m ruff format .

type:
	$(PY) -m mypy .

verify:
	$(PY) -m ruff format --check .
	$(PY) -m ruff check .
	$(PY) -m mypy .
	$(PY) -m pytest
	bash scripts/smoke_test.sh

clean:
	rm -rf artifacts .pytest_cache .mypy_cache .ruff_cache htmlcov .coverage coverage.xml

