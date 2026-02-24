"""Database migrations."""

from config.database_connection import DatabaseConnection


def create_schema():
    """Create all database tables."""
    db = DatabaseConnection()
    print("Schema creation should be done by running: mysql < config/Database.sql")


def upgrade_schema():
    """Apply schema migrations."""
    pass


def downgrade_schema():
    """Rollback schema migrations."""
    pass
