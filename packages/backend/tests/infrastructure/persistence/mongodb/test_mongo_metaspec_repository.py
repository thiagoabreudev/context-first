"""
Integration Tests for MongoMetaspecRepository

Tests with real MongoDB database via Docker Compose.
Database is cleaned before each test (see conftest.py).

IAD-7: Repository Pattern + MongoDB
"""

import uuid
from datetime import datetime

import pytest
from motor.motor_asyncio import AsyncIOMotorDatabase

from domain.entities.metaspec import Metaspec, MetaspecType
from infrastructure.persistence.mongodb.mongo_metaspec_repository import (
    MongoMetaspecRepository,
)


@pytest.mark.asyncio
async def test_create_and_get_metaspec(mongodb_database: AsyncIOMotorDatabase):
    """Test: Create metaspec and retrieve it by ID"""
    # Arrange
    repo = MongoMetaspecRepository(mongodb_database)
    metaspec = Metaspec(
        id=str(uuid.uuid4()),
        demand_id="demand_123",
        type=MetaspecType.BUSINESS,
        content="# Business Requirements\n\nUser story: As a user...",
        version=1,
        created_at=datetime.utcnow(),
    )

    # Act
    created = await repo.create(metaspec)
    found = await repo.get_by_id(metaspec.id)

    # Assert
    assert created.id == metaspec.id
    assert found is not None
    assert found.id == metaspec.id
    assert found.demand_id == "demand_123"
    assert found.type == MetaspecType.BUSINESS
    assert "# Business Requirements" in found.content
    assert found.version == 1
    assert found.created_at is not None
    assert found.updated_at is None


@pytest.mark.asyncio
async def test_get_by_id_not_found(mongodb_database: AsyncIOMotorDatabase):
    """Test: Get non-existent metaspec returns None"""
    # Arrange
    repo = MongoMetaspecRepository(mongodb_database)
    non_existent_id = str(uuid.uuid4())

    # Act
    found = await repo.get_by_id(non_existent_id)

    # Assert
    assert found is None


@pytest.mark.asyncio
async def test_update_metaspec(mongodb_database: AsyncIOMotorDatabase):
    """Test: Update metaspec and verify changes persist"""
    # Arrange
    repo = MongoMetaspecRepository(mongodb_database)
    metaspec = Metaspec(
        id=str(uuid.uuid4()),
        demand_id="demand_123",
        type=MetaspecType.TECHNICAL,
        content="# Technical Spec v1\n\nOriginal content",
        version=1,
        created_at=datetime.utcnow(),
    )
    await repo.create(metaspec)

    # Act - Update metaspec (simulate increment_version)
    metaspec.content = "# Technical Spec v2\n\nUpdated content"
    metaspec.increment_version()  # version = 2, updated_at = now

    updated = await repo.update(metaspec)
    found = await repo.get_by_id(metaspec.id)

    # Assert
    assert updated.id == metaspec.id
    assert found is not None
    assert "v2" in found.content
    assert "Updated content" in found.content
    assert found.version == 2
    assert found.updated_at is not None


@pytest.mark.asyncio
async def test_delete_metaspec(mongodb_database: AsyncIOMotorDatabase):
    """Test: Delete metaspec and verify it's removed"""
    # Arrange
    repo = MongoMetaspecRepository(mongodb_database)
    metaspec = Metaspec(
        id=str(uuid.uuid4()),
        demand_id="demand_123",
        type=MetaspecType.ARCHITECTURE,
        content="# Architecture\n\nTo be deleted",
        created_at=datetime.utcnow(),
    )
    await repo.create(metaspec)

    # Verify it exists
    found_before = await repo.get_by_id(metaspec.id)
    assert found_before is not None

    # Act
    await repo.delete(metaspec.id)

    # Assert
    found_after = await repo.get_by_id(metaspec.id)
    assert found_after is None


