"""Password hashing utilities."""

import hashlib
import secrets
from typing import Tuple


def hash_password(password: str, salt: str = None) -> Tuple[str, str]:
    """
    Hash a password with a salt.
    
    Args:
        password: Plain text password
        salt: Optional salt (generated if not provided)
    
    Returns:
        Tuple of (hashed_password, salt)
    """
    if salt is None:
        salt = secrets.token_hex(16)
    
    # Combine password and salt
    pwd_salt = f"{password}{salt}".encode('utf-8')
    
    # Hash using SHA-256
    hashed = hashlib.sha256(pwd_salt).hexdigest()
    
    return hashed, salt


def verify_password(password: str, hashed_password: str, salt: str) -> bool:
    """
    Verify a password against its hash.
    
    Args:
        password: Plain text password to verify
        hashed_password: Stored hash
        salt: Salt used during hashing
    
    Returns:
        True if password matches, False otherwise
    """
    new_hash, _ = hash_password(password, salt)
    return new_hash == hashed_password


def generate_secure_password(length: int = 12) -> str:
    """
    Generate a secure random password.
    
    Args:
        length: Length of the password
    
    Returns:
        Randomly generated password
    """
    import string
    alphabet = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(alphabet) for _ in range(length))
