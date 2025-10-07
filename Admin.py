class Admin(User):
    def display_menu(self):
        print("\n===== Admin Menu =====")
        print("1. Manage Users")
        print("2. View Audit Logs")
        print("3. View Reports")
        print("4. Logout")

    def manage_users(self):
        print("[ADMIN] Managing users...")

    def view_audit_logs(self):
        print("[ADMIN] Viewing audit logs...")

    def view_reports(self):
        print("[ADMIN] Viewing reports...")
