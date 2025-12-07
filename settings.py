"""Application configuration settings."""

import os
from pathlib import Path
from typing import Optional


class Settings:
    """Application configuration loaded from environment variables."""
    
    def __init__(self):
        # Database configuration
        self.DB_HOST: str = os.getenv("DB_HOST", "localhost")
        self.DB_PORT: int = int(os.getenv("DB_PORT", "3306"))
        self.DB_USER: str = os.getenv("DB_USER", "root")
        self.DB_PASSWORD: str = os.getenv("DB_PASSWORD", "rootAdmin1")
        self.DB_NAME: str = os.getenv("DB_NAME", "ims_db")
        
        # Security settings
        self.LOCK_THRESHOLD: int = int(os.getenv("LOCK_THRESHOLD", "5"))
        self.LOCK_MINUTES: int = int(os.getenv("LOCK_MINUTES", "15"))
        self.PASSWORD_MIN_LENGTH: int = int(os.getenv("PASSWORD_MIN_LENGTH", "6"))
        
        # Application settings
        self.APP_NAME: str = os.getenv("APP_NAME", "Inventory Management System")
        self.DEBUG: bool = os.getenv("DEBUG", "False").lower() in ("true", "1", "yes")
        
        # Logging settings
        self.LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
        self.LOG_FILE: Optional[str] = os.getenv("LOG_FILE", None)
        
        # Paths
        self.BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent
        self.DATA_DIR: Path = self.BASE_DIR / "data"
        self.LOGS_DIR: Path = self.BASE_DIR / "logs"
        
        # Create directories if they don't exist
        self.DATA_DIR.mkdir(exist_ok=True)
        self.LOGS_DIR.mkdir(exist_ok=True)
    
    def get_db_config(self) -> dict:
        """Get database configuration as a dictionary."""
        return {
            "host": self.DB_HOST,
            "port": self.DB_PORT,
            "user": self.DB_USER,
            "password": self.DB_PASSWORD,
            "database": self.DB_NAME,
        }
    
    def load_env_file(self, env_file: str = ".env"):
        """
        Load environment variables from a .env file.
        
        Args:
            env_file: Path to the .env file
        """
        env_path = self.BASE_DIR / env_file
        if not env_path.exists():
            print(f"Warning: {env_file} not found at {env_path}")
            return
        
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                # Skip comments and empty lines
                if not line or line.startswith('#'):
                    continue
                
                # Parse KEY=VALUE
                if '=' in line:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip()
                    # Remove quotes if present
                    if value.startswith('"') and value.endswith('"'):
                        value = value[1:-1]
                    elif value.startswith("'") and value.endswith("'"):
                        value = value[1:-1]
                    
                    os.environ[key] = value
        
        # Reload settings after loading env file
        self.__init__()


# Global settings instance
settings = Settings()


def load_settings(env_file: str = ".env") -> Settings:
    """
    Load settings from environment file.
    
    Args:
        env_file: Path to the .env file
    
    Returns:
        Settings instance
    """
    global settings
    settings.load_env_file(env_file)
    return settings
