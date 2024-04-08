# A variable to define the name of the virtual environment
VENV_NAME := .venv

# Defines the commands that are not files
.PHONY: clean create-venv activate-venv build todos configure run full-run server test help

clean: # Command to clean the virtual environment and compilation files
	@$(if $(filter $(OS),Windows_NT), \
		rmdir /Q /S $(VENV_NAME) && \
		del /Q /S *.pyc && \
		del /Q /S __pycache__, \
		rm -rf $(VENV_NAME) && \
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
	@call .\$(VENV_NAME)\Scripts\activate && cmd /k
		
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
	@set PYTHONPATH=./ && \
	python src\main.py

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
		python src\web\app.py, \
		python3 src/web/app.py)

test: # Run tests with code coverage
	@echo Running tests with code coverage...
	@coverage run --source=src -m pytest
	@coverage report -m --fail-under=10

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
	@echo "  clean         : Clean the project"
	@echo "  test          : Run tests with code coverage"