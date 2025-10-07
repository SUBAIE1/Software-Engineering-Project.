from datetime import datetime

class Role:
    """
    Represents a system role ( Admin, Manager, Cashier).
    Handles role creation, retrieval, and permission mapping.
    """

    def __init__(self, role_id, role_name, description=None, created_at=None):
        self.role_id = role_id
        self.role_name = role_name
        self.description = description if description else "No description provided."
        self.created_at = created_at if created_at else datetime.now()

    
    def __str__(self):
        return f"Role[{self.role_id}] - {self.role_name}"

    def display_role_info(self):
        print(f"--- Role Info ---")
        print(f"ID: {self.role_id}")
        print(f"Name: {self.role_name}")
        print(f"Description: {self.description}")
        print(f"Created: {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}")

    #DB
  
    @staticmethod
    def create_role(db, role_name, description=None):
        cursor = db.cursor()
        sql = "INSERT INTO roles (role_name) VALUES (%s)"
        cursor.execute(sql, (role_name,))
        db.commit()
        print(f"[ROLE] Created new role: {role_name}")

    @staticmethod
    def get_all_roles(db):
        cursor = db.cursor()
        cursor.execute("SELECT role_id, role_name FROM roles;")
        roles = cursor.fetchall()
        print("--- Roles in System ---")
        for role in roles:
            print(f"ID: {role[0]} | Name: {role[1]}")
        return roles

    @staticmethod
    def get_role_by_id(db, role_id):
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM roles WHERE role_id = %s;", (role_id,))
        return cursor.fetchone()

    @staticmethod
    def delete_role(db, role_id):
        cursor = db.cursor()
        cursor.execute("DELETE FROM roles WHERE role_id = %s;", (role_id,))
        db.commit()
        print(f"[ROLE] Deleted role ID {role_id}")
