"""Input validation utilities."""

import re
from typing import Optional


def validate_email(email: str) -> bool:
    """
    Validate email format.
    
    Args:
        email: Email address to validate
    
    Returns:
        True if valid, False otherwise
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_phone(phone: str) -> bool:
    """
    Validate phone number format (basic validation).
    
    Args:
        phone: Phone number to validate
    
    Returns:
        True if valid, False otherwise
    """
    # Remove common separators
    cleaned = re.sub(r'[\s\-\(\)]', '', phone)
    # Check if it's numeric and has reasonable length
    return cleaned.isdigit() and 7 <= len(cleaned) <= 15


def validate_sku(sku: str) -> bool:
    """
    Validate SKU format.
    
    Args:
        sku: SKU to validate
    
    Returns:
        True if valid, False otherwise
    """
    # SKU should be alphanumeric with optional hyphens
    pattern = r'^[A-Z0-9\-]{3,20}$'
    return bool(re.match(pattern, sku.upper()))


def validate_quantity(quantity: any) -> bool:
    """
    Validate that quantity is a positive integer.
    
    Args:
        quantity: Quantity to validate
    
    Returns:
        True if valid, False otherwise
    """
    try:
        qty = int(quantity)
        return qty > 0
    except (ValueError, TypeError):
        return False


def validate_price(price: any) -> bool:
    """
    Validate that price is a positive number.
    
    Args:
        price: Price to validate
    
    Returns:
        True if valid, False otherwise
    """
    try:
        p = float(price)
        return p >= 0
    except (ValueError, TypeError):
        return False


def validate_username(username: str, min_length: int = 3, max_length: int = 50) -> Optional[str]:
    """
    Validate username format.
    
    Args:
        username: Username to validate
        min_length: Minimum length
        max_length: Maximum length
    
    Returns:
        None if valid, error message otherwise
    """
    if not username:
        return "Username is required"
    
    if len(username) < min_length:
        return f"Username must be at least {min_length} characters"
    
    if len(username) > max_length:
        return f"Username must be at most {max_length} characters"
    
    # Username should contain only alphanumeric characters and underscores
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        return "Username can only contain letters, numbers, and underscores"
    
    return None


def validate_password(password: str, min_length: int = 6) -> Optional[str]:
    """
    Validate password strength.
    
    Args:
        password: Password to validate
        min_length: Minimum length
    
    Returns:
        None if valid, error message otherwise
    """
    if not password:
        return "Password is required"
    
    if len(password) < min_length:
        return f"Password must be at least {min_length} characters"
    
    # Optional: Check for complexity requirements
    # if not any(c.isupper() for c in password):
    #     return "Password must contain at least one uppercase letter"
    
    # if not any(c.isdigit() for c in password):
    #     return "Password must contain at least one digit"
    
    return None


def sanitize_input(text: str) -> str:
    """
    Sanitize user input to prevent injection attacks.
    
    Args:
        text: Input text to sanitize
    
    Returns:
        Sanitized text
    """
    # Remove potentially dangerous characters
    # This is a basic implementation - consider using a proper library for production
    dangerous_chars = ['<', '>', '"', "'", '\\', ';', '--']
    sanitized = text
    for char in dangerous_chars:
        sanitized = sanitized.replace(char, '')
    return sanitized.strip()
