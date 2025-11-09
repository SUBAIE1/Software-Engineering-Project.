# PurchaseOrderItems.py
from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import Optional, Dict, Any

from database_connection import get_connection


@dataclass
class PurchaseOrderItem:
    order_item_id: Optional[int]
    order_id: int
    product_id: int
    quantity: int
    unit_price: Decimal

    @property
    def line_total(self) -> Decimal:
        return Decimal(self.quantity) * Decimal(self.unit_price)

    # ---------- Constructors / fetchers ----------
    @staticmethod
    def from_row(row: Dict[str, Any]) -> "PurchaseOrderItem":
        return PurchaseOrderItem(
            order_item_id=row["order_item_id"],
            order_id=row["order_id"],
            product_id=row["product_id"],
            quantity=int(row["quantity"]),
            unit_price=Decimal(row["unit_price"]),
        )

    @staticmethod
    def get(order_item_id: int) -> Optional["PurchaseOrderItem"]:
        sql = """
            SELECT order_item_id, order_id, product_id, quantity, unit_price
            FROM purchase_order_items WHERE order_item_id=%s
        """
        with get_connection() as conn:
            cur = conn.cursor(dictionary=True)
            cur.execute(sql, (order_item_id,))
            row = cur.fetchone()
            cur.close()
        return PurchaseOrderItem.from_row(row) if row else None

    # ---------- Persistence ----------
    def save(self) -> int:
        """Insert or update. Returns order_item_id."""
        if self.quantity <= 0 or Decimal(self.unit_price) < 0:
            raise ValueError("quantity must be > 0 and unit_price >= 0")

        with get_connection() as conn:
            cur = conn.cursor()
            if self.order_item_id is None:
                cur.execute(
                    """
                    INSERT INTO purchase_order_items (order_id, product_id, quantity, unit_price)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (self.order_id, self.product_id, int(self.quantity), str(Decimal(self.unit_price))),
                )
                self.order_item_id = cur.lastrowid
            else:
                cur.execute(
                    """
                    UPDATE purchase_order_items
                    SET order_id=%s, product_id=%s, quantity=%s, unit_price=%s
                    WHERE order_item_id=%s
                    """,
                    (
                        self.order_id,
                        self.product_id,
                        int(self.quantity),
                        str(Decimal(self.unit_price)),
                        self.order_item_id,
                    ),
                )
            # Keep parent order total in sync
            cur.execute(
                """
                UPDATE purchase_orders po
                JOIN (
                    SELECT order_id, COALESCE(SUM(quantity*unit_price),0) AS new_total
                    FROM purchase_order_items
                    WHERE order_id=%s
                ) s ON s.order_id = po.order_id
                SET po.total_amount = s.new_total
                """,
                (self.order_id,),
            )
            conn.commit()
            cur.close()
        return int(self.order_item_id)

    def delete(self):
        if self.order_item_id is None:
            return
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                "DELETE FROM purchase_order_items WHERE order_item_id=%s", (self.order_item_id,)
            )
            # recalc parent total
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
        self.order_item_id = None
