# Makefile

# Nome do ambiente virtual
VENV_NAME := venv

# Comando para ativar o ambiente virtual
VENV_ACTIVATE := . $(VENV_NAME)/bin/activate

# Comando para criar a virtual environment
create-venv:
	python3 -m venv $(VENV_NAME)

# Comando para ativar a virtual environment
activate-venv:
	@echo "Ativando a virtual environment..."
	@$(VENV_ACTIVATE)

# Exemplo de uma tarefa que usa a virtual environment ativada
run:
	$(VENV_ACTIVATE) && python3 seu_script.py

# Definindo a regra padrão (quando você digita apenas `make` no terminal)
.DEFAULT_GOAL := run


help:
	@echo "Available targets:"
	@echo "  run                  - Command to run the main.py script"
	@echo "  teste                - Test script execution"
	@echo "  setup-venv           - Command to create the virtual environment"
	@echo "  activate             - Command to activate the virtual environment"
	@echo "  install-requirements - Command to install the project dependencies"
	@echo "  configure-run        - Command to configure environment variables for running"
	@echo "  build                - Command to set up the virtual environment and install dependencies"
	@echo "  full-run             - Command to run the main.py script with additional options"
	@echo "  clean                - Command to clean up generated files"
	@echo "  docs                 - Command to generate project documentation"

test:
	@echo "Executing script"

clean:
	@echo "Cleaning up generated files"
	# Add commands here to clean up generated files

docs:
	@echo "Generating project documentation"
	# Add commands here to generate project documentation

# Command to run the main.py script
/

# Command to create the virtual environment
setup-venv:
	python -m venv venv

# Command to activate the virtual environment
activate:
	@echo off
	call .\venv\Scripts\activate.bat
	echo Teste



# Command to install the project dependencies
install-requirements:
	pip install -r requirements.txt

# Command to configure environment variables for running
configure-run:
	cmd /c "set PYTHONPATH=."

# Command to set up the virtual environment and install dependencies
build: setup-venv install-requirements

# Command to run the main.py script with additional options
full-run: configure-run
	cmd /c "$(PYTHON) src\main.py --automated True"