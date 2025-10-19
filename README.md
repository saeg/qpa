# Quantum Software Analysis Project

This project provides an automated framework and toolchain for analyzing the source code of popular quantum computing libraries to identify recurring software patterns. It uses `just` as a command runner to orchestrate the entire pipeline, from data collection to final analysis and reporting.

The project features a **dynamic discovery workflow**: it queries the GitHub API to find relevant quantum software projects, clones them, preprocesses their code (including Jupyter Notebooks), and then runs a series of analysis scripts to extract and classify core programming concepts.

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

## Replication Workflow: Step-by-Step Guide

This guide walks you through the exact sequence of commands to set up the project and replicate the study's results.

### Step 0: Initial Project Setup

This single command prepares the entire project. It will:
1.  Discover and clone the target quantum software repositories from GitHub.
2.  Create a unified virtual environment (`.venv`).
3.  Install all required Python dependencies from `pyproject.toml`.
4.  Install the cloned `qiskit` and `pennylane` repositories in editable mode.

```bash
just install
```
*Note: This command is designed to be fully reproducible and will re-run the setup each time to ensure a clean state. The initial run will take significant time and disk space.*

### Step 1: Download Quantum Pattern Definitions

This step fetches the list of known quantum software patterns from the PlanQK Pattern Atlas, which will be used as a baseline for classification.

```bash
just download_pattern_list
```

### Step 2: Extract Core Concepts from Frameworks

Next, run the scripts that parse the source code of Qiskit, PennyLane, and Classiq to identify their core concepts (e.g., functions and classes).

```bash
just identify-concepts
```

This command generates the following raw data files in the `data/` directory, which you will use in the next step:
*   `data/classiq_quantum_concepts.csv`
*   `data/pennylane_quantum_concepts.csv`
*   `data/qiskit_quantum_concepts.csv`

### Step 3: Manual Concept Classification (Optional)

This is the only manual step in the workflow. The goal is to classify the concepts extracted in the previous step. You have two options:

*   **To replicate our exact results:** You don't need to do anything. The pre-classified files are already provided in the `data/` directory:
    *   `data/enriched_classiq_quantum_patterns.csv`
    *   `data/enriched_pennylane_quantum_patterns.csv`
    *   `data/enriched_qiskit_quantum_patterns.csv`

*   **To perform your own classification:**
    1.  Open the `_quantum_concepts.csv` files generated in Step 2.
    2.  Add your classification data to the rows.
    3.  Save the modified files with the `enriched_` prefix (e.g., `data/enriched_qiskit_quantum_patterns.csv`).

### Step 4: Preprocess Jupyter Notebooks

This step finds all Jupyter Notebooks (`.ipynb`) within the cloned projects, converts them to Python scripts (`.ipynb.py`) in-place for analysis, and creates an organized archive of the original notebooks.

```bash
just preprocess-notebooks
```

### Step 5: Run the Main Semantic Analysis

With all data prepared, this command runs the main workflow. It uses the `enriched_*.csv` files and the preprocessed source code to search for quantum computing concepts across all target projects.

```bash
just run_main
```

### Step 6: Generate the Final Report

Finally, generate the final report summarizing the findings of the analysis.

```bash
just report
```

This will create the final output file at `data/final_pattern_report.txt`.

## Command Reference

You can always run `just` to see an interactive list of available commands.

### Main Workflow Commands

*   `install`: Sets up the entire project, including cloning, environment creation, and dependency installation.
*   `identify-concepts`: Runs the core concept extraction for Qiskit, PennyLane, and Classiq.
*   `run_main`: Executes the primary semantic analysis workflow.
*   `report`: Generates the final summary report.

### Individual Data & Preprocessing Steps

*   `download_pattern_list`: Fetches pattern definitions from the PlanQK Pattern Atlas.
*   `discover-and-clone`: Runs only the GitHub search and cloning steps.
*   `preprocess-notebooks`: Converts `.ipynb` files to `.py` and creates an archive.
*   `convert-archived-notebooks`: A separate utility to convert notebooks from the archive folder.

### Utility Commands

*   `clean`: Removes **ALL** generated artifacts: the virtual environment, all cloned code, and the `data`, `notebooks`, and `converted_notebooks` directories. Use this for a complete reset.
*   `upgrade`: Updates the `uv.lock` file based on `pyproject.toml`. Run this after changing dependencies.
*   `setup`: A one-time command to install the `uv` package manager.