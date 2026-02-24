"""Backward compatibility proxy for services.

This module provides backward compatibility with the old structure.
New code should import from src.services directly.
"""

try:
    from src.services.auth_service import AuthService, AuthResult
    from src.services.log_service import LogService
    __all__ = ['AuthService', 'AuthResult', 'LogService']
except ImportError:
    __all__ = []
