from tkinter import messagebox

import mysql.connector
from mysql.connector import Error


class DatabaseConnection:
    

    __instance = None

    def __new__(cls, *args, **kwargs):#single connection per session
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.db_connection = None
            cls.__instance._last_insert_id = None
        return cls.__instance

    def connect(self):
        """Ensure there is an active connection and return it."""

        conn = getattr(self, "db_connection", None)
        if conn is None or not conn.is_connected():
            try:
                self.db_connection = mysql.connector.connect(
                    host="0,0,0,0",#Fill them with your databse configurations
                    port= 0000,
                    user="",
                    password="",
                    database="ims_db",
                    autocommit=False,
                )
                print("Connected successfully to ims_db.")
            except Error as exc:
                messagebox.showerror("Database error", f"Unable to connect: {exc}")
                self.db_connection = None
        return self.db_connection

    def cursor(self, *, dictionary=False):

        connection = self.connect()
        if connection is None:
            raise RuntimeError("Database connection is unavailable.")
        try:
            return connection.cursor(dictionary=dictionary)
        except TypeError:
            # Older connectors may not accept dictionary kwarg
            cursor = connection.cursor()
            
            return cursor

    def close_cursor(self, cursor):
        try:
            if cursor:
                cursor.close()
        except Error as exc:
            messagebox.showerror("Error", str(exc))

    def execute_query(self, sql, params=None, *, commit=True):
        cursor = self.cursor()
        try:
            cursor.execute(sql, params or ())
            if commit and self.db_connection and self.db_connection.is_connected():
                self.db_connection.commit()
            self._last_insert_id = cursor.lastrowid
            return cursor.rowcount
        except Error as exc:
            if self.db_connection and self.db_connection.is_connected():
                self.db_connection.rollback()
            messagebox.showerror("Error", str(exc))
            raise
        finally:
            self.close_cursor(cursor)

    def fetch_all(self, sql, params=None, *, dictionary=False):
        cursor = self.cursor(dictionary=dictionary)
        try:
            cursor.execute(sql, params or ())
            return cursor.fetchall()
        finally:
            self.close_cursor(cursor)

    def fetch_one(self, sql, params=None, *, dictionary=False):
        cursor = self.cursor(dictionary=dictionary)
        try:
            cursor.execute(sql, params or ())
            return cursor.fetchone()
        finally:
            self.close_cursor(cursor)

    def get_last_insert_id(self):
        return self._last_insert_id

    def close_connection(self):
        try:
            if self.db_connection and self.db_connection.is_connected():
                self.db_connection.close()
                messagebox.showinfo("Database connection closed", "Database connection was closed.")
        except Error as exc:
            messagebox.showerror("Error", str(exc))

    def reconnect(self):
        self.close_connection()
        return self.connect()
