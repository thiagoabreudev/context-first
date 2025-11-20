"""
Integration Tests for MongoCheckpointRepository

Tests with real MongoDB database via Docker Compose.
Database is cleaned before each test (see conftest.py).

IAD-7: Repository Pattern + MongoDB
"""

import json
import uuid
from datetime import datetime, timedelta

import pytest
from motor.motor_asyncio import AsyncIOMotorDatabase

from domain.entities.checkpoint import Checkpoint
from infrastructure.persistence.mongodb.mongo_checkpoint_repository import (
    MongoCheckpointRepository,
)


@pytest.mark.asyncio
async def test_create_and_get_checkpoint(mongodb_database: AsyncIOMotorDatabase):
    """Test: Create checkpoint and retrieve it by ID"""
    # Arrange
    repo = MongoCheckpointRepository(mongodb_database)
    snapshot = json.dumps({"messages": [], "state": "active", "tokens": 1000})
    checkpoint = Checkpoint(
        id=str(uuid.uuid4()),
        demand_id="demand_123",
        context_snapshot=snapshot,
        tokens_used=1000,
        created_at=datetime.utcnow(),
    )

    # Act
    created = await repo.create(checkpoint)
    found = await repo.get_by_id(checkpoint.id)

    # Assert
    assert created.id == checkpoint.id
    assert found is not None
    assert found.id == checkpoint.id
    assert found.demand_id == "demand_123"
    assert found.context_snapshot == snapshot
    assert found.tokens_used == 1000
    assert found.created_at is not None
    assert found.expires_at is None


@pytest.mark.asyncio
async def test_get_by_id_not_found(mongodb_database: AsyncIOMotorDatabase):
    """Test: Get non-existent checkpoint returns None"""
    # Arrange
    repo = MongoCheckpointRepository(mongodb_database)
    non_existent_id = str(uuid.uuid4())

    # Act
    found = await repo.get_by_id(non_existent_id)

    # Assert
    assert found is None


@pytest.mark.asyncio
async def test_update_checkpoint(mongodb_database: AsyncIOMotorDatabase):
    """Test: Update checkpoint and verify changes persist"""
    # Arrange
    repo = MongoCheckpointRepository(mongodb_database)
    snapshot_v1 = json.dumps({"version": 1, "messages": []})
    checkpoint = Checkpoint(
        id=str(uuid.uuid4()),
        demand_id="demand_123",
        context_snapshot=snapshot_v1,
        tokens_used=1000,
        created_at=datetime.utcnow(),
    )
    await repo.create(checkpoint)

    # Act - Update checkpoint
    snapshot_v2 = json.dumps({"version": 2, "messages": ["msg1"]})
    checkpoint.context_snapshot = snapshot_v2
    checkpoint.tokens_used = 2000

    updated = await repo.update(checkpoint)
    found = await repo.get_by_id(checkpoint.id)

    # Assert
    assert updated.id == checkpoint.id
    assert found is not None
    assert found.context_snapshot == snapshot_v2
    assert found.tokens_used == 2000
    # Verify JSON is valid
    parsed = json.loads(found.context_snapshot)
    assert parsed["version"] == 2
    assert parsed["messages"] == ["msg1"]


@pytest.mark.asyncio
async def test_delete_checkpoint(mongodb_database: AsyncIOMotorDatabase):
    """Test: Delete checkpoint and verify it's removed"""
    # Arrange
    repo = MongoCheckpointRepository(mongodb_database)
    checkpoint = Checkpoint(
        id=str(uuid.uuid4()),
        demand_id="demand_123",
        context_snapshot='{"state": "to_be_deleted"}',
        tokens_used=500,
        created_at=datetime.utcnow(),
    )
    await repo.create(checkpoint)

    # Verify it exists
    found_before = await repo.get_by_id(checkpoint.id)
    assert found_before is not None

    # Act
    await repo.delete(checkpoint.id)

    # Assert
    found_after = await repo.get_by_id(checkpoint.id)
    assert found_after is None


@pytest.mark.asyncio
async def test_checkpoint_json_snapshot(mongodb_database: AsyncIOMotorDatabase):
    """Test: context_snapshot (JSON string) persists correctly"""
    # Arrange
    repo = MongoCheckpointRepository(mongodb_database)
    complex_snapshot = json.dumps(
        {
            "messages": [
                {"role": "user", "content": "Hello"},
                {"role": "assistant", "content": "Hi there!"},
            ],
            "state": "active",
            "metadata": {"tokens": 1500, "model": "gpt-4"},
            "special_chars": "Test @#$% special chars",
        }
    )
    checkpoint = Checkpoint(
        id=str(uuid.uuid4()),
        demand_id="demand_123",
        context_snapshot=complex_snapshot,
        tokens_used=1500,
        created_at=datetime.utcnow(),
    )

    # Act
    await repo.create(checkpoint)
    found = await repo.get_by_id(checkpoint.id)

    # Assert
    assert found is not None
    assert found.context_snapshot == complex_snapshot

    # Verify JSON is valid and complete
    parsed = json.loads(found.context_snapshot)
    assert len(parsed["messages"]) == 2
    assert parsed["messages"][0]["role"] == "user"
    assert parsed["metadata"]["tokens"] == 1500
    assert parsed["special_chars"] == "Test @#$% special chars"


