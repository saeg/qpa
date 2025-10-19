# Quantum Software Analysis Project

This project provides a framework and toolchain for analyzing the source code of popular quantum computing libraries. It uses `just` as a command runner to automate setup, data collection, and analysis tasks.

The project features a **dynamic discovery workflow**: it automatically queries the GitHub API to find the most relevant and active quantum software projects, filters them based on quality metrics, and then sets up isolated environments to run analysis scripts against their source code.

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
├── .venv/                   # Main virtual environment for project tooling (e.g., search scripts)
├── data/                    # All generated output, including repo lists and analysis results
│   ├── classiq_source_snippets/
│   ├── pennylane_source_snippets/
│   ├── qiskit_source_snippets/
│   ├── classiq_quantum_concepts.csv
│   └── ... (and other JSON/CSV results)
├── src/                     # Main source code for the analysis project
│   ├── conf/                # Project configuration files
│   ├── core_concepts/       # Scripts for identifying concepts in quantum libraries
│   └── preprocessing/       # Scripts for data collection (github_search.py, clone_repos.py)
├── target_github_projects/  # Cloned source code of the quantum libraries to be analyzed
├── .env                     # Local environment variables (contains GITHUB_TOKEN)
├── justfile                 # The command runner script for all project tasks
├── pyproject.toml           # Project dependencies and metadata
└── README.md                # This file
```

## The Two-Command Workflow

The entire project workflow, from setup to final analysis, has been automated. The `justfile` handles all dependencies automatically.

### Step 1: Install Project Tooling

This command sets up the main virtual environment (`.venv`) and installs the Python packages needed to run the project's own scripts (like the GitHub search tool). **You only need to run this once.**

```bash
just install
```

### Step 2: Run the Full Analysis

This single command will automatically perform the entire data acquisition and analysis pipeline:

1.  **Discover & Clone**: It will find the top quantum repos on GitHub and clone their source code.
2.  **Setup Analysis Env**: It will create the dedicated `.venv-analysis` and install all required packages (like `classiq` and `sentence-transformers`) and the cloned libraries into it.
3.  **Identify Concepts**: It will run the analysis scripts against Qiskit, PennyLane, and Classiq.

```bash
just identify-concepts
```

**Note:** The first time you run this command, it will perform the full setup and can take a significant amount of time, network bandwidth, and disk space. Subsequent runs will be much faster as `just` re-uses the existing setup.

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
    *   **The main analysis command.** It ensures the environment is fully set up and then runs all individual concept identification scripts.

*   `install`
    *   Sets up the `.venv` with tools for data acquisition.

*   `setup-analysis-env`
    *   Sets up the `.venv-analysis` with all dependencies needed for the analysis scripts.

### Individual Analysis Tasks

These are useful for debugging a single script without running the others. They will also trigger the full setup if it hasn't been run yet.

*   `identify-qiskit`
*   `identify-pennylane`
*   `identify-classiq`

### Utility Commands

*   `clean`
    *   Removes **ALL** generated artifacts: both virtual environments, all cloned code (`target_github_projects`), and the `data` directory. Use this for a complete reset.

*   `upgrade`
    *   Updates the `uv.lock` file based on `pyproject.toml`. Run this after changing dependencies.

