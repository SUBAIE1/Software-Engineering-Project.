
from tkinter import messagebox

from src.users.database_connection import DatabaseConnection
from datetime import datetime
from src.users.user import User
now = datetime.now()
formatted = now.strftime("%Y, %m, %d, %H, %M, %S")


class InventoryManager(User):

    def __init__(self, username, password, role_id, status='ACTIVE', failed_attempts=0,
                 locked_until=None, last_login=None, last_logout=None, created_at=formatted, db=None):
        super().__init__(
            username=username,
            password=password,
            role_id=role_id,
            status=status,
            db=DatabaseConnection()
        )

    def add_warehouse(self, db, warehouse_name, warehouse_location, manager_username, capacity, status='ACTIVE'):
        sql = (
            "INSERT INTO warehouses "
            "(warehouse_name, warehouse_location, manager_username, capacity, status) "
            "VALUES (%s, %s, %s, %s, %s)"
        )
        try:
            # use helper method instead of manual cursor/commit
            self.db.execute_query(
                sql,
                (warehouse_name, warehouse_location, manager_username, capacity, status)
            )
            print()
        except Exception as e:
            messagebox.showerror("Error", f"Error while adding warehouse: {e}")

    def delete_warehouse(self, db, warehouse_id):
        sql = "DELETE FROM warehouses WHERE warehouse_id=%s"
        try:
            self.db.execute_query(sql, (warehouse_id,))
            print()
        except Exception as e:
            messagebox.showerror("Error", f"Error while deleting warehouse: {e}")

    def update_warehouse(self, db, warehouse_id, updates: dict):
        fields = ", ".join(f"{k}=%s" for k in updates.keys())
        values = list(updates.values()) + [warehouse_id]
        sql = f"UPDATE warehouses SET {fields} WHERE warehouse_id=%s"
        try:
            self.db.execute_query(sql, values)
            print()
        except Exception as e:
            messagebox.showerror("Error", f"Error while updating warehouse: {e}")

    def deactivate_warehouse(self, db, warehouse_id):
        sql = "UPDATE warehouses SET status='INACTIVE' WHERE warehouse_id=%s"
        try:
            self.db.execute_query(sql, (warehouse_id,))
            print()
        except Exception as e:
            messagebox.showerror("Error", f"Error while deactivating warehouse: {e}")

    def reactivate_warehouse(self, db, warehouse_id):
        sql = "UPDATE warehouses SET status='ACTIVE' WHERE warehouse_id=%s"
        try:
            self.db.execute_query(sql, (warehouse_id,))
            print()
        except Exception as e:
            messagebox.showerror("Error", f"Error while reactivating warehouse: {e}")

    def review_all_warehouses(self, db):
        sql = "SELECT * FROM warehouses"
        try:
            rows = self.db.fetch_all(sql)
            for row in rows:
                print(row)
        except Exception as e:
            messagebox.showerror("Error", f"Error while review_all_warehouses: {e}")

    def assign_manager_to_warehouse(self, db, old_manager_id, new_manager_id):
        sql = "UPDATE warehouses SET manager_username=%s WHERE manager_username=%s"
        try:
            self.db.execute_query(sql, (new_manager_id, old_manager_id))
            print()
        except Exception as e:
            messagebox.showerror("Error", f"Error while assign_manager_to_warehouse: {e}")

    ###################################################################################################################################################################################################

    def add_storage_section(self, db, warehouse_id, section_name, status):
        sql = (
            "INSERT INTO storage_sections "
            "(warehouse_id, section_name, capacity, status) "
            "VALUES (%s, %s, %s, %s)"
        )
        try:
            self.db.execute_query(sql, (warehouse_id, section_name, None, status))
            print()
        except Exception as e:
            messagebox.showerror("Error", f"Error while add_storage_section: {e}")

    def delete_storage_section(self, db, section_id):
        sql = "DELETE FROM storage_sections WHERE section_id=%s"
        try:
            self.db.execute_query(sql, (section_id,))
            print()
        except Exception as e:
            messagebox.showerror("Error", f"Error while delete_storage_section: {e}")

    def update_storage_section(self, db, section_id, updates: dict):
        fields = ", ".join(f"{k}=%s" for k in updates.keys())
        values = list(updates.values()) + [section_id]
        sql = f"UPDATE storage_sections SET {fields} WHERE section_id=%s"
        try:
            self.db.execute_query(sql, values)
            print()
        except Exception as e:
            messagebox.showerror("Error", f"Error while update_storage_section: {e}")

    def deactivate_storage_section(self, db, section_id):
        sql = "UPDATE storage_sections SET status='INACTIVE' WHERE section_id=%s"
        try:
            self.db.execute_query(sql, (section_id,))
            print()
        except Exception as e:
            messagebox.showerror("Error", f"Error while deactivate_storage_section: {e}")

    def reactivate_storage_section(self, db, section_id):
        sql = "UPDATE storage_sections SET status='ACTIVE' WHERE section_id=%s"
        try:
            self.db.execute_query(sql, (section_id,))
            print()
        except Exception as e:
            messagebox.showerror("Error", f"Error while reactivate_storage_section: {e}")

    def review_all_storage_section(self, db):
        sql = "SELECT * FROM storage_sections"
        try:
            rows = self.db.fetch_all(sql)
            for row in rows:
                print(row)
        except Exception as e:
            messagebox.showerror("Error", f"Error while review_all_storage_section: {e}")

    ###################################################################################################################################################################################################

    def add_stock(self, db, stock_id, warehouse_id, section_id, stock_name, product_id, quantity, status):
        sql = "INSERT INTO stocks VALUES (%s, %s, %s, %s, %s, %s, %s)"
        try:
            self.db.execute_query(
                sql,
                (stock_id, warehouse_id, section_id, stock_name, product_id, quantity, status)
            )
            print()
        except Exception as e:
            messagebox.showerror("Error", f"Error while add_stock: {e}")

    def delete_stock(self, db, stock_id):
        sql = "DELETE FROM stocks WHERE stock_id=%s"
        try:
            self.db.execute_query(sql, (stock_id,))
            print()
        except Exception as e:
            messagebox.showerror("Error", f"Error while delete_stock: {e}")

    def update_stock(self, db, stock_id, updates: dict):
        fields = ", ".join(f"{k}=%s" for k in updates.keys())
        values = list(updates.values()) + [stock_id]
        sql = f"UPDATE stocks SET {fields} WHERE stock_id=%s"
        try:
            self.db.execute_query(sql, values)
            print()
        except Exception as e:
            messagebox.showerror("Error", f"Error while update_stock: {e}")

    def deactivate_stock(self, db, stock_id):
        sql = "UPDATE stocks SET status='INACTIVE' WHERE stock_id=%s"
        try:
            self.db.execute_query(sql, (stock_id,))
            print()
        except Exception as e:
            messagebox.showerror("Error", f"Error while deactivate_stock: {e}")

    def reactivate_stock(self, db, stock_id):
        sql = "UPDATE stocks SET status='ACTIVE' WHERE stock_id=%s"
        try:
            self.db.execute_query(sql, (stock_id,))
            print()
        except Exception as e:
            messagebox.showerror("Error", f"Error while reactivate_stock: {e}")

    def review_all_stocks(self, db):
        sql = "SELECT * FROM stocks"
        try:
            rows = self.db.fetch_all(sql)
            for row in rows:
                print(row)
        except Exception as e:
            messagebox.showerror("Error", f"Error while review_all_stocks: {e}")


