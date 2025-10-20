"""
Test suite for src/workflows/generate_final_report.py
"""

from pathlib import Path
from unittest.mock import MagicMock, mock_open, patch

import pandas as pd

from src.workflows.generate_final_report import (
    INPUT_CSV_FILE,
    LATEX_OUTPUT_DIR,
    PATTERN_FILES,
    REPORT_MD_PATH,
    REPORT_TXT_PATH,
    TOP_N_CONCEPTS,
    ReportGenerator,
    extract_framework,
    extract_project,
    load_all_patterns_from_files,
    main,
    shorten_concept_name,
)


class TestHelperFunctions:
    """Test helper functions."""

    def test_extract_framework(self):
        """Test framework extraction from concept name."""
        assert extract_framework("qiskit/circuit") == "qiskit"
        assert extract_framework("pennylane/quantum") == "pennylane"
        assert extract_framework("classiq/algorithm") == "classiq"
        assert extract_framework("invalid") == "invalid"  # Returns the string itself when no slash
        assert extract_framework("") == ""  # Returns empty string for empty input

    def test_shorten_concept_name(self):
        """Test concept name shortening."""
        assert shorten_concept_name("qiskit/circuit/QuantumCircuit") == "...QuantumCircuit"
        assert shorten_concept_name("pennylane/quantum/device") == "...device"
        assert shorten_concept_name("simple") == "...simple"
        assert shorten_concept_name("") == "..."  # Returns "..." for empty string

    def test_extract_project(self):
        """Test project extraction from file path."""
        assert extract_project("project1/file.py") == "project1"
        assert extract_project("project2/subdir/file.py") == "project2"
        assert extract_project("file.py") == "file.py"

    def test_load_all_patterns_from_files(self):
        """Test loading patterns from CSV files."""
        # Mock CSV content with header row
        mock_csv_content = "concept,summary,pattern\nconcept1,summary1,pattern1\nconcept2,summary2,pattern2\nconcept3,summary3,\n"
        
        with patch("pathlib.Path.exists", return_value=True):
            with patch("builtins.open", mock_open(read_data=mock_csv_content)):
                patterns = load_all_patterns_from_files([Path("test.csv")])
                assert "pattern1" in patterns
                assert "pattern2" in patterns
                assert "" not in patterns

    def test_load_all_patterns_from_files_missing_file(self):
        """Test loading patterns when file doesn't exist."""
        with patch("pathlib.Path.exists", return_value=False):
            patterns = load_all_patterns_from_files([Path("nonexistent.csv")])
            assert patterns == set()


class TestReportGenerator:
    """Test the ReportGenerator class."""

    def test_initialization(self):
        """Test ReportGenerator initialization."""
        # Create sample DataFrame with framework and project columns
        df = pd.DataFrame({
            "concept_name": ["qiskit/circuit", "pennylane/quantum"],
            "file_path": ["project1/file1.py", "project2/file2.py"],
            "match_type": ["name", "summary"],
            "similarity_score": [0.95, 0.85],
            "pattern": ["Pattern1", "Pattern2"],
            "framework": ["qiskit", "pennylane"],
            "project": ["project1", "project2"]
        })
        all_patterns = {"Pattern1", "Pattern2", "Pattern3"}
        
        generator = ReportGenerator(df, all_patterns)
        
        assert generator.total_matches == 2
        assert generator.unique_files_matched == 2
        assert generator.unique_concepts_matched == 2
        assert abs(generator.avg_score - 0.9) < 0.001  # Handle floating point precision

    def test_prepare_data_with_patterns(self):
        """Test data preparation with pattern data."""
        df = pd.DataFrame({
            "concept_name": ["qiskit/circuit", "pennylane/quantum"],
            "file_path": ["project1/file1.py", "project2/file2.py"],
            "match_type": ["name", "summary"],
            "similarity_score": [0.95, 0.85],
            "pattern": ["Pattern1", "Pattern2"],
            "framework": ["qiskit", "pennylane"],
            "project": ["project1", "project2"]
        })
        all_patterns = {"Pattern1", "Pattern2", "Pattern3"}
        
        generator = ReportGenerator(df, all_patterns)
        
        assert len(generator.found_patterns) == 2
        assert len(generator.unmatched_patterns) == 1
        assert "Pattern3" in generator.unmatched_patterns

    def test_prepare_data_without_patterns(self):
        """Test data preparation without pattern data."""
        df = pd.DataFrame({
            "concept_name": ["qiskit/circuit", "pennylane/quantum"],
            "file_path": ["project1/file1.py", "project2/file2.py"],
            "match_type": ["name", "summary"],
            "similarity_score": [0.95, 0.85],
            "pattern": ["N/A", "N/A"],
            "framework": ["qiskit", "pennylane"],
            "project": ["project1", "project2"]
        })
        all_patterns = {"Pattern1", "Pattern2"}
        
        generator = ReportGenerator(df, all_patterns)
        
        assert len(generator.found_patterns) == 0
        assert len(generator.unmatched_patterns) == 2

    def test_generate_txt_report(self):
        """Test TXT report generation."""
        df = pd.DataFrame({
            "concept_name": ["qiskit/circuit"],
            "file_path": ["project1/file1.py"],
            "match_type": ["name"],
            "similarity_score": [0.95],
            "pattern": ["Pattern1"],
            "framework": ["qiskit"],
            "project": ["project1"]
        })
        all_patterns = {"Pattern1"}
        
        generator = ReportGenerator(df, all_patterns)
        
        with patch("builtins.open", mock_open()) as mock_file:
            with patch("sys.stdout", mock_file):
                with patch("builtins.print") as mock_print:
                    generator.generate_txt_report(Path("test.txt"))
                    mock_file.assert_called()
                    mock_print.assert_called()

    def test_generate_md_report(self):
        """Test Markdown report generation."""
        df = pd.DataFrame({
            "concept_name": ["qiskit/circuit"],
            "file_path": ["project1/file1.py"],
            "match_type": ["name"],
            "similarity_score": [0.95],
            "pattern": ["Pattern1"],
            "framework": ["qiskit"],
            "project": ["project1"]
        })
        all_patterns = {"Pattern1"}
        
        generator = ReportGenerator(df, all_patterns)
        
        with patch("builtins.open", mock_open()) as mock_file:
            generator.generate_md_report(Path("test.md"))
            mock_file.assert_called()

    def test_write_report_content_txt(self):
        """Test report content writing for TXT format."""
        df = pd.DataFrame({
            "concept_name": ["qiskit/circuit"],
            "file_path": ["project1/file1.py"],
            "match_type": ["name"],
            "similarity_score": [0.95],
            "pattern": ["Pattern1"],
            "framework": ["qiskit"],
            "project": ["project1"]
        })
        all_patterns = {"Pattern1"}
        
        generator = ReportGenerator(df, all_patterns)
        
        with patch("builtins.print") as mock_print:
            generator._write_report_content(is_md=False)
            # Should have printed various sections
            assert mock_print.call_count > 0

    def test_write_report_content_md(self):
        """Test report content writing for Markdown format."""
        df = pd.DataFrame({
            "concept_name": ["qiskit/circuit"],
            "file_path": ["project1/file1.py"],
            "match_type": ["name"],
            "similarity_score": [0.95],
            "pattern": ["Pattern1"],
            "framework": ["qiskit"],
            "project": ["project1"]
        })
        all_patterns = {"Pattern1"}
        
        generator = ReportGenerator(df, all_patterns)
        
        # Test with a custom print function that captures output
        output_lines = []
        def capture_print(*args, **kwargs):
            output_lines.extend(args)
        
        generator._write_report_content(is_md=True, md_print=capture_print)
        # Should have captured various sections
        assert len(output_lines) > 0


