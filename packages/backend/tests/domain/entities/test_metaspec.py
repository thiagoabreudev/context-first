"""
Tests for Metaspec Entity
"""

import pytest
from datetime import datetime
from src.domain.entities.metaspec import Metaspec, MetaspecType
from src.domain.exceptions import InvalidMetaspecError


class TestMetaspec:
    """Test suite for Metaspec entity"""

    @pytest.fixture
    def valid_content(self):
        """Fixture: Valid Markdown content"""
        return """# Business Requirements

## Objective
Implement feature X

## Acceptance Criteria
- Criterion 1
- Criterion 2
"""

    def test_create_valid_metaspec(self, valid_content):
        """Test creating valid Metaspec"""
        metaspec = Metaspec(
            id="meta-123",
            demand_id="demand-456",
            type=MetaspecType.BUSINESS,
            content=valid_content,
        )
        assert metaspec.id == "meta-123"
        assert metaspec.demand_id == "demand-456"
        assert metaspec.type == MetaspecType.BUSINESS
        assert metaspec.content == valid_content
        assert metaspec.version == 1
        assert isinstance(metaspec.created_at, datetime)

    def test_all_metaspec_types_exist(self):
        """Test that all MetaspecType values are defined"""
        assert MetaspecType.BUSINESS == "business"
        assert MetaspecType.TECHNICAL == "technical"
        assert MetaspecType.ARCHITECTURE == "architecture"

    def test_cannot_create_metaspec_with_empty_id(self, valid_content):
        """Test that empty id raises ValueError"""
        with pytest.raises(ValueError, match="id cannot be empty"):
            Metaspec(
                id="",
                demand_id="demand-1",
                type=MetaspecType.BUSINESS,
                content=valid_content,
            )

    def test_cannot_create_metaspec_with_empty_demand_id(
        self, valid_content
    ):
        """Test that empty demand_id raises ValueError"""
        with pytest.raises(ValueError, match="demand_id cannot be empty"):
            Metaspec(
                id="meta-1",
                demand_id="",
                type=MetaspecType.BUSINESS,
                content=valid_content,
            )

    def test_cannot_create_metaspec_with_invalid_version(self, valid_content):
        """Test that version < 1 raises ValueError"""
        with pytest.raises(ValueError, match="version must be >= 1"):
            Metaspec(
                id="meta-1",
                demand_id="demand-1",
                type=MetaspecType.BUSINESS,
                content=valid_content,
                version=0,
            )

    def test_cannot_create_metaspec_with_empty_content(self):
        """Test that empty content raises InvalidMetaspecError"""
        with pytest.raises(
            InvalidMetaspecError, match="content cannot be empty"
        ):
            Metaspec(
                id="meta-1",
                demand_id="demand-1",
                type=MetaspecType.BUSINESS,
                content="",
            )

    def test_cannot_create_metaspec_without_markdown_headers(self):
        """Test that content without headers raises InvalidMetaspecError"""
        with pytest.raises(
            InvalidMetaspecError, match="must be valid Markdown"
        ):
            Metaspec(
                id="meta-1",
                demand_id="demand-1",
                type=MetaspecType.BUSINESS,
                content="Just plain text without headers",
            )

    def test_validate_not_empty_returns_true_for_valid_content(
        self, valid_content
    ):
        """Test validate_not_empty returns True for non-empty content"""
        metaspec = Metaspec(
            id="meta-1",
            demand_id="demand-1",
            type=MetaspecType.BUSINESS,
            content=valid_content,
        )
        assert metaspec.validate_not_empty() is True

    def test_validate_not_empty_returns_false_for_empty_string(self):
        """Test validate_not_empty returns False for empty string"""
        # Bypass __post_init__ validation for this test
        metaspec = object.__new__(Metaspec)
        metaspec.content = ""
        assert metaspec.validate_not_empty() is False

    def test_validate_markdown_format_returns_true_with_headers(
        self, valid_content
    ):
        """Test validate_markdown_format returns True when headers present"""
        metaspec = Metaspec(
            id="meta-1",
            demand_id="demand-1",
            type=MetaspecType.BUSINESS,
            content=valid_content,
        )
        assert metaspec.validate_markdown_format() is True

    def test_validate_markdown_format_returns_false_without_headers(self):
        """Test validate_markdown_format returns False without headers"""
        metaspec = object.__new__(Metaspec)
        metaspec.content = "Plain text without headers"
        assert metaspec.validate_markdown_format() is False

    def test_increment_version_increases_version_number(self, valid_content):
        """Test increment_version increases version"""
        metaspec = Metaspec(
            id="meta-1",
            demand_id="demand-1",
            type=MetaspecType.BUSINESS,
            content=valid_content,
        )
        assert metaspec.version == 1

        metaspec.increment_version()
        assert metaspec.version == 2
        assert metaspec.updated_at is not None

        metaspec.increment_version()
        assert metaspec.version == 3

    def test_increment_version_updates_timestamp(self, valid_content):
        """Test increment_version updates updated_at"""
        metaspec = Metaspec(
            id="meta-1",
            demand_id="demand-1",
            type=MetaspecType.BUSINESS,
            content=valid_content,
        )
        assert metaspec.updated_at is None

        metaspec.increment_version()
        assert metaspec.updated_at is not None
        assert isinstance(metaspec.updated_at, datetime)
