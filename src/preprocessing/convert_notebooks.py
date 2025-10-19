"""
A utility script to convert Jupyter Notebooks to Python scripts.

This script walks through a specified source directory (e.g., 'notebooks/'),
finds all `.ipynb` files, and converts them into executable `.py` files.

The key features are:
-   It preserves the original directory structure in the
    destination folder (e.g., 'converted_notebooks/').
-   It skips conversion if the target `.py` file already exists
    and is newer than the source `.ipynb` file, saving time on subsequent runs.
"""

import concurrent.futures
from pathlib import Path
from src.conf import config
import nbformat
from nbconvert import PythonExporter

# notebooks is in ../notebooks
DEFAULT_SOURCE_DIR = config.PROJECT_ROOT / 'notebooks'
DEFAULT_DEST_DIR = config.PROJECT_ROOT / 'converted_notebooks'


def convert_single_notebook(ipynb_path: Path, py_path: Path) -> str:
    """
    Converts a single .ipynb file to a .py file.

    Checks modification times to avoid unnecessary reconversion.

    Args:
        ipynb_path: The path to the source Jupyter Notebook.
        py_path: The path where the destination Python script should be saved.

    Returns:
        A status string: "SUCCESS", "SKIPPED", or "ERROR".
    """
    try:
        # Efficiency check: skip if the .py file is already up-to-date.
        if py_path.exists() and py_path.stat().st_mtime >= ipynb_path.stat().st_mtime:
            return "SKIPPED"

        # Ensure the parent directory exists
        py_path.parent.mkdir(parents=True, exist_ok=True)

        # Perform the conversion
        exporter = PythonExporter()
        with open(ipynb_path, 'r', encoding='utf-8', errors='ignore') as f:
            notebook_node = nbformat.read(f, as_version=4)

        source_code, _ = exporter.from_notebook_node(notebook_node)

        with open(py_path, 'w', encoding='utf-8') as f:
            f.write(source_code)

        return "SUCCESS"
    except Exception as e:
        # Return the error message for better diagnostics
        return f"ERROR: {e.__class__.__name__}"


def process_all_notebooks(source_dir: Path, dest_dir: Path):
    """
    Finds and converts all notebooks from a source to a destination directory.

    Args:
        source_dir: The root directory containing the .ipynb files.
        dest_dir: The root directory where the .py files will be saved.
    """
    print("--- Starting Notebook Conversion Utility ---")

    if not source_dir.is_dir():
        print(f"\nERROR: Source directory not found: '{source_dir}'")
        print("------------------------------------------")
        return

    print(f"Source:      '{source_dir}'")
    print(f"Destination: '{dest_dir}'")

    # Find all notebook files recursively
    notebook_paths = list(source_dir.glob("**/*.ipynb"))

    if not notebook_paths:
        print("\nNo .ipynb files found in the source directory.")
        print("--- Conversion Complete ---")
        return

    print(f"\nFound {len(notebook_paths)} notebooks to process...")

    tasks = []
    for ipynb_path in notebook_paths:
        # Calculate the corresponding output path while preserving the structure
        relative_path = ipynb_path.relative_to(source_dir)
        py_path = (dest_dir / relative_path).with_suffix(".py")
        tasks.append((ipynb_path, py_path))

    # Initialize counters for the summary
    results = {"SUCCESS": 0, "SKIPPED": 0, "ERROR": 0}

    # Use ThreadPoolExecutor for parallel I/O-bound operations
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_path = {
            executor.submit(convert_single_notebook, ipynb_path, py_path): ipynb_path
            for ipynb_path, py_path in tasks
        }

        for future in concurrent.futures.as_completed(future_to_path):
            path = future_to_path[future]
            try:
                status = future.result()
                if "ERROR" in status:
                    results["ERROR"] += 1
                    print(f"[ERROR] {path.relative_to(source_dir)} -> {status}")
                else:
                    results[status] += 1
                    if status == "SUCCESS":
                        print(f"[{status}] Converted {path.relative_to(source_dir)}")

            except Exception as exc:
                results["ERROR"] += 1
                print(f"[CRITICAL ERROR] Processing {path.relative_to(source_dir)} generated an exception: {exc}")

    print("\n--- Conversion Summary ---")
    print(f"Successfully converted: {results['SUCCESS']}")
    print(f"Skipped (up-to-date): {results['SKIPPED']}")
    print(f"Errors encountered:   {results['ERROR']}")
    print("--------------------------")


if __name__ == "__main__":
    process_all_notebooks(DEFAULT_SOURCE_DIR, DEFAULT_DEST_DIR)