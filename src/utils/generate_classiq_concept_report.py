"""
Generates a Markdown summary of the raw quantum concepts extracted from each framework.

This script reads the output CSV files from the 'identify-concepts' step and
compiles them into a single, human-readable Markdown document. Each framework's
concepts are presented in a separate table.
"""

import csv
from pathlib import Path

from src.conf import config

# Define the input CSV files and their specific delimiters
INPUT_FILES = {
    "Qiskit": {
        "path": config.RESULTS_DIR / "qiskit_quantum_concepts.csv",
        "delimiter": ";",
    },
    "PennyLane": {
        "path": config.RESULTS_DIR / "pennylane_quantum_concepts.csv",
        "delimiter": ",",
    },
    "Classiq": {
        "path": config.RESULTS_DIR / "classiq_quantum_concepts.csv",
        "delimiter": ",",
    },
}

OUTPUT_MD_PATH = config.DOCS_DIR / "extracted_concepts_summary.md"


def read_concepts_from_csv(file_path: Path, delimiter: str) -> list[dict]:
    """Reads concept data from a CSV file with a specific delimiter."""
    if not file_path.exists():
        print(f"  - Warning: Input file not found: {file_path}")
        return []

    concepts = []
    try:
        with open(file_path, encoding="utf-8") as f:
            # DictReader automatically uses the first row as headers
            reader = csv.DictReader(f, delimiter=delimiter)
            for row in reader:
                concepts.append(row)
        return concepts
    except Exception as e:
        print(f"  - Error reading {file_path}: {e}")
        return []


def generate_markdown_table(concepts: list[dict]) -> str:
    """Formats a list of concepts into a Markdown table string."""
    if not concepts:
        return "*No concepts were extracted for this framework.*\n"

    # Use a list of strings for efficient building
    table_parts = []

    # --- Table Header ---
    table_parts.append("| Concept Name | Summary |")
    table_parts.append("|--------------|---------|")

    # --- Table Rows ---
    for concept in concepts:
        # Get data, providing default empty strings if keys are missing
        name = concept.get("name", "N/A").strip()
        summary = concept.get("summary", "").strip()

        # Clean up content for Markdown table cells
        # Replace pipe characters to prevent breaking table formatting
        name = name.replace("|", "\\|")
        # Remove newlines and extra whitespace from summary
        summary = " ".join(summary.split()).replace("|", "\\|")

        table_parts.append(f"| `{name}` | {summary} |")

    return "\n".join(table_parts) + "\n"


def main():
    """Main function to read all CSVs and write the final Markdown report."""
    print("--- Generating Summary Report for Extracted Quantum Concepts ---")

    # --- Build the full Markdown document ---
    all_md_content = [
        "# Summary of Extracted Quantum Concepts (Pre-Classification)\n",
        "This document summarizes the raw quantum concepts automatically extracted from the source code of the Qiskit, PennyLane, and Classiq frameworks. These concepts were identified by the `src/core_concepts/identify_*.py` scripts and serve as the input for the manual pattern classification step.\n",
    ]

    for framework_name, details in INPUT_FILES.items():
        print(f"\nProcessing concepts for {framework_name}...")

        # Add a section header for the framework
        all_md_content.append(f"## {framework_name} Concepts\n")

        # Read the concepts from the corresponding CSV file
        concepts = read_concepts_from_csv(details["path"], details["delimiter"])

        if concepts:
            print(f"  - Found {len(concepts)} concepts. Generating table...")
            # Generate and append the Markdown table for these concepts
            table_md = generate_markdown_table(concepts)
            all_md_content.append(table_md)
        else:
            all_md_content.append("*No concepts found or file was missing.*\n")

    final_md = "\n".join(all_md_content)

    # --- Write the final report to disk ---
    print(f"\nWriting Markdown report to: {OUTPUT_MD_PATH}")
    try:
        with open(OUTPUT_MD_PATH, "w", encoding="utf-8") as f:
            f.write(final_md)
        print("--- Report generation complete. ---")
    except OSError as e:
        print(f"Error: Could not write to file '{OUTPUT_MD_PATH}'. {e}")


if __name__ == "__main__":
    main()
