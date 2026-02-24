"""Reporting service."""

from typing import List, Dict, Optional
from config.database_connection import DatabaseConnection


class ReportingService:
    """Business logic for generating reports."""
    
    def __init__(self, db=None):
        self.db = db or DatabaseConnection()
    
    def get_inventory_summary(self) -> List[Dict]:
        """Get inventory summary."""
        sql = """
            SELECT p.product_id, p.product_name, p.quantity, p.uom, p.price,
                   c.category_name, p.status
            FROM products p
            LEFT JOIN categories c ON p.category_id = c.category_id
            WHERE p.deleted_at IS NULL
            ORDER BY p.product_name
        """
        try:
            return self.db.fetch_all(sql, dictionary=True)
        except Exception as e:
            print(f"Error fetching inventory summary: {e}")
            return []
    
    def get_warehouse_utilization(self) -> List[Dict]:
        """Get warehouse utilization."""
        sql = """
            SELECT w.warehouse_id, w.warehouse_name, w.capacity,
                   COUNT(DISTINCT s.stock_id) as stock_count,
                   SUM(s.quantity) as total_quantity
            FROM warehouses w
            LEFT JOIN stocks s ON w.warehouse_id = s.warehouse_id
            WHERE w.status = 'ACTIVE'
            GROUP BY w.warehouse_id, w.warehouse_name, w.capacity
        """
        try:
            return self.db.fetch_all(sql, dictionary=True)
        except Exception as e:
            print(f"Error fetching warehouse utilization: {e}")
            return []
    
    def get_low_stock_items(self, threshold: int = 10) -> List[Dict]:
        """Get low stock items."""
        sql = """
            SELECT product_id, product_name, quantity, uom, status
            FROM products
            WHERE quantity < %s AND status = 'AVAILABLE' AND deleted_at IS NULL
            ORDER BY quantity ASC
        """
        try:
            return self.db.fetch_all(sql, (threshold,), dictionary=True)
        except Exception as e:
            print(f"Error fetching low stock items: {e}")
            return []
    
    def get_user_activity_summary(self) -> List[Dict]:
        """Get user activity summary."""
        sql = """
            SELECT u.username, r.role_name, u.status, u.last_login,
                   u.last_logout, u.failed_attempts
            FROM users u
            LEFT JOIN roles r ON u.role_id = r.role_id
            WHERE u.deleted_at IS NULL
            ORDER BY u.last_login DESC
        """
        try:
            return self.db.fetch_all(sql, dictionary=True)
        except Exception as e:
            print(f"Error fetching user activity: {e}")
            return []
