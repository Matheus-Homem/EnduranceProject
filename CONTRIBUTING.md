<!-- omit in toc -->
# Project Naming Conventions and Commit Guidelines

- [Introduction](#introduction)
- [Branch Naming Conventions](#branch-naming-conventions)
  - [1. *Feature*](#1-feature)
  - [2. *Refactor*](#2-refactor)
  - [3. *Test*](#3-test)
  - [4. *Fix*](#4-fix)
  - [5. *Chore*](#5-chore)

## Introduction

This document outlines the naming conventions and commit guidelines to be followed while working on this project.  
Adhering to these conventions will ensure a standardized and clear approach to development.

## Branch Naming Conventions

### 1. *Feature*

- Used for developing **new features** or adding **new functionality** to the project.
- This branch changes code.
- Workflow: `feat/branch` -> `dev` -> `main`

### 2. *Refactor*

- Used to **update existing features** in the project.
- This branch changes code.
- Workflow: `refactor/branch` -> `dev` -> `main`

### 3. *Test*

- Used to add or change **code used for testing project code**.
- This branch changes code used for testing.
- Workflow: `test/branch` -> `dev` -> `main`

### 4. *Fix*

- Used to **fix a feature** that isn't working properly in the `main` branch.
- This branch changes code.
- Workflow: `fix/branch` -> `main`

### 5. *Chore*

- Used to **delete files**, **add docs**, **change dependencies**, and make other alterations that aren't code-related.
- This branch does not change code.
- Workflow: `chore` -> `dev` -> `main`
