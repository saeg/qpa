"""
Prepares Jupyter notebooks for code analysis.

This script is a helper tool to solve a specific problem: our static
analyzer can only read plain Python (.py) files, but a lot of useful code
is written in Jupyter Notebooks (.ipynb).

This preprocessor finds all notebooks in the project and does two
main things for each one, running them in parallel to be fast:

1.  **Converts notebooks to Python scripts:**
    - It turns each `.ipynb` file into a standard `.py` file.
    - The new script is saved in the same directory as the original notebook,
      allowing our other analysis tools to find it and parse its code.
    - It won't re-convert a notebook if the Python script is already
      newer, which saves a lot of time on subsequent runs.

2.  **Archives the original notebooks:**
    - It copies the original `.ipynb` file to a central `notebooks/` directory.
    - This creates an organized backup of every notebook found, sorted into
      folders by project name, making it easy to find and inspect them manually.
"""

import concurrent.futures
import os
import shutil
from pathlib import Path

import nbformat
from nbconvert import PythonExporter

from src.conf import config

# Define project-relative paths to be completely ignored during notebook processing.
# Any notebook found within these directories will be skipped.
IGNORED_NOTEBOOK_PATHS = {}

NOTEBOOKS_DEST_ROOT = config.PROJECT_ROOT / "notebooks"


def convert_single_notebook(ipynb_path: str):
    """
    Converts a single .ipynb file to a .py file in-place.
    The new file will be named 'original_name.ipynb.py'.
    Returns a status string.
    """
    output_py_path = ipynb_path + ".py"

    if os.path.exists(output_py_path):
        if os.path.getmtime(output_py_path) >= os.path.getmtime(ipynb_path):
            return "SKIPPED_UP_TO_DATE"

    try:
        exporter = PythonExporter()
        with open(ipynb_path, encoding="utf-8", errors="ignore") as f:
            notebook_node = nbformat.read(f, as_version=4)

        source_code, _ = exporter.from_notebook_node(notebook_node)

        with open(output_py_path, "w", encoding="utf-8") as f:
            f.write(source_code)

        return "SUCCESS"
    except Exception as e:
        return f"CONVERT_ERROR: {str(e)}"


def copy_single_notebook(
    ipynb_path: str, destination_folder_name: str, destination_root: Path
):
    """
    Copies a notebook to a structured destination folder.
    Returns a status string.
    """
    try:
        project_dest_dir = destination_root / destination_folder_name
        project_dest_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ipynb_path, project_dest_dir)
        return "COPIED_SUCCESS"
    except Exception as e:
        return f"COPY_ERROR: {str(e)}"


def process_single_notebook(
    ipynb_path: str, project_name: str, copy_destination_root: Path
):
    """
    A single worker function that performs both conversion and copying for one notebook.
    """
    conversion_status = convert_single_notebook(ipynb_path)

    # The archive destination is now ALWAYS the project's name. No special handling.
    copy_status = copy_single_notebook(ipynb_path, project_name, copy_destination_root)

    return {
        "conversion_status": conversion_status,
        "copy_status": copy_status,
    }


def run_preprocessor():
    """
    Finds all .ipynb files, filters them, then converts and copies them to an
    archive directory in parallel.
    """
    print("\n Starting Notebook Pre-processing Step ")
    print(f"Notebooks will be archived in: {NOTEBOOKS_DEST_ROOT}")

    # Step 1: Find all notebooks by walking through target project directories
    initial_notebooks_found = []
    found_paths = set()
    print("Searching for all notebooks...")

    for project_subpath in config.TARGET_PROJECTS:
        current_project_path = config.TARGET_PROJECTS_BASE_PATH / project_subpath
        project_name_for_dir = project_subpath.strip("/").replace("/", "_")
        if not current_project_path.is_dir():
            continue

        for root, dirs, files in os.walk(current_project_path):
            dirs[:] = [d for d in dirs if not d.startswith(".")]
            for filename in files:
                if filename.endswith(".ipynb"):
                    full_path = os.path.join(root, filename)
                    if full_path not in found_paths:
                        initial_notebooks_found.append(
                            {"path": full_path, "project": project_name_for_dir}
                        )
                        found_paths.add(full_path)

    # Step 2: Filter the found notebooks based on the exclusion list
    print(
        f"\nFound {len(initial_notebooks_found)} total notebooks. Applying exclusion filters..."
    )
    full_ignored_paths = {
        config.TARGET_PROJECTS_BASE_PATH / p for p in IGNORED_NOTEBOOK_PATHS
    }

    notebooks_to_process = []
    for nb_info in initial_notebooks_found:
        notebook_path = Path(nb_info["path"])
        is_ignored = any(
            ignored_dir in notebook_path.parents for ignored_dir in full_ignored_paths
        )
        if not is_ignored:
            notebooks_to_process.append(nb_info)

    if not notebooks_to_process:
        print("No .ipynb files left to pre-process after filtering.")
        print("--- Pre-processing Complete ---\n")
        return

    print(
        f"Found {len(notebooks_to_process)} unique notebooks to process after filtering. Running in parallel..."
    )

    # Step 3: Process the filtered list in parallel
    results_counter = {
        "SUCCESS": 0,
        "SKIPPED_UP_TO_DATE": 0,
        "CONVERT_ERROR": 0,
        "COPIED_SUCCESS": 0,
        "COPY_ERROR": 0,
    }
    error_messages = []

    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_info = {
            executor.submit(
                process_single_notebook,
                nb_info["path"],
                nb_info["project"],
                NOTEBOOKS_DEST_ROOT,
            ): nb_info
            for nb_info in notebooks_to_process
        }

        for future in concurrent.futures.as_completed(future_to_info):
            nb_info = future_to_info[future]
            try:
                result = future.result()
                if "CONVERT_ERROR" in result["conversion_status"]:
                    results_counter["CONVERT_ERROR"] += 1
                    error_messages.append(
                        f"  - Conversion failed for {os.path.basename(nb_info['path'])}: {result['conversion_status']}"
                    )
                else:
                    results_counter[result["conversion_status"]] += 1

                if "COPY_ERROR" in result["copy_status"]:
                    results_counter["COPY_ERROR"] += 1
                    error_messages.append(
                        f"  - Copy failed for {os.path.basename(nb_info['path'])}: {result['copy_status']}"
                    )
                else:
                    results_counter[result["copy_status"]] += 1

            except Exception as exc:
                results_counter["CONVERT_ERROR"] += 1
                results_counter["COPY_ERROR"] += 1
                error_messages.append(
                    f"  - Exception during processing of {os.path.basename(nb_info['path'])}: {exc}"
                )

    # Step 4: Print a clean summary
    print("\n--- Pre-processing Summary ---")
    print("\nConversion to .py files:")
    print(f"  - Successfully converted/updated: {results_counter['SUCCESS']}")
    print(f"  - Skipped (already up-to-date): {results_counter['SKIPPED_UP_TO_DATE']}")
    print(f"  - Errors: {results_counter['CONVERT_ERROR']}")

    print("\nCopying of .ipynb files to archive:")
    print(f"  - Successfully copied: {results_counter['COPIED_SUCCESS']}")
    print(f"  - Errors: {results_counter['COPY_ERROR']}")

    if error_messages:
        print("\nError Details:")
        for msg in error_messages:
            print(msg)

    print("\n--- Pre-processing Complete ---\n")


if __name__ == "__main__":
    run_preprocessor()
