"""
Integration Tests for MongoProjectRepository

Tests with real MongoDB database via Docker Compose.
Database is cleaned before each test (see conftest.py).

IAD-7: Repository Pattern + MongoDB
"""

import uuid
from datetime import datetime

import pytest
from motor.motor_asyncio import AsyncIOMotorDatabase

from domain.entities.project import Project
from domain.value_objects.context_budget import ContextBudget
from infrastructure.persistence.mongodb.mongo_project_repository import (
    MongoProjectRepository,
)


@pytest.mark.asyncio
async def test_create_and_get_project(mongodb_database: AsyncIOMotorDatabase):
    """Test: Create project and retrieve it by ID"""
    # Arrange
    repo = MongoProjectRepository(mongodb_database)
    project = Project(
        id=str(uuid.uuid4()),
        name="Test Project",
        description="A test project for integration testing",
        owner_id="user_123",
        context_budget=ContextBudget(max_tokens=100000, used_tokens=0),
        created_at=datetime.utcnow(),
    )

    # Act
    created = await repo.create(project)
    found = await repo.get_by_id(project.id)

    # Assert
    assert created.id == project.id
    assert found is not None
    assert found.id == project.id
    assert found.name == "Test Project"
    assert found.description == "A test project for integration testing"
    assert found.owner_id == "user_123"
    assert found.context_budget.max_tokens == 100000
    assert found.context_budget.used_tokens == 0
    assert found.created_at is not None
    assert found.updated_at is None


@pytest.mark.asyncio
async def test_get_by_id_not_found(mongodb_database: AsyncIOMotorDatabase):
    """Test: Get non-existent project returns None"""
    # Arrange
    repo = MongoProjectRepository(mongodb_database)
    non_existent_id = str(uuid.uuid4())

    # Act
    found = await repo.get_by_id(non_existent_id)

    # Assert
    assert found is None


@pytest.mark.asyncio
async def test_update_project(mongodb_database: AsyncIOMotorDatabase):
    """Test: Update project and verify changes persist"""
    # Arrange
    repo = MongoProjectRepository(mongodb_database)
    project = Project(
        id=str(uuid.uuid4()),
        name="Original Name",
        description="Original description",
        owner_id="user_123",
        context_budget=ContextBudget(max_tokens=100000, used_tokens=5000),
        created_at=datetime.utcnow(),
    )
    await repo.create(project)

    # Act - Update project
    project.name = "Updated Name"
    project.description = "Updated description"
    project.context_budget = ContextBudget(max_tokens=100000, used_tokens=10000)
    project.updated_at = datetime.utcnow()

    updated = await repo.update(project)
    found = await repo.get_by_id(project.id)

    # Assert
    assert updated.id == project.id
    assert found is not None
    assert found.name == "Updated Name"
    assert found.description == "Updated description"
    assert found.context_budget.used_tokens == 10000
    assert found.updated_at is not None


@pytest.mark.asyncio
async def test_delete_project(mongodb_database: AsyncIOMotorDatabase):
    """Test: Delete project and verify it's removed"""
    # Arrange
    repo = MongoProjectRepository(mongodb_database)
    project = Project(
        id=str(uuid.uuid4()),
        name="To Be Deleted",
        description="This project will be deleted",
        owner_id="user_123",
        context_budget=ContextBudget(max_tokens=100000, used_tokens=0),
        created_at=datetime.utcnow(),
    )
    await repo.create(project)

    # Verify it exists
    found_before = await repo.get_by_id(project.id)
    assert found_before is not None

    # Act
    await repo.delete(project.id)

    # Assert
    found_after = await repo.get_by_id(project.id)
    assert found_after is None


@pytest.mark.asyncio
async def test_context_budget_conversion(mongodb_database: AsyncIOMotorDatabase):
    """Test: ContextBudget Value Object converts correctly to/from subdocument"""
    # Arrange
    repo = MongoProjectRepository(mongodb_database)
    context_budget = ContextBudget(max_tokens=200000, used_tokens=75000)
    project = Project(
        id=str(uuid.uuid4()),
        name="Budget Test",
        description="Testing context budget conversion",
        owner_id="user_456",
        context_budget=context_budget,
        created_at=datetime.utcnow(),
    )

    # Act
    await repo.create(project)
    found = await repo.get_by_id(project.id)

    # Assert - ContextBudget properties
    assert found is not None
    assert found.context_budget.max_tokens == 200000
    assert found.context_budget.used_tokens == 75000
    assert found.context_budget.remaining_tokens == 125000
    assert found.context_budget.percentage_used == 0.375  # Fraction (37.5%)

    # Assert - Verify it's stored as subdocument in MongoDB
    collection = mongodb_database["projects"]
    document = await collection.find_one({"id": project.id})
    assert "context_budget" in document
    assert document["context_budget"]["max_tokens"] == 200000
    assert document["context_budget"]["used_tokens"] == 75000


@pytest.mark.asyncio
async def test_multiple_projects_isolation(mongodb_database: AsyncIOMotorDatabase):
    """Test: Multiple projects don't interfere with each other"""
    # Arrange
    repo = MongoProjectRepository(mongodb_database)
    project1 = Project(
        id=str(uuid.uuid4()),
        name="Project 1",
        description="First project",
        owner_id="user_1",
        context_budget=ContextBudget(max_tokens=100000, used_tokens=0),
        created_at=datetime.utcnow(),
    )
    project2 = Project(
        id=str(uuid.uuid4()),
        name="Project 2",
        description="Second project",
        owner_id="user_2",
        context_budget=ContextBudget(max_tokens=200000, used_tokens=5000),
        created_at=datetime.utcnow(),
    )

    # Act
    await repo.create(project1)
    await repo.create(project2)

    found1 = await repo.get_by_id(project1.id)
    found2 = await repo.get_by_id(project2.id)

    # Assert
    assert found1 is not None
    assert found2 is not None
    assert found1.id == project1.id
    assert found2.id == project2.id
    assert found1.name == "Project 1"
    assert found2.name == "Project 2"
    assert found1.owner_id == "user_1"
    assert found2.owner_id == "user_2"
