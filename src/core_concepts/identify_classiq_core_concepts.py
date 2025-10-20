"""
Generates a structured dataset of core quantum concepts by dynamically importing
the public API (`__all__`) from the `classiq` SDK.

This script now performs three main actions:
1.  Identifies all public functions from specified Classiq modules,
    extracts their docstrings and metadata, saves them to a JSON file, and
    stores them in a ChromaDB vector database.
2.  Saves the complete source code of each identified function
    to a separate .py file for inspection.
3.  Saves the name and summary of each concept to a CSV file for
    easy review.
"""

import ast
import csv
import importlib
import json
import logging
import re
from pathlib import Path
from typing import Any

import classiq

from src.conf import config

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

SOURCE_SNIPPETS_DIR = config.RESULTS_DIR / "classiq_source_snippets"


TARGET_MODULES = [
    "classiq.open_library.functions",
]

SOURCE_CODE_SEARCH_PATHS = [
    "open_library/functions",
    "qmod/builtins/functions",
]

COLLECTION_NAME = "core_quantum_concepts"

OUTPUT_JSON_PATH = config.RESULTS_DIR / "classiq_quantum_concepts.json"
OUTPUT_CSV_PATH = config.RESULTS_DIR / "classiq_quantum_concepts.csv"
VEND_LIB_PATH = config.PROJECT_ROOT / ".venv" / "lib"

BOILERPLATE_STRINGS = [
    "[Qmod Classiq-library function]",
    "[Qmod core-library function]",
]


def _create_summary_from_docstring(docstring: str) -> str:
    """
    Extracts the first two sentences from a docstring to create a summary.
    """
    if not docstring:
        return ""

    first_paragraph = docstring.strip().split("\n\n")[0]
    text_block = " ".join(first_paragraph.split())

    parts = text_block.split(".")

    sentences = [s.strip() for s in parts if s.strip()]

    if len(sentences) >= 2:
        return f"{sentences[0]}. {sentences[1]}."
    elif sentences:
        return f"{sentences[0]}."
    else:
        return first_paragraph


class _PublicApiVisitor(ast.NodeVisitor):
    """AST visitor to find functions listed in a public API set and extract their details."""

    def __init__(
        self,
        source_text: str,
        file_path: Path,
        sdk_root: Path,
        public_api_names: set[str],
    ):
        self.found_concepts: dict[str, dict[str, Any]] = {}
        self.public_api_names = public_api_names
        self.source_text = source_text
        self.file_path = file_path
        self.sdk_root = sdk_root

    def visit_FunctionDef(self, node: ast.FunctionDef):
        if node.name in self.public_api_names:
            function_docstring = ast.get_docstring(node)

            if function_docstring:
                # 1. Start with the raw docstring.
                cleaned_docstring = function_docstring

                for bp_string in BOILERPLATE_STRINGS:
                    pattern = re.compile(r"\s*" + re.escape(bp_string) + r"\.?\s*")
                    # Replace with a single space to avoid merging words, then strip later.
                    cleaned_docstring = pattern.sub(" ", cleaned_docstring)

                # 3. Perform a final strip to remove leading/trailing whitespace or characters.
                #    This is key for handling docstrings that *only* contained boilerplate.
                cleaned_docstring = cleaned_docstring.strip()

                # 4. CRITICAL CHECK: If the docstring is now empty, skip this function.
                if not cleaned_docstring:
                    logging.warning(
                        f"  -> Skipping public API function '{node.name}' in {self.file_path.name} because its docstring only contained boilerplate."
                    )
                    self.generic_visit(node)
                    return
                # End of changed section >>>

                # 5. Generate the summary from the fully cleaned docstring
                summary = _create_summary_from_docstring(cleaned_docstring)

                relative_path = self.file_path.relative_to(self.sdk_root)
                module_path_parts = list(relative_path.parts)
                module_path_parts[-1] = relative_path.stem
                full_concept_name = (
                    f"/classiq/{'.'.join(module_path_parts)}.{node.name}"
                )

                if full_concept_name not in self.found_concepts:
                    function_source_code = ast.get_source_segment(
                        self.source_text, node
                    )

                    self.found_concepts[full_concept_name] = {
                        "name": full_concept_name,
                        "summary": summary,
                        "docstring": cleaned_docstring,
                        "source_code": function_source_code,
                    }
                    logging.debug(f"  -> Found public API concept: {node.name}")
            else:
                logging.warning(
                    f"  -> Skipping public API function '{node.name}' in {self.file_path.name} because it has NO docstring."
                )
        self.generic_visit(node)


def _find_concepts_in_file(
    py_path: Path, sdk_root: Path, public_api_names: set[str]
) -> list:
    try:
        with open(py_path, encoding="utf-8") as f:
            source_text = f.read()
            tree = ast.parse(source_text, filename=str(py_path))
        visitor = _PublicApiVisitor(source_text, py_path, sdk_root, public_api_names)
        visitor.visit(tree)
        return list(visitor.found_concepts.values())
    except Exception as e:
        logging.warning(f"Could not parse file {py_path.name}: {e}")
        return []


def _get_sdk_root_path() -> Path | None:
    """Finds the installed Classiq SDK path directly from the imported package."""
    try:
        # __path__[0] gives the directory of the package
        sdk_path = Path(classiq.__path__[0])
        if sdk_path.is_dir():
            logging.info(f"Found installed Classiq SDK at: {sdk_path}")
            return sdk_path
        else:
            logging.error(f"Classiq SDK path does not exist: '{sdk_path}'")
            return None
    except (ImportError, AttributeError, IndexError):
        logging.error(
            "Could not find the installed 'classiq' package. Is it installed in the venv?"
        )
        return None


