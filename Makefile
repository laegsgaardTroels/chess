include .python-environment

#################################################################################
# COMMANDS                                                                      #
#################################################################################

## Delete all compiled Python files
.PHONY: clean 
clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete

## Lint using flake8
.PHONY: lint 
lint:
	flake8 chess 

## Run tests
.PHONY: tests 
tests:
	${PYTHON_INTERPRETER} -m pytest

## Create a chess game
.DEFAULT_GOAL := game
.PHONY: game
game:
	${PYTHON_INTERPRETER} -m chess
