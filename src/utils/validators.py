"""Input validation utilities."""

import re
from typing import Optional


def validate_email(email: str) -> bool:
    """Validate email format."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_phone(phone: str) -> bool:
    """Validate phone number."""
    cleaned = re.sub(r'[\s\-\(\)]', '', phone)
    return cleaned.isdigit() and 7 <= len(cleaned) <= 15


def validate_sku(sku: str) -> bool:
    """Validate SKU format."""
    pattern = r'^[A-Z0-9\-]{3,20}$'
    return bool(re.match(pattern, sku.upper()))


def validate_quantity(quantity: any) -> bool:
    """Validate quantity is positive integer."""
    try:
        qty = int(quantity)
        return qty > 0
    except (ValueError, TypeError):
        return False


def validate_price(price: any) -> bool:
    """Validate price is positive number."""
    try:
        p = float(price)
        return p >= 0
    except (ValueError, TypeError):
        return False


def validate_username(username: str, min_length: int = 3, max_length: int = 50) -> Optional[str]:
    """Validate username."""
    if not username:
        return "Username is required"
    if len(username) < min_length:
        return f"Username must be at least {min_length} characters"
    if len(username) > max_length:
        return f"Username must be at most {max_length} characters"
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        return "Username can only contain letters, numbers, and underscores"
    return None


def validate_password(password: str, min_length: int = 6) -> Optional[str]:
    """Validate password strength."""
    if not password:
        return "Password is required"
    if len(password) < min_length:
        return f"Password must be at least {min_length} characters"
    return None


def sanitize_input(text: str) -> str:
    """Sanitize user input."""
    dangerous_chars = ['<', '>', '"', "'", '\\', ';', '--']
    sanitized = text
    for char in dangerous_chars:
        sanitized = sanitized.replace(char, '')
    return sanitized.strip()
