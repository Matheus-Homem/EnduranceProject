<!-- omit in toc -->
# The Compass Project

## Table of Contents
- [Table of Contents](#table-of-contents)
- [Environment Configuration](#environment-configuration)
	- [Step 01](#step-01)
	- [Step 02](#step-02)
	- [Step 03](#step-03)
	- [Step 04](#step-04)
	- [Step 05](#step-05)
	- [Step 06](#step-06)


## Environment Configuration

### Step 01

- To upgrade `pip`:

```plaintext
python -m pip install --upgrade pip
```

### Step 02

- To setup `venv`, use:

```plaintext
python -m venv venv
```

### Step 03

- To activate `venv`, use:

```plaintext
venv/Scripts/Activate.ps1
```

### Step 04

- To install requirements, use:
  
```plaintext
pip install -r requirements.txt
```

### Step 05

- To add root to `PYTHONPATH`, use:

```plaintext
$env:PYTHONPATH = "."
```

### Step 06

- To execute `main.py`, use:

```plaintext
python src/main.py
```