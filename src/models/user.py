
# user.py
from abc import ABC, abstractmethod
from datetime import datetime

from connection import DatabaseConnection


class User(ABC):
    def __init__(
        self,
        username,
        password,
        role_id,
        status="ACTIVE",
        failed_attempts=0,
        locked_until=None,
        last_login=None,
        last_logout=None,
        created_at=None,
        db=None,
    ):
        self.username = username
        self.password = password
        self.role_id = role_id  # rolename instead
        self.status = status
        self.failed_attempts = failed_attempts
        self.locked_until = locked_until
        self.last_login = last_login
        self.last_logout = last_logout
        self.created_at = created_at or datetime.utcnow()
        self.db = db or DatabaseConnection()


    def _get_identifier(self):
        """Return the primary key identifier for this user."""
        return self.username

    def login(self):
        self.last_login = datetime.utcnow()
        query = "UPDATE users SET last_login = %s WHERE username = %s"
        self.db.execute_query(query, (self.last_login, self._get_identifier()))
        print(f"[INFO] {self.username} logged in at {self.last_login}")

    def logout(self):
        """Record user logout."""
        self.last_logout = datetime.utcnow()
        query = "UPDATE users SET last_logout = %s WHERE username = %s"
        self.db.execute_query(query, (self.last_logout, self._get_identifier()))
        print(f"[INFO] {self.username} logged out at {self.last_logout}")

    @abstractmethod
    def perform_role_duties(self):
        """Each subclass must define its role-specific behavior."""
        raise NotImplementedError
