"""
Reviewer Agent

Reviews code and validates against specs (Jidoka principle).
TODO: Implement full agent in IAD-12
"""


class ReviewerAgent:
    """Reviewer agent placeholder."""

    def __init__(self):
        pass

    async def review(self, code: str, spec: str) -> dict:
        """Review code against spec."""
        raise NotImplementedError("ReviewerAgent will be implemented in IAD-12")
