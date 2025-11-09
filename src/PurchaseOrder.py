# PurchaseOrder.py
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, date
from decimal import Decimal
from typing import Optional, List, Dict, Any

from database_connection import get_connection  # must return a mysql.connector (or pymysql) connection


VALID_STATUS = {"PENDING", "APPROVED", "SHIPPED", "DELIVERED", "CANCELLED"}
VALID_TRANSITIONS = {
    "PENDING": {"APPROVED", "CANCELLED"},
    "APPROVED": {"SHIPPED", "CANCELLED"},
    "SHIPPED": {"DELIVERED"},
    "DELIVERED": set(),
    "CANCELLED": set(),
}


@dataclass
class PurchaseOrder:
    order_id: Optional[int]
    supplier_id: int
    created_by_id: int
    order_date: Optional[datetime] = None
    expected_delivery_date: Optional[date] = None
    status: str = "PENDING"
    total_amount: Decimal = Decimal("0.00")

    # ---------- Constructors / fetchers ----------
    @staticmethod
    def from_row(row: Dict[str, Any]) -> "PurchaseOrder":
        return PurchaseOrder(
            order_id=row["order_id"],
            supplier_id=row["supplier_id"],
            created_by_id=row["created_by_id"],
            order_date=row["order_date"],
            expected_delivery_date=row["expected_delivery_date"],
            status=row["status"],
            total_amount=Decimal(row["total_amount"]),
        )

    @staticmethod
    def get(order_id: int) -> Optional["PurchaseOrder"]:
        sql = """
            SELECT order_id, supplier_id, created_by_id, order_date,
                   expected_delivery_date, status, total_amount
            FROM purchase_orders WHERE order_id = %s
        """
        with get_connection() as conn:
            cur = conn.cursor(dictionary=True)
            cur.execute(sql, (order_id,))
            row = cur.fetchone()
            cur.close()
        return PurchaseOrder.from_row(row) if row else None

    @staticmethod
    def list_by_supplier(supplier_id: int) -> List["PurchaseOrder"]:
        sql = """
            SELECT order_id, supplier_id, created_by_id, order_date,
                   expected_delivery_date, status, total_amount
            FROM purchase_orders
            WHERE supplier_id = %s
            ORDER BY order_date DESC, order_id DESC
        """
        with get_connection() as conn:
            cur = conn.cursor(dictionary=True)
            cur.execute(sql, (supplier_id,))
            rows = cur.fetchall()
            cur.close()
        return [PurchaseOrder.from_row(r) for r in rows]

    # ---------- Persistence ----------
    def save(self) -> int:
        """Insert or update. Returns order_id."""
        if self.status not in VALID_STATUS:
            raise ValueError(f"Invalid status: {self.status}")

        with get_connection() as conn:
            cur = conn.cursor()
            if self.order_id is None:
                sql = """
                    INSERT INTO purchase_orders
                        (supplier_id, created_by_id, order_date,
                         expected_delivery_date, status, total_amount)
                    VALUES (%s, %s, NOW(), %s, %s, %s)
                """
                cur.execute(
                    sql,
                    (
                        self.supplier_id,
                        self.created_by_id,
                        self.expected_delivery_date,
                        self.status,
                        str(self.total_amount),
                    ),
                )
                self.order_id = cur.lastrowid
            else:
                sql = """
                    UPDATE purchase_orders
                    SET supplier_id=%s,
                        created_by_id=%s,
                        expected_delivery_date=%s,
                        status=%s,
                        total_amount=%s
                    WHERE order_id=%s
                """
                cur.execute(
                    sql,
                    (
                        self.supplier_id,
                        self.created_by_id,
                        self.expected_delivery_date,
                        self.status,
                        str(self.total_amount),
                        self.order_id,
                    ),
                )
            conn.commit()
            cur.close()

        return int(self.order_id)

    # ---------- Business helpers ----------
    def can_transition_to(self, new_status: str) -> bool:
        if new_status not in VALID_STATUS:
            return False
        current = self.status or "PENDING"
        return new_status in VALID_TRANSITIONS.get(current, set())

    def set_status(self, new_status: str, acting_user_id: Optional[int] = None):
        if not self.can_transition_to(new_status):
            raise ValueError(f"Invalid status transition {self.status} -> {new_status}")

        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                "UPDATE purchase_orders SET status=%s WHERE order_id=%s",
                (new_status, self.order_id),
            )
            # optional audit log
            if acting_user_id:
                cur.execute(
                    "INSERT INTO audit_logs (user_id, action) VALUES (%s, %s)",
                    (acting_user_id, f"PO #{self.order_id} status {self.status} -> {new_status}"),
                )
            conn.commit()
            cur.close()
        self.status = new_status

    def add_item(self, product_id: int, quantity: int, unit_price: Decimal):
        if self.order_id is None:
            raise ValueError("Save the order before adding items.")
        if self.status not in {"PENDING", "APPROVED"}:
            raise ValueError("Items can be added only when order is PENDING or APPROVED.")
        if quantity <= 0 or Decimal(unit_price) < 0:
            raise ValueError("quantity must be > 0 and unit_price >= 0")

        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                """
                INSERT INTO purchase_order_items (order_id, product_id, quantity, unit_price)
                VALUES (%s, %s, %s, %s)
                """,
                (self.order_id, product_id, int(quantity), str(Decimal(unit_price))),
            )
            # update total from DB calc to avoid race
            cur.execute(
                """
                UPDATE purchase_orders po
                JOIN (
                    SELECT order_id, SUM(quantity * unit_price) AS new_total
                    FROM purchase_order_items WHERE order_id=%s
                ) s ON s.order_id = po.order_id
                SET po.total_amount = s.new_total
                WHERE po.order_id=%s
                """,
                (self.order_id, self.order_id),
            )
            conn.commit()
            cur.close()

        # refresh local total
        self.reload_total()

    def remove_item(self, order_item_id: int):
        if self.order_id is None:
            raise ValueError("Order not saved.")
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                "DELETE FROM purchase_order_items WHERE order_item_id=%s AND order_id=%s",
                (order_item_id, self.order_id),
            )
            # recalc total
            cur.execute(
                """
                UPDATE purchase_orders po
                LEFT JOIN (
                    SELECT order_id, COALESCE(SUM(quantity*unit_price),0) AS new_total
                    FROM purchase_order_items WHERE order_id=%s
                ) s ON s.order_id = po.order_id
                SET po.total_amount = COALESCE(s.new_total, 0)
                WHERE po.order_id=%s
                """,
                (self.order_id, self.order_id),
            )
            conn.commit()
            cur.close()
        self.reload_total()

    def reload_total(self):
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                "SELECT total_amount FROM purchase_orders WHERE order_id=%s",
                (self.order_id,),
            )
            (tot,) = cur.fetchone()
            cur.close()
        self.total_amount = Decimal(tot)

    def items(self) -> List[Dict[str, Any]]:
        """Return all items in this order."""
        if self.order_id is None:
            return []
        with get_connection() as conn:
            cur = conn.cursor(dictionary=True)
            cur.execute(
                """
                SELECT order_item_id, order_id, product_id, quantity, unit_price,
                       (quantity*unit_price) AS line_total
                FROM purchase_order_items
                WHERE order_id=%s
                ORDER BY order_item_id
                """,
                (self.order_id,),
            )
            rows = cur.fetchall()
            cur.close()
        return rows

    def delete(self):
        """Deletes the order (items cascade via FK)."""
        if self.order_id is None:
            return
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute("DELETE FROM purchase_orders WHERE order_id=%s", (self.order_id,))
            conn.commit()
            cur.close()
        self.order_id = None
