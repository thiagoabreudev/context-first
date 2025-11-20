"""
Tests for ContextBudget Value Object
"""

import pytest
from src.domain.value_objects.context_budget import ContextBudget


class TestContextBudget:
    """Test suite for ContextBudget value object"""

    def test_create_valid_budget(self):
        """Test creating valid ContextBudget"""
        budget = ContextBudget(max_tokens=1000, used_tokens=200)
        assert budget.max_tokens == 1000
        assert budget.used_tokens == 200

    def test_cannot_create_with_negative_max_tokens(self):
        """Test that negative max_tokens raises ValueError"""
        with pytest.raises(ValueError, match="max_tokens must be >= 0"):
            ContextBudget(max_tokens=-100, used_tokens=0)

    def test_cannot_create_with_negative_used_tokens(self):
        """Test that negative used_tokens raises ValueError"""
        with pytest.raises(ValueError, match="used_tokens must be >= 0"):
            ContextBudget(max_tokens=1000, used_tokens=-50)

    def test_remaining_tokens_calculation(self):
        """Test remaining_tokens property"""
        budget = ContextBudget(max_tokens=1000, used_tokens=300)
        assert budget.remaining_tokens == 700

    def test_remaining_tokens_never_negative(self):
        """Test that remaining_tokens is never negative even if overused"""
        budget = ContextBudget(max_tokens=100, used_tokens=150)
        assert budget.remaining_tokens == 0

    def test_percentage_used_calculation(self):
        """Test percentage_used property"""
        budget = ContextBudget(max_tokens=1000, used_tokens=250)
        assert budget.percentage_used == 0.25

    def test_percentage_used_when_fully_used(self):
        """Test percentage_used when budget is fully consumed"""
        budget = ContextBudget(max_tokens=1000, used_tokens=1000)
        assert budget.percentage_used == 1.0

    def test_percentage_used_when_overused(self):
        """Test percentage_used caps at 1.0 even when overused"""
        budget = ContextBudget(max_tokens=100, used_tokens=150)
        assert budget.percentage_used == 1.0

    def test_percentage_used_when_zero_max_tokens(self):
        """Test percentage_used when max_tokens is zero"""
        budget = ContextBudget(max_tokens=0, used_tokens=0)
        assert budget.percentage_used == 0.0

    @pytest.mark.parametrize(
        "max_tokens,used_tokens,expected",
        [
            (100, 0, True),  # Healthy: 0% used
            (100, 50, True),  # Healthy: 50% used
            (100, 70, True),  # Healthy: 70% used (boundary)
            (100, 71, False),  # Warning: 71% used
            (100, 90, False),  # Warning: 90% used
            (100, 91, False),  # Critical: 91% used
        ],
    )
    def test_is_healthy(self, max_tokens, used_tokens, expected):
        """Test is_healthy for various usage levels"""
        budget = ContextBudget(max_tokens=max_tokens, used_tokens=used_tokens)
        assert budget.is_healthy() == expected

    @pytest.mark.parametrize(
        "max_tokens,used_tokens,expected",
        [
            (100, 0, False),  # Healthy: 0% used
            (100, 50, False),  # Healthy: 50% used
            (100, 70, False),  # Healthy: 70% used
            (100, 71, True),  # Warning: 71% used (boundary)
            (100, 90, True),  # Warning: 90% used (boundary)
            (100, 91, True),  # Warning: 91% used (also critical, but still warning range)
        ],
    )
    def test_is_warning(self, max_tokens, used_tokens, expected):
        """Test is_warning for various usage levels"""
        budget = ContextBudget(max_tokens=max_tokens, used_tokens=used_tokens)
        assert budget.is_warning() == expected

    @pytest.mark.parametrize(
        "max_tokens,used_tokens,expected",
        [
            (100, 0, False),  # Healthy: 0% used
            (100, 70, False),  # Healthy: 70% used
            (100, 90, False),  # Warning: 90% used
            (100, 91, True),  # Critical: 91% used (boundary)
            (100, 95, True),  # Critical: 95% used
            (100, 100, True),  # Critical: 100% used
        ],
    )
    def test_is_critical(self, max_tokens, used_tokens, expected):
        """Test is_critical for various usage levels"""
        budget = ContextBudget(max_tokens=max_tokens, used_tokens=used_tokens)
        assert budget.is_critical() == expected

    def test_can_consume_with_sufficient_budget(self):
        """Test can_consume returns True when budget is sufficient"""
        budget = ContextBudget(max_tokens=1000, used_tokens=200)
        assert budget.can_consume(500) is True

    def test_can_consume_with_insufficient_budget(self):
        """Test can_consume returns False when budget is insufficient"""
        budget = ContextBudget(max_tokens=1000, used_tokens=900)
        assert budget.can_consume(200) is False

    def test_can_consume_with_exact_budget(self):
        """Test can_consume with exact remaining amount"""
        budget = ContextBudget(max_tokens=1000, used_tokens=700)
        assert budget.can_consume(300) is True

    def test_can_consume_rejects_negative_tokens(self):
        """Test can_consume raises ValueError for negative tokens"""
        budget = ContextBudget(max_tokens=1000, used_tokens=200)
        with pytest.raises(ValueError, match="tokens must be >= 0"):
            budget.can_consume(-50)

    def test_consume_returns_new_budget_instance(self):
        """Test that consume returns new ContextBudget (immutability)"""
        original = ContextBudget(max_tokens=1000, used_tokens=200)
        new_budget = original.consume(300)

        # Original unchanged (immutable)
        assert original.used_tokens == 200
        assert original.remaining_tokens == 800

        # New budget has consumed tokens
        assert new_budget.used_tokens == 500
        assert new_budget.remaining_tokens == 500

    def test_consume_with_sufficient_budget(self):
        """Test consume succeeds with sufficient budget"""
        budget = ContextBudget(max_tokens=1000, used_tokens=200)
        new_budget = budget.consume(300)
        assert new_budget.used_tokens == 500

    def test_consume_raises_error_when_insufficient_budget(self):
        """Test consume raises ValueError when budget exceeded"""
        budget = ContextBudget(max_tokens=1000, used_tokens=900)
        with pytest.raises(
            ValueError, match="Cannot consume 200 tokens.*Only 100 remaining"
        ):
            budget.consume(200)

    def test_consume_rejects_negative_tokens(self):
        """Test consume raises ValueError for negative tokens"""
        budget = ContextBudget(max_tokens=1000, used_tokens=200)
        with pytest.raises(ValueError, match="tokens must be >= 0"):
            budget.consume(-50)

    def test_budget_is_immutable(self):
        """Test that ContextBudget is truly immutable (frozen dataclass)"""
        budget = ContextBudget(max_tokens=1000, used_tokens=200)
        with pytest.raises(Exception):  # FrozenInstanceError
            budget.used_tokens = 300
