"""Product repository for database operations."""

from typing import Optional, Dict, List
from config.database_connection import DatabaseConnection


class ProductRepository:
    """Data access layer for products."""
    
    def __init__(self, db=None):
        self.db = db or DatabaseConnection()
    
    def find_by_id(self, product_id: int) -> Optional[Dict]:
        """Find a product by ID."""
        sql = """
            SELECT p.*, c.category_name 
            FROM products p
            LEFT JOIN categories c ON p.category_id = c.category_id
            WHERE p.product_id = %s AND p.deleted_at IS NULL
        """
        return self.db.fetch_one(sql, (product_id,), dictionary=True)
    
    def find_all(self, include_unavailable=False) -> List[Dict]:
        """Get all products."""
        if include_unavailable:
            sql = """
                SELECT p.*, c.category_name 
                FROM products p
                LEFT JOIN categories c ON p.category_id = c.category_id
                WHERE p.deleted_at IS NULL
            """
        else:
            sql = """
                SELECT p.*, c.category_name 
                FROM products p
                LEFT JOIN categories c ON p.category_id = c.category_id
                WHERE p.status = 'AVAILABLE' AND p.deleted_at IS NULL
            """
        return self.db.fetch_all(sql, dictionary=True)
    
    def find_by_category(self, category_id: int) -> List[Dict]:
        """Find products by category."""
        sql = """
            SELECT p.*, c.category_name 
            FROM products p
            LEFT JOIN categories c ON p.category_id = c.category_id
            WHERE p.category_id = %s AND p.deleted_at IS NULL
        """
        return self.db.fetch_all(sql, (category_id,), dictionary=True)
    
    def create(self, product_name: str, category_id: Optional[int], 
               price: float, quantity: int, uom: str) -> int:
        """Create a new product."""
        sql = """
            INSERT INTO products 
            (product_name, category_id, price, quantity, uom, created_at) 
            VALUES (%s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
        """
        self.db.execute_query(sql, (product_name, category_id, price, quantity, uom))
        return self.db.get_last_insert_id()
    
    def update(self, product_id: int, updates: Dict) -> int:
        """Update product details."""
        fields = ", ".join(f"{k}=%s" for k in updates.keys())
        values = list(updates.values()) + [product_id]
        sql = f"UPDATE products SET {fields} WHERE product_id=%s"
        return self.db.execute_query(sql, values)
    
    def delete(self, product_id: int) -> int:
        """Soft delete a product."""
        sql = "UPDATE products SET deleted_at = CURRENT_TIMESTAMP WHERE product_id = %s"
        return self.db.execute_query(sql, (product_id,))
    
    def update_quantity(self, product_id: int, quantity_change: int) -> int:
        """Update product quantity."""
        sql = "UPDATE products SET quantity = quantity + %s WHERE product_id = %s"
        return self.db.execute_query(sql, (quantity_change, product_id))
