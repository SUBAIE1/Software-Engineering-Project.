from abc import ABC, abstractmethod
from datetime import datetime

class User(ABC):
    """
    Abstract base class for all system users.
    Provides shared attributes, authentication, and profile operations.
    """

    def __init__(self, user_id, name, email, password, role_id, status="Active", created_at=None):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.password = password      # 🔒 hashed in real DB
        self.role_id = role_id
        self.status = status
        self.created_at = created_at if created_at else datetime.now()

    
    def login(self):
        self.last_login = datetime.now()
        print(f"[LOGIN] {self.name} ({self.email}) logged in at {self.last_login.strftime('%Y-%m-%d %H:%M:%S')}")

    def logout(self):
        print(f"[LOGOUT] {self.name} logged out.")

    def update_profile(self, new_name=None, new_email=None, new_phone=None):
        if new_name: self.name = new_name
        if new_email: self.email = new_email
        if new_phone: self.phone = new_phone
        print(f"[PROFILE] {self.name}'s profile updated successfully.")

    def deactivate(self):
        self.status = "Inactive"
        print(f"[ACCOUNT] {self.name}'s account has been deactivated.")

    #def activate(self):
        
        

    def display_user_summary(self):
        print(f"--- User Info ---")
        print(f"ID: {self.user_id}")
        print(f"Name: {self.name}")
        print(f"Email: {self.email}")
        print(f"Role ID: {self.role_id}")
        print(f"Status: {self.status}")
        print(f"Created: {self.created_at.strftime('%Y-%m-%d')}")
        if self.last_login:
            print(f"Last Login: {self.last_login.strftime('%Y-%m-%d %H:%M:%S')}")

    @abstractmethod
    def display_menu(self):
        """Abstract: each role implements its own operational menu."""
        pass
