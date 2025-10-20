"""
Test suite for src/preprocessing/github_search.py
"""

from unittest.mock import MagicMock, patch

import pytest

from src.preprocessing.github_search import (
    EXCLUSION_KEYWORDS,
    MAX_INACTIVITY_MONTHS,
    MIN_CONTRIBUTORS,
    MIN_STARS,
    OUTPUT_FOLDER,
    SORT_BY,
    SORT_ORDER,
    TARGET_RESULT_COUNT,
    check_for_exclusion,
)


class TestCheckForExclusion:
    """Test the check_for_exclusion function."""

    def test_exclusion_by_name(self):
        """Test exclusion based on repository name."""
        mock_repo = MagicMock()
        mock_repo.full_name = "test/provider-repo"
        mock_repo.description = "A test repository"
        mock_repo.topics = []
        
        is_excluded, reason = check_for_exclusion(mock_repo)
        assert is_excluded is True
        assert "provider" in reason

    def test_no_exclusion(self):
        """Test when repository should not be excluded."""
        mock_repo = MagicMock()
        mock_repo.full_name = "test/quantum-algorithm"
        mock_repo.description = "A quantum algorithm library"
        mock_repo.topics = ["quantum", "algorithms"]
        
        is_excluded, reason = check_for_exclusion(mock_repo)
        assert is_excluded is False
        assert reason is None


class TestConstants:
    """Test module constants."""

    def test_search_constants(self):
        """Test search-related constants."""
        assert TARGET_RESULT_COUNT == 60
        assert SORT_BY == "stars"
        assert SORT_ORDER == "desc"

    def test_filter_constants(self):
        """Test filtering constants."""
        assert MIN_STARS == 50
        assert MIN_CONTRIBUTORS == 10
        assert MAX_INACTIVITY_MONTHS == 12

    def test_exclusion_keywords(self):
        """Test exclusion keywords constant."""
        assert isinstance(EXCLUSION_KEYWORDS, list)
        assert "provider" in EXCLUSION_KEYWORDS
        assert "hardware" in EXCLUSION_KEYWORDS

    def test_output_folder(self):
        """Test output folder constant."""
        assert OUTPUT_FOLDER.name == "data"
