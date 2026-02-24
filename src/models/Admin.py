from tkinter import messagebox  

from src.users.base_page import BasePage  
from src.users.user import User  
from src.users.log_service import LogService 
import mysql.connector  
from src.users.database_connection import DatabaseConnection 
import datetime 

now = datetime.now() 
formatted = now.strftime("%Y, %m, %d, %H, %M, %S")  

class Admin(User): 


    def __init__(self, username, password, role_id, status='ACTIVE', failed_attempts=0,  
                 locked_until=None, last_login=None, last_logout=None, created_at=formatted, db=None):  
        super().__init__( 
            username=username, 
            password=password, 
            role_id=role_id, 
            status=status,  
            db=DatabaseConnection() 
        )  






    def create_user(self , db , username , password, role_id ):  

        try:  
            self.db.execute_query("INSERT INTO users (username ,password, role_id, last_login, created_at) VALUES (%s, %s, %s, %s, %s);", (username , password, role_id, datetime.utcnow(), datetime.utcnow()))  

            print(f"User {self.username} , and password {self.password} is created successfully and assigned to {self.rolename} role")  
            self.logger.log_action(self.user_id, f"Created new user '{username}' with role_id {role_id}")  

        except Exception as e:  
            messagebox.showerror("Error", str(e))  


    def delete_user(self , db ,  username ):  

        try:  
            self.db.execute_query("DELETE FROM users WHERE username = %s", (username,))  
            print( f"User {username} is deleted successfully")  

        except Exception as e:  
            messagebox.showerror("Error", str(e))  


    def update_user(self, db, username, updates: dict):  

        cursor = None  
        try:  
            fields = ", ".join(f"{k}=%s" for k in updates.keys())  
            values = list(updates.values()) + [username]  
            sql = f"UPDATE users SET {fields} WHERE username=%s"  
            cursor = db.cursor()  
            cursor.execute(sql, values)  
            db.commit()  
            print(f"[ADMIN] Updated user {username} with fields {list(updates.keys())}")  

        except Exception as e:  
            messagebox.showerror("Error", str(e))  
        finally:  
            try:  
                if cursor:  
                    cursor.close()  
            except Exception:  
                pass  

    def reset_password(self , db, username, password):  
        try:  
            self.db.execute_query("UPDATE users SET password = %s WHERE username = %s" ,(password, username))  
            print(f"Password of user {self.username}  has been reset to {self.password} successfully")  
        except Exception as e:  
            print(f"[ERROR][reset_password] {e}")  

    def update_role(self , db , username, role_id):  
        try:  
            self.db.execute_query("UPDATE roles SET role_id=%s WHERE username=%s" ,(role_id,username) )  

            print(f"[ADMIN] Updated role {role_id} for user {self.username} .")  
        except Exception as e:  
            print(f"[ERROR][update_role] {e}")  


    def reactviate_user(self , db, username):  

        try:  
            self.db.execute_query("UPDATE users SET status = 'ACTIVE' WHERE username = %s AND status = 'INACTIVE'" , (username,))  
            print(f"User {self.username}  has been reactivated successfully")  
        except Exception as e:  
            print(f"[ERROR][reactviate_user] {e}")  


    def list_all_users(self , db):  
        try:  
            self.db.fetch_all("SELECT username FROM users;")  
        except Exception as e:  
            print(f"[ERROR][list_all_users] {e}")  

    def list_users_by_attribute(self , db):  
        pass  

    def view_audit_logs(self, db):  
        cursor = None  
        try:  
            cursor = db.cursor()  
            sql = "SELECT * FROM audit_logs"  
            cursor.execute(sql)  
            for row in cursor.fetchall():  
                print(row)  

        except Exception as e:  
            messagebox.showerror("Error", str(e))  
        finally:  
            try:  
                if cursor:  
                    cursor.close()  
            except Exception:  
                messagebox.showerror("Error", str(e))  

    def deactivate_user(self , db, username):  
        try:  
            self.db.execute_query("UPDATE  users SET status = 'INACTIVE' WHERE username = %s AND status = 'ACTIVE'", (  
                username,))  
            print(f"User {self.username}  has been deactivated successfully")  

        except Exception as e:  
            messagebox.showerror("Error", str(e))
