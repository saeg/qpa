"""
Loads the final analysis results, performs summarization, and generates reports
in multiple formats (TXT, Markdown, and LaTeX).
"""
import csv
import sys
from pathlib import Path
import pandas as pd
from src.conf import config

INPUT_CSV_FILE = config.RESULTS_DIR / 'quantum_concept_matches_with_patterns.csv'
REPORT_TXT_PATH = config.RESULTS_DIR / 'final_pattern_report.txt'
REPORT_MD_PATH = config.DOCS_DIR / 'final_pattern_report.md'
LATEX_OUTPUT_DIR = config.RESULTS_DIR / 'latex_report_tables'

PATTERN_FILES = [
    config.RESULTS_DIR / 'enriched_classiq_quantum_patterns.csv',
    config.RESULTS_DIR / 'enriched_pennylane_quantum_patterns.csv',
    config.RESULTS_DIR / 'enriched_qiskit_quantum_patterns.csv'
]
TOP_N_CONCEPTS = 20

# --- Helper Functions ---
def extract_framework(concept_name: str) -> str:
    try:
        return concept_name.strip('/').split('/')[0]
    except (AttributeError, IndexError):
        return "unknown"

def shorten_concept_name(full_name: str) -> str:
    try:
        last_part = full_name.replace('/', '.').split('.')[-1]
        return f"...{last_part}"
    except Exception:
        return full_name

def extract_project(file_path: str) -> str:
    try:
        return Path(file_path).parts[0]
    except IndexError:
        return file_path

