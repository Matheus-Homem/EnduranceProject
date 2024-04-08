<!-- omit in toc -->
# The Compass Project

## Table of Contents

- [Table of Contents](#table-of-contents)
- [Environment Configuration](#environment-configuration)
  - [Step 01: Build the Project](#step-01-build-the-project)
  - [Step 02: Configure the Environment](#step-02-configure-the-environment)
  - [Run the Project](#run-the-project)
  - [Run Full Pipeline](#run-full-pipeline)
  - [Host Server](#host-server)
  - [Clean Up](#clean-up)

## Environment Configuration

### Step 01: Build the Project

First, build the project to set up the virtual environment and activate it.

```plaintext
make build
```

This command creates a virtual environment and activates it to ensure the project runs in an isolated environment.

### Step 02: Configure the Environment

After building the project, configure the virtual environment by installing project dependencies.

```plaintext
make configure
```

This command upgrades pip and installs the required dependencies specified in the `requirements.txt` file.

### Run the Project

To execute the project, simply use:

```plaintext
make run
```

This command runs the project using the main script `main.py`.

### Run Full Pipeline

For a complete automated pipeline execution, use:

```plaintext
make full-run
```

This command runs the project in automated mode, which may include additional tasks or tests specified in the pipeline.

### Host Server

To host a local server, user:

```plaintext
make server
```

This command executes an `app.py` file enabling a local host for the web page from the project.

### Clean Up

Finally, deactivate the virtual environment and clean up any generated files.

```plaintext
deactivate
make clean
```

This command deactivates the virtual environment and removes any temporary files or directories generated during project execution.
