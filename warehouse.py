"""Warehouse model for storage facilities."""

from datetime import datetime
from typing import Optional


class Warehouse:
    """Represents a warehouse in the system."""
    
    def __init__(
        self,
        warehouse_id: Optional[int] = None,
        warehouse_name: str = "",
        warehouse_location: str = "",
        manager_username: Optional[str] = None,
        capacity: Optional[int] = None,
        status: str = "ACTIVE",
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
        deleted_at: Optional[datetime] = None
    ):
        self.warehouse_id = warehouse_id
        self.warehouse_name = warehouse_name
        self.warehouse_location = warehouse_location
        self.manager_username = manager_username
        self.capacity = capacity
        self.status = status
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at
        self.deleted_at = deleted_at
    
    def __repr__(self):
        return f"Warehouse({self.warehouse_id}, {self.warehouse_name})"


class StorageSection:
    """Represents a storage section within a warehouse."""
    
    def __init__(
        self,
        section_id: Optional[int] = None,
        warehouse_id: Optional[int] = None,
        section_name: str = "",
        capacity: Optional[int] = None,
        status: str = "ACTIVE",
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.section_id = section_id
        self.warehouse_id = warehouse_id
        self.section_name = section_name
        self.capacity = capacity
        self.status = status
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at
    
    def __repr__(self):
        return f"StorageSection({self.section_id}, {self.section_name})"


class Stock:
    """Represents stock items in storage."""
    
    def __init__(
        self,
        stock_id: Optional[int] = None,
        warehouse_id: Optional[int] = None,
        section_id: Optional[int] = None,
        stock_name: str = "",
        product_id: Optional[int] = None,
        quantity: int = 0,
        status: str = "ACTIVE"
    ):
        self.stock_id = stock_id
        self.warehouse_id = warehouse_id
        self.section_id = section_id
        self.stock_name = stock_name
        self.product_id = product_id
        self.quantity = quantity
        self.status = status
    
    def __repr__(self):
        return f"Stock({self.stock_id}, {self.stock_name}, qty={self.quantity})"
