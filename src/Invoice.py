#Build an invoice from a delivered purchase order ----1----
#Return invoice totals and remaining balance ----2----


from datetime import date
from decimal import Decimal


#------------------------------- 1 -------------------------------
def create_invoice_from_po(db, po_id: int, invoice_no: str, inv_date: date, due_date: date | None = None) -> int:
    cur = db.cursor()
    cur.execute("SELECT supplier_id FROM purchase_orders WHERE order_id=%s;", (po_id,))
    supplier_id = cur.fetchone()[0]
    cur.execute("SELECT COALESCE(SUM(quantity*unit_price),0) FROM purchase_order_items WHERE order_id=%s;", (po_id,))
    total = Decimal(cur.fetchone()[0] or 0)
    cur.execute(
        "INSERT INTO invoices (order_id, supplier_id, invoice_number, invoice_date, due_date, total_amount, paid_amount, status) "
        "VALUES (%s,%s,%s,%s,%s,%s,0.0,'UNPAID');",
        (po_id, supplier_id, invoice_no, inv_date, due_date, str(total))
    )
    db.commit()
    cur.execute("SELECT LAST_INSERT_ID();")
    inv_id = cur.fetchone()[0]
    print(f"[INV] invoice #{inv_id} created for PO #{po_id}.")
    return inv_id
    
    
    
#------------------------------- 2 -------------------------------
def get_invoice_with_balance(db, invoice_id: int) -> dict | None:
    # Return invoice totals and remaining balance
    cur = db.cursor(dictionary=True)
    cur.execute("SELECT invoice_id, supplier_id, total_amount, paid_amount, status FROM invoices WHERE invoice_id=%s;", (invoice_id,))
    inv = cur.fetchone()
    if not inv:
        print("[INV] invoice not found.")
        return None
    cur.execute("SELECT COALESCE(SUM(amount),0) FROM payments WHERE invoice_id=%s;", (invoice_id,))
    paid_now = cur.fetchone()[0]
    inv["remaining"] = float(inv["total_amount"]) - float(paid_now)
    print(f"[INV] invoice #{invoice_id} has {inv['remaining']} remaining.")
    return inv