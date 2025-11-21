"""
Repository Interfaces (Ports)

Defines the contracts for data persistence.
Implementations (adapters) are in Infrastructure Layer.

IAD-7: Repository Pattern + MongoDB
"""

from application.interfaces.i_checkpoint_repository import ICheckpointRepository
from application.interfaces.i_demand_repository import IDemandRepository
from application.interfaces.i_metaspec_repository import IMetaspecRepository
from application.interfaces.i_project_repository import IProjectRepository

__all__ = [
    "ICheckpointRepository",
    "IDemandRepository",
    "IMetaspecRepository",
    "IProjectRepository",
]
