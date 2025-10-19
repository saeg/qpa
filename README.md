
# Quantum Software Analysis Project

Repository for the paper "Mining Quantum Software Patterns in Open-Source Projects: An Empirical Study".

This project provides a framework and toolchain for analyzing the source code of popular quantum computing libraries. It uses `just` as a command runner to automate setup, data collection, and analysis tasks. The core design involves two separate Python virtual environments: one for the project's own tooling and another dedicated, isolated environment for running analysis against the cloned quantum libraries.

## Prerequisites

Before you begin, ensure you have the following installed:
*   **Python 3.10+**
*   **Just**: A modern command runner. If you don't have it, you can find installation instructions [here](https://github.com/casey/just#installation).
*   **Git**: For cloning the target repositories.

## Quick Start & Main Workflow

This is the recommended sequence of commands to get the project fully set up and ready for analysis.

1.  **Install `uv` (the Python package manager)**:
    The `justfile` includes a helper to install `uv` for your operating system.
    ```bash
    just setup
    ```

2.  **Install Project Dependencies**:
    This creates the main virtual environment (`.venv`) for the project's internal scripts.
    ```bash
    just install
    ```

3.  **Set up the Analysis Environment**:
    This is the most important command. It performs all the heavy lifting: it clones dozens of quantum software repositories into the `target_github_projects/` directory and then creates a dedicated virtual environment (`.venv-analysis`) with all of those repositories installed in editable mode.
    ```bash
    just setup-analysis-env
    ```
    *Note: This command can take a significant amount of time and disk space, as it downloads many large repositories.*

4.  **Run an Analysis Script**:
    Once the setup is complete, you can execute a Python script using the dedicated analysis environment, which has access to all the cloned quantum libraries.
    ```bash
    just run-analysis path/to/your/script.py
    ```

## Command Reference

If you are unsure which command to run, you can always execute `just` without any arguments to get an interactive chooser.

```bash
just
```

### Setup & Installation

*   `just setup`
    *   Installs `uv`, the fast Python package manager used by this project. It automatically detects your OS (macOS, Linux, or Windows).

*   `just install`
    *   Creates the main project virtual environment at `.venv`.
    *   Installs the dependencies listed in `pyproject.toml` (e.g., `qparser`) into this environment. This environment is for running the project's own tools, not for analyzing the target libraries.

*   `just setup-analysis-env`
    *   **This is the main entry point for setting up the project.** It orchestrates the entire analysis environment setup.
    *   It first runs `just clone` to download all required quantum library source code.
    *   It then creates a separate, isolated virtual environment at `.venv-analysis`.
    *   Finally, it installs all the cloned repositories (Qiskit, PyQuil, Classiq, etc.) and other analysis dependencies (matplotlib, networkx) into the `.venv-analysis` environment in editable mode.

### Core Analysis Tasks

*   `just run-analysis <SCRIPT>`
    *   Executes a given Python script using the interpreter from the dedicated `.venv-analysis` environment. This ensures your script has access to all the installed quantum libraries.
    *   **Example**: `just run-analysis qparser/embedding_dataset/generate_method_embedding.py`

### Data & Repository Management

*   `just search-repos`
    *   Runs the `qparser.preprocessing.github_search` script to find popular quantum projects on GitHub and populate the initial repository list.

*   `just clone`
    *   Clones or pulls the latest versions of all specified quantum software repositories into the `target_github_projects/` directory.
    *   It handles a large list of libraries including Qiskit, Cirq, PyQuil, and PennyLane. It also includes special handling to download and unpack the `classiq` wheel, making its source code available for analysis.

*   `just clone-filtered`
    *   A more targeted version of `clone`. It clones only the repositories listed in the `results/filtered_repo_list.txt` file.

### Cleanup

*   `just clean`
    *   Removes **ALL** generated artifacts: both virtual environments (`.venv`, `.venv-analysis`), the `target_github_projects` directory, and all `__pycache__` directories. Use this for a complete reset.

*   `just clean-analysis`
    *   Performs a less destructive cleanup. It only removes the analysis-specific environment (`.venv-analysis`), leaving the main project environment and the cloned repositories intact.

### Dependency Management

*   `just upgrade`
    *   Runs `uv lock --upgrade` to update the `requirements.lock` file with the latest compatible versions of the project's dependencies.

## Understanding the Environments

This project uses two distinct virtual environments to maintain a clean separation of concerns:

*   **`.venv` (Main Project Environment)**:
    *   Contains the packages required to run the tools *within this project* (e.g., the scripts for searching GitHub or cloning repos).
    *   Created by `just install`.

*   **`.venv-analysis` (Dedicated Analysis Environment)**:
    *   Contains all the *target quantum libraries* (Qiskit, Cirq, etc.) that you want to analyze.
    *   This is the environment used by the `just run-analysis` command. It is specifically designed to be an isolated space containing the code under analysis.
    *   Created by `just setup-analysis-env`.
