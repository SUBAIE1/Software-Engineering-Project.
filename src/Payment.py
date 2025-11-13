#Record supplier payment and adjust invoice status ----1----
#List all payments tied to an invoice ----2----
#Calculate supplier’s outstanding vs paid totals ----3----



from datetime import datetime
from decimal import Decimal


#--------------------------- 1 ---------------------------
def record_payment(db, invoice_id: int, amount: float, method: str = "BANK_TRANSFER") -> int:
    cur = db.cursor()
    cur.execute("SELECT total_amount, paid_amount FROM invoices WHERE invoice_id=%s;", (invoice_id,))
    total, paid = [Decimal(x) for x in cur.fetchone()]
    new_paid = paid + Decimal(amount)
    status = "PAID" if new_paid >= total else "PARTIALLY_PAID"
    cur.execute(
        "INSERT INTO payments (invoice_id, payment_date, amount, payment_method) VALUES (%s,%s,%s,%s);",
        (invoice_id, datetime.now(), str(amount), method)
    )
    cur.execute("UPDATE invoices SET paid_amount=%s, status=%s WHERE invoice_id=%s;", (str(new_paid), status, invoice_id))
    db.commit()
    cur.execute("SELECT LAST_INSERT_ID();")
    pay_id = cur.fetchone()[0]
    print(f"[PAY] payment #{pay_id} recorded for invoice #{invoice_id}.")
    return pay_id
    
#--------------------------- 2 ---------------------------
def payments_for_invoice(db, invoice_id: int) -> list[dict]:
    cur = db.cursor(dictionary=True)
    cur.execute("SELECT * FROM payments WHERE invoice_id=%s ORDER BY payment_date DESC;", (invoice_id,))
    return cur.fetchall()

#--------------------------- 3 ---------------------------
def supplier_balance(db, supplier_id: int) -> dict:
    cur = db.cursor(dictionary=True)
    cur.execute(
        "SELECT COALESCE(SUM(total_amount - paid_amount),0) AS outstanding, "
        "COALESCE(SUM(paid_amount),0) AS paid "
        "FROM invoices WHERE supplier_id=%s;", (supplier_id,)
    )
    return cur.fetchone()