from abc import ABC, abstractmethod

class User(ABC):
    """
    Abstract base class representing a system user.
    Shared attributes: user_id, name, email, password, role_id
    """

    def __init__(self, user_id, name, email, password, role_id):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.password = password
        self.role_id = role_id

    def login(self):
        print(f"[LOGIN] {self.name} ({self.email}) logged in.")

    def logout(self):
        print(f"[LOGOUT] {self.name} logged out.")

    @abstractmethod
    def display_menu(self):
        """Each subclass must implement its own menu."""
        pass
