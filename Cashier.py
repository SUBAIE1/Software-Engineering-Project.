#reduce product quantity and record the sale ====== 1
#show all products available for sale ============= 2
#create a neat text receipt for the sold items ==== 3
#quick sanity check for product id and quantity === 4
#unified way to get a database cursor ============= 5

from datetime import datetime



# ======================= 1 =======================
def process_sale(db, product_id: int, quantity: int, cashier_id: int):
    cur = db.cursor()
    cur.execute("SELECT quantity FROM products WHERE product_id=%s;", (product_id,))
    stock = cur.fetchone()
    if not stock or stock[0] < quantity:
        print("Not enough stock.")
        return False
    cur.execute("UPDATE products SET quantity = quantity - %s WHERE product_id = %s;", (quantity, product_id))
    cur.execute("INSERT INTO sales (product_id, quantity, cashier_id, created_at) VALUES (%s,%s,%s,%s);",
                (product_id, quantity, cashier_id, datetime.now()))
    db.commit()
    print("Sale processed successfully.")
    return True
