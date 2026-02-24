"""Password hashing utilities."""

import hashlib
import secrets
from typing import Tuple


def hash_password(password: str, salt: str = None) -> Tuple[str, str]:
    """Hash password with salt."""
    if salt is None:
        salt = secrets.token_hex(16)
    
    pwd_salt = f"{password}{salt}".encode('utf-8')
    hashed = hashlib.sha256(pwd_salt).hexdigest()
    
    return hashed, salt


def verify_password(password: str, hashed_password: str, salt: str) -> bool:
    """Verify password against hash."""
    new_hash, _ = hash_password(password, salt)
    return new_hash == hashed_password


def generate_secure_password(length: int = 12) -> str:
    """Generate secure random password."""
    import string
    alphabet = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(alphabet) for _ in range(length))
