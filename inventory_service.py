"""Inventory service for managing products, warehouses, and stock."""

from tkinter import messagebox
from typing import Optional, Dict, List
from connection import DatabaseConnection


class InventoryService:
    """Business logic for inventory management."""
    
    def __init__(self, db=None):
        self.db = db or DatabaseConnection()
    
    # Warehouse operations
    def add_warehouse(self, warehouse_name: str, warehouse_location: str, 
                     manager_username: Optional[str], capacity: Optional[int], 
                     status: str = 'ACTIVE'):
        """Add a new warehouse to the system."""
        sql = (
            "INSERT INTO warehouses "
            "(warehouse_name, warehouse_location, manager_username, capacity, status) "
            "VALUES (%s, %s, %s, %s, %s)"
        )
        try:
            self.db.execute_query(
                sql,
                (warehouse_name, warehouse_location, manager_username, capacity, status)
            )
            print(f"Warehouse {warehouse_name} added successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Error while adding warehouse: {e}")
            raise

    def delete_warehouse(self, warehouse_id: int):
        """Delete a warehouse by ID."""
        sql = "DELETE FROM warehouses WHERE warehouse_id=%s"
        try:
            self.db.execute_query(sql, (warehouse_id,))
            print(f"Warehouse {warehouse_id} deleted successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Error while deleting warehouse: {e}")
            raise

    def update_warehouse(self, warehouse_id: int, updates: Dict):
        """Update warehouse details."""
        fields = ", ".join(f"{k}=%s" for k in updates.keys())
        values = list(updates.values()) + [warehouse_id]
        sql = f"UPDATE warehouses SET {fields} WHERE warehouse_id=%s"
        try:
            self.db.execute_query(sql, values)
            print(f"Warehouse {warehouse_id} updated successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Error while updating warehouse: {e}")
            raise

    def deactivate_warehouse(self, warehouse_id: int):
        """Deactivate a warehouse."""
        sql = "UPDATE warehouses SET status='INACTIVE' WHERE warehouse_id=%s"
        try:
            self.db.execute_query(sql, (warehouse_id,))
            print(f"Warehouse {warehouse_id} deactivated")
        except Exception as e:
            messagebox.showerror("Error", f"Error while deactivating warehouse: {e}")
            raise

    def reactivate_warehouse(self, warehouse_id: int):
        """Reactivate a warehouse."""
        sql = "UPDATE warehouses SET status='ACTIVE' WHERE warehouse_id=%s"
        try:
            self.db.execute_query(sql, (warehouse_id,))
            print(f"Warehouse {warehouse_id} reactivated")
        except Exception as e:
            messagebox.showerror("Error", f"Error while reactivating warehouse: {e}")
            raise

    def get_all_warehouses(self) -> List:
        """Retrieve all warehouses."""
        sql = "SELECT * FROM warehouses"
        try:
            return self.db.fetch_all(sql, dictionary=True)
        except Exception as e:
            messagebox.showerror("Error", f"Error while fetching warehouses: {e}")
            return []

    # Storage section operations
    def add_storage_section(self, warehouse_id: int, section_name: str, 
                           capacity: Optional[int], status: str = 'ACTIVE'):
        """Add a new storage section to a warehouse."""
        sql = (
            "INSERT INTO storage_sections "
            "(warehouse_id, section_name, capacity, status) "
            "VALUES (%s, %s, %s, %s)"
        )
        try:
            self.db.execute_query(sql, (warehouse_id, section_name, capacity, status))
            print(f"Storage section {section_name} added")
        except Exception as e:
            messagebox.showerror("Error", f"Error while adding storage section: {e}")
            raise

    def delete_storage_section(self, section_id: int):
        """Delete a storage section."""
        sql = "DELETE FROM storage_sections WHERE section_id=%s"
        try:
            self.db.execute_query(sql, (section_id,))
            print(f"Storage section {section_id} deleted")
        except Exception as e:
            messagebox.showerror("Error", f"Error while deleting storage section: {e}")
            raise

    def update_storage_section(self, section_id: int, updates: Dict):
        """Update storage section details."""
        fields = ", ".join(f"{k}=%s" for k in updates.keys())
        values = list(updates.values()) + [section_id]
        sql = f"UPDATE storage_sections SET {fields} WHERE section_id=%s"
        try:
            self.db.execute_query(sql, values)
            print(f"Storage section {section_id} updated")
        except Exception as e:
            messagebox.showerror("Error", f"Error while updating storage section: {e}")
            raise

    # Stock operations
    def add_stock(self, warehouse_id: int, section_id: int, stock_name: str, 
                  product_id: int, quantity: int, status: str = 'ACTIVE'):
        """Add new stock to a storage section."""
        sql = "INSERT INTO stocks (warehouse_id, section_id, stock_name, product_id, quantity, status) VALUES (%s, %s, %s, %s, %s, %s)"
        try:
            self.db.execute_query(
                sql,
                (warehouse_id, section_id, stock_name, product_id, quantity, status)
            )
            print(f"Stock {stock_name} added")
        except Exception as e:
            messagebox.showerror("Error", f"Error while adding stock: {e}")
            raise

    def update_stock(self, stock_id: int, updates: Dict):
        """Update stock details."""
        fields = ", ".join(f"{k}=%s" for k in updates.keys())
        values = list(updates.values()) + [stock_id]
        sql = f"UPDATE stocks SET {fields} WHERE stock_id=%s"
        try:
            self.db.execute_query(sql, values)
            print(f"Stock {stock_id} updated")
        except Exception as e:
            messagebox.showerror("Error", f"Error while updating stock: {e}")
            raise

    def get_all_stocks(self) -> List:
        """Retrieve all stocks."""
        sql = "SELECT * FROM stocks"
        try:
            return self.db.fetch_all(sql, dictionary=True)
        except Exception as e:
            messagebox.showerror("Error", f"Error while fetching stocks: {e}")
            return []
