from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, date
from decimal import Decimal, ROUND_HALF_UP, InvalidOperation
from typing import List, Optional, Dict, Any

try:
	# Try to import the PurchaseOrderItems class for rich item handling
	# This allows get_items() to return typed objects instead of raw dicts
	from PurchaseOrderItems import PurchaseOrderItems as POItemModel
except Exception:
	# Graceful fallback: if import fails, we'll return raw DB rows instead
	POItemModel = None  # type: ignore


# Decimal precision for monetary calculations (2 decimal places)
# All money values are rounded to cents using this precision
_DEC2 = Decimal("0.01")


def _dec(v) -> Decimal:
	"""
	Convert a value to Decimal with 2 decimal places.
	Used for consistent monetary calculations throughout the class.
	Returns Decimal('0.00') if conversion fails.
	"""
	if isinstance(v, Decimal):
		return v.quantize(_DEC2, rounding=ROUND_HALF_UP)
	try:
		return Decimal(str(v)).quantize(_DEC2, rounding=ROUND_HALF_UP)
	except (InvalidOperation, TypeError, ValueError):
		return Decimal("0.00")


class PurchaseOrder:

	# Valid status values for purchase orders
	ALLOWED_STATUSES = {"PENDING", "APPROVED", "SHIPPED", "DELIVERED", "CANCELLED"}
	
	# This prevents invalid transitions like DELIVERED -> PENDING
	TRANSITIONS = {
		"PENDING": {"APPROVED", "CANCELLED"},      # New orders can be approved or cancelled
		"APPROVED": {"SHIPPED", "CANCELLED"},      # Approved orders can ship or be cancelled
		"SHIPPED": {"DELIVERED"},                  # Shipped orders can only be marked delivered
		"DELIVERED": set(),                        # Terminal state - no further transitions
		"CANCELLED": set(),                        # Terminal state - no further transitions
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
	) -> None:
		"""
		Initialize a PurchaseOrder instance.
		
		Args:
			db: MySQL database connection object
			order_id: Existing order ID (for loaded orders)
			supplier_id: ID of the supplier
			created_by_id: ID of the user creating the order
			order_date: When the order was created (defaults to now)
			expected_delivery_date: Expected delivery date
			status: Order status (defaults to PENDING)
			total_amount: Total order amount (auto-calculated from items)
		"""
		self.db = db
		self.order_id = order_id
		self.supplier_id = supplier_id
		self.created_by_id = created_by_id
		self.order_date = order_date or datetime.utcnow()
		self.expected_delivery_date = expected_delivery_date
		self.status = status if status in self.ALLOWED_STATUSES else "PENDING"
		self.total_amount = _dec(total_amount)

	def create(self) -> int:
		"""
		Create a new purchase order in the database.
		Inserts into purchase_orders table and sets the order_id.
		
		Returns:
			The newly created order_id
		"""
		cursor = self.db.cursor()
		sql = (
			"""
			INSERT INTO purchase_orders
				(supplier_id, created_by_id, order_date, expected_delivery_date, status, total_amount)
			VALUES
				(%s, %s, %s, %s, %s, %s)
			"""
		)
		cursor.execute(
			sql,
			(
				self.supplier_id,
				self.created_by_id,
				self.order_date,
				self.expected_delivery_date,
				self.status,
				str(self.total_amount),  # Convert Decimal to string for MySQL
			),
		)
		self.db.commit()
		
		# Retrieve the auto-generated order_id from MySQL
		cursor.execute("SELECT LAST_INSERT_ID();")
		self.order_id = cursor.fetchone()[0]
		return int(self.order_id)

	@classmethod
	def from_db(cls, db, order_id: int) -> Optional["PurchaseOrder"]:
		"""
		Load an existing purchase order from the database.
		
		Args:
			db: Database connection
			order_id: ID of the order to load
			
		Returns:
			PurchaseOrder instance if found, None otherwise
		"""
		cur = db.cursor(dictionary=True)
		cur.execute("SELECT * FROM purchase_orders WHERE order_id=%s", (order_id,))
		row = cur.fetchone()
		if not row:
			return None
		return cls(
			db=db,
			order_id=row["order_id"],
			supplier_id=row["supplier_id"],
			created_by_id=row["created_by_id"],
			order_date=row["order_date"],
			expected_delivery_date=row.get("expected_delivery_date"),
			status=row["status"],
			total_amount=_dec(row.get("total_amount", 0)),
		)

	@classmethod
	def list_by_status(cls, db, status: str) -> List[Dict[str, Any]]:
		"""
		Retrieve all purchase orders with a specific status.
		
		Args:
			db: Database connection
			status: Status to filter by (must be valid)
			
		Returns:
			List of order dictionaries, ordered by date (newest first)
		"""
		cur = db.cursor(dictionary=True)
		if status not in cls.ALLOWED_STATUSES:
			raise ValueError("invalid status")
		cur.execute(
			"SELECT * FROM purchase_orders WHERE status=%s ORDER BY order_date DESC",
			(status,),
		)
		return list(cur.fetchall() or [])

	def add_item(self, product_id: int, quantity: int, unit_price) -> int:
		"""
		Add a product to this purchase order.
		Automatically recalculates the order total after adding.
		
		Args:
			product_id: ID of the product to add
			quantity: Quantity to order (must be > 0)
			unit_price: Price per unit
			
		Returns:
			The ID of the newly created order item
			
		Raises:
			RuntimeError: If order hasn't been created yet
			ValueError: If quantity is invalid
		"""
		# Validate: order must exist in DB before adding items
		if not self.order_id:
			raise RuntimeError("create or load the purchase order before adding items")
		if quantity <= 0:
			raise ValueError("quantity must be > 0")
		
		# Normalize price to 2 decimal places
		unit_price = _dec(unit_price)
		
		# Insert the item into purchase_order_items table
		cur = self.db.cursor()
		cur.execute(
			"""
			INSERT INTO purchase_order_items (order_id, product_id, quantity, unit_price)
			VALUES (%s, %s, %s, %s)
			""",
			(self.order_id, product_id, int(quantity), str(unit_price)),
		)
		self.db.commit()
		
		# Get the new item's ID
		cur.execute("SELECT LAST_INSERT_ID();")
		item_id = cur.fetchone()[0]
		
		# IMPORTANT: Recalculate total_amount to reflect the new item
		self.recalculate_total()
		
		return int(item_id)

	def get_items(self) -> List[Any]:
		"""
		Retrieve all items in this purchase order.
		
		Returns:
			List of PurchaseOrderItems objects if available,
			otherwise returns raw dictionary rows from database
		"""
		if not self.order_id:
			return []
		
		# Fetch all items from the junction table
		cur = self.db.cursor(dictionary=True)
		cur.execute(
			"SELECT * FROM purchase_order_items WHERE order_id=%s ORDER BY order_item_id",
			(self.order_id,),
		)
		rows = list(cur.fetchall() or [])
		
		# If PurchaseOrderItems class is available, wrap DB rows in typed objects
		# This gives us calculation methods like subtotal(), discount support, etc.
		if POItemModel:
			items: List[Any] = []
			for r in rows:
				items.append(
					POItemModel(
						id=r["order_item_id"],
						purchase_order_id=r["order_id"],
						product_sku=None,  # Not stored in DB, can be enriched later
						product_name=None,  # Not stored in DB, can be enriched later
						quantity=r["quantity"],
						unit_price=_dec(r["unit_price"]),
					)
				)
			return items
		
		# Fallback: return raw database rows as dictionaries
		return rows

	def recalculate_total(self) -> Decimal:
		"""
		Recalculate the total amount from all order items.
		Updates both the instance and the database.
		
		Returns:
			The calculated total amount
		"""
		if not self.order_id:
			return self.total_amount
		
		# Calculate total by summing (quantity × unit_price) for all items
		# COALESCE returns 0 if there are no items (prevents NULL)
		cur = self.db.cursor()
		cur.execute(
			"""
			SELECT COALESCE(SUM(quantity * unit_price), 0)
			FROM purchase_order_items WHERE order_id=%s
			""",
			(self.order_id,),
		)
		total = _dec(cur.fetchone()[0])
		
		# Update both the instance variable and the database
		self.total_amount = total
		cur.execute(
			"UPDATE purchase_orders SET total_amount=%s WHERE order_id=%s",
			(str(total), self.order_id),
		)
		self.db.commit()
		return total

	def change_status(self, new_status: str) -> None:
		"""
		Change the order status following the defined workflow.
		Only valid transitions are allowed (see TRANSITIONS).
		
		Args:
			new_status: The new status to transition to
			
		Raises:
			ValueError: If status is invalid or transition not allowed
		"""
		# Validate that the new status is in our allowed set
		if new_status not in self.ALLOWED_STATUSES:
			raise ValueError("invalid status")
		
		# Check if this transition is permitted by our state machine
		# Example: Can't go from DELIVERED back to PENDING
		allowed = self.TRANSITIONS.get(self.status, set())
		if new_status not in allowed:
			raise ValueError(f"invalid transition {self.status} -> {new_status}")
		
		# Update the status in the database
		cur = self.db.cursor()
		cur.execute(
			"UPDATE purchase_orders SET status=%s WHERE order_id=%s",
			(new_status, self.order_id),
		)
		self.db.commit()
		
		# Update the instance to reflect the new state
		self.status = new_status

	def approve(self) -> None:
		"""Approve a pending purchase order."""
		self.change_status("APPROVED")

	def cancel(self) -> None:
		"""
		Cancel a purchase order.
		Only PENDING or APPROVED orders can be cancelled.
		
		Raises:
			ValueError: If order cannot be cancelled in current state
		"""
		if self.status not in {"PENDING", "APPROVED"}:
			raise ValueError("can only cancel PENDING or APPROVED orders")
		cur = self.db.cursor()
		cur.execute(
			"UPDATE purchase_orders SET status='CANCELLED' WHERE order_id=%s",
			(self.order_id,),
		)
		self.db.commit()
		self.status = "CANCELLED"

	def set_expected_delivery(self, when: date | str | None) -> None:
		"""
		Set or update the expected delivery date.
		
		Args:
			when: Date object, ISO date string, or None to clear
		"""
		if isinstance(when, str):
			when = date.fromisoformat(when)
		cur = self.db.cursor()
		cur.execute(
			"UPDATE purchase_orders SET expected_delivery_date=%s WHERE order_id=%s",
			(when, self.order_id),
		)
		self.db.commit()
		self.expected_delivery_date = when

	def to_dict(self) -> Dict[str, Any]:
		"""
		Convert the purchase order to a dictionary.
		Useful for JSON serialization and API responses.
		
		Returns:
			Dictionary with all order fields
		"""
		return {
			"order_id": self.order_id,
			"supplier_id": self.supplier_id,
			"created_by_id": self.created_by_id,
			"order_date": self.order_date.isoformat() if self.order_date else None,
			"expected_delivery_date": self.expected_delivery_date.isoformat() if self.expected_delivery_date else None,
			"status": self.status,
			"total_amount": str(self.total_amount),
		}


__all__ = ["PurchaseOrder"]

