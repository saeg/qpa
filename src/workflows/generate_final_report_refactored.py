"""
Main coordination script for final report generation.

This script orchestrates the entire report generation process by using
specialized classes for different responsibilities:
- DataProcessor: Handles data loading and processing
- StatisticsCalculator: Calculates various statistics
- ReportGenerator: Generates text and markdown reports
- CSVExporter: Exports tables to CSV files
"""

from pathlib import Path

import pandas as pd

from src.conf import config
from .csv_exporter import CSVExporter
from .data_processor import DataProcessor
from .report_generator import ReportGenerator
from .statistics_calculator import StatisticsCalculator

# Configuration constants
INPUT_CSV_FILE = config.RESULTS_DIR / "quantum_concept_matches_with_patterns.csv"
REPORT_TXT_PATH = config.RESULTS_DIR / "final_pattern_report.txt"
REPORT_MD_PATH = config.DOCS_DIR / "final_pattern_report.md"
CSV_OUTPUT_DIR = config.RESULTS_DIR / "report"

PATTERN_FILES = [
    config.RESULTS_DIR / "enriched_classiq_quantum_patterns.csv",
    config.RESULTS_DIR / "enriched_pennylane_quantum_patterns.csv",
    config.RESULTS_DIR / "enriched_qiskit_quantum_patterns.csv",
]


def main():
    """Main function to orchestrate the report generation process."""
    try:
        # Step 1: Load and process data
        print("Loading and processing data...")
        data_processor = DataProcessor(INPUT_CSV_FILE, PATTERN_FILES)
        
        df = data_processor.load_main_data()
        all_patterns = data_processor.load_patterns()
        
        print(f"Loaded {len(df)} matches and {len(all_patterns)} patterns")
        
        # Step 2: Calculate statistics
        print("Calculating statistics...")
        statistics = StatisticsCalculator(df, all_patterns)
        
        # Step 3: Generate reports
        print("Generating reports...")
        report_generator = ReportGenerator(statistics)
        
        # Generate text and markdown reports
        report_generator.generate_txt_report(REPORT_TXT_PATH)
        report_generator.generate_md_report(REPORT_MD_PATH)
        
        # Step 4: Export CSV tables
        print("Exporting CSV tables...")
        csv_exporter = CSVExporter(CSV_OUTPUT_DIR)
        csv_exporter.export_all_tables(statistics)
        
        print("Report generation completed successfully!")
        
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return
    except pd.errors.EmptyDataError as e:
        print(f"Error: {e}")
        return
    except Exception as e:
        print(f"Unexpected error: {e}")
        return


if __name__ == "__main__":
    main()


