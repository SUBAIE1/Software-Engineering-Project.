"""Supplier functions."""

from datetime import datetime


def add_supplier(db, name: str, contact: str = "", phone: str = "", email: str = "", address: str = "") -> int:
    """Add supplier record."""
    cur = db.cursor()
    cur.execute(
        "INSERT INTO suppliers (supplier_name, contact_name, phone, email, address, status, created_at) "
        "VALUES (%s,%s,%s,%s,%s,'ACTIVE',%s);",
        (name, contact, phone, email, address, datetime.now())
    )
    db.commit()
    cur.execute("SELECT LAST_INSERT_ID();")
    new_id = cur.fetchone()[0]
    print(f"[SUP] supplier #{new_id} created.")
    return new_id


def list_active_suppliers(db) -> list:
    """List active suppliers."""
    cur = db.cursor(dictionary=True)
    cur.execute("SELECT supplier_id, supplier_name FROM suppliers WHERE status='ACTIVE' ORDER BY supplier_name;")
    rows = cur.fetchall()
    print(f"[SUP] {len(rows)} active suppliers found.")
    return rows
