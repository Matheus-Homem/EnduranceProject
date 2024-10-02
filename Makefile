VENV_NAME := .venv

.PHONY: clean create-venv activate-venv prepare-environment prepare-requirements server test help tutorial

clear:
	@$(if $(filter $(OS),Windows_NT), \
		del /Q /S src\*.pyc && \
		del /Q /S src\__pycache__, \
		find src -type f -name '*.pyc' -delete && \
		rm -rf src/__pycache__)

create-venv:
	@echo Creating virtual environment...
	@$(if $(filter $(OS),Windows_NT), \
		python -m venv $(VENV_NAME), \
		python3 -m venv $(VENV_NAME))
	@echo Virtual environment created successfully!

activate-venv:
	@echo Activating virtual environment...
	@$(if $(filter $(OS),Windows_NT), \
		call .\$(VENV_NAME)\Scripts\activate && cmd /k, \
		echo This is not a Windows system. Please activate the virtual environment with: && \
		echo source $(VENV_NAME)/bin/activate)
		
prepare-environment:
	@echo Building project...
	@make clean
	@make create-venv
	@make activate-venv

prepare-requirements:
	@echo Installing project dependencies...
	@$(if $(filter $(OS),Windows_NT), \
		python -m pip install --upgrade pip && \
		pip install -r requirements.txt, \
		python3 -m pip install --upgrade pip && \
		pip install -r requirements.txt)
	@echo Project dependencies installed successfully!

server:
	@echo Running the web application...
	@$(if $(filter $(OS),Windows_NT), \
		set PYTHONPATH=./ && \
		python src\web\app.py, \
		export PYTHONPATH=./ && \
		python3 src/web/app.py)

sql-export:
	@echo Running the web application...
	@$(if $(filter $(OS),Windows_NT), \
		set PYTHONPATH=./ && \
		python scripts/schema_exporter.py, \
		export PYTHONPATH=./ && \
		python3 scripts/schema_exporter.py)

chore:
	@echo Running autoflake...
	@autoflake --remove-all-unused-imports --in-place --recursive tests/
	@autoflake --remove-all-unused-imports --in-place --recursive src/
	@autoflake --remove-all-unused-imports --in-place --recursive scripts/
	@echo Running isort...
	@isort tests/
	@isort src/
	@isort scripts/
	@echo Running black...
	@black tests/
	@black src/
	@black scripts/
	@echo autoflake, isort, and black ran successfully!

test:
	@make chore
	@echo Running tests with code coverage...
	@pytest -vv --cov=src --cov-config=.coveragerc --cov-report=term-missing --cov-fail-under=90
	@python -c "import os; os.remove('.coverage') if os.path.exists('.coverage') else None"
	@echo Tests with code coverage ran successfully!

help:
	@echo     __________________________________________________________________________________________________
	@echo "  |                       :                                                                          |
	@echo "  |        COMMANDS       :                             DESCRIPTIONS                                 |
	@echo "  |  clear                : Clean up the environment by removing __pycache__ and *.pyc files         |
	@echo "  |  create-venv          : Create the virtual environment                                           |
	@echo "  |  activate-venv        : Activate the virtual environment                                         |
	@echo "  |  prepare-environment  : Build the project (clean, create virtual environment, and activate it)   |
	@echo "  |  prepare-requirements : Install project dependencies from requirements.txt                       |
	@echo "  |  server               : Run the web application                                                  |
	@echo "  |  chore                : Run code formatting tools (isort and black) on the project               |
	@echo "  |  test                 : Run tests with code coverage and clean up afterward                      |
	@echo "  |__________________________________________________________________________________________________|

tutorial:
	@echo     ____________________________________________ 
	@echo "  |                                            |
	@echo "  |   To build the project, run these steps:   |
	@echo "  |        1. make prepare-environment         |
	@echo "  |        2. make prepare-requirements        |
	@echo "  |____________________________________________|