@pytest.mark.asyncio
async def test_optional_expires_at_none(mongodb_database: AsyncIOMotorDatabase):
    """Test: Optional expires_at works when None"""
    # Arrange
    repo = MongoCheckpointRepository(mongodb_database)
    checkpoint = Checkpoint(
        id=str(uuid.uuid4()),
        demand_id="demand_123",
        context_snapshot='{"state": "no_expiration"}',
        tokens_used=1000,
        created_at=datetime.utcnow(),
        expires_at=None,
    )

    # Act
    await repo.create(checkpoint)
    found = await repo.get_by_id(checkpoint.id)

    # Assert
    assert found is not None
    assert found.expires_at is None
    assert not found.is_expired()

    # Verify it's not in MongoDB document (or is None)
    collection = mongodb_database["checkpoints"]
    document = await collection.find_one({"id": checkpoint.id})
    assert "expires_at" not in document or document.get("expires_at") is None


@pytest.mark.asyncio
async def test_optional_expires_at_with_value(mongodb_database: AsyncIOMotorDatabase):
    """Test: Optional expires_at works when provided"""
    # Arrange
    repo = MongoCheckpointRepository(mongodb_database)
    expiration = datetime.utcnow() + timedelta(days=7)
    checkpoint = Checkpoint(
        id=str(uuid.uuid4()),
        demand_id="demand_123",
        context_snapshot='{"state": "with_expiration"}',
        tokens_used=1000,
        created_at=datetime.utcnow(),
        expires_at=expiration,
    )

    # Act
    await repo.create(checkpoint)
    found = await repo.get_by_id(checkpoint.id)

    # Assert
    assert found is not None
    assert found.expires_at is not None
    assert not found.is_expired()  # 7 days in future

    # Verify it's stored in MongoDB
    collection = mongodb_database["checkpoints"]
    document = await collection.find_one({"id": checkpoint.id})
    assert "expires_at" in document
    assert document["expires_at"] is not None


@pytest.mark.asyncio
async def test_is_expired_method(mongodb_database: AsyncIOMotorDatabase):
    """Test: is_expired() method works correctly"""
    # Arrange
    repo = MongoCheckpointRepository(mongodb_database)

    # Checkpoint in the past (expired)
    past_expiration = datetime.utcnow() - timedelta(hours=1)
    expired_checkpoint = Checkpoint(
        id=str(uuid.uuid4()),
        demand_id="demand_123",
        context_snapshot='{"state": "expired"}',
        tokens_used=1000,
        created_at=datetime.utcnow() - timedelta(days=1),
        expires_at=past_expiration,
    )

    # Checkpoint in the future (not expired)
    future_expiration = datetime.utcnow() + timedelta(hours=1)
    active_checkpoint = Checkpoint(
        id=str(uuid.uuid4()),
        demand_id="demand_456",
        context_snapshot='{"state": "active"}',
        tokens_used=2000,
        created_at=datetime.utcnow(),
        expires_at=future_expiration,
    )

    # Act
    await repo.create(expired_checkpoint)
    await repo.create(active_checkpoint)

    found_expired = await repo.get_by_id(expired_checkpoint.id)
    found_active = await repo.get_by_id(active_checkpoint.id)

    # Assert
    assert found_expired is not None
    assert found_expired.is_expired() is True

    assert found_active is not None
    assert found_active.is_expired() is False


@pytest.mark.asyncio
async def test_multiple_checkpoints_isolation(mongodb_database: AsyncIOMotorDatabase):
    """Test: Multiple checkpoints don't interfere with each other"""
    # Arrange
    repo = MongoCheckpointRepository(mongodb_database)
    checkpoint1 = Checkpoint(
        id=str(uuid.uuid4()),
        demand_id="demand_1",
        context_snapshot='{"checkpoint": 1}',
        tokens_used=1000,
        created_at=datetime.utcnow(),
    )
    checkpoint2 = Checkpoint(
        id=str(uuid.uuid4()),
        demand_id="demand_2",
        context_snapshot='{"checkpoint": 2}',
        tokens_used=2000,
        created_at=datetime.utcnow(),
        expires_at=datetime.utcnow() + timedelta(days=1),
    )

    # Act
    await repo.create(checkpoint1)
    await repo.create(checkpoint2)

    found1 = await repo.get_by_id(checkpoint1.id)
    found2 = await repo.get_by_id(checkpoint2.id)

    # Assert
    assert found1 is not None
    assert found2 is not None
    assert found1.id == checkpoint1.id
    assert found2.id == checkpoint2.id
    assert found1.demand_id == "demand_1"
    assert found2.demand_id == "demand_2"
    assert found1.tokens_used == 1000
    assert found2.tokens_used == 2000
    assert found1.expires_at is None
    assert found2.expires_at is not None
    assert '{"checkpoint": 1}' in found1.context_snapshot
    assert '{"checkpoint": 2}' in found2.context_snapshot
