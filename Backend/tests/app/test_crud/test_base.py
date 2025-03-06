# tests/app/test_crud/test_base.py
import pytest
from typing import Dict, Any

from app.crud.base import CRUDBase
from tests.conftest import TestItem, TestItemCreate, TestItemUpdate


class TestCRUDBase:
    # Initialize the CRUD object with the test model
    crud = CRUDBase(TestItem)
    
    def test_create(self, db, test_item_create):
        """Test creating an item."""
        item = self.crud.create(db, obj_in=test_item_create)
        assert item.title == "Test Item"
        assert item.description == "Test Description"
        assert item.id is not None
    
    def test_create_with_owner(self, db, test_item_create):
        """Test creating an item with an owner."""
        owner_id = 1
        item = self.crud.create(db, obj_in=test_item_create, owner_id=owner_id)
        assert item.owner_id == owner_id
    
    def test_get(self, db, test_item_create):
        """Test getting an item by id."""
        item = self.crud.create(db, obj_in=test_item_create)
        retrieved_item = self.crud.get(db, id=item.id)
        assert retrieved_item.id == item.id
        assert retrieved_item.title == item.title
    
    def test_get_multi(self, db, test_item_create):
        """Test getting multiple items."""
        # Create multiple items
        self.crud.create(db, obj_in=test_item_create)
        self.crud.create(db, obj_in=TestItemCreate(title="Another Item", description="Another Description"))
        
        items = self.crud.get_multi(db)
        assert len(items) == 2
    
    def test_get_multi_with_skip_limit(self, db, test_item_create):
        """Test getting multiple items with skip and limit."""
        # Create multiple items
        for i in range(5):
            self.crud.create(db, obj_in=TestItemCreate(title=f"Item {i}", description=f"Description {i}"))
        
        items = self.crud.get_multi(db, skip=1, limit=2)
        assert len(items) == 2
        assert items[0].title == "Item 1"
    
    def test_update_with_obj(self, db, test_item_create, test_item_update):
        """Test updating an item with Pydantic model."""
        item = self.crud.create(db, obj_in=test_item_create)
        updated_item = self.crud.update(db, db_obj=item, obj_in=TestItemUpdate(**test_item_update))
        assert updated_item.title == "Updated Item"
        assert updated_item.description == "Updated Description"
    
    def test_update_with_dict(self, db, test_item_create, test_item_update):
        """Test updating an item with dict."""
        item = self.crud.create(db, obj_in=test_item_create)
        updated_item = self.crud.update(db, db_obj=item, obj_in=test_item_update)
        assert updated_item.title == "Updated Item"
        assert updated_item.description == "Updated Description"
    
    def test_remove(self, db, test_item_create):
        """Test removing an item."""
        item = self.crud.create(db, obj_in=test_item_create)
        removed_item = self.crud.remove(db, id=item.id)
        assert removed_item.id == item.id
        
        # Verify item no longer exists
        non_existent_item = self.crud.get(db, id=item.id)
        assert non_existent_item is None