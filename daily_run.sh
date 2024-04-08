#!/bin/bash

# Change the current directory to the compass_project directory
cd compass_project

# Run the build command from the Makefile, which cleans the virtual environment, creates a new one, and activates it
make build

# Activate the virtual environment
source .venv/bin/activate

# Run the configure command from the Makefile, which installs the project dependencies
make configure

# Run the full-run command, which runs the full pipeline including e-mailing the report
make full-run