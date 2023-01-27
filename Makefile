#################################################################################
# GAMEPLAY                                                                      #
#################################################################################

## Create a chess game.
.DEFAULT_GOAL := human_vs_machine
.PHONY: human_vs_machine
human_vs_machine: 
	conda run --no-capture-output --prefix envs/chess python -m chess human_vs_machine


#################################################################################
# DEVELOPMENT                                                                   #
#################################################################################

.PHONY: self_play
self_play:
	conda run --no-capture-output --prefix envs/chess python -m chess self_play

.PHONY: profiling
profiling:
	conda run --no-capture-output --prefix envs/chess python -m chess profiling

.PHONY: envs
envs:
	conda env create --prefix envs/chess 
	conda install conda-build

## Delete all compiled Python files.
.PHONY: clean 
clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete

## Lint using flake8.
.PHONY: lint 
lint:
	conda run --no-capture-output --prefix envs/chess python -m flake8 chess

## Run tests.
.PHONY: tests 
tests:
	conda run --no-capture-output --prefix envs/chess python -m pytest tests -x --log-cli-level=ERROR

