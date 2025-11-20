"""
ICheckpointRepository Interface

Port (interface) for Checkpoint persistence operations.
Adapter (implementation) will be in Infrastructure Layer.

IAD-7: Repository Pattern + MongoDB
"""

from abc import ABC, abstractmethod
from typing import Optional

from domain.entities.checkpoint import Checkpoint


class ICheckpointRepository(ABC):
    """Interface for Checkpoint repository operations (CRUD basic)"""

    @abstractmethod
    async def create(self, checkpoint: Checkpoint) -> Checkpoint:
        """
        Persist a new checkpoint.

        Args:
            checkpoint: Checkpoint entity to persist

        Returns:
            The persisted checkpoint entity

        Raises:
            DuplicateCheckpointError: If checkpoint with same ID already exists
            RepositoryError: If persistence fails
        """
        pass

    @abstractmethod
    async def get_by_id(self, checkpoint_id: str) -> Optional[Checkpoint]:
        """
        Retrieve a checkpoint by its UUID.

        Args:
            checkpoint_id: Checkpoint UUID string

        Returns:
            Checkpoint entity if found, None otherwise

        Raises:
            RepositoryError: If retrieval fails
        """
        pass

    @abstractmethod
    async def update(self, checkpoint: Checkpoint) -> Checkpoint:
        """
        Update an existing checkpoint.

        Args:
            checkpoint: Checkpoint entity with updated data

        Returns:
            The updated checkpoint entity

        Raises:
            CheckpointNotFoundError: If checkpoint does not exist
            RepositoryError: If update fails
        """
        pass

    @abstractmethod
    async def delete(self, checkpoint_id: str) -> None:
        """
        Remove a checkpoint.

        Args:
            checkpoint_id: Checkpoint UUID string

        Raises:
            CheckpointNotFoundError: If checkpoint does not exist
            RepositoryError: If deletion fails
        """
        pass
