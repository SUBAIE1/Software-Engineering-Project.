class Manager(User):
    def display_menu(self):
        print("\n===== Manager Menu =====")
        print("1. Manage Inventory")
        print("2. Manage Purchase Orders")
        print("3. View Reports")
        print("4. Logout")

    def manage_inventory(self):
        print("[MANAGER] Managing inventory...")

    def manage_purchase_orders(self):
        print("[MANAGER] Managing supplier purchase orders...")

    def view_reports(self):
        print("[MANAGER] Viewing performance and stock reports...")
