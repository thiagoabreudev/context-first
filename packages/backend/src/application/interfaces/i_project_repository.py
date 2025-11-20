"""
IProjectRepository Interface

Port (interface) for Project persistence operations.
Adapter (implementation) will be in Infrastructure Layer.

IAD-7: Repository Pattern + MongoDB
"""

from abc import ABC, abstractmethod
from typing import Optional

from domain.entities.project import Project


class IProjectRepository(ABC):
    """Interface for Project repository operations (CRUD basic)"""

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
    async def delete(self, project_id: str) -> None:
        """
        Remove a project.

        Args:
            project_id: Project UUID string

        Raises:
            ProjectNotFoundError: If project does not exist
            RepositoryError: If deletion fails
        """
        pass
