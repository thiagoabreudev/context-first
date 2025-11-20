"""
Tests for Project Entity
"""

import pytest
from datetime import datetime
from src.domain.entities.project import Project
from src.domain.value_objects.context_budget import ContextBudget
from src.domain.exceptions import ContextBudgetExceededError


class TestProject:
    """Test suite for Project entity"""

    @pytest.fixture
    def valid_budget(self):
        """Fixture: Valid ContextBudget"""
        return ContextBudget(max_tokens=10000, used_tokens=2000)

    @pytest.fixture
    def valid_project(self, valid_budget):
        """Fixture: Valid Project"""
        return Project(
            id="proj-123",
            name="Test Project",
            description="A test project",
            owner_id="user-456",
            context_budget=valid_budget,
        )

    def test_create_valid_project(self, valid_budget):
        """Test creating valid Project"""
        project = Project(
            id="proj-123",
            name="Test Project",
            description="A test project",
            owner_id="user-456",
            context_budget=valid_budget,
        )
        assert project.id == "proj-123"
        assert project.name == "Test Project"
        assert project.owner_id == "user-456"
        assert project.context_budget == valid_budget
        assert isinstance(project.created_at, datetime)

    def test_cannot_create_project_with_empty_id(self, valid_budget):
        """Test that empty id raises ValueError"""
        with pytest.raises(ValueError, match="id cannot be empty"):
            Project(
                id="",
                name="Test",
                description="Test",
                owner_id="user-1",
                context_budget=valid_budget,
            )

    def test_cannot_create_project_with_empty_name(self, valid_budget):
        """Test that empty name raises ValueError"""
        with pytest.raises(ValueError, match="name cannot be empty"):
            Project(
                id="proj-1",
                name="",
                description="Test",
                owner_id="user-1",
                context_budget=valid_budget,
            )

    def test_cannot_create_project_with_whitespace_only_name(
        self, valid_budget
    ):
        """Test that whitespace-only name raises ValueError"""
        with pytest.raises(ValueError, match="name cannot be empty"):
            Project(
                id="proj-1",
                name="   ",
                description="Test",
                owner_id="user-1",
                context_budget=valid_budget,
            )

    def test_cannot_create_project_with_empty_owner_id(self, valid_budget):
        """Test that empty owner_id raises ValueError"""
        with pytest.raises(ValueError, match="owner_id cannot be empty"):
            Project(
                id="proj-1",
                name="Test",
                description="Test",
                owner_id="",
                context_budget=valid_budget,
            )

    def test_can_consume_tokens_with_sufficient_budget(self, valid_project):
        """Test can_consume_tokens returns True when budget is sufficient"""
        assert valid_project.can_consume_tokens(5000) is True

    def test_can_consume_tokens_with_insufficient_budget(self, valid_project):
        """Test can_consume_tokens returns False when budget exceeded"""
        assert valid_project.can_consume_tokens(10000) is False

    def test_consume_tokens_succeeds_with_sufficient_budget(
        self, valid_project
    ):
        """Test consume_tokens updates budget correctly"""
        initial_used = valid_project.context_budget.used_tokens
        valid_project.consume_tokens(1000)

        assert (
            valid_project.context_budget.used_tokens == initial_used + 1000
        )
        assert valid_project.updated_at is not None

    def test_consume_tokens_raises_error_when_budget_exceeded(
        self, valid_project
    ):
        """Test consume_tokens raises error when budget insufficient"""
        with pytest.raises(
            ContextBudgetExceededError,
            match="Cannot consume 10000 tokens.*Only 8000 remaining",
        ):
            valid_project.consume_tokens(10000)

    def test_consume_tokens_updates_timestamp(self, valid_project):
        """Test that consume_tokens updates updated_at"""
        assert valid_project.updated_at is None
        valid_project.consume_tokens(100)
        assert valid_project.updated_at is not None
        assert isinstance(valid_project.updated_at, datetime)

    def test_is_budget_critical_when_critical(self):
        """Test is_budget_critical returns True when < 10% remaining"""
        budget = ContextBudget(max_tokens=1000, used_tokens=950)
        project = Project(
            id="proj-1",
            name="Test",
            description="Test",
            owner_id="user-1",
            context_budget=budget,
        )
        assert project.is_budget_critical() is True

    def test_is_budget_critical_when_not_critical(self):
        """Test is_budget_critical returns False when > 10% remaining"""
        budget = ContextBudget(max_tokens=1000, used_tokens=500)
        project = Project(
            id="proj-1",
            name="Test",
            description="Test",
            owner_id="user-1",
            context_budget=budget,
        )
        assert project.is_budget_critical() is False

    def test_is_budget_warning_when_warning(self):
        """Test is_budget_warning returns True when < 30% remaining"""
        budget = ContextBudget(max_tokens=1000, used_tokens=750)
        project = Project(
            id="proj-1",
            name="Test",
            description="Test",
            owner_id="user-1",
            context_budget=budget,
        )
        assert project.is_budget_warning() is True

    def test_is_budget_warning_when_not_warning(self):
        """Test is_budget_warning returns False when > 30% remaining"""
        budget = ContextBudget(max_tokens=1000, used_tokens=500)
        project = Project(
            id="proj-1",
            name="Test",
            description="Test",
            owner_id="user-1",
            context_budget=budget,
        )
        assert project.is_budget_warning() is False
