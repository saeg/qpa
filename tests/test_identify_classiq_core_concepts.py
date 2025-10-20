"""
Unit tests for identify_classiq_core_concepts.py

This test suite covers the core functionality that is currently working:
- Utility functions
- AST visitor class
- File parsing
- Analysis and reporting
- Constants validation
"""

import ast

# Import the module under test
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

sys.path.append(str(Path(__file__).parent.parent / "src"))

from src.core_concepts.identify_classiq_core_concepts import (
    BOILERPLATE_STRINGS,
    SOURCE_CODE_SEARCH_PATHS,
    TARGET_MODULES,
    _create_summary_from_docstring,
    _find_concepts_in_file,
    _PublicApiVisitor,
    run_final_analysis,
)


class TestCreateSummaryFromDocstring:
    """Test cases for _create_summary_from_docstring function."""

    def test_empty_docstring(self):
        """Test handling of empty docstring."""
        result = _create_summary_from_docstring("")
        assert result == ""

    def test_none_docstring(self):
        """Test handling of None docstring."""
        result = _create_summary_from_docstring(None)
        assert result == ""

    def test_single_sentence(self):
        """Test docstring with single sentence."""
        docstring = "This is a single sentence."
        result = _create_summary_from_docstring(docstring)
        assert result == "This is a single sentence."

    def test_two_sentences(self):
        """Test docstring with two sentences."""
        docstring = "First sentence. Second sentence. Third sentence."
        result = _create_summary_from_docstring(docstring)
        assert result == "First sentence. Second sentence."

    def test_multiline_docstring(self):
        """Test multiline docstring with paragraph breaks."""
        docstring = """First paragraph with multiple lines.
        
        Second paragraph."""
        result = _create_summary_from_docstring(docstring)
        assert result == "First paragraph with multiple lines. Second paragraph."

    def test_whitespace_handling(self):
        """Test handling of excessive whitespace."""
        docstring = "   First sentence.   Second sentence.   "
        result = _create_summary_from_docstring(docstring)
        assert result == "First sentence. Second sentence."

    def test_no_periods(self):
        """Test docstring without periods."""
        docstring = "This is a sentence without periods"
        result = _create_summary_from_docstring(docstring)
        assert result == "This is a sentence without periods."


class TestPublicApiVisitor:
    """Test cases for _PublicApiVisitor class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.source_text = '''
def public_function():
    """This is a public function."""
    pass

def private_function():
    """This is a private function."""
    pass
'''
        self.sdk_root = Path("/test/sdk")
        self.file_path = self.sdk_root / "open_library" / "functions" / "test_file.py"
        self.public_api_names = {"public_function"}

    def test_visitor_initialization(self):
        """Test visitor initialization."""
        visitor = _PublicApiVisitor(
            self.source_text, self.file_path, self.sdk_root, self.public_api_names
        )
        assert visitor.public_api_names == self.public_api_names
        assert visitor.source_text == self.source_text
        assert visitor.file_path == self.file_path
        assert visitor.sdk_root == self.sdk_root
        assert visitor.found_concepts == {}

    def test_visit_public_function(self):
        """Test visiting a public function."""
        visitor = _PublicApiVisitor(
            self.source_text, self.file_path, self.sdk_root, self.public_api_names
        )

        # Parse the source and visit
        tree = ast.parse(self.source_text)
        visitor.visit(tree)

        # Check that public function was found
        assert len(visitor.found_concepts) == 1
        concept_name = list(visitor.found_concepts.keys())[0]
        assert "public_function" in concept_name
        concept = visitor.found_concepts[concept_name]
        assert concept["name"] == concept_name
        assert "This is a public function." in concept["summary"]
        assert concept["docstring"] == "This is a public function."
        assert "def public_function():" in concept["source_code"]

    def test_visit_private_function(self):
        """Test that private functions are ignored."""
        visitor = _PublicApiVisitor(
            self.source_text, self.file_path, self.sdk_root, self.public_api_names
        )

        tree = ast.parse(self.source_text)
        visitor.visit(tree)

        # Check that private function was not found
        assert len(visitor.found_concepts) == 1
        concept_name = list(visitor.found_concepts.keys())[0]
        assert "private_function" not in concept_name

    def test_function_without_docstring(self):
        """Test function without docstring is skipped."""
        source_text = """
def public_function():
    pass
