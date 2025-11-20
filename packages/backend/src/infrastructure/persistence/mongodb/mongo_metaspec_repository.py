"""
MongoMetaspecRepository Implementation

MongoDB adapter for Metaspec persistence.
Implements IMetaspecRepository interface from Application Layer.

IAD-7: Repository Pattern + MongoDB
"""

from typing import Optional

from motor.motor_asyncio import AsyncIOMotorDatabase

from application.interfaces.i_metaspec_repository import IMetaspecRepository
from domain.entities.metaspec import Metaspec, MetaspecType


class MongoMetaspecRepository(IMetaspecRepository):
    """MongoDB implementation of IMetaspecRepository"""

    def __init__(self, database: AsyncIOMotorDatabase):
        """
        Initialize MongoDB repository.

        Args:
            database: Motor AsyncIOMotorDatabase instance
        """
        self._db = database
        self._collection = database["metaspecs"]

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
        document = self._to_document(metaspec)
        await self._collection.insert_one(document)
        return metaspec

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
        document = await self._collection.find_one({"id": metaspec_id})
        if document is None:
            return None
        return self._to_entity(document)

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
        document = self._to_document(metaspec)
        await self._collection.replace_one({"id": metaspec.id}, document)
        return metaspec

    async def delete(self, metaspec_id: str) -> None:
        """
        Remove a metaspec.

        Args:
            metaspec_id: Metaspec UUID string

        Raises:
            MetaspecNotFoundError: If metaspec does not exist
            RepositoryError: If deletion fails
        """
        await self._collection.delete_one({"id": metaspec_id})

    def _to_document(self, metaspec: Metaspec) -> dict:
        """
        Convert Metaspec entity to MongoDB document.

        Args:
            metaspec: Metaspec entity

        Returns:
            MongoDB document dict
        """
        document = {
            "id": metaspec.id,  # UUID string
            "demand_id": metaspec.demand_id,
            "type": metaspec.type.value,  # Enum → string
            "content": metaspec.content,
            "version": metaspec.version,
            "created_at": metaspec.created_at,
        }

        # Only include updated_at if not None (MongoDB schema requires date type)
        if metaspec.updated_at is not None:
            document["updated_at"] = metaspec.updated_at

        return document

    def _to_entity(self, document: dict) -> Metaspec:
        """
        Convert MongoDB document to Metaspec entity.

        Args:
            document: MongoDB document dict

        Returns:
            Metaspec entity
        """
        return Metaspec(
            id=document["id"],
            demand_id=document["demand_id"],
            type=MetaspecType(document["type"]),  # string → Enum
            content=document["content"],
            version=document["version"],
            created_at=document["created_at"],
            updated_at=document.get("updated_at"),
        )
