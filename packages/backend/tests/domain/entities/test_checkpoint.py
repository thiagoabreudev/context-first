"""
Tests for Checkpoint Entity
"""

import pytest
from datetime import datetime, timedelta
from src.domain.entities.checkpoint import Checkpoint
from src.domain.exceptions import InvalidCheckpointError


class TestCheckpoint:
    """Test suite for Checkpoint entity"""

    @pytest.fixture
    def valid_snapshot(self):
        """Fixture: Valid context snapshot (JSON)"""
        return '{"messages": [], "context": "some context"}'

    def test_create_valid_checkpoint(self, valid_snapshot):
        """Test creating valid Checkpoint"""
        checkpoint = Checkpoint(
            id="checkpoint-123",
            demand_id="demand-456",
            context_snapshot=valid_snapshot,
            tokens_used=5000,
        )
        assert checkpoint.id == "checkpoint-123"
        assert checkpoint.demand_id == "demand-456"
        assert checkpoint.context_snapshot == valid_snapshot
        assert checkpoint.tokens_used == 5000
        assert isinstance(checkpoint.created_at, datetime)
        assert checkpoint.expires_at is None

    def test_cannot_create_checkpoint_with_empty_id(self, valid_snapshot):
        """Test that empty id raises ValueError"""
        with pytest.raises(ValueError, match="id cannot be empty"):
            Checkpoint(
                id="",
                demand_id="demand-1",
                context_snapshot=valid_snapshot,
                tokens_used=100,
            )

    def test_cannot_create_checkpoint_with_empty_demand_id(
        self, valid_snapshot
    ):
        """Test that empty demand_id raises ValueError"""
        with pytest.raises(ValueError, match="demand_id cannot be empty"):
            Checkpoint(
                id="checkpoint-1",
                demand_id="",
                context_snapshot=valid_snapshot,
                tokens_used=100,
            )

    def test_cannot_create_checkpoint_with_empty_snapshot(self):
        """Test that empty context_snapshot raises InvalidCheckpointError"""
        with pytest.raises(
            InvalidCheckpointError,
            match="context_snapshot cannot be empty",
        ):
            Checkpoint(
                id="checkpoint-1",
                demand_id="demand-1",
                context_snapshot="",
                tokens_used=100,
            )

    def test_cannot_create_checkpoint_with_zero_tokens(self, valid_snapshot):
        """Test that tokens_used=0 raises InvalidCheckpointError"""
        with pytest.raises(
            InvalidCheckpointError, match="tokens_used must be positive"
        ):
            Checkpoint(
                id="checkpoint-1",
                demand_id="demand-1",
                context_snapshot=valid_snapshot,
                tokens_used=0,
            )

    def test_cannot_create_checkpoint_with_negative_tokens(
        self, valid_snapshot
    ):
        """Test that negative tokens_used raises InvalidCheckpointError"""
        with pytest.raises(
            InvalidCheckpointError, match="tokens_used must be positive"
        ):
            Checkpoint(
                id="checkpoint-1",
                demand_id="demand-1",
                context_snapshot=valid_snapshot,
                tokens_used=-100,
            )

    def test_validate_not_empty_returns_true_for_valid_snapshot(
        self, valid_snapshot
    ):
        """Test validate_not_empty returns True for non-empty snapshot"""
        checkpoint = Checkpoint(
            id="checkpoint-1",
            demand_id="demand-1",
            context_snapshot=valid_snapshot,
            tokens_used=100,
        )
        assert checkpoint.validate_not_empty() is True

    def test_validate_not_empty_returns_false_for_empty_snapshot(self):
        """Test validate_not_empty returns False for empty snapshot"""
        checkpoint = object.__new__(Checkpoint)
        checkpoint.context_snapshot = ""
        assert checkpoint.validate_not_empty() is False

    def test_validate_tokens_positive_returns_true_for_positive_tokens(
        self, valid_snapshot
    ):
        """Test validate_tokens_positive returns True for positive tokens"""
        checkpoint = Checkpoint(
            id="checkpoint-1",
            demand_id="demand-1",
            context_snapshot=valid_snapshot,
            tokens_used=100,
        )
        assert checkpoint.validate_tokens_positive() is True

    def test_validate_tokens_positive_returns_false_for_zero_tokens(self):
        """Test validate_tokens_positive returns False for zero tokens"""
        checkpoint = object.__new__(Checkpoint)
        checkpoint.tokens_used = 0
        assert checkpoint.validate_tokens_positive() is False

    def test_is_expired_returns_false_when_no_expiration(self, valid_snapshot):
        """Test is_expired returns False when expires_at is None"""
        checkpoint = Checkpoint(
            id="checkpoint-1",
            demand_id="demand-1",
            context_snapshot=valid_snapshot,
            tokens_used=100,
        )
        assert checkpoint.is_expired() is False

    def test_is_expired_returns_false_when_not_expired(self, valid_snapshot):
        """Test is_expired returns False when expires_at is in future"""
        future_time = datetime.utcnow() + timedelta(hours=1)
        checkpoint = Checkpoint(
            id="checkpoint-1",
            demand_id="demand-1",
            context_snapshot=valid_snapshot,
            tokens_used=100,
            expires_at=future_time,
        )
        assert checkpoint.is_expired() is False

    def test_is_expired_returns_true_when_expired(self, valid_snapshot):
        """Test is_expired returns True when expires_at is in past"""
        past_time = datetime.utcnow() - timedelta(hours=1)
        checkpoint = Checkpoint(
            id="checkpoint-1",
            demand_id="demand-1",
            context_snapshot=valid_snapshot,
            tokens_used=100,
            expires_at=past_time,
        )
        assert checkpoint.is_expired() is True