def load_all_patterns_from_files(file_paths: list[Path]) -> set[str]:
    all_patterns = set()
    for path in file_paths:
        if path.exists():
            with open(path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                next(reader)
                for row in reader:
                    if len(row) >= 3 and row[2].strip():
                        all_patterns.add(row[2].strip())
    return all_patterns

# --- ReportGenerator Class ---
class ReportGenerator:
    def __init__(self, df: pd.DataFrame, all_patterns: set):
        self.df = df
        self.all_patterns = all_patterns
        self._prepare_data()

    def _prepare_data(self):
        """Pre-calculates all the metrics and dataframes needed for the reports."""
        self.total_matches = len(self.df)
        self.unique_files_matched = self.df['file_path'].nunique()
        self.unique_concepts_matched = self.df['concept_name'].nunique()
        self.avg_score = self.df['similarity_score'].mean()

        self.matches_by_type = self.df['match_type'].value_counts()
        self.avg_score_by_type = self.df.groupby('match_type')['similarity_score'].mean()
        self.matches_by_framework = self.df['framework'].value_counts()
        self.matches_by_project = self.df['project'].value_counts()

        top_concepts_overall = self.df['concept_name'].value_counts().nlargest(TOP_N_CONCEPTS).reset_index()
        top_concepts_overall.columns = ['concept_name', 'Matches']
        framework_map = self.df[['concept_name', 'framework']].drop_duplicates()
        top_concepts_df = pd.merge(top_concepts_overall, framework_map, on='concept_name')
        top_concepts_df['Concept'] = top_concepts_df['concept_name'].apply(shorten_concept_name)
        top_concepts_df['Framework'] = top_concepts_df['framework'].str.capitalize()
        self.top_20_table_data = top_concepts_df[['Framework', 'Concept', 'Matches']]

        self.df_with_patterns = self.df[self.df['pattern'].notna() & (self.df['pattern'] != 'N/A')].copy()
        self.found_patterns = set(self.df_with_patterns['pattern'].unique())
        self.unmatched_patterns = sorted(list(self.all_patterns - self.found_patterns))

        if not self.df_with_patterns.empty:
            self.matches_by_pattern = self.df_with_patterns['pattern'].value_counts()
            self.avg_score_by_pattern = self.df_with_patterns.groupby('pattern')['similarity_score'].mean()
            self.patterns_in_frameworks = self.df_with_patterns.groupby('framework')['pattern'].value_counts()

            cross_framework_analysis = self.df_with_patterns.groupby('pattern').agg(
                total_matches=('pattern', 'size'),
                source_framework_names=('framework', lambda n: ', '.join(sorted(n.unique()))),
                target_project_coverage=('project', 'nunique'),
                target_project_names=('project', lambda p: ', '.join(sorted(p.unique())))
            )
            self.source_table = cross_framework_analysis[['total_matches', 'source_framework_names']].sort_values(by='total_matches', ascending=False)
            self.adoption_table = cross_framework_analysis[['target_project_coverage', 'target_project_names']].sort_values(by='target_project_coverage', ascending=False)

    def generate_txt_report(self, path: Path):
        """Generates the plain text report."""
        original_stdout = sys.stdout
        with open(path, 'w', encoding='utf-8') as f:
            sys.stdout = f
            self._write_report_content(is_md=False)
        sys.stdout = original_stdout
        print(f"Text report successfully generated at '{path}'")

    def generate_md_report(self, path: Path):
        """Generates the Markdown report."""
        with open(path, 'w', encoding='utf-8') as f:
            # Redirect print to the file
            def md_print(*args, **kwargs):
                print(*args, file=f, **kwargs)
            self._write_report_content(is_md=True, md_print=md_print)
        print(f"Markdown report successfully generated at '{path}'")

    def _write_report_content(self, is_md: bool, md_print=print):
        """Writes the report content, adapting format for TXT or MD."""
        # Helper to format tables
        def to_format(df, index=False, headers="keys"):
            if is_md:
                return df.to_markdown(index=index, headers=headers)
            else:
                return df.to_string(index=index, header=True if headers=="keys" else bool(headers))

        # Title
        if is_md:
            md_print("# QUANTUM CONCEPT ANALYSIS REPORT\n")
        else:
            print("="*80 + "\n" + "                      QUANTUM CONCEPT ANALYSIS REPORT" + "\n" + "="*80)

        # I. Overall Summary
        md_print("## I. Overall Summary" if is_md else "\n--- I. Overall Summary ---")
        md_print(f"- **Total Matches Found:** {self.total_matches}" if is_md else f"Total Matches Found:          {self.total_matches}")
        md_print(f"- **Unique Files with Matches:** {self.unique_files_matched}" if is_md else f"Unique Files with Matches:    {self.unique_files_matched}")
        md_print(f"- **Unique Concepts Matched:** {self.unique_concepts_matched}" if is_md else f"Unique Concepts Matched:      {self.unique_concepts_matched}")
        md_print(f"- **Total Patterns Defined:** {len(self.all_patterns)}" if is_md else f"Total Patterns Defined:       {len(self.all_patterns)}")
        md_print(f"- **Total Patterns Found:** {len(self.found_patterns)}" if is_md else f"Total Patterns Found:         {len(self.found_patterns)}")
        md_print(f"- **Average Similarity Score:** {self.avg_score:.4f}" if is_md else f"Average Similarity Score:     {self.avg_score:.4f}")

        # II. Match Type Breakdown
        md_print("\n## II. Match Type Breakdown" if is_md else "\n--- II. Match Type Breakdown ---")
        md_print("\n### Match Type Counts\n" if is_md else "")
        md_print(to_format(self.matches_by_type.reset_index()))
        md_print("\n### Average Score by Match Type\n" if is_md else "\nAverage Score by Match Type:")
        md_print(to_format(self.avg_score_by_type.round(4).reset_index()))

        md_print("\n---\n" if is_md else "\n" + "-"*80)

        # III. Source Framework & Target Project Breakdown
        md_print("## III. Source Framework & Target Project Breakdown" if is_md else "\n--- III. Source Framework & Target Project Breakdown ---")
        md_print("\n### Matches by Source Framework\n" if is_md else "\nMatches by Source Framework:")
        md_print(to_format(self.matches_by_framework.reset_index()))
        md_print("\n### Matches by Target Project\n" if is_md else "\nMatches by Target Project:")
        md_print(to_format(self.matches_by_project.reset_index()))

        md_print("\n---\n" if is_md else "\n" + "-"*80)

        # IV & V. Pattern Analysis
        if not self.df_with_patterns.empty:
            md_print("## IV. Cross-Framework Pattern Analysis" if is_md else "\n--- IV. Cross-Framework Pattern Analysis ---")
            source_headers = {'total_matches': 'Total Matches', 'source_framework_names': 'Source Frameworks'}
            md_print("\n### Table 4.1: Source Pattern Analysis (Where patterns originate)\n" if is_md else "\nTable 4.1: Source Pattern Analysis (Where patterns originate)")
            md_print(to_format(self.source_table.reset_index().rename(columns=source_headers)))

            adoption_headers = {'target_project_coverage': 'Project Coverage', 'target_project_names': 'Found In Projects'}
            md_print("\n### Table 4.2: Adoption Pattern Analysis (Where patterns are used)\n" if is_md else "\n\nTable 4.2: Adoption Pattern Analysis (Where patterns are used)")
            md_print(to_format(self.adoption_table.reset_index().rename(columns=adoption_headers)))

            md_print("\n---\n" if is_md else "\n" + "-"*80)

            md_print("## V. Quantum Pattern Analysis" if is_md else "\n--- V. Quantum Pattern Analysis ---")
            md_print("\n### Patterns by Match Count (Overall)\n" if is_md else "\nPatterns by Match Count (Overall):")
            md_print(to_format(self.matches_by_pattern.reset_index()))

            md_print("\n### Average Score by Pattern\n" if is_md else "\nAverage Score by Pattern:")
            md_print(to_format(self.avg_score_by_pattern.round(4).sort_values(ascending=False).reset_index()))

            md_print("\n### All Patterns within each Source Framework (Sorted by Frequency)\n" if is_md else "\nAll Patterns within each Source Framework (Sorted by Frequency):")
            for framework, data in self.patterns_in_frameworks.groupby(level=0):
                md_print(f"\n#### {framework.capitalize()}\n" if is_md else f"\n  -- {framework} --")
                md_print(to_format(data.droplevel(0).reset_index()))

        md_print("\n---\n" if is_md else "\n" + "-"*80)

        # VI. Top Matched Concepts
        md_print("## VI. Top Matched Concepts" if is_md else "\n--- VI. Top Matched Concepts ---")
        md_print(f"\n### Top {TOP_N_CONCEPTS} Most Frequently Matched Concepts\n" if is_md else f"\nTop {TOP_N_CONCEPTS} Most Frequently Matched Concepts:")
        md_print(to_format(self.top_20_table_data, headers=['Framework', 'Concept', 'Matches']))

        md_print("\n---\n" if is_md else "\n" + "-"*80)

        # VII. Unmatched Pattern Analysis
        md_print("## VII. Unmatched Pattern Analysis" if is_md else "\n--- VII. Unmatched Pattern Analysis ---")
        if self.unmatched_patterns:
            md_print(f"\nThe following **{len(self.unmatched_patterns)}** patterns from the source files were **NOT found** in any project:\n" if is_md else f"\nThe following {len(self.unmatched_patterns)} patterns from the source files were NOT found in any project:")
            for pattern in self.unmatched_patterns:
                md_print(f"- {pattern}")
        else:
            md_print("\nAll patterns defined in the source files were found in the analysis.")

        # End of Report
        if not is_md:
            print("\n" + "="*80 + "\n" + "                              END OF REPORT" + "\n" + "="*80)

# --- Main Execution ---
def main():
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
    df['framework'] = df['concept_name'].apply(extract_framework)
    df['project'] = df['file_path'].apply(extract_project)

    all_patterns = load_all_patterns_from_files(PATTERN_FILES)

    reporter = ReportGenerator(df, all_patterns)

    # Generate both reports
    reporter.generate_txt_report(REPORT_TXT_PATH)
    reporter.generate_md_report(REPORT_MD_PATH)

if __name__ == '__main__':
    main()