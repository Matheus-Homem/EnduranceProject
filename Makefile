# Makefile

# Define the name of the virtual environment
VENV_NAME := .venv


create-venv: # Command to create the virtual environment
	@echo Creating virtual environment...
	@python -m venv $(VENV_NAME)
	@echo Virtual environment created successfully!


activate-venv: # Command to activate the virtual environment and modify the command prompt
	@echo Activating virtual environment...
	@call .\$(VENV_NAME)\Scripts\activate && \
	@cmd /k


build: # Command to create the virtual environment and activate it
	@echo Building project...
	@make create-venv
	@make activate-venv


configure: # Command to install project dependencies
	@echo Configuring virtual environment...
	@python -m pip install --upgrade pip
	@pip install -r requirements.txt
	@echo Virtual environment configured successfully!


run: # Command to run the project
	@set PYTHONPATH=./ && \
	python src\main.py


full-run: # Command to run the project in automated mode 
	@set PYTHONPATH=./ && \
	python src\main.py --automated True


clean: # Command to clean the virtual environment and compilation files
	del /Q $(VENV_NAME)
    del /Q /S *.pyc
	del /Q /S __pycache__


test: # Run tests with code coverage
	@echo Running tests with code coverage...
	@coverage run --source=src -m pytest
	@coverage report -m --fail-under=10


help: # Help target to display available commands
	@echo "Available commands:"
	@echo
	@echo "  create-venv   : Create the virtual environment"
	@echo "  activate-venv : Activate the virtual environment"
	@echo "  build         : Build the project"
	@echo "  configure     : Configure project dependencies"
	@echo "  run           : Run the project"
	@echo "  full-run      : Run the project in automated mode"
	@echo "  clean         : Clean the project"
	@echo "  test          : Run tests with code coverage"


# Defines the commands that are not files
.PHONY: create-venv activate-venv install-dependencies run clean
