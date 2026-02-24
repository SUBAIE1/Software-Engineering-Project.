"""Requisition repository for database operations."""

from typing import Optional, Dict, List
from config.database_connection import DatabaseConnection


class RequisitionRepository:
    """Data access layer for requisitions."""
    
    def __init__(self, db=None):
        self.db = db or DatabaseConnection()
    
    def find_by_id(self, requisition_id: int) -> Optional[Dict]:
        """Find a requisition by ID."""
        sql = """
            SELECT r.*, p.project_name 
            FROM requisition r
            LEFT JOIN projects p ON r.project_id = p.project_id
            WHERE r.requisition_id = %s AND r.deleted_at IS NULL
        """
        return self.db.fetch_one(sql, (requisition_id,), dictionary=True)
    
    def find_by_requester(self, requester_username: str) -> List[Dict]:
        """Find all requisitions by a requester."""
        sql = """
            SELECT r.*, p.project_name 
            FROM requisition r
            LEFT JOIN projects p ON r.project_id = p.project_id
            WHERE r.requester_username = %s AND r.deleted_at IS NULL
            ORDER BY r.created_at DESC
        """
        return self.db.fetch_all(sql, (requester_username,), dictionary=True)
    
    def find_by_status(self, status: str) -> List[Dict]:
        """Find all requisitions with a specific status."""
        sql = """
            SELECT r.*, p.project_name 
            FROM requisition r
            LEFT JOIN projects p ON r.project_id = p.project_id
            WHERE r.status = %s AND r.deleted_at IS NULL
            ORDER BY r.created_at DESC
        """
        return self.db.fetch_all(sql, (status,), dictionary=True)
    
    def find_all(self) -> List[Dict]:
        """Get all requisitions."""
        sql = """
            SELECT r.*, p.project_name 
            FROM requisition r
            LEFT JOIN projects p ON r.project_id = p.project_id
            WHERE r.deleted_at IS NULL
            ORDER BY r.created_at DESC
        """
        return self.db.fetch_all(sql, dictionary=True)
    
    def create(self, requester_username: str, project_id: Optional[int]) -> int:
        """Create a new requisition."""
        sql = """
            INSERT INTO requisition 
            (requester_username, project_id, status, created_at) 
            VALUES (%s, %s, 'PENDING', CURRENT_TIMESTAMP)
        """
        self.db.execute_query(sql, (requester_username, project_id))
        return self.db.get_last_insert_id()
    
    def update(self, requisition_id: int, updates: Dict) -> int:
        """Update requisition details."""
        fields = ", ".join(f"{k}=%s" for k in updates.keys())
        values = list(updates.values()) + [requisition_id]
        sql = f"UPDATE requisition SET {fields} WHERE requisition_id=%s"
        return self.db.execute_query(sql, values)
    
    def delete(self, requisition_id: int) -> int:
        """Soft delete a requisition."""
        sql = "UPDATE requisition SET deleted_at = CURRENT_TIMESTAMP WHERE requisition_id = %s"
        return self.db.execute_query(sql, (requisition_id,))


class RequisitionItemRepository:
    """Data access layer for requisition items."""
    
    def __init__(self, db=None):
        self.db = db or DatabaseConnection()
    
    def find_by_requisition(self, requisition_id: int) -> List[Dict]:
        """Find all items for a requisition."""
        sql = """
            SELECT ri.*, p.product_name, p.uom 
            FROM requisition_items ri
            LEFT JOIN products p ON ri.item_id = p.product_id
            WHERE ri.requisition_id = %s
        """
        return self.db.fetch_all(sql, (requisition_id,), dictionary=True)
    
    def create(self, requisition_id: int, item_id: int, quantity: int) -> int:
        """Add an item to a requisition."""
        sql = """
            INSERT INTO requisition_items 
            (requisition_id, item_id, quantity, created_at) 
            VALUES (%s, %s, %s, CURRENT_TIMESTAMP)
        """
        self.db.execute_query(sql, (requisition_id, item_id, quantity))
        return self.db.get_last_insert_id()
    
    def update(self, req_item_id: int, quantity: int) -> int:
        """Update requisition item quantity."""
        sql = "UPDATE requisition_items SET quantity = %s WHERE req_item_id = %s"
        return self.db.execute_query(sql, (quantity, req_item_id))
    
    def delete(self, req_item_id: int) -> int:
        """Delete a requisition item."""
        sql = "DELETE FROM requisition_items WHERE req_item_id = %s"
        return self.db.execute_query(sql, (req_item_id,))
