import csv
import sys
from pathlib import Path

import pandas as pd

from src.conf import config

INPUT_CSV_FILE = config.RESULTS_DIR / 'quantum_concept_matches_with_patterns.csv'
REPORT_PATH = config.RESULTS_DIR / 'final_pattern_report.txt'

PATTERN_FILES = [
    config.RESULTS_DIR / 'enriched_classiq_quantum_patterns.csv',
    config.RESULTS_DIR / 'enriched_pennylane_quantum_patterns.csv',
    config.RESULTS_DIR / 'enriched_qiskit_quantum_patterns.csv'
]
LATEX_OUTPUT_DIR = config.RESULTS_DIR / 'latex_report_tables'


TOP_N_CONCEPTS = 20


def extract_framework(concept_name: str) -> str:
    """Extracts the source framework name (e.g., 'qiskit') from a concept path."""
    try:
        return concept_name.strip('/').split('/')[0]
    except (AttributeError, IndexError):
        return "unknown"


def shorten_concept_name(full_name: str) -> str:
    """Shortens a full concept path to the format '...concept_name' for readability."""
    try:
        last_part = full_name.replace('/', '.').split('.')[-1]
        return f"...{last_part}"
    except Exception:
        return full_name


def extract_project(file_path: str) -> str:
    """Extracts the target project's root directory from a file path."""
    try:
        return Path(file_path).parts[0]
    except IndexError:
        return file_path


