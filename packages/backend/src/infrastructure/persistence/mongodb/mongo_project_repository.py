"""
MongoProjectRepository Implementation

MongoDB adapter for Project persistence.
Implements IProjectRepository interface from Application Layer.

IAD-7: Repository Pattern + MongoDB
"""

from typing import Optional

from motor.motor_asyncio import AsyncIOMotorDatabase

from application.interfaces.i_project_repository import IProjectRepository
from domain.entities.project import Project
from domain.value_objects.context_budget import ContextBudget


class MongoProjectRepository(IProjectRepository):
    """MongoDB implementation of IProjectRepository"""

    def __init__(self, database: AsyncIOMotorDatabase):
        """
        Initialize MongoDB repository.

        Args:
            database: Motor AsyncIOMotorDatabase instance
        """
        self._db = database
        self._collection = database["projects"]

    async def create(self, project: Project) -> Project:
        """
        Persist a new project.

        Args:
            project: Project entity to persist

        Returns:
            The persisted project entity

        Raises:
            DuplicateProjectError: If project with same ID already exists
            RepositoryError: If persistence fails
        """
        document = self._to_document(project)
        await self._collection.insert_one(document)
        return project

    async def get_by_id(self, project_id: str) -> Optional[Project]:
        """
        Retrieve a project by its UUID.

        Args:
            project_id: Project UUID string

        Returns:
            Project entity if found, None otherwise

        Raises:
            RepositoryError: If retrieval fails
        """
        document = await self._collection.find_one({"id": project_id})
        if document is None:
            return None
        return self._to_entity(document)

    async def update(self, project: Project) -> Project:
        """
        Update an existing project.

        Args:
            project: Project entity with updated data

        Returns:
            The updated project entity

        Raises:
            ProjectNotFoundError: If project does not exist
            RepositoryError: If update fails
        """
        document = self._to_document(project)
        await self._collection.replace_one({"id": project.id}, document)
        return project

    async def delete(self, project_id: str) -> None:
        """
        Remove a project.

        Args:
            project_id: Project UUID string

        Raises:
            ProjectNotFoundError: If project does not exist
            RepositoryError: If deletion fails
        """
        await self._collection.delete_one({"id": project_id})

    def _to_document(self, project: Project) -> dict:
        """
        Convert Project entity to MongoDB document.

        Args:
            project: Project entity

        Returns:
            MongoDB document dict
        """
        document = {
            "id": project.id,  # UUID string
            "name": project.name,
            "description": project.description,
            "user_id": project.owner_id,  # MongoDB schema uses user_id
            "context_budget": {  # Subdocument for Value Object
                "max_tokens": project.context_budget.max_tokens,
                "used_tokens": project.context_budget.used_tokens,
            },
            "created_at": project.created_at,
        }

        # Only include updated_at if not None (MongoDB schema requires date type)
        if project.updated_at is not None:
            document["updated_at"] = project.updated_at

        return document

    def _to_entity(self, document: dict) -> Project:
        """
        Convert MongoDB document to Project entity.

        Args:
            document: MongoDB document dict

        Returns:
            Project entity
        """
        return Project(
            id=document["id"],
            name=document["name"],
            description=document["description"],
            owner_id=document["user_id"],  # Convert back from user_id to owner_id
            context_budget=ContextBudget(
                max_tokens=document["context_budget"]["max_tokens"],
                used_tokens=document["context_budget"]["used_tokens"],
            ),
            created_at=document["created_at"],
            updated_at=document.get("updated_at"),
        )
