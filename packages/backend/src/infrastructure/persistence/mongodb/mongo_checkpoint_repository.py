"""
MongoCheckpointRepository Implementation

MongoDB adapter for Checkpoint persistence.
Implements ICheckpointRepository interface from Application Layer.

IAD-7: Repository Pattern + MongoDB
"""

from typing import Optional

from motor.motor_asyncio import AsyncIOMotorDatabase

from application.interfaces.i_checkpoint_repository import ICheckpointRepository
from domain.entities.checkpoint import Checkpoint


class MongoCheckpointRepository(ICheckpointRepository):
    """MongoDB implementation of ICheckpointRepository"""

    def __init__(self, database: AsyncIOMotorDatabase):
        """
        Initialize MongoDB repository.

        Args:
            database: Motor AsyncIOMotorDatabase instance
        """
        self._db = database
        self._collection = database["checkpoints"]

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
        document = self._to_document(checkpoint)
        await self._collection.insert_one(document)
        return checkpoint

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
        document = await self._collection.find_one({"id": checkpoint_id})
        if document is None:
            return None
        return self._to_entity(document)

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
        document = self._to_document(checkpoint)
        await self._collection.replace_one({"id": checkpoint.id}, document)
        return checkpoint

    async def delete(self, checkpoint_id: str) -> None:
        """
        Remove a checkpoint.

        Args:
            checkpoint_id: Checkpoint UUID string

        Raises:
            CheckpointNotFoundError: If checkpoint does not exist
            RepositoryError: If deletion fails
        """
        await self._collection.delete_one({"id": checkpoint_id})

    def _to_document(self, checkpoint: Checkpoint) -> dict:
        """
        Convert Checkpoint entity to MongoDB document.

        Args:
            checkpoint: Checkpoint entity

        Returns:
            MongoDB document dict
        """
        document = {
            "id": checkpoint.id,  # UUID string
            "demand_id": checkpoint.demand_id,
            "context_snapshot": checkpoint.context_snapshot,  # JSON string
            "tokens_used": checkpoint.tokens_used,
            "created_at": checkpoint.created_at,
        }

        # Only include expires_at if not None (TTL index)
        if checkpoint.expires_at is not None:
            document["expires_at"] = checkpoint.expires_at

        return document

    def _to_entity(self, document: dict) -> Checkpoint:
        """
        Convert MongoDB document to Checkpoint entity.

        Args:
            document: MongoDB document dict

        Returns:
            Checkpoint entity
        """
        return Checkpoint(
            id=document["id"],
            demand_id=document["demand_id"],
            context_snapshot=document["context_snapshot"],
            tokens_used=document["tokens_used"],
            created_at=document["created_at"],
            expires_at=document.get("expires_at"),
        )
