PYTHON ?= python3
VENV   := .venv
PY     := $(VENV)/bin/python

.PHONY: help venv test tables check clean

help:
	@echo "make venv    - create the virtualenv and install dev deps"
	@echo "make test    - run the model test suite"
	@echo "make tables  - regenerate docs/annex-a-parameters.md from the model"
	@echo "make check   - test + regenerate tables + verify they are up to date"
	@echo "make clean   - remove the virtualenv and caches"

$(VENV):
	$(PYTHON) -m venv $(VENV)
	$(VENV)/bin/pip install --quiet --upgrade pip
	$(VENV)/bin/pip install --quiet pytest

venv: $(VENV)

test: $(VENV)
	$(PY) -m pytest tests/ -q

tables: $(VENV)
	$(PY) tools/gen_tables.py > docs/annex-a-parameters.md
	@echo "regenerated docs/annex-a-parameters.md"

check: test
	@$(PY) tools/gen_tables.py > /tmp/annex-a-check.md
	@if diff -q /tmp/annex-a-check.md docs/annex-a-parameters.md >/dev/null; then \
		echo "annex A is up to date"; \
	else \
		echo "ERROR: docs/annex-a-parameters.md is stale. Run 'make tables'."; \
		diff /tmp/annex-a-check.md docs/annex-a-parameters.md | head -20; \
		exit 1; \
	fi

clean:
	rm -rf $(VENV) .pytest_cache
	find . -name __pycache__ -type d -exec rm -rf {} +
