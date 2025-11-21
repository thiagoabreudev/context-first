"""
IMetaspecRepository Interface

Port (interface) for Metaspec persistence operations.
Adapter (implementation) will be in Infrastructure Layer.

IAD-7: Repository Pattern + MongoDB
"""

from abc import ABC, abstractmethod
from typing import Optional

from domain.entities.metaspec import Metaspec


class IMetaspecRepository(ABC):
    """Interface for Metaspec repository operations (CRUD basic)"""

    @abstractmethod
    async def create(self, metaspec: Metaspec) -> Metaspec:
        """
        Persist a new metaspec.

        Args:
            metaspec: Metaspec entity to persist

        Returns:
            The persisted metaspec entity

        Raises:
            DuplicateMetaspecError: If metaspec with same ID already exists
            RepositoryError: If persistence fails
        """
        pass

    @abstractmethod
    async def get_by_id(self, metaspec_id: str) -> Optional[Metaspec]:
        """
        Retrieve a metaspec by its UUID.

        Args:
            metaspec_id: Metaspec UUID string

        Returns:
            Metaspec entity if found, None otherwise

        Raises:
            RepositoryError: If retrieval fails
        """
        pass

    @abstractmethod
    async def update(self, metaspec: Metaspec) -> Metaspec:
        """
        Update an existing metaspec.

        Args:
            metaspec: Metaspec entity with updated data

        Returns:
            The updated metaspec entity

        Raises:
            MetaspecNotFoundError: If metaspec does not exist
            RepositoryError: If update fails
        """
        pass

    @abstractmethod
    async def delete(self, metaspec_id: str) -> None:
        """
        Remove a metaspec.

        Args:
            metaspec_id: Metaspec UUID string

        Raises:
            MetaspecNotFoundError: If metaspec does not exist
            RepositoryError: If deletion fails
        """
        pass
