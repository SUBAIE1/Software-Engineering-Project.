
"""Entry point for the Inventory Management System."""

from pathlib import Path
import sys

# Add project root to Python path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from settings import load_settings


def main():
    """Initialize and run the application."""
    # Load environment settings
    load_settings()
    
    # TODO: Implement App class or GUI framework integration
    print("IMS Started successfully")
    print("Database configured. Ready for use.")
    # Create and run the application
    # app = App()
    # app.mainloop()


if __name__ == "__main__":
    main()
