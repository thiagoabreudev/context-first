"""
Integration Tests for MongoDemandRepository

Tests with real MongoDB database via Docker Compose.
Database is cleaned before each test (see conftest.py).

IAD-7: Repository Pattern + MongoDB
"""

import uuid
from datetime import datetime

import pytest
from motor.motor_asyncio import AsyncIOMotorDatabase

from domain.entities.demand import Demand
from domain.value_objects.context_budget import ContextBudget
from domain.value_objects.demand_status import DemandStatus
from infrastructure.persistence.mongodb.mongo_demand_repository import (
    MongoDemandRepository,
)


@pytest.mark.asyncio
async def test_create_and_get_demand(mongodb_database: AsyncIOMotorDatabase):
    """Test: Create demand and retrieve it by ID"""
    # Arrange
    repo = MongoDemandRepository(mongodb_database)
    demand = Demand(
        id=str(uuid.uuid4()),
        project_id="project_123",
        title="Test Demand",
        description="A test demand for integration testing",
        status=DemandStatus.DRAFT,
        created_at=datetime.utcnow(),
    )

    # Act
    created = await repo.create(demand)
    found = await repo.get_by_id(demand.id)

    # Assert
    assert created.id == demand.id
    assert found is not None
    assert found.id == demand.id
    assert found.project_id == "project_123"
    assert found.title == "Test Demand"
    assert found.description == "A test demand for integration testing"
    assert found.status == DemandStatus.DRAFT
    assert found.context_budget is None
    assert found.created_at is not None
    assert found.updated_at is None


@pytest.mark.asyncio
async def test_get_by_id_not_found(mongodb_database: AsyncIOMotorDatabase):
    """Test: Get non-existent demand returns None"""
    # Arrange
    repo = MongoDemandRepository(mongodb_database)
    non_existent_id = str(uuid.uuid4())

    # Act
    found = await repo.get_by_id(non_existent_id)

    # Assert
    assert found is None


@pytest.mark.asyncio
async def test_update_demand(mongodb_database: AsyncIOMotorDatabase):
    """Test: Update demand and verify changes persist"""
    # Arrange
    repo = MongoDemandRepository(mongodb_database)
    demand = Demand(
        id=str(uuid.uuid4()),
        project_id="project_123",
        title="Original Title",
        description="Original description",
        status=DemandStatus.DRAFT,
        created_at=datetime.utcnow(),
    )
    await repo.create(demand)

    # Act - Update demand
    demand.title = "Updated Title"
    demand.description = "Updated description"
    demand.status = DemandStatus.SPEC_APPROVED
    demand.updated_at = datetime.utcnow()

    updated = await repo.update(demand)
    found = await repo.get_by_id(demand.id)

    # Assert
    assert updated.id == demand.id
    assert found is not None
    assert found.title == "Updated Title"
    assert found.description == "Updated description"
    assert found.status == DemandStatus.SPEC_APPROVED
    assert found.updated_at is not None


@pytest.mark.asyncio
async def test_delete_demand(mongodb_database: AsyncIOMotorDatabase):
    """Test: Delete demand and verify it's removed"""
    # Arrange
    repo = MongoDemandRepository(mongodb_database)
    demand = Demand(
        id=str(uuid.uuid4()),
        project_id="project_123",
        title="To Be Deleted",
        description="This demand will be deleted",
        status=DemandStatus.DRAFT,
        created_at=datetime.utcnow(),
    )
    await repo.create(demand)

    # Verify it exists
    found_before = await repo.get_by_id(demand.id)
    assert found_before is not None

    # Act
    await repo.delete(demand.id)

    # Assert
    found_after = await repo.get_by_id(demand.id)
    assert found_after is None


