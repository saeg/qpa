"""
Generates a detailed Markdown report from the quantum_patterns.json file.

This script reads the structured JSON data downloaded from the PlanQK Pattern Atlas
and converts it into a human-readable Markdown document, with clear sections
for each pattern's intent, context, solution, and more.
"""
import json

# Assuming you have a config file that defines the data directory.
# If not, you can replace `config.DATA_DIR` with `Path("data")`.
from src.conf import config

# Define the input and output file paths
INPUT_JSON_PATH = config.RESULTS_DIR / "quantum_patterns.json"
OUTPUT_MD_PATH = config.DOCS_DIR / "quantum_patterns_report.md"


def generate_markdown_for_pattern(pattern: dict) -> str:
    """Formats a single pattern dictionary into a Markdown string."""
    # Use a list of strings for efficient building
    md_parts = []

    # --- Title (H2) ---
    md_parts.append(f"## {pattern.get('name', 'Unnamed Pattern')}\n")

    # --- Alias (if it exists and is not a placeholder) ---
    alias = pattern.get('alias')
    if alias and alias.strip() != '—':
        md_parts.append(f"***Also known as:** {alias}*\n")

    # --- Sections (H3 + content) ---
    sections = {
        "Intent": "intent",
        "Context": "context",
        "Problem & Forces": "forces",
        "Solution": "solution",
        "Resulting Context": "result",
    }

    for title, key in sections.items():
        content = pattern.get(key)
        if content:
            # Add section header and the content, ensuring proper spacing
            md_parts.append(f"### {title}\n")
            md_parts.append(f"{content.strip()}\n")

    return "\n".join(md_parts)


def main():
    """Main function to read JSON and write the Markdown report."""
    print(f"Reading quantum patterns from: {INPUT_JSON_PATH}")
    if not INPUT_JSON_PATH.exists():
        print(f"Error: Input file not found at '{INPUT_JSON_PATH}'.")
        print("Please run 'just download_pattern_list' first.")
        return

    try:
        with open(INPUT_JSON_PATH, 'r', encoding='utf-8') as f:
            patterns_data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error: Could not parse JSON file. {e}")
        return

    # --- Build the full Markdown document ---
    all_md_content = [
        "# Quantum Software Patterns Report\n",
        "This document is an auto-generated report of the quantum software patterns sourced from the [PlanQK Pattern Atlas](https://patternatlas.planqk.de/).\n",
    ]

    print(f"Found {len(patterns_data)} patterns to process...")

    for i, pattern in enumerate(patterns_data):
        print(f"  - Formatting pattern: {pattern.get('name')}")
        md_for_pattern = generate_markdown_for_pattern(pattern)
        all_md_content.append(md_for_pattern)

        # Add a horizontal rule between patterns, but not after the last one
        if i < len(patterns_data) - 1:
            all_md_content.append("\n---\n")

    final_md = "\n".join(all_md_content)

    # --- Write the final report to disk ---
    print(f"\nWriting Markdown report to: {OUTPUT_MD_PATH}")
    try:
        with open(OUTPUT_MD_PATH, 'w', encoding='utf-8') as f:
            f.write(final_md)
        print("Report generation complete.")
    except IOError as e:
        print(f"Error: Could not write to file '{OUTPUT_MD_PATH}'. {e}")


if __name__ == "__main__":
    main()