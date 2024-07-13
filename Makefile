PYTHON_VERSION := $(subst ., ,$(shell cat .python-version))
PYTHON_MAJOR_VERSION := $(word 1,$(PYTHON_VERSION))
PYTHON_MINOR_VERSION := $(word 2,$(PYTHON_VERSION))
PYTHON_INTERPRETER := python


all: venv 

.PHONY: compile
compile:
	. venv/bin/activate; \
		${PYTHON_INTERPRETER} setup.py build_ext --inplace

venv: .python-version
	rm -rf venv
	${PYTHON_INTERPRETER} -c \
		'import sys; assert sys.version_info.major == ${PYTHON_MAJOR_VERSION}'
	${PYTHON_INTERPRETER} -c \
		'import sys; assert sys.version_info.minor >= ${PYTHON_MINOR_VERSION}'
	${PYTHON_INTERPRETER} -m venv venv
	. venv/bin/activate; \
		${PYTHON_INTERPRETER} -m pip install --upgrade setuptools; \
		${PYTHON_INTERPRETER} -m pip install --upgrade wheel; \
		${PYTHON_INTERPRETER} -m pip install --upgrade pip; \
		${PYTHON_INTERPRETER} -m pip install -r requirements.txt; \
		${PYTHON_INTERPRETER} -m pip install -e .[dev]
	. venv/bin/activate; \
		${PYTHON_INTERPRETER} setup.py build_ext --inplace

.PHONY: clean
clean:
	python setup.py clean --all
	rm -rf venv
	find . -type f -name "*.so" -delete
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete
 
.PHONY: test
test:
	source venv/bin/activate; pytest tests -vvvv

.PHONY: lint
lint: 
	. venv/bin/activate; \
		${PYTHON_INTERPRETER} -m flake8 src
	. venv/bin/activate; \
		${PYTHON_INTERPRETER} -m flake8 tests

.PHONY: profile
profile:
	. venv/bin/activate; \
		${PYTHON_INTERPRETER} -m cProfile --sort time -m chess "RandomAgent(seed=42)" "RandomAgent(seed=42)"

.PHONY: play_human_vs_machine
play_human_vs_machine:
	. venv/bin/activate; \
		chess -v "HumanAgent()" "AlphaBetaAgent(depth=3)"

.PHONY: play_machine_vs_machine
play_machine_vs_machine:
	. venv/bin/activate; \
		chess -v "AlphaBetaAgent(depth=3)" "AlphaBetaAgent(depth=3)"
