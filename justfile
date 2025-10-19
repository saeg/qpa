# justfile

set shell := ["bash", "-c"]

VENV            := ".venv"
REPO_LIST_FILE  := "data/filtered_repo_list.txt"

# It creates the venv, installs ALL dependencies, and clones the repos.
install: discover-and-clone
    @echo "\n>>> Setting up the project environment in '{{VENV}}'..."
    @uv venv --clear --seed {{VENV}}

    @echo " Installing all dependencies from pyproject.toml..."
    @uv sync --python {{VENV}}/bin/python

    @echo " Installing cloned repositories in editable mode..."
    @uv pip install --python {{VENV}}/bin/python -e ./target_github_projects/qiskit
    @uv pip install --python {{VENV}}/bin/python -e ./target_github_projects/pennylane
    @echo ">>> Unified environment setup complete."
    @echo "To activate it manually, run: source {{VENV}}/bin/activate"

# Runs all core concept identification scripts. This is the main analysis command.
# It now depends on `install` to ensure the environment is ready.
identify-concepts: install
    @echo "\n>>> Running all core concept identification tasks..."
    @just identify-qiskit
    @just identify-pennylane
    @just identify-classiq
    @echo "\n All core concept identification tasks are complete."
    @echo "Results are saved in the 'data/' directory."


# Runs the GitHub search script to find and filter top quantum projects.
search-repos:
    @echo ">>> Running GitHub search to find and filter top quantum projects..."
    @if [ ! -d "{{VENV}}" ]; then just _bootstrap-tools; fi
    @{{VENV}}/bin/python -m src.preprocessing.github_search

# Clones/updates repositories listed in the dynamically generated file.
clone-filtered:
    @echo "\n>>> Cloning/updating repositories from '{{REPO_LIST_FILE}}'..."
    @if [ ! -d "{{VENV}}" ]; then just _bootstrap-tools; fi
    @{{VENV}}/bin/python -m src.preprocessing.clone_repos {{REPO_LIST_FILE}}

# The data acquisition task.
discover-and-clone: search-repos clone-filtered
    @echo "\n>>> All source repositories are ready."


# Identifies and extracts core concepts from the Qiskit source code.
identify-qiskit:
    @echo "\n--- Identifying core concepts in Qiskit ---"
    @{{VENV}}/bin/python -m src.core_concepts.identify_qiskit_core_concepts

# Identifies and extracts core concepts from the PennyLane source code.
identify-pennylane:
    @echo "\n--- Identifying core concepts in PennyLane ---"
    @{{VENV}}/bin/python -m src.core_concepts.identify_pennylane_core_concepts

# Identifies and extracts core concepts from the Classiq source code.
identify-classiq:
    @echo "\n--- Identifying core concepts in Classiq ---"
    @{{VENV}}/bin/python -m src.core_concepts.identify_classiq_core_concepts


# A special recipe to create a  venv just for the data acquisition scripts.
_bootstrap-tools:
    @echo ">>> Bootstrapping minimal tools environment..."
    @uv venv --clear --seed {{VENV}}
    @uv pip install --python {{VENV}}/bin/python PyGithub python-dotenv python-dateutil
    @echo ">>> Bootstrap complete."

# Cleans up ALL generated files and environments.
clean:
    @echo ">>> Cleaning up ALL generated files and environments..."
    @rm -rf {{VENV}} target_github_projects data
    @find . -type d -name "__pycache__" -exec rm -rf {} +
    @find . -name "*.ipynb.py" -type f -delete
    @echo ">>> Cleanup complete."

upgrade:
  uv lock --upgrade

# == One-Time Setup ============================================================

default:
  @just --choose

setup:
    @just _setup-{{ os() }}

_setup-macos:
    @echo "Installing uv for macOS..."
    @curl -LsSf https://astral.sh/uv/install.sh | sh

_setup-linux:
    @echo "Installing uv for Linux..."
    @curl -LsSf https://astral.sh/uv/install.sh | sh

_setup-windows:
    @echo "Installing uv for Windows..."
    @powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"