class TestMainFunction:
    """Test the main function."""

    def test_main_file_not_found(self):
        """Test main function when input file doesn't exist."""
        with patch("pathlib.Path.exists", return_value=False):
            with patch("builtins.print") as mock_print:
                main()
                mock_print.assert_called_with(f"Error: Input file '{INPUT_CSV_FILE}' not found.")

    def test_main_empty_file(self):
        """Test main function with empty CSV file."""
        with patch("pathlib.Path.exists", return_value=True):
            with patch("pandas.read_csv", side_effect=pd.errors.EmptyDataError()):
                with patch("builtins.print") as mock_print:
                    main()
                    mock_print.assert_called_with(f"The file '{INPUT_CSV_FILE}' is empty.")

    def test_main_successful_execution(self):
        """Test successful main execution."""
        # Mock DataFrame
        mock_df = pd.DataFrame({
            "concept_name": ["qiskit/circuit"],
            "file_path": ["project1/file1.py"],
            "match_type": ["name"],
            "similarity_score": [0.95],
            "pattern": ["Pattern1"]
        })
        
        with patch("pathlib.Path.exists", return_value=True):
            with patch("pandas.read_csv", return_value=mock_df):
                with patch("src.workflows.generate_final_report.load_all_patterns_from_files", return_value={"Pattern1"}):
                    with patch("src.workflows.generate_final_report.ReportGenerator") as mock_generator_class:
                        mock_generator = MagicMock()
                        mock_generator_class.return_value = mock_generator
                        
                        with patch("builtins.print"):
                            main()
                            
                            # Should create ReportGenerator and generate reports
                            mock_generator_class.assert_called_once()
                            mock_generator.generate_txt_report.assert_called_once()
                            mock_generator.generate_md_report.assert_called_once()


class TestConstants:
    """Test module constants."""

    def test_input_csv_file(self):
        """Test INPUT_CSV_FILE constant."""
        assert INPUT_CSV_FILE.name == "quantum_concept_matches_with_patterns.csv"

    def test_report_paths(self):
        """Test report path constants."""
        assert REPORT_TXT_PATH.name == "final_pattern_report.txt"
        assert REPORT_MD_PATH.name == "final_pattern_report.md"
        assert LATEX_OUTPUT_DIR.name == "latex_report_tables"

    def test_pattern_files(self):
        """Test PATTERN_FILES constant."""
        assert len(PATTERN_FILES) == 3
        assert all("enriched" in str(f) for f in PATTERN_FILES)

    def test_top_n_concepts(self):
        """Test TOP_N_CONCEPTS constant."""
        assert TOP_N_CONCEPTS == 20
