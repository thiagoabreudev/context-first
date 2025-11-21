"""
MongoDemandRepository Implementation

MongoDB adapter for Demand persistence.
Implements IDemandRepository interface from Application Layer.

IAD-7: Repository Pattern + MongoDB
"""

from typing import Optional

from motor.motor_asyncio import AsyncIOMotorDatabase

from application.interfaces.i_demand_repository import IDemandRepository
from domain.entities.demand import Demand
from domain.value_objects.context_budget import ContextBudget
from domain.value_objects.demand_status import DemandStatus


class MongoDemandRepository(IDemandRepository):
    """MongoDB implementation of IDemandRepository"""

    def __init__(self, database: AsyncIOMotorDatabase):
        """
        Initialize MongoDB repository.

        Args:
            database: Motor AsyncIOMotorDatabase instance
        """
        self._db = database
        self._collection = database["demands"]

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
        document = self._to_document(demand)
        await self._collection.insert_one(document)
        return demand

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
        document = await self._collection.find_one({"id": demand_id})
        if document is None:
            return None
        return self._to_entity(document)

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
        document = self._to_document(demand)
        await self._collection.replace_one({"id": demand.id}, document)
        return demand

    async def delete(self, demand_id: str) -> None:
        """
        Remove a demand.

        Args:
            demand_id: Demand UUID string

        Raises:
            DemandNotFoundError: If demand does not exist
            RepositoryError: If deletion fails
        """
        await self._collection.delete_one({"id": demand_id})

    def _to_document(self, demand: Demand) -> dict:
        """
        Convert Demand entity to MongoDB document.

        Args:
            demand: Demand entity

        Returns:
            MongoDB document dict
        """
        document = {
            "id": demand.id,  # UUID string
            "project_id": demand.project_id,
            "title": demand.title,
            "description": demand.description,
            "status": demand.status.value,  # Enum → string
            "created_at": demand.created_at,
        }

        # Optional ContextBudget as subdocument
        if demand.context_budget is not None:
            document["context_budget"] = {
                "max_tokens": demand.context_budget.max_tokens,
                "used_tokens": demand.context_budget.used_tokens,
            }

        # Only include updated_at if not None (MongoDB schema requires date type)
        if demand.updated_at is not None:
            document["updated_at"] = demand.updated_at

        return document

    def _to_entity(self, document: dict) -> Demand:
        """
        Convert MongoDB document to Demand entity.

        Args:
            document: MongoDB document dict

        Returns:
            Demand entity
        """
        # Optional ContextBudget conversion
        context_budget = None
        if "context_budget" in document and document["context_budget"] is not None:
            context_budget = ContextBudget(
                max_tokens=document["context_budget"]["max_tokens"],
                used_tokens=document["context_budget"]["used_tokens"],
            )

        return Demand(
            id=document["id"],
            project_id=document["project_id"],
            title=document["title"],
            description=document["description"],
            status=DemandStatus(document["status"]),  # string → Enum
            context_budget=context_budget,
            created_at=document["created_at"],
            updated_at=document.get("updated_at"),
        )