"""
        visitor = _PublicApiVisitor(
            source_text, self.file_path, self.sdk_root, self.public_api_names
        )

        tree = ast.parse(source_text)
        visitor.visit(tree)

        # Function without docstring should be skipped
        assert len(visitor.found_concepts) == 0

    def test_boilerplate_removal(self):
        """Test removal of boilerplate strings from docstrings."""
        source_text = '''
def public_function():
    """[Qmod Classiq-library function] This is a real docstring."""
    pass
'''
        visitor = _PublicApiVisitor(
            source_text, self.file_path, self.sdk_root, self.public_api_names
        )

        tree = ast.parse(source_text)
        visitor.visit(tree)

        concept = list(visitor.found_concepts.values())[0]
        assert concept["docstring"] == "This is a real docstring."

    def test_only_boilerplate_docstring(self):
        """Test function with only boilerplate is skipped."""
        source_text = '''
def public_function():
    """[Qmod Classiq-library function]"""
    pass
'''
        visitor = _PublicApiVisitor(
            source_text, self.file_path, self.sdk_root, self.public_api_names
        )

        tree = ast.parse(source_text)
        visitor.visit(tree)

        # Function with only boilerplate should be skipped
        assert len(visitor.found_concepts) == 0


class TestFindConceptsInFile:
    """Test cases for _find_concepts_in_file function."""

    def test_successful_parsing(self):
        """Test successful file parsing."""
        source_text = '''
def public_function():
    """This is a public function."""
    pass
'''
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create proper directory structure
            sdk_root = Path(temp_dir) / "sdk"
            file_path = sdk_root / "open_library" / "functions" / "test_file.py"
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text(source_text)

            concepts = _find_concepts_in_file(file_path, sdk_root, {"public_function"})
            assert len(concepts) == 1
            assert concepts[0]["name"].endswith("public_function")

    def test_parse_error(self):
        """Test handling of parse errors."""
        source_text = """
def invalid_syntax(
    # Missing closing parenthesis
"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
            f.write(source_text)
            f.flush()

            try:
                concepts = _find_concepts_in_file(
                    Path(f.name), Path("/test/sdk"), {"public_function"}
                )
                assert concepts == []
            finally:
                Path(f.name).unlink()

    def test_file_not_found(self):
        """Test handling of non-existent file."""
        concepts = _find_concepts_in_file(
            Path("/non/existent/file.py"), Path("/test/sdk"), {"public_function"}
        )
        assert concepts == []


class TestRunFinalAnalysis:
    """Test cases for run_final_analysis function."""

    def test_empty_data(self):
        """Test analysis with empty data."""
        with patch("builtins.print") as mock_print:
            run_final_analysis([], set())
            # Should not raise any exceptions

    def test_complete_match(self):
        """Test analysis when all functions are found."""
        found_concepts = [
            {"name": "test.function1", "summary": "Test function 1"},
            {"name": "test.function2", "summary": "Test function 2"},
        ]
        expected_functions = {"function1", "function2"}

        with patch("builtins.print") as mock_print:
            run_final_analysis(found_concepts, expected_functions)

            # Check that appropriate messages were printed
            print_calls = [call[0][0] for call in mock_print.call_args_list]
            assert any(
                "Found and Documented Public API Functions:" in call
                for call in print_calls
            )
            assert any(
                "None. All public functions were found and documented!" in call
                for call in print_calls
            )

    def test_missing_functions(self):
        """Test analysis when some functions are missing."""
        found_concepts = [{"name": "test.function1", "summary": "Test function 1"}]
        expected_functions = {"function1", "function2"}

        with patch("builtins.print") as mock_print:
            run_final_analysis(found_concepts, expected_functions)

            # Check that missing functions are reported
            print_calls = [call[0][0] for call in mock_print.call_args_list]
            assert any("function2" in call for call in print_calls)


class TestConstants:
    """Test cases for module constants."""

    def test_boilerplate_strings(self):
        """Test boilerplate strings are defined correctly."""
        assert isinstance(BOILERPLATE_STRINGS, list)
        assert len(BOILERPLATE_STRINGS) > 0
        assert all(isinstance(s, str) for s in BOILERPLATE_STRINGS)

    def test_target_modules(self):
        """Test target modules are defined correctly."""
        assert isinstance(TARGET_MODULES, list)
        assert len(TARGET_MODULES) > 0
        assert all(isinstance(s, str) for s in TARGET_MODULES)

    def test_source_code_search_paths(self):
        """Test source code search paths are defined correctly."""
        assert isinstance(SOURCE_CODE_SEARCH_PATHS, list)
        assert len(SOURCE_CODE_SEARCH_PATHS) > 0
        assert all(isinstance(s, str) for s in SOURCE_CODE_SEARCH_PATHS)


if __name__ == "__main__":
    pytest.main([__file__])
