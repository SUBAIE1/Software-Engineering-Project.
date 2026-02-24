"""User repository for database operations."""

from typing import Optional, Dict, List
from config.database_connection import DatabaseConnection


class UserRepository:
    """Data access layer for users."""
    
    def __init__(self, db=None):
        self.db = db or DatabaseConnection()
    
    def find_by_username(self, username: str) -> Optional[Dict]:
        """Find a user by username."""
        sql = """
            SELECT u.username, u.password, u.status, u.role_id, 
                   u.failed_attempts, u.locked_until, u.last_login, u.last_logout,
                   r.role_name
            FROM users u
            LEFT JOIN roles r ON u.role_id = r.role_id
            WHERE u.username = %s AND u.deleted_at IS NULL
        """
        return self.db.fetch_one(sql, (username,), dictionary=True)
    
    def find_all(self, include_inactive=False) -> List[Dict]:
        """Get all users."""
        if include_inactive:
            sql = "SELECT * FROM users WHERE deleted_at IS NULL"
        else:
            sql = "SELECT * FROM users WHERE status = 'ACTIVE' AND deleted_at IS NULL"
        return self.db.fetch_all(sql, dictionary=True)
    
    def create(self, username: str, password: str, role_id: int) -> int:
        """Create a new user."""
        sql = """
            INSERT INTO users (username, password, role_id, created_at) 
            VALUES (%s, %s, %s, CURRENT_TIMESTAMP)
        """
        self.db.execute_query(sql, (username, password, role_id))
        return self.db.get_last_insert_id()
    
    def update(self, username: str, updates: Dict) -> int:
        """Update user details."""
        fields = ", ".join(f"{k}=%s" for k in updates.keys())
        values = list(updates.values()) + [username]
        sql = f"UPDATE users SET {fields} WHERE username=%s"
        return self.db.execute_query(sql, values)
    
    def delete(self, username: str) -> int:
        """Soft delete a user."""
        sql = "UPDATE users SET deleted_at = CURRENT_TIMESTAMP WHERE username = %s"
        return self.db.execute_query(sql, (username,))
    
    def deactivate(self, username: str) -> int:
        """Deactivate a user account."""
        sql = "UPDATE users SET status = 'INACTIVE' WHERE username = %s"
        return self.db.execute_query(sql, (username,))
    
    def reactivate(self, username: str) -> int:
        """Reactivate a user account."""
        sql = "UPDATE users SET status = 'ACTIVE' WHERE username = %s"
        return self.db.execute_query(sql, (username,))
    
    def reset_password(self, username: str, new_password: str) -> int:
        """Reset user password."""
        sql = "UPDATE users SET password = %s WHERE username = %s"
        return self.db.execute_query(sql, (new_password, username))
