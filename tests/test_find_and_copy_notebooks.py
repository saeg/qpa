"""
Test suite for src/preprocessing/find_and_copy_notebooks.py
"""

import os
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from src.preprocessing.find_and_copy_notebooks import (
    IGNORED_NOTEBOOK_PATHS,
    NOTEBOOKS_DEST_ROOT,
    convert_single_notebook,
    copy_single_notebook,
    process_single_notebook,
)


class TestConvertSingleNotebook:
    """Test the convert_single_notebook function."""

    def test_skip_up_to_date_file(self):
        """Test skipping conversion when target file is newer."""
        ipynb_path = "test.ipynb"
        
        with patch("os.path.exists", return_value=True):
            with patch("os.path.getmtime") as mock_getmtime:
                # Mock getmtime to return different times
                def mock_mtime(path):
                    if path == "test.ipynb":
                        return 500  # ipynb file is older
                    elif path == "test.ipynb.py":
                        return 1000  # py file is newer
                mock_getmtime.side_effect = mock_mtime
                
                result = convert_single_notebook(ipynb_path)
                assert result == "SKIPPED_UP_TO_DATE"

    def test_conversion_error(self):
        """Test conversion error handling."""
        ipynb_path = "test.ipynb"
        
        with patch("os.path.exists", return_value=False):
            with patch("nbformat.read", side_effect=Exception("Read error")):
                result = convert_single_notebook(ipynb_path)
                assert "CONVERT_ERROR:" in result


class TestCopySingleNotebook:
    """Test the copy_single_notebook function."""

    def test_successful_copy(self):
        """Test successful notebook copying."""
        ipynb_path = "test.ipynb"
        destination_folder_name = "project1"
        destination_root = Path("/dest")
        
        with patch("pathlib.Path.mkdir"):
            with patch("shutil.copy2") as mock_copy2:
                result = copy_single_notebook(ipynb_path, destination_folder_name, destination_root)
                assert result == "COPIED_SUCCESS"
                mock_copy2.assert_called_once_with(ipynb_path, destination_root / "project1")

    def test_copy_error(self):
        """Test copy error handling."""
        ipynb_path = "test.ipynb"
        destination_folder_name = "project1"
        destination_root = Path("/dest")
        
        with patch("pathlib.Path.mkdir"):
            with patch("shutil.copy2", side_effect=Exception("Copy error")):
                result = copy_single_notebook(ipynb_path, destination_folder_name, destination_root)
                assert result == "COPY_ERROR: Copy error"


class TestProcessSingleNotebook:
    """Test the process_single_notebook function."""

    def test_successful_processing(self):
        """Test successful notebook processing."""
        ipynb_path = "test.ipynb"
        project_name = "project1"
        copy_destination_root = Path("/dest")
        
        with patch("src.preprocessing.find_and_copy_notebooks.convert_single_notebook", return_value="SUCCESS"):
            with patch("src.preprocessing.find_and_copy_notebooks.copy_single_notebook", return_value="COPIED_SUCCESS"):
                result = process_single_notebook(ipynb_path, project_name, copy_destination_root)
                
                assert result["conversion_status"] == "SUCCESS"
                assert result["copy_status"] == "COPIED_SUCCESS"


class TestConstants:
    """Test module constants."""

    def test_ignored_notebook_paths(self):
        """Test IGNORED_NOTEBOOK_PATHS constant."""
        assert isinstance(IGNORED_NOTEBOOK_PATHS, dict)

    def test_notebooks_dest_root(self):
        """Test NOTEBOOKS_DEST_ROOT constant."""
        assert NOTEBOOKS_DEST_ROOT.name == "notebooks"
