#from models.user import User
from datetime import datetime

class Cashier(User):
    """
    Cashier user handles orders, invoices, and  payments.
    """

    def display_menu(self):
        print("\n===== CASHIER MENU =====")
        print("1. Create New Order")
        print("2. Add Order Item")
        print("3. Process Payment")
        print("4. Print Invoice")
        print("5. Logout")

    
    def create_order(self, db, customer_id, status="Pending"):
        cursor = db.cursor()
        sql = "INSERT INTO orders (customer_id, date, status) VALUES (%s, %s, %s)"
        cursor.execute(sql, (customer_id, datetime.now(), status))
        db.commit()
        print(f"[CASHIER] Created order for customer ID {customer_id}.")

    def add_order_item(self, db, order_id, product_id, quantity, price):
        cursor = db.cursor()
        sql = "INSERT INTO order_items (order_id, product_id, quantity, price) VALUES (%s,%s,%s,%s)"
        cursor.execute(sql, (order_id, product_id, quantity, price))
        db.commit()
        print(f"[CASHIER] Added product {product_id} (x{quantity}) to order #{order_id}.")

    def process_payment(self, db, invoice_id, amount, method):
        cursor = db.cursor()
        sql = "INSERT INTO payments (invoice_id, method, amount) VALUES (%s,%s,%s)"
        cursor.execute(sql, (invoice_id, method, amount))
        db.commit()
        print(f"[CASHIER] Processed payment of {amount} via {method} for invoice #{invoice_id}.")

    def print_invoice(self, db, order_id):
        cursor = db.cursor()
        sql = "SELECT invoices.invoice_id, invoices.total, invoices.date FROM invoices WHERE order_id = %s"
        cursor.execute(sql, (order_id,))
        invoice = cursor.fetchone()
        if invoice:
            print(f"--- Invoice #{invoice[0]} ---")
            print(f"Total: {invoice[1]} SAR | Date: {invoice[2]}")
        else:
            print("No invoice found for this order.")
