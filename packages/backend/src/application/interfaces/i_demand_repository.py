"""
IDemandRepository Interface

Port (interface) for Demand persistence operations.
Adapter (implementation) will be in Infrastructure Layer.

IAD-7: Repository Pattern + MongoDB
"""

from abc import ABC, abstractmethod
from typing import Optional

from domain.entities.demand import Demand


class IDemandRepository(ABC):
    """Interface for Demand repository operations (CRUD basic)"""

    @abstractmethod
    async def create(self, demand: Demand) -> Demand:
        """
        Persist a new demand.

        Args:
            demand: Demand entity to persist

        Returns:
            The persisted demand entity

        Raises:
            DuplicateDemandError: If demand with same ID already exists
            RepositoryError: If persistence fails
        """
        pass

    @abstractmethod
    async def get_by_id(self, demand_id: str) -> Optional[Demand]:
        """
        Retrieve a demand by its UUID.

        Args:
            demand_id: Demand UUID string

        Returns:
            Demand entity if found, None otherwise

        Raises:
            RepositoryError: If retrieval fails
        """
        pass

    @abstractmethod
    async def update(self, demand: Demand) -> Demand:
        """
        Update an existing demand.

        Args:
            demand: Demand entity with updated data

        Returns:
            The updated demand entity

        Raises:
            DemandNotFoundError: If demand does not exist
            RepositoryError: If update fails
        """
        pass

    @abstractmethod
    async def delete(self, demand_id: str) -> None:
        """
        Remove a demand.

        Args:
            demand_id: Demand UUID string

        Raises:
            DemandNotFoundError: If demand does not exist
            RepositoryError: If deletion fails
        """
        pass
