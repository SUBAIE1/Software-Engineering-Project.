from datetime import datetime

class StorageSection:
    def __init__(self, db_conn, section_id=None, warehouse_id=None, name=None, capacity=None, status='ACTIVE'):
        self.db = db_conn
        self.section_id = section_id
        self.warehouse_id = warehouse_id
        self.name = name
        self.capacity = capacity
        self.status = status

    def create(self):
        cursor = self.db.cursor()
        sql = """INSERT INTO storage_sections (warehouse_id, section_name, capacity, status)
                 VALUES (%s, %s, %s, %s)"""
        cursor.execute(sql, (self.warehouse_id, self.name, self.capacity, self.status))
        self.db.commit()
        print(f"✅ Section '{self.name}' created in warehouse {self.warehouse_id}.")

    def update(self, **kwargs):
        cursor = self.db.cursor()
        fields = ", ".join(f"{k}=%s" for k in kwargs.keys())
        values = list(kwargs.values()) + [self.section_id]
        sql = f"UPDATE storage_sections SET {fields} WHERE section_id=%s"
        cursor.execute(sql, values)
        self.db.commit()
        print(f"🔄 Section '{self.section_id}' updated.")

    def delete(self):
        cursor = self.db.cursor()
        cursor.execute("DELETE FROM storage_sections WHERE section_id=%s", (self.section_id,))
        self.db.commit()
        print(f"❌ Section '{self.section_id}' deleted.")

    def list_stock(self):
        cursor = self.db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM stock WHERE section_id=%s", (self.section_id,))
        return cursor.fetchall()

    def __repr__(self):
        return f"<Section {self.name} (Warehouse {self.warehouse_id})>"
