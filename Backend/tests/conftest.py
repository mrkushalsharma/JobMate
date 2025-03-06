# tests/conftest.py
import os
import pytest
from sqlalchemy import create_engine, Column, Integer, String
# Updated import for declarative_base
from sqlalchemy.orm import sessionmaker, declarative_base
from typing import Generator, Dict, Any

# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base model using the updated import
Base = declarative_base()

# Define a test model
class TestItem(Base):
    __tablename__ = "test_items"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    owner_id = Column(Integer, index=True)


@pytest.fixture(scope="function")
def db() -> Generator:
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    # Use a session for tests
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        # Drop tables after test
        Base.metadata.drop_all(bind=engine)


# In a real project, you'd import your schemas from your app,
# but for this example, let's define them here:
from pydantic import BaseModel

class TestItemCreate(BaseModel):
    title: str
    description: str = None

class TestItemUpdate(BaseModel):
    title: str = None
    description: str = None

@pytest.fixture
def test_item_create() -> TestItemCreate:
    return TestItemCreate(title="Test Item", description="Test Description")

@pytest.fixture
def test_item_update() -> Dict[str, Any]:
    return {"title": "Updated Item", "description": "Updated Description"}