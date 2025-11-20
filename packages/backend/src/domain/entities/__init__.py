"""
Domain Entities

Entidades de negócio com identidade e comportamento.
"""

from .project import Project
from .demand import Demand
from .metaspec import Metaspec, MetaspecType
from .checkpoint import Checkpoint

__all__ = [
    "Project",
    "Demand",
    "Metaspec",
    "MetaspecType",
    "Checkpoint",
]
