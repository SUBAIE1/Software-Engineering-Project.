from dataclasses import dataclass, field, asdict
from datetime import datetime
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from typing import Optional, Dict, Any
import json


# Decimal precision for monetary calculations (2 decimal places)
_DECIMAL_CONTEXT = Decimal('0.01')


def _to_decimal(value) -> Decimal:
	"""
	Convert a value to Decimal with 2 decimal places.
	Handles None, existing Decimals, and numeric types.
	
	Args:
		value: Value to convert (can be int, float, str, Decimal, or None)
		
	Returns:
		Decimal with 2 decimal places, or 0.00 if None
		
	Raises:
		ValueError: If value cannot be converted to Decimal
	"""
	if value is None:
		return Decimal('0.00')
	if isinstance(value, Decimal):
		return value.quantize(_DECIMAL_CONTEXT, rounding=ROUND_HALF_UP)
	try:
		return Decimal(str(value)).quantize(_DECIMAL_CONTEXT, rounding=ROUND_HALF_UP)
	except (InvalidOperation, ValueError, TypeError) as e:
		raise ValueError(f"Invalid decimal value: {value}") from e


@dataclass
class PurchaseOrderItems:
	
	id: Optional[int] = None
	purchase_order_id: Optional[int] = None
	product_id: int = 0
	product_sku: Optional[str] = None
	product_name: Optional[str] = None
	quantity: int = 0
	unit_price: Decimal = field(default_factory=lambda: Decimal('0.00'))
	uom: str = ""
	discount: Decimal = field(default_factory=lambda: Decimal('0.00'))
	tax_rate: Decimal = field(default_factory=lambda: Decimal('0.00'))
	created_at: Optional[datetime] = None
	updated_at: Optional[datetime] = None
	metadata: Dict[str, Any] = field(default_factory=dict)

	def __post_init__(self):
		
		# Normalize all monetary values to consistent 2 decimal places
		# This ensures calculations are accurate and prevents floating-point errors
		self.unit_price = _to_decimal(self.unit_price)
		self.discount = _to_decimal(self.discount)
		self.tax_rate = _to_decimal(self.tax_rate)
		
		# Ensure quantity is always an integer (convert if needed)
		try:
			self.quantity = int(self.quantity)
		except (ValueError, TypeError):
			raise ValueError("quantity must be an integer")
		
		# Set timestamps to now if they weren't provided
		# This happens when creating new items (not loading from DB)
		now = datetime.utcnow()
		if self.created_at is None:
			self.created_at = now
		if self.updated_at is None:
			self.updated_at = now
		
		# Run validation to ensure all values are within acceptable ranges
		self.validate()

	def validate(self) -> None:
		
		if self.quantity < 0:
			raise ValueError("quantity must be >= 0")
		if self.unit_price < Decimal('0.00'):
			raise ValueError("unit_price must be >= 0")
		if self.discount < Decimal('0.00'):
			raise ValueError("discount must be >= 0")
		if self.tax_rate < Decimal('0.00'):
			raise ValueError("tax_rate must be >= 0")
		if self.discount > (self.unit_price * self.quantity):
			raise ValueError("discount cannot exceed line subtotal")

	def subtotal(self) -> Decimal:
		return (self.unit_price * Decimal(self.quantity)).quantize(_DECIMAL_CONTEXT, rounding=ROUND_HALF_UP)

	def total_after_discount(self) -> Decimal:
		subtotal = self.subtotal()
		result = (subtotal - self.discount)
		# Prevent negative totals (discount can't exceed subtotal)
		if result < Decimal('0.00'):
			return Decimal('0.00')
		return result.quantize(_DECIMAL_CONTEXT, rounding=ROUND_HALF_UP)

	def tax_amount(self) -> Decimal:
		# Tax is applied AFTER discount (not on original price)
		taxed = (self.total_after_discount() * self.tax_rate)
		return taxed.quantize(_DECIMAL_CONTEXT, rounding=ROUND_HALF_UP)

	def total(self) -> Decimal:
		
		return (self.total_after_discount() + self.tax_amount()).quantize(_DECIMAL_CONTEXT, rounding=ROUND_HALF_UP)

	def apply_discount_amount(self, amount) -> None:
		
		amount_dec = _to_decimal(amount)
		if amount_dec < Decimal('0.00'):
			raise ValueError("discount amount must be >= 0")
		if amount_dec > self.subtotal():
			raise ValueError("discount cannot exceed line subtotal")
		self.discount = amount_dec
		self.touch()
		self.validate()

	def apply_discount_percent(self, percent) -> None:
		
		# Convert percentage to decimal (e.g., 10% -> 0.10)
		try:
			pct = Decimal(str(percent)) / Decimal('100')
		except (InvalidOperation, TypeError):
			raise ValueError("percent must be numeric")
		
		# Validate percentage is in valid range
		if pct < Decimal('0.00') or pct > Decimal('1.00'):
			raise ValueError("percent must be between 0 and 100")
		
		# Calculate and apply the discount amount
		# Example: $100 subtotal × 10% = $10 discount
		self.discount = (self.subtotal() * pct).quantize(_DECIMAL_CONTEXT, rounding=ROUND_HALF_UP)
		self.touch()  # Update the modified timestamp
		self.validate()  # Ensure discount doesn't exceed subtotal

	def touch(self) -> None:
		self.updated_at = datetime.utcnow()

	def to_dict(self) -> Dict[str, Any]:
		
		d = asdict(self)
		# Convert Decimals to strings (JSON doesn't support Decimal type)
		d['unit_price'] = str(self.unit_price)
		d['discount'] = str(self.discount)
		d['tax_rate'] = str(self.tax_rate)
		# Convert datetimes to ISO 8601 strings (e.g., "2025-11-10T14:30:00")
		d['created_at'] = self.created_at.isoformat() if self.created_at else None
		d['updated_at'] = self.updated_at.isoformat() if self.updated_at else None
		return d

	@classmethod
	def from_dict(cls, data: Dict[str, Any]) -> "PurchaseOrderItems":
		
		# Make a copy to avoid modifying the original data
		kw = dict(data)
		
		# Convert string values back to Decimals
		if 'unit_price' in kw:
			kw['unit_price'] = _to_decimal(kw.get('unit_price'))
		if 'discount' in kw:
			kw['discount'] = _to_decimal(kw.get('discount'))
		if 'tax_rate' in kw:
			kw['tax_rate'] = _to_decimal(kw.get('tax_rate'))
		
		# Ensure quantity is an integer
		if 'quantity' in kw:
			try:
				kw['quantity'] = int(kw.get('quantity', 0))
			except (ValueError, TypeError):
				raise ValueError("quantity must be integer-like")
		
		# Convert ISO datetime strings back to datetime objects
		if 'created_at' in kw and isinstance(kw['created_at'], str):
			kw['created_at'] = datetime.fromisoformat(kw['created_at'])
		if 'updated_at' in kw and isinstance(kw['updated_at'], str):
			kw['updated_at'] = datetime.fromisoformat(kw['updated_at'])
		
		return cls(**kw)

	def to_json(self) -> str:
		return json.dumps(self.to_dict(), ensure_ascii=False)

	@classmethod
	def from_json(cls, payload: str) -> "PurchaseOrderItems":
		data = json.loads(payload)
		return cls.from_dict(data)

	def clone_with(self, **overrides) -> "PurchaseOrderItems":
	
		base = self.to_dict()
		base.update(overrides)
		return PurchaseOrderItems.from_dict(base)

	def __repr__(self) -> str:
		return (f"PurchaseOrderItems(id={self.id!r}, sku={self.product_sku!r}, "
				f"qty={self.quantity}, unit_price={self.unit_price}, total={self.total()})")