"""Product model for inventory items."""

from datetime import datetime
from typing import Optional


class Product:
    """Represents a product in the inventory system."""
    
    def __init__(
        self,
        product_id: Optional[int] = None,
        product_name: str = "",
        category_id: Optional[int] = None,
        price: float = 0.0,
        quantity: int = 0,
        uom: str = "",
        status: str = "AVAILABLE",
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
        deleted_at: Optional[datetime] = None
    ):
        self.product_id = product_id
        self.product_name = product_name
        self.category_id = category_id
        self.price = price
        self.quantity = quantity
        self.uom = uom
        self.status = status
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at
        self.deleted_at = deleted_at
    
    def __repr__(self):
        return f"Product({self.product_id}, {self.product_name}, qty={self.quantity})"
