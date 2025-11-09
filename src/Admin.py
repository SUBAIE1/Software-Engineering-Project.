from user import User
import mysql.connector

class Admin(User):
    """
        1-create user
        2-delete user
        4-modify user (role , ....)
        5-view audit_logs
        """

    def create_user(self , db , username , user_id, password, role_id ):

        cursor = db.cursor()
        sql = """
        INSERT INTO users (username, user_id, password, role_id, last_login, created_at) VALUES (%s, %s, %s, %s, %s, %s);
        """
        cursor.execute(sql , (username , user_id, password, role_id))
        cursor.commit()
        print(f"User {self.username} , with user_id {self.user_id} , and password {self.password} is created successfully and assigned to {self.rolename} role")

    def delete_user(self , db ,  user_id ):

        cursor = db.cursor()
        sql = "DELET FROM users WHERE user_id = %s"

        cursor.execute(sql, (user_id))
        cursor.commit()
        print(
            f"User {self.username} , with user_id {self.user_id} , and password {self.password} is deleted successfully")

    def update_user(self, db, user_id, updates: dict):
        """
        Dynamically updates multiple fields in one go.
        Example: {"username": "newname", "role_id": 2}
        """
        fields = ", ".join(f"{k}=%s" for k in updates.keys())
        values = list(updates.values()) + [user_id]
        sql = f"UPDATE users SET {fields} WHERE user_id=%s"
        cursor = db.cursor()
        cursor.execute(sql, values)
        db.commit()
        print(f"[ADMIN] Updated user {user_id} with fields {list(updates.keys())}")

    def deacivate_user(self , db, user_id):
        cursor = db.cursor()
        #MUST CHECK IF THE USER IS ACTIVE FIRST

        sql = "UPDATE  users SET status = 'INACTIVE' WHERE user_id = %s AND status = 'ACTIVE'"
        cursor.execute (sql , user_id)
        db.commit()
        print(f"User {self.username} , with ID {self.user_id} has been deactivated successfully")

    def reactviate_user(self , db, user_id):
        cursor = db.cursor()

        sql = "UPDATE users SET status = 'ACTIVE' WHERE user_id = %s AND status = 'INACTIVE'"

        cursor.execute(sql , user_id)
        cursor.commit()

        print(f"User {self.username} , with ID {self.user_id} has been reactivated successfully")

    def list_all_users(self , db):

        cursor = db.cursor()

        sql = "SELECT * FROM users"
        cursor.execute(sql)
        for row in cursor.fetchall():
            print(row)

    def list_users_by_attribute(self , db):
        pass

    def reset_password(self , db, user_id , password):
        cursor = db.cursor()

        sql = "UPDATE users SET password = %s WHERE user_id = %s"

        cursor.execute(sql , (user_id , password))
        db.commit()
        print(f"Password of user {self.username} , with ID {self.user_id} has been reset to {self.password} successfully")

    def assign_role(self , db , user_id , role_id):
        """
        CHANGING ROLE OF THE USER.
        """
        cursor = db.cursor()

        sql = " UPDATE users SET role_id = %s WHERE user_id = %s  "
        cursor.execute(sql , (role_id, user_id))
        db.commit()
        #I need to show the role name instead of role_id
        print(f"Role of user {self.username} having ID {self.user_id} is changed to {self.role_id} successfully")

    def view_audit_logs(self, db):

        cursor = db.cursor()
        #order by whatever needed
        sql = "SELECT * FROM audit_logs"
        cursor.execute(sql)
        for row in cursor.fetchall():
            print(row)
