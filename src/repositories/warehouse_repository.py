"""Warehouse repository for database operations."""

from typing import Optional, Dict, List
from config.database_connection import DatabaseConnection


class WarehouseRepository:
    """Data access layer for warehouses."""
    
    def __init__(self, db=None):
        self.db = db or DatabaseConnection()
    
    def find_by_id(self, warehouse_id: int) -> Optional[Dict]:
        """Find a warehouse by ID."""
        sql = """
            SELECT * FROM warehouses 
            WHERE warehouse_id = %s AND deleted_at IS NULL
        """
        return self.db.fetch_one(sql, (warehouse_id,), dictionary=True)
    
    def find_all(self, include_inactive=False) -> List[Dict]:
        """Get all warehouses."""
        if include_inactive:
            sql = "SELECT * FROM warehouses WHERE deleted_at IS NULL"
        else:
            sql = "SELECT * FROM warehouses WHERE status = 'ACTIVE' AND deleted_at IS NULL"
        return self.db.fetch_all(sql, dictionary=True)
    
    def create(self, warehouse_name: str, warehouse_location: str, 
               manager_username: Optional[str], capacity: Optional[int]) -> int:
        """Create a new warehouse."""
        sql = """
            INSERT INTO warehouses 
            (warehouse_name, warehouse_location, manager_username, capacity, created_at) 
            VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP)
        """
        self.db.execute_query(sql, (warehouse_name, warehouse_location, 
                                    manager_username, capacity))
        return self.db.get_last_insert_id()
    
    def update(self, warehouse_id: int, updates: Dict) -> int:
        """Update warehouse details."""
        fields = ", ".join(f"{k}=%s" for k in updates.keys())
        values = list(updates.values()) + [warehouse_id]
        sql = f"UPDATE warehouses SET {fields} WHERE warehouse_id=%s"
        return self.db.execute_query(sql, values)
    
    def delete(self, warehouse_id: int) -> int:
        """Soft delete a warehouse."""
        sql = "UPDATE warehouses SET deleted_at = CURRENT_TIMESTAMP WHERE warehouse_id = %s"
        return self.db.execute_query(sql, (warehouse_id,))


class StorageSectionRepository:
    """Data access layer for storage sections."""
    
    def __init__(self, db=None):
        self.db = db or DatabaseConnection()
    
    def find_by_id(self, section_id: int) -> Optional[Dict]:
        """Find a storage section by ID."""
        sql = """
            SELECT s.*, w.warehouse_name 
            FROM storage_sections s
            LEFT JOIN warehouses w ON s.warehouse_id = w.warehouse_id
            WHERE s.section_id = %s
        """
        return self.db.fetch_one(sql, (section_id,), dictionary=True)
    
    def find_by_warehouse(self, warehouse_id: int) -> List[Dict]:
        """Find all storage sections in a warehouse."""
        sql = """
            SELECT * FROM storage_sections 
            WHERE warehouse_id = %s AND status = 'ACTIVE'
        """
        return self.db.fetch_all(sql, (warehouse_id,), dictionary=True)
    
    def create(self, warehouse_id: int, section_name: str, 
               capacity: Optional[int]) -> int:
        """Create a new storage section."""
        sql = """
            INSERT INTO storage_sections 
            (warehouse_id, section_name, capacity, created_at) 
            VALUES (%s, %s, %s, CURRENT_TIMESTAMP)
        """
        self.db.execute_query(sql, (warehouse_id, section_name, capacity))
        return self.db.get_last_insert_id()
    
    def update(self, section_id: int, updates: Dict) -> int:
        """Update storage section details."""
        fields = ", ".join(f"{k}=%s" for k in updates.keys())
        values = list(updates.values()) + [section_id]
        sql = f"UPDATE storage_sections SET {fields} WHERE section_id=%s"
        return self.db.execute_query(sql, values)
    
    def delete(self, section_id: int) -> int:
        """Delete a storage section."""
        sql = "DELETE FROM storage_sections WHERE section_id = %s"
        return self.db.execute_query(sql, (section_id,))
