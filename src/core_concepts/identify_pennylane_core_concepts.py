import ast
import csv
import json
from pathlib import Path
from typing import Any

from src.conf import config

# Define input paths relative to the project root
PENNYLANE_PROJECT_ROOT = config.PROJECT_ROOT / "target_github_projects" / "pennylane"

# Define output directories and names

SOURCE_SNIPPETS_DIR = config.RESULTS_DIR / "pennylane_source_snippets"
OUTPUT_JSON_PATH = config.RESULTS_DIR / "pennylane_quantum_concepts.json"

# Define the specific subdirectories to scan within the PennyLane repo
SEARCH_SUBDIRS = ["pennylane/templates/"]


class _PennylaneConceptVisitor(ast.NodeVisitor):
    """AST visitor to find classes with docstrings and extract their details."""

    def __init__(self, source_text: str, file_path: Path, sdk_root: Path):
        self.found_concepts: dict[str, dict[str, Any]] = {}
        self.source_text = source_text
        self.file_path = file_path
        self.sdk_root = sdk_root

    def visit_ClassDef(self, node: ast.ClassDef):
        """This method is called for every class definition found."""
        class_name = node.name
        docstring = ast.get_docstring(node)

        if docstring:
            relative_path = self.file_path.relative_to(self.sdk_root)
            module_path_parts = list(relative_path.parts)
            module_path_parts[-1] = relative_path.stem  # Remove .py extension
            module_path_str = ".".join(module_path_parts)
            full_concept_name = f"/pennylane/{module_path_str}.{class_name}"

            if full_concept_name not in self.found_concepts:
                cleaned_docstring = docstring.strip()
                summary = cleaned_docstring.split("\n\n")[0].strip().replace("\n", " ")
                class_source_code = ast.get_source_segment(self.source_text, node)

                self.found_concepts[full_concept_name] = {
                    "name": full_concept_name,
                    "summary": summary,
                    "docstring": cleaned_docstring,
                    "source_code": class_source_code,
                }
        self.generic_visit(node)


def _find_concepts_in_file(py_path: Path, sdk_root: Path) -> list:
    """Parses a single Python file and returns a list of found concepts."""
    try:
        with open(py_path, encoding="utf-8") as f:
            source_text = f.read()
            if len(source_text.strip()) < 50:
                return []
            tree = ast.parse(source_text, filename=str(py_path))

        visitor = _PennylaneConceptVisitor(source_text, py_path, sdk_root)
        visitor.visit(tree)
        return list(visitor.found_concepts.values())
    except Exception as e:
        print(f"  - Warning: Could not parse file {py_path.name}: {e}")
        return []


def extract_pennylane_concepts() -> list[dict[str, Any]]:
    """
    Scans the local PennyLane repository, extracts quantum concepts from classes,
    and returns them as a list.
    """
    if not PENNYLANE_PROJECT_ROOT.is_dir():
        print(
            f"Error: PennyLane project root not found at '{PENNYLANE_PROJECT_ROOT.resolve()}'"
        )
        print("Please ensure the repository is cloned at that location.")
        return []

    print(f"Scanning PennyLane project at: {PENNYLANE_PROJECT_ROOT.resolve()}")

    all_py_files = []
    for sub_dir in SEARCH_SUBDIRS:
        search_path = PENNYLANE_PROJECT_ROOT / sub_dir
        if search_path.is_dir():
            all_py_files.extend(list(search_path.rglob("*.py")))
        else:
            print(f"  - Warning: SDK subdirectory not found, skipping: {search_path}")

    if not all_py_files:
        print("  - No Python files found in the PennyLane search directories.")
        return []

    all_concepts_data = {}
    print(f"\nProcessing {len(all_py_files)} total Python files from the SDK...")
    for py_file in sorted(all_py_files):
        if py_file.name == "__init__.py":
            continue

        found_concepts = _find_concepts_in_file(py_file, PENNYLANE_PROJECT_ROOT)
        for concept in found_concepts:
            if concept["name"] not in all_concepts_data:
                all_concepts_data[concept["name"]] = concept

    return list(all_concepts_data.values())


def _save_source_code_snippets(concepts_data: list[dict[str, Any]]):
    """
    Saves the source code of each concept's class to a separate .py file.
    """
    if not concepts_data:
        return

    print("\n--- Saving source code snippets for debugging ---")
    SOURCE_SNIPPETS_DIR.mkdir(parents=True, exist_ok=True)
    print(
        f"Saving {len(concepts_data)} source files to: {SOURCE_SNIPPETS_DIR.resolve()}"
    )

    count = 0
    for concept in concepts_data:
        source_code = concept.get("source_code")
        if source_code:
            sanitized_name = concept["name"].replace("/", "_").replace(".", "_")
            if sanitized_name.startswith("_"):
                sanitized_name = sanitized_name[1:]
            file_name = f"{sanitized_name}.py"

            output_path = SOURCE_SNIPPETS_DIR / file_name
            try:
                with open(output_path, "w", encoding="utf-8") as f:
                    f.write(source_code)
                count += 1
            except Exception as e:
                print(
                    f"  - Warning: Could not write source file for '{concept['name']}': {e}"
                )

    print(f"Successfully saved {count} source code files.")


def _save_concepts_to_csv(concepts_data: list[dict[str, Any]]):
    """Saves the name and summary of each concept to a CSV file."""
    if not concepts_data:
        return

    output_csv_path = OUTPUT_JSON_PATH.with_suffix(".csv")
    print(f"\nSaving summary data to CSV: {output_csv_path.resolve()}")

    try:
        with open(output_csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["name", "summary"])
            for concept in concepts_data:
                writer.writerow([concept.get("name", ""), concept.get("summary", "")])
        print(
            f"Successfully saved {len(concepts_data)} concepts to '{output_csv_path.name}'."
        )
    except Exception as e:
        print(f"Error: Could not save the dataset to CSV. {e}")


def main():
    """Main function to run extraction and save results."""
    print("--- Starting PennyLane Core Quantum Concepts Generation and Storage ---")

    final_data = extract_pennylane_concepts()

    if not final_data:
        print("\nNo quantum concepts were found.")
        print("--- Generation Complete ---")
        return

    print(f"\nSuccessfully extracted {len(final_data)} unique quantum concepts.")

    _save_source_code_snippets(final_data)
    _save_concepts_to_csv(final_data)

    try:
        json_data = [
            {k: v for k, v in item.items() if k != "source_code"} for item in final_data
        ]
        OUTPUT_JSON_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(OUTPUT_JSON_PATH, "w", encoding="utf-8") as f:
            json.dump(json_data, f, indent=2)
        print(f"Dataset saved successfully to: '{OUTPUT_JSON_PATH}'")
    except Exception as e:
        print(f"Error: Could not save the dataset to JSON. {e}")

    print("\n--- Generation Complete ---")


if __name__ == "__main__":
    main()
