# Quantum Software Analysis Project

This project provides an automated framework and toolchain for analyzing the source code of popular quantum computing libraries. It uses `just` as a command runner to orchestrate the entire pipeline, from data collection to final analysis.

The project features a **dynamic discovery workflow**: it queries the GitHub API to find the most relevant and active quantum software projects, clones them, preprocesses their code (including Jupyter Notebooks), and then runs a series of analysis scripts to extract core programming concepts.

## Prerequisites

Before you begin, ensure you have the following installed:

*   **Python 3.12+**
*   **Just**: A modern command runner. If you don't have it, you can find installation instructions [here](https://github.com/casey/just#installation).
*   **Git**: For cloning the target repositories.
*   **A GitHub Personal Access Token (PAT)**: The discovery script requires a GitHub token to avoid API rate limits. Create a token and save it in a `.env` file in the project root:

    ```text
    # in .env file
    GITHUB_TOKEN="ghp_YourTokenHere"
    ```

## Project Structure

The project follows a standard Python `src` layout and separates generated data from source code.

```text
quantum_patterns/
├── .venv/                   # The single, unified virtual environment for the entire project
├── data/                    # All generated output, including repo lists and analysis results
│   ├── classiq_source_snippets/
│   ├── pennylane_source_snippets/
│   ├── qiskit_source_snippets/
│   ├── classiq_quantum_concepts.json
│   └── ... (and other JSON/CSV results)
├── notebooks/               # An archive of all original Jupyter Notebooks found in the target projects
├── converted_notebooks/     # A directory for Python scripts converted from the archived notebooks
├── src/                     # Main source code for the analysis project
│   ├── conf/                # Project configuration files
│   ├── core_concepts/       # Scripts for identifying concepts in quantum libraries
│   └── preprocessing/       # Scripts for data collection and preparation
├── target_github_projects/  # Cloned source code of the quantum libraries to be analyzed
├── .env                     # Local environment variables (contains GITHUB_TOKEN)
├── justfile                 # The command runner script for all project tasks
├── pyproject.toml           # Project dependencies and metadata
└── README.md                # This file
```

## The Two-Command Workflow

The entire project workflow, from setup to final analysis, has been automated into two simple commands.

### Step 1: Install Project Tooling

This command installs `uv`, the fast package manager used by the project. **You only need to run this once.**

```bash
just setup
```

### Step 2: Run the Full Analysis

This single command will automatically perform the entire data acquisition and analysis pipeline:

1.  **Discover & Clone**: It will find the top quantum repos on GitHub and clone their source code.
2.  **Preprocess Notebooks**: It will find all Jupyter Notebooks (`.ipynb`) in the cloned projects, convert them to Python scripts (`.ipynb.py`) in-place, and create an archive.
3.  **Setup Environment**: It will create a fresh, unified virtual environment (`.venv`) and install all project dependencies, including the cloned libraries in editable mode.
4.  **Identify Concepts**: It will run the final analysis scripts against Qiskit, PennyLane, and Classiq.

```bash
just identify-concepts
```

**Note:** This command is designed to be fully reproducible. It re-runs the setup process each time to ensure a clean and consistent environment. The initial run will take a significant amount of time, while subsequent runs will be faster as cloned repositories are updated instead of re-cloned.

### Expected Output

After `just identify-concepts` completes, the `data/` directory will be populated with:
*   `_quantum_concepts.json`: Structured data about each identified concept.
*   `_quantum_concepts.csv`: A simplified summary for easy review.
*   `_source_snippets/`: A directory containing the raw source code of each concept for inspection.
*   `filtered_repo_list.txt`: The list of repositories that were cloned.

## Command Reference

You can always run `just` to see an interactive list of available commands.

### Main Workflow Commands

*   `identify-concepts`
    *   **The main entry point.** It automatically runs the full setup and analysis pipeline.

*   `install`
    *   The core setup recipe that handles environment creation, dependency installation, and repo cloning/preprocessing. It is called automatically by `identify-concepts`.

### Individual Analysis Tasks

These are useful for debugging a single script without running the others. They will also trigger the full setup if it hasn't been run yet.

*   `identify-qiskit`
*   `identify-pennylane`
*   `identify-classiq`

### Preprocessing Tasks

*   `preprocess-notebooks`
    *   Finds all notebooks in `target_github_projects/`, converts them to `.py` files in-place, and copies the originals to the `notebooks/` archive.

*   `convert-archived-notebooks`
    *   A separate utility that converts notebooks from the `notebooks/` archive into the `converted_notebooks/` directory.

### Utility Commands

*   `clean`
    *   Removes **ALL** generated artifacts: the virtual environment, all cloned code, and the `data`, `notebooks`, and `converted_notebooks` directories. Use this for a complete reset.

*   `upgrade`
    *   Updates the `uv.lock` file based on `pyproject.toml`. Run this after changing dependencies.