"""Purchase order model."""

from decimal import Decimal, ROUND_HALF_UP, InvalidOperation
from typing import List, Optional, Dict, Any
from datetime import datetime, date


_DEC2 = Decimal("0.01")


def _dec(v) -> Decimal:
    """Convert value to Decimal."""
    if isinstance(v, Decimal):
        return v.quantize(_DEC2, rounding=ROUND_HALF_UP)
    try:
        return Decimal(str(v)).quantize(_DEC2, rounding=ROUND_HALF_UP)
    except (InvalidOperation, TypeError, ValueError):
        return Decimal("0.00")


class PurchaseOrder:
    """Purchase order class."""
    
    ALLOWED_STATUSES = {"PENDING", "APPROVED", "SHIPPED", "DELIVERED", "CANCELLED"}
    TRANSITIONS = {
        "PENDING": {"APPROVED", "CANCELLED"},
        "APPROVED": {"SHIPPED", "CANCELLED"},
        "SHIPPED": {"DELIVERED"},
        "DELIVERED": set(),
        "CANCELLED": set(),
    }

    def __init__(
        self,
        db,
        order_id: Optional[int] = None,
        supplier_id: Optional[int] = None,
        created_by_id: Optional[int] = None,
        order_date: Optional[datetime] = None,
        expected_delivery_date: Optional[date] = None,
        status: str = "PENDING",
        total_amount: Decimal = Decimal("0.00"),
    ):
        self.db = db
        self.order_id = order_id
        self.supplier_id = supplier_id
        self.created_by_id = created_by_id
        self.order_date = order_date or datetime.utcnow()
        self.expected_delivery_date = expected_delivery_date
        self.status = status if status in self.ALLOWED_STATUSES else "PENDING"
        self.total_amount = _dec(total_amount)

    def create(self) -> int:
        """Create purchase order."""
        cursor = self.db.cursor()
        sql = """
            INSERT INTO purchase_orders
            (supplier_id, created_by_id, order_date, expected_delivery_date, status, total_amount)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (self.supplier_id, self.created_by_id, self.order_date,
                            self.expected_delivery_date, self.status, str(self.total_amount)))
        self.db.commit()
        
        cursor.execute("SELECT LAST_INSERT_ID();")
        self.order_id = cursor.fetchone()[0]
        return int(self.order_id)

    def approve(self) -> None:
        """Approve purchase order."""
        self.change_status("APPROVED")

    def cancel(self) -> None:
        """Cancel purchase order."""
        if self.status not in {"PENDING", "APPROVED"}:
            raise ValueError("can only cancel PENDING or APPROVED orders")
        cur = self.db.cursor()
        cur.execute("UPDATE purchase_orders SET status='CANCELLED' WHERE order_id=%s", (self.order_id,))
        self.db.commit()
        self.status = "CANCELLED"

    def change_status(self, new_status: str) -> None:
        """Change purchase order status."""
        if new_status not in self.ALLOWED_STATUSES:
            raise ValueError("invalid status")
        allowed = self.TRANSITIONS.get(self.status, set())
        if new_status not in allowed:
            raise ValueError(f"invalid transition {self.status} -> {new_status}")
        
        cur = self.db.cursor()
        cur.execute("UPDATE purchase_orders SET status=%s WHERE order_id=%s", (new_status, self.order_id))
        self.db.commit()
        self.status = new_status

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "order_id": self.order_id,
            "supplier_id": self.supplier_id,
            "created_by_id": self.created_by_id,
            "order_date": self.order_date.isoformat() if self.order_date else None,
            "expected_delivery_date": self.expected_delivery_date.isoformat() if self.expected_delivery_date else None,
            "status": self.status,
            "total_amount": str(self.total_amount),
        }
