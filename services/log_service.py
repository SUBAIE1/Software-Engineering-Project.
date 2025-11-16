# logger.py
from datetime import datetime
from tkinter import messagebox
from mysql.connector import Error

from src.users.database_connection import DatabaseConnection


class LogService:
    def __init__(self, db = None):
        self.db = db or DatabaseConnection()



    def log_action(self, username, action):
        timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        try:
            sql = """
                INSERT INTO audit_logs (user_id, action, action_time)
                VALUES (%s, %s, %s)
            """
            DatabaseConnection.execute_query(sql, (username, action, timestamp))
        except Error as exc:
            messagebox.showerror("Error", str(exc))
