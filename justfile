set shell := ["bash", "-c"]
# Define variables for our virtual environments to keep things clean.
VENV            := ".venv"
ANALYSIS_VENV   := ".venv-analysis"

CLASSIQ_WHL_URL := "https://files.pythonhosted.org/packages/ce/1b/e29d4da6255cdfd172117371104065343de1920b643551940b1d6a99d362/classiq-0.88.0-py3-none-any.whl"
CLASSIQ_SQK_DIR := "target_github_projects/classiq_sqk"

REPO_LIST_FILE := "results/filtered_repo_list.txt"

search-repos:
    @echo ">>> Running GitHub search to find top quantum projects..."
    @python -m qparser.preprocessing.github_search
# sets up the main Python environment for the project.
install:
    @echo ">>> Setting up main project environment in '{{VENV}}'..."
    @uv venv --seed {{VENV}}
    @echo " Installing dependencies from pyproject.toml..."
    @uv sync
    @echo ">>> Main environment setup complete."

# Cleans up ALL generated files and environments.
clean:
    @echo ">>> Cleaning up ALL generated files and environments..."
    @rm -rf {{VENV}} {{ANALYSIS_VENV}} target_github_projects
    @find . -type d -name "__pycache__" -exec rm -rf {} +
    @find . -name "*.ipynb.py" -type f -delete
    @echo ">>> Cleanup complete."

# Sets up the dedicated, isolated environment for code analysis.
# This is the main command you should run.
setup-analysis-env: clone
    @echo "\n>>> Setting up dedicated analysis environment in '{{ANALYSIS_VENV}}'..."
    @uv venv {{ANALYSIS_VENV}}
    @just install-analysis-deps
    @echo "\n>>> Analysis environment setup complete."
    @echo "To activate it manually, run: source {{ANALYSIS_VENV}}/bin/activate"
    @echo "Then, configure IntelliJ to use the interpreter at: {{justfile_directory()}}/{{ANALYSIS_VENV}}/bin/python"

# Installs the required libraries for analysis into the dedicated environment.
install-analysis-deps: clone
    @echo " Installing analysis dependencies into '{{ANALYSIS_VENV}}'..."
    # Use the system `uv` and target the new environment's python interpreter.
    @uv pip install --python {{ANALYSIS_VENV}}/bin/python -e ./target_github_projects/qiskit
    @uv pip install --python {{ANALYSIS_VENV}}/bin/python -e ./target_github_projects/pyquil
    @uv pip install --python {{ANALYSIS_VENV}}/bin/python -e ./target_github_projects/classiq-library
    # -- MODIFIED: Added the unpacked Classiq wheel directory --
    @uv pip install --python {{ANALYSIS_VENV}}/bin/python -e ./{{CLASSIQ_SQK_DIR}}
    @uv pip install --python {{ANALYSIS_VENV}}/bin/python -e ./target_github_projects/grove
    @uv pip install --python {{ANALYSIS_VENV}}/bin/python -e ./target_github_projects/qiskit-algorithms
    @uv pip install --python {{ANALYSIS_VENV}}/bin/python matplotlib networkx scipy
    @echo " Analysis dependencies installed successfully."

# Runs a python script using the dedicated analysis environment.
# Example: just run-analysis qparser/embedding_dataset/generate_method_embedding.py
run-analysis SCRIPT:
    @echo ">>> Running '{{SCRIPT}}' using the '{{ANALYSIS_VENV}}' environment..."
    @{{ANALYSIS_VENV}}/bin/python {{SCRIPT}}

# Cleans up ONLY the analysis environment.
clean-analysis:
    @echo ">>> Cleaning up analysis environment..."
    @rm -rf {{ANALYSIS_VENV}}
    @echo ">>> Analysis environment removed."

clone-filtered:
    @echo "\n>>> Cloning/updating repositories from '{{REPO_LIST_FILE}}'..."
    @python scripts/clone_repos.py {{REPO_LIST_FILE}}