def load_all_patterns_from_files(file_paths: list[Path]) -> set[str]:
    """Reads all pattern CSVs to get a master set of all possible patterns."""
    all_patterns = set()
    for path in file_paths:
        if path.exists():
            with open(path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                next(reader)  # Skip header
                for row in reader:
                    if len(row) >= 3 and row[2].strip():
                        all_patterns.add(row[2].strip())
    return all_patterns


def generate_latex_table(data: pd.DataFrame | pd.Series, output_filepath: Path, caption: str, label: str,
                         headers: list[str], column_format: str, add_total: bool = False):
    """Generates a standard LaTeX table from a pandas object and saves it to a file."""
    output_filepath.parent.mkdir(parents=True, exist_ok=True)
    df = data.reset_index() if isinstance(data, pd.Series) else data.reset_index()

    latex_parts = [
        "\\begin{table}[h!]",
        "\\centering",
        f"\\caption{{{caption}}}",
        f"\\label{{{label}}}",
        f"\\begin{{tabularx}}{{\\columnwidth}}{{{column_format}}}",
        "\\toprule",
        " & ".join(headers) + " \\\\",
        "\\midrule",
    ]

    for _, row in df.iterrows():
        sanitized_items = [str(item).replace("&", "\\&").replace("_", "\\_") for item in row]
        latex_parts.append(" & ".join(sanitized_items) + " \\\\")

    if add_total:
        total = df.iloc[:, -1].sum()
        latex_parts.extend([
            "\\midrule",
            f"\\textbf{{Total}} & \\textbf{{{total}}} \\\\",
        ])

    latex_parts.extend(["\\bottomrule", "\\end{tabularx}", "\\end{table}"])

    with open(output_filepath, 'w', encoding='utf-8') as f:
        f.write("\n".join(latex_parts))
    print(f"  -> Generated LaTeX table: {output_filepath.name}")


def generate_top_concepts_latex_table(data: pd.DataFrame, output_filepath: Path):
    """Generates the specialized Top Concepts LaTeX table with its unique formatting."""
    output_filepath.parent.mkdir(parents=True, exist_ok=True)
    latex_parts = [
        "\\begin{table}[ht]",
        "\\centering",
        f"\\caption{{Top {TOP_N_CONCEPTS} Most Frequently Matched Quantum Concepts}}",
        "\\label{tab:top-quantum-concepts}",
        "\\begin{tabular*}{\\columnwidth}{@{} l @{\\extracolsep{\\fill}} l r @{}}",
        "\\toprule",
        "\\textbf{Source Framework} & \\textbf{Concept Name} & \\textbf{Matches} \\\\",
        "\\midrule",
    ]

    for _, row in data.iterrows():
        framework = str(row['Framework']).replace("_", "\\_")
        concept = str(row['Concept']).replace("_", "\\_")
        matches = row['Matches']
        latex_parts.append(f"{framework} & \\texttt{{{concept}}} & {matches} \\\\")

    latex_parts.extend(["\\bottomrule", "\\end{tabular*}", "\\end{table}"])

    with open(output_filepath, 'w', encoding='utf-8') as f:
        f.write("\n".join(latex_parts))
    print(f"  -> Generated LaTeX table: {output_filepath.name}")


def analyze_results():
    """
    Main function to load data, perform analysis, and generate both text and LaTeX reports.
    """
    # --- 1. Load and Prepare Data ---
    if not INPUT_CSV_FILE.exists():
        print(f"Error: Input file '{INPUT_CSV_FILE}' not found.")
        return

    try:
        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', 1200)
        df = pd.read_csv(INPUT_CSV_FILE, delimiter=';')
    except pd.errors.EmptyDataError:
        print(f"The file '{INPUT_CSV_FILE}' is empty.")
        return

    print(f"Analyzing data from '{INPUT_CSV_FILE}'...")

    # Enrich the DataFrame with new columns for easier analysis
    df['framework'] = df['concept_name'].apply(extract_framework)
    df['project'] = df['file_path'].apply(extract_project)

    # --- 2. Calculate Key Performance Indicators (KPIs) ---

    # Overall summary metrics
    total_matches = len(df)
    unique_files_matched = df['file_path'].nunique()
    unique_concepts_matched = df['concept_name'].nunique()
    avg_score = df['similarity_score'].mean()

    # Breakdown metrics
    matches_by_type = df['match_type'].value_counts()
    avg_score_by_type = df.groupby('match_type')['similarity_score'].mean()
    matches_by_framework = df['framework'].value_counts()
    matches_by_project = df['project'].value_counts()

    # Prepare data for the Top Concepts table
    top_concepts_overall = df['concept_name'].value_counts().nlargest(TOP_N_CONCEPTS).reset_index()
    top_concepts_overall.columns = ['concept_name', 'Matches']
    framework_map = df[['concept_name', 'framework']].drop_duplicates()
    top_concepts_df = pd.merge(top_concepts_overall, framework_map, on='concept_name')
    top_concepts_df['Concept'] = top_concepts_df['concept_name'].apply(shorten_concept_name)
    top_concepts_df['Framework'] = top_concepts_df['framework'].str.capitalize()
    top_20_table_data = top_concepts_df[['Framework', 'Concept', 'Matches']]

    # Pattern-related metrics
    df_with_patterns = df[df['pattern'].notna() & (df['pattern'] != 'N/A')].copy()
    all_possible_patterns = load_all_patterns_from_files(PATTERN_FILES)
    found_patterns = set(df_with_patterns['pattern'].unique())
    unmatched_patterns = sorted(list(all_possible_patterns - found_patterns))

    if not df_with_patterns.empty:
        matches_by_pattern = df_with_patterns['pattern'].value_counts()
        avg_score_by_pattern = df_with_patterns.groupby('pattern')['similarity_score'].mean()
        patterns_in_frameworks = df_with_patterns.groupby('framework')['pattern'].value_counts()
        cross_framework_analysis = df_with_patterns.groupby('pattern').agg(
            total_matches=('pattern', 'size'),
            source_framework_names=('framework', lambda n: ', '.join(sorted(n.unique()))),
            target_project_coverage=('project', 'nunique'),
            target_project_names=('project', lambda p: ', '.join(sorted(p.unique())))
        )
        source_table = cross_framework_analysis[['total_matches', 'source_framework_names']].sort_values(
            by='total_matches', ascending=False)
        adoption_table = cross_framework_analysis[['target_project_coverage', 'target_project_names']].sort_values(
            by='target_project_coverage', ascending=False)

    # --- 3. Generate All LaTeX Table Files ---
    print(f"\nGenerating LaTeX tables in '{LATEX_OUTPUT_DIR}'...")

    generate_top_concepts_latex_table(top_20_table_data, LATEX_OUTPUT_DIR / 'top_20_matched_concepts.tex')
    generate_latex_table(matches_by_framework, LATEX_OUTPUT_DIR / 'matches_by_source_framework.tex',
                         caption="Matches by Source Framework", label="tab:matches_by_framework",
                         headers=["\\textbf{Source Framework}", "\\textbf{Number of Matches}"], column_format="X c",
                         add_total=True)
    generate_latex_table(matches_by_project, LATEX_OUTPUT_DIR / 'matches_by_target_project.tex',
                         caption="Matches by Target Project", label="tab:matches_by_project",
                         headers=["\\textbf{Target Project}", "\\textbf{Number of Matches}"], column_format="X c",
                         add_total=True)

    if not df_with_patterns.empty:
        generate_latex_table(source_table, LATEX_OUTPUT_DIR / 'source_pattern_analysis.tex',
                             caption="Source Pattern Analysis (Where Patterns Originate)",
                             label="tab:source_pattern_analysis",
                             headers=["\\textbf{Quantum Pattern}", "\\textbf{Total Matches}",
                                      "\\textbf{Source Frameworks}"], column_format="X r l")
        generate_latex_table(adoption_table, LATEX_OUTPUT_DIR / 'adoption_pattern_analysis.tex',
                             caption="Adoption Pattern Analysis (Where Patterns are Used)",
                             label="tab:adoption_pattern_analysis",
                             headers=["\\textbf{Quantum Pattern}", "\\textbf{Project Coverage}",
                                      "\\textbf{Found In Projects}"], column_format="X r l")
        multiline_header = "\\textbf{\\begin{tabular}{@{}c@{}}Number of\\\\Concepts\\end{tabular}}"
        for framework, data in patterns_in_frameworks.groupby(level=0):
            generate_latex_table(data.droplevel(0), LATEX_OUTPUT_DIR / f'{framework}_patterns_summary.tex',
                                 caption=f"Summary of {framework.capitalize()} Quantum Patterns and Concept Counts",
                                 label=f"tab:{framework}_quantum_patterns",
                                 headers=["\\textbf{Quantum Pattern}", multiline_header], column_format="X c",
                                 add_total=True)

    original_stdout = sys.stdout
    with open(REPORT_PATH, 'w', encoding='utf-8') as f:
        sys.stdout = f

        print("=" * 80)
        print("                      QUANTUM CONCEPT ANALYSIS REPORT")
        print("=" * 80)

        print("\n--- I. Overall Summary ---")
        print(f"Total Matches Found:          {total_matches}")
        print(f"Unique Files with Matches:    {unique_files_matched}")
        print(f"Unique Concepts Matched:      {unique_concepts_matched}")
        print(f"Total Patterns Defined:       {len(all_possible_patterns)}")
        print(f"Total Patterns Found:         {len(found_patterns)}")
        print(f"Average Similarity Score:     {avg_score:.4f}")

        print("\n--- II. Match Type Breakdown ---")
        print(matches_by_type.to_string())
        print("\nAverage Score by Match Type:")
        print(avg_score_by_type.round(4).to_string())

        print("\n" + "-" * 80)

        print("\n--- III. Source Framework & Target Project Breakdown ---")
        print(f"\nMatches by Source Framework:")
        print(matches_by_framework.to_string())
        print(f"\nMatches by Target Project:")
        print(matches_by_project.to_string())

        print("\n" + "-" * 80)

        if not df_with_patterns.empty:
            print("\n--- IV. Cross-Framework Pattern Analysis ---")
            print("\nTable 4.1: Source Pattern Analysis (Where patterns originate)")
            print(source_table.rename(
                columns={'total_matches': 'Total Matches', 'source_framework_names': 'Source Frameworks'}).to_string())
            print("\n\nTable 4.2: Adoption Pattern Analysis (Where patterns are used)")
            print(adoption_table.rename(columns={'target_project_coverage': 'Project Coverage',
                                                 'target_project_names': 'Found In Projects'}).to_string())

            print("\n" + "-" * 80)

            print("\n--- V. Quantum Pattern Analysis ---")
            print(f"\nPatterns by Match Count (Overall):")
            print(matches_by_pattern.to_string())
            print("\nAverage Score by Pattern:")
            print(avg_score_by_pattern.round(4).sort_values(ascending=False).to_string())
            print("\nAll Patterns within each Source Framework (Sorted by Frequency):")
            for framework, data in patterns_in_frameworks.groupby(level=0):
                print(f"\n  -- {framework} --")
                print(data.droplevel(0).to_string())

        print("\n" + "-" * 80)

        print("\n--- VI. Top Matched Concepts ---")
        print(f"\nTop {TOP_N_CONCEPTS} Most Frequently Matched Concepts:")
        print(top_20_table_data.to_string(index=False))

        print("\n" + "-" * 80)

        print("\n--- VII. Unmatched Pattern Analysis ---")
        if unmatched_patterns:
            print(
                f"\nThe following {len(unmatched_patterns)} patterns from the source files were NOT found in any project:")
            for pattern in unmatched_patterns:
                print(f"  - {pattern}")
        else:
            print("\nAll patterns defined in the source files were found in the analysis.")

        print("\n" + "=" * 80)
        print("                              END OF REPORT")
        print("=" * 80)

    sys.stdout = original_stdout
    print(f"\nText report successfully generated and saved to '{REPORT_PATH}'")


if __name__ == '__main__':
    analyze_results()
