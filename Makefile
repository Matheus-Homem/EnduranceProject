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

# Defines the commands that are not files
.PHONY: create-venv activate-venv install-dependencies run clean
