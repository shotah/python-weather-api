PIPENV_IGNORE_VIRTUALENVS=1
export AWS_SAM_STACK_NAME=adobe-app
INTEGRATION_DIR = ./integration_tests

all: hooks install-dev lint test

PHONY: clean
clean:
# pipenv clean || echo "no environment found to clean"
	pipenv run python -c "import os; os.remove('requirements.txt')" || echo "no lock file to remove"
	pipenv run python -c "import os; os.remove('Pipfile.lock')" || echo "no lock file to remove"
	pipenv --rm || echo "no environment found to remove"

PHONY: lint
lint:
	pre-commit run --all-files

PHONY: test
test:
	pipenv run pytest --new-first

PHONY: test-failed
test-failed:
	pipenv run pytest --last-failed --exitfirst

PHONY: install
install:
	pipenv install

PHONY: install-dev
install-dev:
	pipenv install --dev

PHONY: sync
sync:
	pipenv sync

PHONY: sync-dev
sync-dev:
	pipenv sync --dev

PHONY: build
build:
	pipenv run pip freeze > requirements.txt
	sam build -c --use-container

# TODO: Not implemented, this is to really deploy it to AWS Lambda
# PHONY: deploy
# deploy: build
# 	sam deploy --guided

PHONY: start
start: build
	sam local start-api --env-vars env.json

PHONY: integration
integration: build
	sam local invoke "Function" -e integration_tests/default_event.json
	sam local invoke "Function" -e integration_tests/weather_event.json

# TODO: strip leading "./"
# returns ./integration_tests/event.json vs integration_tests/event.json
# PHONY: folder-based-integration
# folder-based-integration:
# $(foreach file, $(wildcard $(INTEGRATION_DIR)/*), sam local invoke "Function" -e $(file);)

PHONY: hooks
hooks:
	pip install pre-commit
	pre-commit install
