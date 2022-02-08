PROJECT_NAME := $(shell pwd)
VIRTUAL_ENV_DIR := .venv
VIRTUAL_ENVIRONMENT := $(CURDIR)/$(VIRTUAL_ENV_DIR)
LOCAL_PYTHON := $(VIRTUAL_ENVIRONMENT)/bin/python3

define HELP
Manage $(PROJECTNAME). Usage:

make run        - Run $(PROJECT_NAME).
make install    - Create virtual env, install dependencies and create symlinks.
make format     - Format the code, using black.
make lint       - Lint with flake8.
make clean      - Remove cached files and lock files.
endef
export HELP

.PHONY: run install format lint clean help


env: .venv/bin/python3


all help:
	@echo "$$HELP"


.PHONY: install
install:
	echo $(VIRTUAL_ENV_DIR)
	if [ ! -d "./.venv" ]; then virtualenv $(VIRTUAL_ENV_DIR); fi
	chmod u+x $(VIRTUAL_ENV_DIR)/bin/activate
	. $(VIRTUAL_ENV_DIR)/bin/activate && python -m pip install --upgrade pip setuptools wheel && python -m pip install -r requirements.txt
	ln -sfn ../src src

.PHONY: run
run: env
	$(shell . .venv/bin/activate && python src/app.py)


.PHONY: format
format: env
	black .


.PHONY: lint
lint:
	flake8 src --count \
			--show-source \
			--statistics


.PHONY: clean
clean:
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -delete
	find . -name 'poetry.lock' -delete
	find . -name 'Pipefile.lock' -delete
	find . -name '*.log' -delete
	find . -wholename 'logs/*.json' -delete
	find . -wholename '.pytest_cache' -delete
	find . -wholename '**/.pytest_cache' -delete
	find . -wholename './logs/*.json' -delete
	find . -wholename '**/.webassets-cache/' -delete
	find . -wholename './logs' -delete
