"""Inventory Management System package.

Main entry point for the application. Provides access to all core functionality.

Usage:
    from src.models import Product
    from src.repositories import ProductRepository
    from src.services import InventoryService
    from src.utils import validators
"""

__version__ = "1.0.0"
__author__ = "Engineering Team"
__all__ = [
    'models',
    'repositories',
    'services',
    'utils',
    'purchase_orders',
]
