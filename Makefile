include .python-environment

#################################################################################
# GAMEPLAY                                                                      #
#################################################################################

## Create a chess game.
.DEFAULT_GOAL := game
.PHONY: game
game: .venv/bin/activate
	${PYTHON_INTERPRETER} -m chess

.PHONY: self_play
self_play: .venv/bin/activate
	${PYTHON_INTERPRETER} -m chess --self_play True

#################################################################################
# DEVELOPMENT                                                                   #
#################################################################################

## Used to create a virtual environment for development.
.venv/bin/activate: .python-environment requirements.txt
	rm -rf .venv
	${PYTHON_INTERPRETER} -c 'import sys; assert sys.version_info.major == ${PYTHON_MAJOR_VERSION} and sys.version_info.minor == ${PYTHON_MINOR_VERSION}'
	${PYTHON_INTERPRETER} -m pip install --upgrade pip
	${PYTHON_INTERPRETER} -m venv .venv
	. .venv/bin/activate; \
		pip install -r requirements.txt

## Delete all compiled Python files.
.PHONY: clean 
clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete

## Lint using flake8.
.PHONY: lint 
lint: .venv/bin/activate
	. .venv/bin/activate; \
		${PYTHON_INTERPRETER} -m flake8 chess 

## Run tests.
.PHONY: tests 
tests: .venv/bin/activate clean lint
	. .venv/bin/activate; \
		${PYTHON_INTERPRETER} -m pytest tests -x --log-cli-level=ERROR