# Clones all required source code repositories.
clone:
    @echo ">>> Ensuring target directory 'target_github_projects' exists..."
    @mkdir -p target_github_projects

    # Qiskit repositories
    @echo "\n Processing Qiskit Repositories..."
    @for org_repo in \
        Qiskit/qiskit \
        qiskit-community/qiskit-algorithms \
        qiskit-community/qiskit-dynamics \
        qiskit-community/qiskit-experiments \
        qiskit-community/qiskit-finance \
        qiskit-community/qiskit-machine-learning \
        qiskit-community/qiskit-nature \
        qiskit-community/qiskit-optimization; do \
            dir_name=$(basename "$org_repo"); \
            if [ -d "target_github_projects/$dir_name" ]; then \
                echo "    Updating $dir_name..."; \
                (cd "target_github_projects/$dir_name" && git pull) || echo "    Could not update $dir_name, continuing..."; \
            else \
                echo "    Cloning $dir_name..."; \
                git clone --depth 1 "https://github.com/$org_repo.git" "target_github_projects/$dir_name"; \
            fi; \
    done

    # Cirq monorepo
    @echo "\n--> Processing Cirq Monorepo..."
    @if [ -d "target_github_projects/Cirq" ]; then \
        echo "    Updating Cirq..."; \
        (cd "target_github_projects/Cirq" && git pull) || echo "    Could not update Cirq, continuing..."; \
    else \
        echo "    Cloning Cirq..."; \
        git clone --depth 1 "https://github.com/quantumlib/cirq.git" "target_github_projects/Cirq"; \
    fi

    # Other frameworks
    @echo "\n--> Processing Other Frameworks..."
    @for org_repo in \
        rigetti/grove \
        amazon-braket/amazon-braket-algorithm-library \
        qutip/qutip \
        qiboteam/qibo \
        quantumlib/ReCirq \
        mit-han-lab/torchquantum \
        rigetti/pyquil \
        PennyLaneAI/pennylane \
        PennyLaneAI/qml \
        ProjectQ-Framework/ProjectQ \
        XanaduAI/strawberryfields \
        eclipse-qrisp/Qrisp \
        PennyLaneAI/qml \
        jcmgray/quimb \
        quantumlib/Qualtran \
        amazon-braket/amazon-braket-examples \
        quantumlib/OpenFermion \
        tencent-quantum-lab/tensorcircuit \
        CQCL/guppylang \
        Classiq/classiq-library; do \
            dir_name=$(basename "$org_repo"); \
            if [ -d "target_github_projects/$dir_name" ]; then \
                echo "    Updating $dir_name..."; \
                (cd "target_github_projects/$dir_name" && git pull) || echo "    Could not update $dir_name, continuing..."; \
            else \
                echo "    Cloning $dir_name..."; \
                git clone --depth 1 "https://github.com/$org_repo.git" "target_github_projects/$dir_name"; \
            fi; \
    done

    # Special cases from GitHub
    @echo "\n Processing special cases..."
    @org_repo='tensorflow/quantum'; \
    dir_name='tensorflow-quantum'; \
    if [ -d "target_github_projects/$dir_name" ]; then \
        echo "    Updating $dir_name..."; \
        (cd "target_github_projects/$dir_name" && git pull); \
    else \
        echo "    Cloning $dir_name..."; \
        git clone --depth 1 "https://github.com/$org_repo.git" "target_github_projects/$dir_name"; \
    fi

    # Download and unpack the Classiq wheel from PyPI
    @echo "\n--> Processing Classiq Wheel..."
    @if [ -d "{{CLASSIQ_SQK_DIR}}" ]; then \
        echo "    Directory '{{CLASSIQ_SQK_DIR}}' already exists, skipping download and unpack."; \
    else \
        echo "    Downloading Classiq wheel from {{CLASSIQ_WHL_URL}}..."; \
        curl -L -o /tmp/classiq.whl "{{CLASSIQ_WHL_URL}}"; \
        echo "    Unpacking wheel to '{{CLASSIQ_SQK_DIR}}'..."; \
        mkdir -p "{{CLASSIQ_SQK_DIR}}"; \
        unzip -q /tmp/classiq.whl -d "{{CLASSIQ_SQK_DIR}}"; \
        echo "    Cleaning up temporary wheel file..."; \
        rm /tmp/classiq.whl; \
        echo "    Classiq wheel successfully unpacked."; \
    fi

    @echo "\n All source repositories and files are up to date."

upgrade:
  uv lock --upgrade

_setup-macos:
    @echo "Installing uv for macOS..."
    @curl -LsSf https://astral.sh/uv/install.sh | sh

_setup-linux:
    @echo "Installing uv for Linux..."
    @curl -LsSf https://astral.sh/uv/install.sh | sh

_setup-windows:
    @echo "Installing uv for Windows..."
    @powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

default:
  @just --choose

setup:
    @just _setup-{{ os() }}