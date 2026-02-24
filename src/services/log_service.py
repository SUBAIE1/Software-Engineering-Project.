"""Logging service."""

import logging
import sys
from datetime import datetime
from pathlib import Path
from tkinter import messagebox
from mysql.connector import Error
from config.database_connection import DatabaseConnection


def setup_logging(log_file: str = None, level=logging.INFO):
    """Configure logging for the application."""
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    handlers = [logging.StreamHandler(sys.stdout)]
    
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        handlers.append(logging.FileHandler(log_file))
    
    logging.basicConfig(level=level, format=log_format, handlers=handlers)
    return logging.getLogger(__name__)


class LogService:
    """Service for logging user actions."""
    
    def __init__(self, db=None):
        self.db = db or DatabaseConnection()
        self.logger = logging.getLogger(__name__)

    def log_action(self, username, action):
        """Log a user action."""
        timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        try:
            sql = """
                INSERT INTO audit_logs (username, action, action_time)
                VALUES (%s, %s, %s)
            """
            self.db.execute_query(sql, (username, action, timestamp))
            self.logger.info(f"Logged action for {username}: {action}")
        except Error as exc:
            self.logger.error(f"Failed to log action: {exc}")
            messagebox.showerror("Error", str(exc))
    
    def get_user_logs(self, username: str, limit: int = 100):
        """Get audit logs for a user."""
        sql = """
            SELECT log_id, username, action, action_time 
            FROM audit_logs 
            WHERE username = %s 
            ORDER BY action_time DESC 
            LIMIT %s
        """
        try:
            return self.db.fetch_all(sql, (username, limit), dictionary=True)
        except Error as exc:
            self.logger.error(f"Failed to retrieve logs: {exc}")
            return []
    
    def get_all_logs(self, limit: int = 1000):
        """Get all audit logs."""
        sql = """
            SELECT log_id, username, action, action_time 
            FROM audit_logs 
            ORDER BY action_time DESC 
            LIMIT %s
        """
        try:
            return self.db.fetch_all(sql, (limit,), dictionary=True)
        except Error as exc:
            self.logger.error(f"Failed to retrieve all logs: {exc}")
            return []