@pytest.mark.asyncio
async def test_metaspec_type_conversion(mongodb_database: AsyncIOMotorDatabase):
    """Test: MetaspecType enum converts correctly to/from string"""
    # Arrange
    repo = MongoMetaspecRepository(mongodb_database)

    # Test all type values
    types = [
        MetaspecType.BUSINESS,
        MetaspecType.TECHNICAL,
        MetaspecType.ARCHITECTURE,
    ]

    for metaspec_type in types:
        metaspec = Metaspec(
            id=str(uuid.uuid4()),
            demand_id="demand_123",
            type=metaspec_type,
            content=f"# {metaspec_type.value.title()} Spec\n\nContent here",
            created_at=datetime.utcnow(),
        )

        # Act
        await repo.create(metaspec)
        found = await repo.get_by_id(metaspec.id)

        # Assert
        assert found is not None
        assert found.type == metaspec_type
        assert isinstance(found.type, MetaspecType)

        # Verify it's stored as string in MongoDB
        collection = mongodb_database["metaspecs"]
        document = await collection.find_one({"id": metaspec.id})
        assert document["type"] == metaspec_type.value
        assert isinstance(document["type"], str)


@pytest.mark.asyncio
async def test_metaspec_version_increment(mongodb_database: AsyncIOMotorDatabase):
    """Test: Version increments correctly"""
    # Arrange
    repo = MongoMetaspecRepository(mongodb_database)
    metaspec = Metaspec(
        id=str(uuid.uuid4()),
        demand_id="demand_123",
        type=MetaspecType.BUSINESS,
        content="# Version 1\n\nInitial version",
        version=1,
        created_at=datetime.utcnow(),
    )
    await repo.create(metaspec)

    # Act - Increment version multiple times
    for expected_version in [2, 3, 4]:
        metaspec.increment_version()
        await repo.update(metaspec)

        found = await repo.get_by_id(metaspec.id)
        assert found is not None
        assert found.version == expected_version
        assert found.updated_at is not None


@pytest.mark.asyncio
async def test_metaspec_content_persistence(mongodb_database: AsyncIOMotorDatabase):
    """Test: Markdown content persists correctly (including special chars)"""
    # Arrange
    repo = MongoMetaspecRepository(mongodb_database)
    markdown_content = """# Business Requirements

## User Stories

- As a **user**, I want to `login` with email
- Special chars: @#$%^&*()

## Acceptance Criteria

1. Email validation
2. Password requirements
"""

    metaspec = Metaspec(
        id=str(uuid.uuid4()),
        demand_id="demand_123",
        type=MetaspecType.BUSINESS,
        content=markdown_content,
        created_at=datetime.utcnow(),
    )

    # Act
    await repo.create(metaspec)
    found = await repo.get_by_id(metaspec.id)

    # Assert
    assert found is not None
    assert found.content == markdown_content
    assert "**user**" in found.content
    assert "`login`" in found.content
    assert "@#$%^&*()" in found.content


@pytest.mark.asyncio
async def test_multiple_metaspecs_isolation(mongodb_database: AsyncIOMotorDatabase):
    """Test: Multiple metaspecs don't interfere with each other"""
    # Arrange
    repo = MongoMetaspecRepository(mongodb_database)
    metaspec1 = Metaspec(
        id=str(uuid.uuid4()),
        demand_id="demand_1",
        type=MetaspecType.BUSINESS,
        content="# Business Spec\n\nContent 1",
        version=1,
        created_at=datetime.utcnow(),
    )
    metaspec2 = Metaspec(
        id=str(uuid.uuid4()),
        demand_id="demand_2",
        type=MetaspecType.TECHNICAL,
        content="# Technical Spec\n\nContent 2",
        version=3,
        created_at=datetime.utcnow(),
    )

    # Act
    await repo.create(metaspec1)
    await repo.create(metaspec2)

    found1 = await repo.get_by_id(metaspec1.id)
    found2 = await repo.get_by_id(metaspec2.id)

    # Assert
    assert found1 is not None
    assert found2 is not None
    assert found1.id == metaspec1.id
    assert found2.id == metaspec2.id
    assert found1.type == MetaspecType.BUSINESS
    assert found2.type == MetaspecType.TECHNICAL
    assert found1.version == 1
    assert found2.version == 3
    assert "Content 1" in found1.content
    assert "Content 2" in found2.content
