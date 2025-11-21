"""
Pytest Configuration and Fixtures

Global fixtures for testing, including MongoDB test database setup.

IAD-7: Repository Pattern + MongoDB
"""

import pytest_asyncio
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase


@pytest_asyncio.fixture(scope="function")
async def mongodb_database() -> AsyncIOMotorDatabase:
    """
    Clean MongoDB database for each test (function scope).

    Clears all collections before each test to ensure isolation.
    Uses separate test database to avoid interfering with dev data.
    """
    # Create client for this test
    client = AsyncIOMotorClient(
        "mongodb://context_first_app:app_password_change_in_production@localhost:27017/context_first_dev?authSource=context_first_dev"
    )
    # Use same database as dev (will clean collections before/after tests)
    db = client["context_first_dev"]

    # Clean all collections before test
    await db["projects"].delete_many({})
    await db["demands"].delete_many({})
    await db["metaspecs"].delete_many({})
    await db["checkpoints"].delete_many({})

    yield db

    # Optional: Clean after test too (redundant but safe)
    await db["projects"].delete_many({})
    await db["demands"].delete_many({})
    await db["metaspecs"].delete_many({})
    await db["checkpoints"].delete_many({})

    # Close client
    client.close()
