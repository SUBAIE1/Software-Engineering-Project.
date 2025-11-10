import mysql.connector
from datetime import datetime
from storage_section import StorageSection

class Warehouse:
    def __init__(self, db_conn, warehouse_id=None, name=None, location=None, manager_id=None, capacity=None, status='ACTIVE'):
        self.db = db_conn
        self.warehouse_id = warehouse_id
        self.name = name
        self.location = location
        self.manager_id = manager_id
        self.capacity = capacity
        self.status = status

    def create(self):
        cursor = self.db.cursor()
        sql = """INSERT INTO warehouses (warehouse_name, warehouse_location, manager_id, capacity, status)
                 VALUES (%s, %s, %s, %s, %s)"""
        cursor.execute(sql, (self.name, self.location, self.manager_id, self.capacity, self.status))
        self.db.commit()
        print(f"✅ Warehouse '{self.name}' created successfully.")

    def update(self, **kwargs):
        cursor = self.db.cursor()
        fields = ", ".join(f"{k}=%s" for k in kwargs.keys())
        values = list(kwargs.values()) + [self.warehouse_id]
        sql = f"UPDATE warehouses SET {fields} WHERE warehouse_id=%s"
        cursor.execute(sql, values)
        self.db.commit()
        print(f"🔄 Warehouse '{self.warehouse_id}' updated.")

    def delete(self):
        cursor = self.db.cursor()
        cursor.execute("DELETE FROM warehouses WHERE warehouse_id=%s", (self.warehouse_id,))
        self.db.commit()
        print(f"❌ Warehouse '{self.warehouse_id}' deleted.")

    def list_sections(self):
        cursor = self.db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM storage_sections WHERE warehouse_id=%s", (self.warehouse_id,))
        return cursor.fetchall()

    def __repr__(self):
        return f"<Warehouse {self.name} - {self.location}>"