def extract_core_concepts(
    package_root_path: Path, public_api_names: set[str]
) -> list[dict[str, Any]]:
    """
    Scans a predefined set of directories for the source code of public API functions.
    """
    all_concepts_data = {}
    documented_function_names = set()

    for sub_dir in SOURCE_CODE_SEARCH_PATHS:
        if documented_function_names == public_api_names:
            logging.info("All public API functions found. Halting search.")
            break

        search_path = package_root_path / sub_dir
        if not search_path.is_dir():
            logging.warning(f"Source code directory not found, skipping: {search_path}")
            continue

        all_py_files = list(search_path.rglob("*.py"))
        logging.info(f"Scanning {len(all_py_files)} files in '{sub_dir}'...")

        for py_file in sorted(all_py_files):
            if py_file.name == "__init__.py":
                continue

            found_concepts = _find_concepts_in_file(
                py_file, package_root_path, public_api_names
            )
            for concept in found_concepts:
                simple_name = concept["name"].split(".")[-1]
                if concept["name"] not in all_concepts_data:
                    all_concepts_data[concept["name"]] = concept
                    documented_function_names.add(simple_name)

    return list(all_concepts_data.values())


def run_final_analysis(
    found_concepts_data: list[dict[str, Any]], expected_public_functions: set[str]
):
    """Compares found concepts against the expected list and prints a report."""
    logging.info("\n--- Final Analysis Report ---")
    found_function_names = {item["name"].split(".")[-1] for item in found_concepts_data}
    logging.info(
        f"Total concepts found and documented by script: {len(found_function_names)}"
    )
    logging.info(
        f"Total functions in public API (`__all__`): {len(expected_public_functions)}"
    )
    missing_functions = expected_public_functions - found_function_names
    print("\n Found and Documented Public API Functions:")
    if found_function_names:
        for i, func in enumerate(sorted(list(found_function_names)), 1):
            print(f"  {i}. {func}")
    else:
        print("  None.")
    print("\nPublic API Functions Not Found/Documented (e.g., missing docstrings):")
    if missing_functions:
        for i, func in enumerate(sorted(list(missing_functions)), 1):
            print(f"  {i}. {func}")
    else:
        print("  None. All public functions were found and documented!")
    logging.info("\n--- End of Analysis Report ---")


def main():
    """Main function to run extraction and save results."""
    logging.info("--- Starting Core Quantum Concepts Generation and Storage ---")

    package_root_path = _get_sdk_root_path()
    if not package_root_path:
        return

    all_public_apis = set()
    for module_name in TARGET_MODULES:
        try:
            module = importlib.import_module(module_name)
            public_api_names = set(module.__all__)
            logging.info(
                f"Targeting public API for '{module_name}' with {len(public_api_names)} functions."
            )
            all_public_apis.update(public_api_names)
        except (ImportError, AttributeError) as e:
            logging.error(f"Could not load public API for module '{module_name}': {e}")
            return

    # Now run the extraction using the combined public API list
    final_data = extract_core_concepts(package_root_path, all_public_apis)

    if not final_data:
        logging.warning("No quantum concepts were found.")
        logging.info("--- Generation Complete ---")
        return

    logging.info(
        f"\nSuccessfully extracted {len(final_data)} unique, documented public API concepts."
    )

    run_final_analysis(final_data, all_public_apis)

    _save_source_code_snippets(final_data)

    try:
        json_data = [
            {k: v for k, v in item.items() if k != "source_code"} for item in final_data
        ]
        OUTPUT_JSON_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(OUTPUT_JSON_PATH, "w", encoding="utf-8") as f:
            json.dump(json_data, f, indent=2)
        logging.info(f"Debug dataset saved successfully to: '{OUTPUT_JSON_PATH}'")
    except Exception as e:
        logging.error(f"Error: Could not save the debug dataset to JSON. {e}")

    _save_concepts_to_csv(final_data)

    logging.info("\n--- Generation Complete ---")


def _save_source_code_snippets(concepts_data: list[dict[str, Any]]):
    if not concepts_data:
        return
    logging.info("\n--- Saving source code snippets for debugging ---")
    SOURCE_SNIPPETS_DIR.mkdir(parents=True, exist_ok=True)
    logging.info(
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
                logging.warning(
                    f"Could not write source file for '{concept['name']}': {e}"
                )
    logging.info(f"Successfully saved {count} source code files.")


def _save_concepts_to_csv(concepts_data: list[dict[str, Any]]):
    """Saves the concept name and summary to a CSV file."""
    if not concepts_data:
        logging.warning("No concepts data to save to CSV.")
        return

    logging.info("\n--- Saving concept summaries to CSV ---")
    headers = ["name", "summary"]

    try:
        OUTPUT_CSV_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(OUTPUT_CSV_PATH, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            for concept in concepts_data:
                row = {
                    "name": concept.get("name", ""),
                    "summary": concept.get("summary", ""),
                }
                writer.writerow(row)
        logging.info(
            f"Successfully saved {len(concepts_data)} concepts to: '{OUTPUT_CSV_PATH}'"
        )
    except Exception as e:
        logging.error(f"Error: Could not save the dataset to CSV. {e}")


if __name__ == "__main__":
    main()
