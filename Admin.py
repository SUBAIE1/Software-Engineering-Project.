#from models.user import User

class Admin(User):
    """
    Admin user has full privileges for user management, audit logs, and system configuration.
    """

    def display_menu(self):
        print("\n===== ADMIN MENU =====")
        print("1. Manage Users")
        print("2. View Audit Logs")
        print("3. Generate System Reports")
        print("4. System Configuration")
        print("5. Logout")

   
    def create_user(self, db, name, email, password, role_id):
        """
        Inserts a new user record into the database.
        """
        cursor = db.cursor()
        sql = "INSERT INTO users (name, email, password, role_id) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (name, email, password, role_id))
        db.commit()
        print(f"[ADMIN] Created user '{name}' with role ID {role_id}.")

    def delete_user(self, db, user_id):
        cursor = db.cursor()
        sql = "DELETE FROM users WHERE user_id = %s"
        cursor.execute(sql, (user_id,))
        db.commit()
        print(f"[ADMIN] Deleted user ID {user_id}.")

    def view_audit_logs(self, db):
        cursor = db.cursor()
        cursor.execute("SELECT * FROM audit_logs ORDER BY timestamp DESC LIMIT 10;")
        for log in cursor.fetchall():
            print(log)

    def system_settings(self):
        print("[ADMIN] Accessing system configuration...")