@pytest.mark.asyncio
async def test_demand_status_conversion(mongodb_database: AsyncIOMotorDatabase):
    """Test: DemandStatus enum converts correctly to/from string"""
    # Arrange
    repo = MongoDemandRepository(mongodb_database)

    # Test all status values
    statuses = [
        DemandStatus.DRAFT,
        DemandStatus.SPEC_APPROVED,
        DemandStatus.ARCHITECTURE_DONE,
        DemandStatus.CODE_COMPLETE,
        DemandStatus.PR_MERGED,
    ]

    for status in statuses:
        demand = Demand(
            id=str(uuid.uuid4()),
            project_id="project_123",
            title=f"Test {status.value}",
            description="Testing status conversion",
            status=status,
            created_at=datetime.utcnow(),
        )

        # Act
        await repo.create(demand)
        found = await repo.get_by_id(demand.id)

        # Assert
        assert found is not None
        assert found.status == status
        assert isinstance(found.status, DemandStatus)

        # Verify it's stored as string in MongoDB
        collection = mongodb_database["demands"]
        document = await collection.find_one({"id": demand.id})
        assert document["status"] == status.value
        assert isinstance(document["status"], str)


@pytest.mark.asyncio
async def test_optional_context_budget_none(mongodb_database: AsyncIOMotorDatabase):
    """Test: Optional ContextBudget works when None"""
    # Arrange
    repo = MongoDemandRepository(mongodb_database)
    demand = Demand(
        id=str(uuid.uuid4()),
        project_id="project_123",
        title="No Budget",
        description="Demand without context budget",
        status=DemandStatus.DRAFT,
        context_budget=None,
        created_at=datetime.utcnow(),
    )

    # Act
    await repo.create(demand)
    found = await repo.get_by_id(demand.id)

    # Assert
    assert found is not None
    assert found.context_budget is None

    # Verify it's not in MongoDB document
    collection = mongodb_database["demands"]
    document = await collection.find_one({"id": demand.id})
    assert "context_budget" not in document or document.get("context_budget") is None


@pytest.mark.asyncio
async def test_optional_context_budget_with_value(
    mongodb_database: AsyncIOMotorDatabase,
):
    """Test: Optional ContextBudget works when provided"""
    # Arrange
    repo = MongoDemandRepository(mongodb_database)
    context_budget = ContextBudget(max_tokens=50000, used_tokens=10000)
    demand = Demand(
        id=str(uuid.uuid4()),
        project_id="project_123",
        title="With Budget",
        description="Demand with context budget",
        status=DemandStatus.DRAFT,
        context_budget=context_budget,
        created_at=datetime.utcnow(),
    )

    # Act
    await repo.create(demand)
    found = await repo.get_by_id(demand.id)

    # Assert
    assert found is not None
    assert found.context_budget is not None
    assert found.context_budget.max_tokens == 50000
    assert found.context_budget.used_tokens == 10000
    assert found.context_budget.remaining_tokens == 40000

    # Verify it's stored as subdocument in MongoDB
    collection = mongodb_database["demands"]
    document = await collection.find_one({"id": demand.id})
    assert "context_budget" in document
    assert document["context_budget"]["max_tokens"] == 50000
    assert document["context_budget"]["used_tokens"] == 10000


@pytest.mark.asyncio
async def test_multiple_demands_isolation(mongodb_database: AsyncIOMotorDatabase):
    """Test: Multiple demands don't interfere with each other"""
    # Arrange
    repo = MongoDemandRepository(mongodb_database)
    demand1 = Demand(
        id=str(uuid.uuid4()),
        project_id="project_1",
        title="Demand 1",
        description="First demand",
        status=DemandStatus.DRAFT,
        created_at=datetime.utcnow(),
    )
    demand2 = Demand(
        id=str(uuid.uuid4()),
        project_id="project_2",
        title="Demand 2",
        description="Second demand",
        status=DemandStatus.SPEC_APPROVED,
        context_budget=ContextBudget(max_tokens=100000, used_tokens=0),
        created_at=datetime.utcnow(),
    )

    # Act
    await repo.create(demand1)
    await repo.create(demand2)

    found1 = await repo.get_by_id(demand1.id)
    found2 = await repo.get_by_id(demand2.id)

    # Assert
    assert found1 is not None
    assert found2 is not None
    assert found1.id == demand1.id
    assert found2.id == demand2.id
    assert found1.title == "Demand 1"
    assert found2.title == "Demand 2"
    assert found1.status == DemandStatus.DRAFT
    assert found2.status == DemandStatus.SPEC_APPROVED
    assert found1.context_budget is None
    assert found2.context_budget is not None
