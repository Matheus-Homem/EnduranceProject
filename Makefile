# A variable to define the name of the virtual environment
VENV_NAME := .venv

# Defines the commands that are not files
.PHONY: clean create-venv activate-venv build todos configure run full-run server test help

clear: # Command to clean the virtual environment and compilation files
	@$(if $(filter $(OS),Windows_NT), \
		del /Q /S *.pyc && \
		del /Q /S __pycache__, \
		find . -type f -name '*.pyc' -delete && \
		rm -rf __pycache__)

create-venv: # Command to create the virtual environment
	@echo Creating virtual environment...
	@$(if $(filter $(OS),Windows_NT), \
		python -m venv $(VENV_NAME), \
		python3 -m venv $(VENV_NAME))
	@echo Virtual environment created successfully!

activate-venv: # Command to activate the virtual environment and modify the command prompt
	@echo Activating virtual environment...
	@$(if $(filter $(OS),Windows_NT), \
		call .\$(VENV_NAME)\Scripts\activate && cmd /k, \
		echo This is not a Windows system. Please activate the virtual environment with: && \
		echo source $(VENV_NAME)/bin/activate)
		
build: # Command to create the virtual environment and activate it
	@echo Building project...
	@make clean
	@make create-venv
	@make activate-venv

configure: # Command to install project dependencies
	@echo Configuring virtual environment...
	@$(if $(filter $(OS),Windows_NT), \
		python -m pip install --upgrade pip && \
		pip install -r requirements.txt, \
		python3 -m pip install --upgrade pip && \
		pip install -r requirements.txt)
	@echo Virtual environment configured successfully!
	@make todos

run: # Command to run the project
	@echo Running the project...
	@$(if $(filter $(OS),Windows_NT), \
		set PYTHONPATH=./ && \
		python src\main.py, \
		export PYTHONPATH=./ && \
		python3 src/main.py)

full-run: # Command to run the project in automated mode 
	@echo Running the project in automated mode...
	@$(if $(filter $(OS),Windows_NT), \
		set PYTHONPATH=./ && \
		python src\main.py --automated True, \
		export PYTHONPATH=./ && \
		python3 src/main.py --automated True)

server: # Command to run the web application
	@echo Running the web application...
	@$(if $(filter $(OS),Windows_NT), \
		set PYTHONPATH=./ && \
		python src\web\app.py, \
		export PYTHONPATH=./ && \
		python3 src/web/app.py)

chore: # Run isort and black
	@echo Running isort...
	@isort tests/
	@isort src/etl/
	@isort src/shared
	@isort src/web
	@isort src/main.py
	@echo Running black...
	@black tests/
	@black src/etl/
	@black src/shared
	@black src/web
	@black src/main.py

test: # Run chore and tests with code coverage
	@make chore
	@echo Running tests with code coverage...
	@pytest -vv --cov=src --cov-config=.coveragerc --cov-report=term-missing --cov-fail-under=80

todos: # Generate TODO.md from #TODO comments in the code
	@echo Generating TODO.md...
	@$(if $(filter $(OS),Windows_NT), \
		python src\generate_todos.py, \
		python3 src/generate_todos.py)
	@echo TODO.md generated successfully!

help: # Help target to display available commands
	@echo "Available commands:"
	@echo
	@echo "  create-venv   : Create the virtual environment"
	@echo "  activate-venv : Activate the virtual environment"
	@echo "  build         : Build the project"
	@echo "  configure     : Configure project dependencies"
	@echo "  run           : Run the project"
	@echo "  full-run      : Run the project in automated mode"
	@echo "  server        : Run the web application"
	@echo "  todos         : Generate TODO.md from #TODO comments in the code"
	@echo "  clear         : Clean the virtual environment and compilation files"
	@echo "  test          : Run tests with code coverage"