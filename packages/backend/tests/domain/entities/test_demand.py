"""
Tests for Demand Entity
"""

import pytest
from datetime import datetime
from src.domain.entities.demand import Demand
from src.domain.value_objects.demand_status import DemandStatus
from src.domain.value_objects.context_budget import ContextBudget
from src.domain.exceptions import (
    InvalidStatusTransitionError,
    DemandAlreadyCompletedError,
)


class TestDemand:
    """Test suite for Demand entity"""

    @pytest.fixture
    def valid_demand(self):
        """Fixture: Valid Demand in DRAFT status"""
        return Demand(
            id="demand-123",
            project_id="proj-456",
            title="Implement feature X",
            description="A detailed description",
            status=DemandStatus.DRAFT,
        )

    def test_create_valid_demand(self):
        """Test creating valid Demand"""
        demand = Demand(
            id="demand-123",
            project_id="proj-456",
            title="Test Demand",
            description="Test description",
        )
        assert demand.id == "demand-123"
        assert demand.project_id == "proj-456"
        assert demand.title == "Test Demand"
        assert demand.status == DemandStatus.DRAFT  # Default
        assert isinstance(demand.created_at, datetime)

    def test_cannot_create_demand_with_empty_id(self):
        """Test that empty id raises ValueError"""
        with pytest.raises(ValueError, match="id cannot be empty"):
            Demand(
                id="",
                project_id="proj-1",
                title="Test",
                description="Test",
            )

    def test_cannot_create_demand_with_empty_project_id(self):
        """Test that empty project_id raises ValueError"""
        with pytest.raises(ValueError, match="project_id cannot be empty"):
            Demand(
                id="demand-1",
                project_id="",
                title="Test",
                description="Test",
            )

    def test_cannot_create_demand_with_empty_title(self):
        """Test that empty title raises ValueError"""
        with pytest.raises(ValueError, match="title cannot be empty"):
            Demand(
                id="demand-1",
                project_id="proj-1",
                title="",
                description="Test",
            )

    def test_cannot_create_demand_with_whitespace_only_title(self):
        """Test that whitespace-only title raises ValueError"""
        with pytest.raises(ValueError, match="title cannot be empty"):
            Demand(
                id="demand-1",
                project_id="proj-1",
                title="   ",
                description="Test",
            )

    def test_can_transition_to_next_status(self, valid_demand):
        """Test can_transition_to returns True for next status"""
        assert (
            valid_demand.can_transition_to(DemandStatus.SPEC_APPROVED) is True
        )

    def test_cannot_transition_to_non_sequential_status(self, valid_demand):
        """Test can_transition_to returns False for non-sequential status"""
        assert (
            valid_demand.can_transition_to(DemandStatus.CODE_COMPLETE)
            is False
        )

    def test_transition_to_next_status_succeeds(self, valid_demand):
        """Test transition_to changes status correctly"""
        valid_demand.transition_to(DemandStatus.SPEC_APPROVED)
        assert valid_demand.status == DemandStatus.SPEC_APPROVED
        assert valid_demand.updated_at is not None

    def test_transition_to_invalid_status_raises_error(self, valid_demand):
        """Test transition_to raises error for invalid transition"""
        with pytest.raises(
            InvalidStatusTransitionError,
            match="Cannot transition from draft to code_complete",
        ):
            valid_demand.transition_to(DemandStatus.CODE_COMPLETE)

    def test_transition_from_final_status_raises_error(self):
        """Test transition_to raises error when demand is completed"""
        demand = Demand(
            id="demand-1",
            project_id="proj-1",
            title="Test",
            description="Test",
            status=DemandStatus.PR_MERGED,
        )
        with pytest.raises(
            DemandAlreadyCompletedError,
            match="Cannot transition.*already completed",
        ):
            demand.transition_to(DemandStatus.DRAFT)

    def test_advance_to_next_status_succeeds(self, valid_demand):
        """Test advance_to_next_status moves to next status"""
        valid_demand.advance_to_next_status()
        assert valid_demand.status == DemandStatus.SPEC_APPROVED
        assert valid_demand.updated_at is not None

    def test_advance_to_next_status_multiple_times(self, valid_demand):
        """Test advancing through multiple statuses"""
        valid_demand.advance_to_next_status()
        assert valid_demand.status == DemandStatus.SPEC_APPROVED

        valid_demand.advance_to_next_status()
        assert valid_demand.status == DemandStatus.ARCHITECTURE_DONE

        valid_demand.advance_to_next_status()
        assert valid_demand.status == DemandStatus.CODE_COMPLETE

        valid_demand.advance_to_next_status()
        assert valid_demand.status == DemandStatus.PR_MERGED

    def test_advance_from_final_status_raises_error(self):
        """Test advance_to_next_status raises error when completed"""
        demand = Demand(
            id="demand-1",
            project_id="proj-1",
            title="Test",
            description="Test",
            status=DemandStatus.PR_MERGED,
        )
        with pytest.raises(
            DemandAlreadyCompletedError,
            match="Cannot advance.*already completed",
        ):
            demand.advance_to_next_status()

    def test_is_completed_returns_true_when_pr_merged(self):
        """Test is_completed returns True for PR_MERGED status"""
        demand = Demand(
            id="demand-1",
            project_id="proj-1",
            title="Test",
            description="Test",
            status=DemandStatus.PR_MERGED,
        )
        assert demand.is_completed() is True

    def test_is_completed_returns_false_when_not_pr_merged(
        self, valid_demand
    ):
        """Test is_completed returns False for non-final statuses"""
        assert valid_demand.is_completed() is False

        valid_demand.advance_to_next_status()
        assert valid_demand.is_completed() is False

    def test_demand_with_context_budget(self):
        """Test Demand can have optional context_budget"""
        budget = ContextBudget(max_tokens=5000, used_tokens=1000)
        demand = Demand(
            id="demand-1",
            project_id="proj-1",
            title="Test",
            description="Test",
            context_budget=budget,
        )
        assert demand.context_budget == budget
