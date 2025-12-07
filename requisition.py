"""Requisition models for material requests."""

from datetime import datetime
from typing import Optional, List


class Requisition:
    """Represents a material requisition request."""
    
    def __init__(
        self,
        requisition_id: Optional[int] = None,
        requester_username: str = "",
        project_id: Optional[int] = None,
        status: str = "PENDING",
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
        submitted_at: Optional[datetime] = None,
        approved_at: Optional[datetime] = None,
        deleted_at: Optional[datetime] = None
    ):
        self.requisition_id = requisition_id
        self.requester_username = requester_username
        self.project_id = project_id
        self.status = status
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at
        self.submitted_at = submitted_at
        self.approved_at = approved_at
        self.deleted_at = deleted_at
        self.items: List[RequisitionItem] = []
    
    def __repr__(self):
        return f"Requisition({self.requisition_id}, {self.status})"


class RequisitionItem:
    """Represents an item within a requisition."""
    
    def __init__(
        self,
        req_item_id: Optional[int] = None,
        requisition_id: Optional[int] = None,
        item_id: Optional[int] = None,
        quantity: int = 0,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.req_item_id = req_item_id
        self.requisition_id = requisition_id
        self.item_id = item_id
        self.quantity = quantity
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at
    
    def __repr__(self):
        return f"RequisitionItem({self.req_item_id}, item={self.item_id}, qty={self.quantity})"
