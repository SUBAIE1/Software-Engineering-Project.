"""Inventory management service."""

from tkinter import messagebox
from typing import Optional, Dict, List
from config.database_connection import DatabaseConnection


class InventoryService:
    """Business logic for inventory management."""
    
    def __init__(self, db=None):
        self.db = db or DatabaseConnection()
    
    # Warehouse operations
    def add_warehouse(self, warehouse_name: str, warehouse_location: str, 
                     manager_username: Optional[str], capacity: Optional[int], 
                     status: str = 'ACTIVE'):
        """Add a new warehouse."""
        sql = (
            "INSERT INTO warehouses "
            "(warehouse_name, warehouse_location, manager_username, capacity, status) "
            "VALUES (%s, %s, %s, %s, %s)"
        )
        try:
            self.db.execute_query(sql, (warehouse_name, warehouse_location, manager_username, capacity, status))
            print(f"Warehouse {warehouse_name} added successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Error adding warehouse: {e}")
            raise

    def delete_warehouse(self, warehouse_id: int):
        """Delete a warehouse."""
        sql = "DELETE FROM warehouses WHERE warehouse_id=%s"
        try:
            self.db.execute_query(sql, (warehouse_id,))
            print(f"Warehouse {warehouse_id} deleted successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Error deleting warehouse: {e}")
            raise

    def update_warehouse(self, warehouse_id: int, updates: Dict):
        """Update warehouse details."""
        fields = ", ".join(f"{k}=%s" for k in updates.keys())
        values = list(updates.values()) + [warehouse_id]
        sql = f"UPDATE warehouses SET {fields} WHERE warehouse_id=%s"
        try:
            self.db.execute_query(sql, values)
            print(f"Warehouse {warehouse_id} updated")
        except Exception as e:
            messagebox.showerror("Error", f"Error updating warehouse: {e}")
            raise

    def get_all_warehouses(self) -> List:
        """Get all warehouses."""
        sql = "SELECT * FROM warehouses"
        try:
            return self.db.fetch_all(sql, dictionary=True)
        except Exception as e:
            messagebox.showerror("Error", f"Error fetching warehouses: {e}")
            return []

    # Storage section operations
    def add_storage_section(self, warehouse_id: int, section_name: str, 
                           capacity: Optional[int], status: str = 'ACTIVE'):
        """Add a storage section."""
        sql = (
            "INSERT INTO storage_sections "
            "(warehouse_id, section_name, capacity, status) "
            "VALUES (%s, %s, %s, %s)"
        )
        try:
            self.db.execute_query(sql, (warehouse_id, section_name, capacity, status))
            print(f"Storage section added")
        except Exception as e:
            messagebox.showerror("Error", f"Error adding storage section: {e}")
            raise

    # Stock operations
    def add_stock(self, warehouse_id: int, section_id: int, stock_name: str, 
                  product_id: int, quantity: int, status: str = 'ACTIVE'):
        """Add stock."""
        sql = """
            INSERT INTO stocks 
            (warehouse_id, section_id, stock_name, product_id, quantity, status) 
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        try:
            self.db.execute_query(sql, (warehouse_id, section_id, stock_name, product_id, quantity, status))
            print(f"Stock {stock_name} added")
        except Exception as e:
            messagebox.showerror("Error", f"Error adding stock: {e}")
            raise

    def get_all_stocks(self) -> List:
        """Get all stocks."""
        sql = "SELECT * FROM stocks"
        try:
            return self.db.fetch_all(sql, dictionary=True)
        except Exception as e:
            messagebox.showerror("Error", f"Error fetching stocks: {e}")
            return []
