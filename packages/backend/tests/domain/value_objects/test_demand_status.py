"""
Tests for DemandStatus Value Object
"""

import pytest
from src.domain.value_objects.demand_status import DemandStatus


class TestDemandStatus:
    """Test suite for DemandStatus enum"""

    def test_all_statuses_exist(self):
        """Test that all expected statuses are defined"""
        assert DemandStatus.DRAFT == "draft"
        assert DemandStatus.SPEC_APPROVED == "spec_approved"
        assert DemandStatus.ARCHITECTURE_DONE == "architecture_done"
        assert DemandStatus.CODE_COMPLETE == "code_complete"
        assert DemandStatus.PR_MERGED == "pr_merged"

    def test_next_status_returns_correct_sequence(self):
        """Test that next_status follows the workflow sequence"""
        assert DemandStatus.DRAFT.next_status() == DemandStatus.SPEC_APPROVED
        assert (
            DemandStatus.SPEC_APPROVED.next_status()
            == DemandStatus.ARCHITECTURE_DONE
        )
        assert (
            DemandStatus.ARCHITECTURE_DONE.next_status()
            == DemandStatus.CODE_COMPLETE
        )
        assert (
            DemandStatus.CODE_COMPLETE.next_status() == DemandStatus.PR_MERGED
        )

    def test_next_status_returns_none_for_final_status(self):
        """Test that PR_MERGED has no next status"""
        assert DemandStatus.PR_MERGED.next_status() is None

    def test_can_transition_to_next_status(self):
        """Test that transition to immediate next status is allowed"""
        assert DemandStatus.DRAFT.can_transition_to(
            DemandStatus.SPEC_APPROVED
        )
        assert DemandStatus.SPEC_APPROVED.can_transition_to(
            DemandStatus.ARCHITECTURE_DONE
        )
        assert DemandStatus.ARCHITECTURE_DONE.can_transition_to(
            DemandStatus.CODE_COMPLETE
        )
        assert DemandStatus.CODE_COMPLETE.can_transition_to(
            DemandStatus.PR_MERGED
        )

    def test_cannot_transition_to_non_sequential_status(self):
        """Test that skipping statuses is not allowed"""
        assert not DemandStatus.DRAFT.can_transition_to(
            DemandStatus.ARCHITECTURE_DONE
        )
        assert not DemandStatus.DRAFT.can_transition_to(
            DemandStatus.CODE_COMPLETE
        )
        assert not DemandStatus.DRAFT.can_transition_to(DemandStatus.PR_MERGED)
        assert not DemandStatus.SPEC_APPROVED.can_transition_to(
            DemandStatus.CODE_COMPLETE
        )

    def test_cannot_transition_from_final_status(self):
        """Test that PR_MERGED cannot transition to any status"""
        assert not DemandStatus.PR_MERGED.can_transition_to(
            DemandStatus.DRAFT
        )
        assert not DemandStatus.PR_MERGED.can_transition_to(
            DemandStatus.SPEC_APPROVED
        )

    def test_is_final_returns_true_only_for_pr_merged(self):
        """Test that only PR_MERGED is considered final"""
        assert not DemandStatus.DRAFT.is_final()
        assert not DemandStatus.SPEC_APPROVED.is_final()
        assert not DemandStatus.ARCHITECTURE_DONE.is_final()
        assert not DemandStatus.CODE_COMPLETE.is_final()
        assert DemandStatus.PR_MERGED.is_final()
