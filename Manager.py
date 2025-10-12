from user import User


class InventoryManager(User):

    def add_warehouse(self, db, warehouse_id, warehouse_name, warehouse_location, manager_id, capacity, status):
        cursor = db.cursor()

        sql = "INSERT INTO warehouse VALUES (%s, %s, %s, %s, %s, %s)"

        cursor.execute(sql, (warehouse_id, warehouse_name, warehouse_location, manager_id, capacity, status))
        cursor.commit()
        print()

    def delete_warehouse(self, db, warehouse_id):
        cursor = db.cursor()
        sql = f"DELETE FROM warehouses WHERE warehouse_id=%s"
        cursor.execute(sql, [warehouse_id])
        db.commit()
        print()

    def update_warehouse(self, db, warehouse_id, updates: dict):
        cursor = db.cursor()
        fields = ", ".join(f"{k}=%s" for k in updates.keys())
        values = list(updates.values()) + [warehouse_id]
        sql = f"UPDATE warehouses SET {fields} WHERE warehouse_id=%s"

        cursor.execute(sql, values)
        db.commit()

        print()

    def deactivate_warehouse(self, db, warehouse_id):

        cursor = db.cursor()

        sql = "UPDATE warehouses SET status='INACTIVE' WHERE warehouse_id=%s"

        cursor.execute(sql, (warehouse_id)) 
        cursor.commit()
        print()

    def reactivate_warehouse(self, db, warehouse_id):
        cursor = db.cursor()
        sql = "UPDATE warehouses SET status='ACTIVE' WHERE warehouse_id=%s"
        cursor.execute(sql, (warehouse_id))
        print()

    def review_all_warehouses(self, db):
        cursor = db.cursor()
        sql = "SELECT * FROM warehouses"
        cursor.execute(sql)
        rows = cursor.fetchall()
        for row in rows:
            print(row)

    def assign_manager_to_warehouse(self, db, old_manager_id, new_manager_id):
        cursor = db.cursor()

        sql = "UPDATE warehouses SET manager_id=%s WHERE manager_id=%s"
        cursor.execute(sql, (old_manager_id, new_manager_id))
        cursor.commit()
        print()

    ###################################################################################################################################################################################################

    def add_storage_section(self, db, section_id, warehouse_id, section_name, status):
        cursor = db.cursor()

        sql = "INSERT INTO storage_sections VALUES (%s, %s, %s, %s, %s)"

        cursor.execute(sql, (section_id, warehouse_id, section_name, status))
        cursor.commit()
        print()

    def delete_storage_section(self, db, section_id):
        cursor = db.cursor()
        sql = f"DELETE FROM storage_sections WHERE section_id=%s"
        cursor.execute(sql, (section_id))
        db.commit()
        print()

    def update_storage_section(self, db, section_id, updates: dict):
        cursor = db.cursor()
        fields = ", ".join(f"{k}=%s" for k in updates.keys())
        values = list(updates.values()) + [section_id]
        sql = f"UPDATE storage_sections SET {fields} WHERE section_id=%s"

        cursor.execute(sql, values)
        db.commit()

        print()

    def deactivate_storage_section(self, db, section_id):

        cursor = db.cursor()

        sql = "UPDATE storage_sections SET status='INACTIVE' WHERE section_id=%s"

        cursor.execute(sql, (section_id))
        cursor.commit()
        print()

    def reactivate_storage_section(self, db, section_id):
        cursor = db.cursor()
        sql = "UPDATE storage_sections SET status='ACTIVE' WHERE section_id=%s"
        cursor.execute(sql, (section_id))
        print()

    def review_all_storage_section(self, db):
        cursor = db.cursor()
        sql = "SELECT * FROM storage_sections"
        cursor.execute(sql)
        rows = cursor.fetchall()
        for row in rows:
            print(row)

    ###################################################################################################################################################################################################

    def add_stock(self, db, stock_id, warehouse_id, section_id, stock_name, product_id, quantity, status):

        cursor = db.cursor()
        sql = "INSERT INTO stocks VALUES (%s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, (stock_id, warehouse_id, section_id, stock_name, product_id, quantity, status))
        db.commit()
        print()
    
    def delete_stock(self, db, stock_id):
        cursor = db.cursor()
        sql = f"DELETE FROM stocks WHERE stock_id=%s"
        cursor.execute(sql, (stock_id))
        db.commit()
        print()
    
    def update_stock(self, db, stock_id, updates: dict):
        cursor = db.cursor()
        fields = ", ".join(f"{k}=%s" for k in updates.keys())
        values = list(updates.values()) + [stock_id]
        sql = f"UPDATE stock SET {fields} WHERE stock_id=%s"

        cursor.execute(sql, values)
        db.commit()

        print()
    
    def deactivate_stock(self, db, stock_id):
        cursor = db.cursor()
        sql = "UPDATE stocks SET status='INACTIVE' WHERE stock_id=%s"
        cursor.execute(sql, (stock_id))
        cursor.commit()
        print()
    
    def reactivate_stock(self, db, stock_id):
        cursor = db.cursor()
        sql = "UPDATE stocks SET status='ACTIVE' WHERE stock_id=%s"
        cursor.execute(sql, (stock_id))
        cursor.commit()
        print()
    
    def review_all_stocks(self, db):
        cursor = db.cursor()
        sql = "SELECT * FROM stocks"
        cursor.execute(sql)
        rows = cursor.fetchall()
        for row in rows:
            print(row)

###################################################################################################################################################################################################
