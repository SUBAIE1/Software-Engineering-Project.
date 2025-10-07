#from models.user import User

class Manager(User):
    """
    Manager user can see wherhouses inventory, suppliers, and purchase orders.
    """

    def display_menu(self):
        print("\n===== MANAGER MENU =====")
        print("1. Manage Inventory")
        print("2. Manage Suppliers")
        print("3. Approve Purchase Orders")
        print("4. View Reports")
        print("5. Logout")

    
    def add_product(self, db, name, description, price, quantity, category_id):
        cursor = db.cursor()
        sql = "INSERT INTO products (name, description, price, quantity, category_id) VALUES (%s,%s,%s,%s,%s)"
        cursor.execute(sql, (name, description, price, quantity, category_id))
        db.commit()
        print(f"[MANAGER] Added product '{name}' successfully.")

    def update_stock(self, db, product_id, quantity):
        cursor = db.cursor()
        sql = "UPDATE products SET quantity = %s WHERE product_id = %s"
        cursor.execute(sql, (quantity, product_id))
        db.commit()
        print(f"[MANAGER] Updated stock of product ID {product_id} to {quantity}.")

    def approve_purchase_order(self, db, purchase_order_id):
        cursor = db.cursor()
        sql = "UPDATE purchase_orders SET status = 'Approved' WHERE purchase_order_id = %s"
        cursor.execute(sql, (purchase_order_id,))
        db.commit()
        print(f"[MANAGER] Approved purchase order #{purchase_order_id}.")

    def generate_inventory_report(self, db):
        cursor = db.cursor()
        cursor.execute("SELECT name, quantity, price FROM products ORDER BY quantity ASC;")
        print("--- Inventory Report ---")
        for row in cursor.fetchall():
            print(f"Product: {row[0]}, Qty: {row[1]}, Price: {row[2]}")
