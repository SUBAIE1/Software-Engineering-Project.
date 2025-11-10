from datetime import datetime

class Stock:
    def __init__(self, db_conn, stock_id=None, stock_name=None, section_id=None, warehouse_id=None, product_id=None, status='AVAILABLE'):
        self.db = db_conn
        self.stock_id = stock_id
        self.stock_name = stock_name
        self.section_id = section_id
        self.warehouse_id = warehouse_id
        self.product_id = product_id
        self.status = status

    def create(self):
        cursor = self.db.cursor()
        sql = """INSERT INTO stock (stock_name, section_id, warehouse_id, product_id, status)
                 VALUES (%s, %s, %s, %s, %s)"""
        cursor.execute(sql, (self.stock_name, self.section_id, self.warehouse_id, self.product_id, self.status))
        self.db.commit()
        print(f"✅ Stock '{self.stock_name}' created successfully.")

    def update(self, **kwargs):
        cursor = self.db.cursor()
        fields = ", ".join(f"{k}=%s" for k in kwargs.keys())
        values = list(kwargs.values()) + [self.stock_id]
        sql = f"UPDATE stock SET {fields} WHERE stock_id=%s"
        cursor.execute(sql, values)
        self.db.commit()
        print(f"🔄 Stock '{self.stock_id}' updated.")

    def delete(self):
        cursor = self.db.cursor()
        cursor.execute("DELETE FROM stock WHERE stock_id=%s", (self.stock_id,))
        self.db.commit()
        print(f"❌ Stock '{self.stock_id}' deleted.")

    def get_stock_details(self):
        cursor = self.db.cursor(dictionary=True)
        cursor.execute("""
            SELECT s.*, p.product_name, w.warehouse_name, ss.section_name
            FROM stock s
            JOIN products p ON s.product_id = p.product_id
            JOIN warehouses w ON s.warehouse_id = w.warehouse_id
            JOIN storage_sections ss ON s.section_id = ss.section_id
            WHERE s.stock_id = %s
        """, (self.stock_id,))
        return cursor.fetchone()

    def __repr__(self):
        return f"<Stock {self.stock_name} (Product {self.product_id})>"
