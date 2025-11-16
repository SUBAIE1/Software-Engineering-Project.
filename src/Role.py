from datetime import datetime
from tkinter import messagebox

from mysql.connector import Error
from src.users.database_connection import DatabaseConnection
now = datetime.now()
formatted = now.strftime("%Y, %m, %d, %H, %M, %S")


class Role:
    

    def __init__(self , role_name , description= None, created_at=None , role_id = None , db=None ):
        self.role_name = role_name
        self.description = description or "No description provided."
        self.created_at = formatted
        self.role_id = role_id
        self.db = DatabaseConnection()


    def display_role_info(self) :

        print("\n--- Role Info ---")
        print(f"ID          : {self.role_id if self.role_id else 'Not assigned yet'}")
        print(f"Name        : {self.role_name}")
        print(f"Description : {self.description}")
        print(f"Created     : {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}")

    @staticmethod
    def create_role(self , db, role_name, description=None):
        try:

            sql = "INSERT INTO roles (role_name, description) VALUES (%s, %s)"
            self.db.execute_query(sql, (self.role_name, description))
            print(f"Role {self.role_name} is created successfully")

        except Error as e:
            messagebox.showerror("Error" , e)


    @staticmethod
    def get_all_roles(self , db):
        try:

            sql = "SELECT role_id, role_name, description, created_at FROM roles ORDER BY role_id;"
            self.db.fetch_all(sql)
            print("\n--- Roles in System ---")


        except Error as e:
            messagebox.showerror("Error" , e)


    @staticmethod
    def get_role_by_id(self , db, role_id):
        
        try:

            self.db.execute_query(f"SELECT * FROM roles WHERE role_id = {role_id}")
            # if not role:
            #     print(f"[WARN] No role found with ID {role_id}.")
        except Error as e:
            messagebox.showerror("Error" , e)
            return None

    @staticmethod
    def update_role(self, db, role_id, updates: dict) :
       
        try:
            cursor = db.cursor()
            fields = ", ".join(f"{k}=%s" for k in updates.keys())
            values = list(updates.values()) + [role_id]
            sql = f"UPDATE roles SET {fields} WHERE role_id=%s"

            cursor.execute(sql, values)
            db.commit()

            print("role updated successfully ")

        except Error as e:
            db.rollback()
            messagebox.showerror("Error" , e)

    @staticmethod
    def delete_role(self , db, role_id):
       
        try:
            self.db.execute_query(f"DELETE FROM roles WHERE role_id = {role_id}")
        except Error as e:
            db.rollback()
            print(f"[ERROR] Failed to delete role ID {role_id}: {e}")


