class Cashier(User):
    def display_menu(self):
        print("\n===== Cashier Menu =====")
        print("1. Create Order")
        print("2. Process Payment")
        print("3. Logout")

    def create_order(self):
        print("[CASHIER] Creating new customer order...")

    def process_payment(self):
        print("[CASHIER] Processing payment...")
