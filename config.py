"""
Configuration management for the Deixis AI Agent system.
"""

import os
from dotenv import load_dotenv
from typing import Dict, Any
import logging

# Load environment variables
load_dotenv()

class Config:
    """Configuration class for the Deixis AI Agent."""
    
    # API Keys (only these come from .env)
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
    
    # Application Configuration (sensible defaults)
    DATABASE_PATH = "data/responses.db"
    LOG_LEVEL = "INFO"
    LOG_FILE = "logs/deixis_agent.log"
    MAX_TOKENS = 2000
    TEMPERATURE = 0.7
    BATCH_SIZE = 10
    
    # Deictic Framings
    DEICTIC_FRAMINGS = [
        "anchored_cot",
        "role_based",
        "cosmological",
        "neutral",
        "shamanic"
    ]
    
    # Ethical Stances
    ETHICAL_STANCES = [
        "deontological",
        "consequentialist", 
        "relational",
        "virtue",
        "shamanic",
        "mixed",
        "unclear"
    ]
    
    # Data Directories
    DATA_DIR = "data"
    LOGS_DIR = "logs"
    TEMPLATES_DIR = "templates"
    EXPORTS_DIR = "exports"
    
    @classmethod
    def setup_directories(cls):
        """Create necessary directories if they don't exist."""
        directories = [cls.DATA_DIR, cls.LOGS_DIR, cls.TEMPLATES_DIR, cls.EXPORTS_DIR]
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
    
    @classmethod
    def setup_logging(cls):
        """Setup logging configuration."""
        cls.setup_directories()
        logging.basicConfig(
            level=getattr(logging, cls.LOG_LEVEL),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(cls.LOG_FILE),
                logging.StreamHandler()
            ]
        )
    
    @classmethod
    def validate_config(cls) -> Dict[str, Any]:
        """Validate configuration and return status."""
        status = {
            "openai_key": bool(cls.OPENAI_API_KEY),
            "directories_created": False,
            "logging_setup": False
        }
        
        try:
            cls.setup_directories()
            status["directories_created"] = True
        except Exception as e:
            logging.error(f"Failed to create directories: {e}")
        
        try:
            cls.setup_logging()
            status["logging_setup"] = True
        except Exception as e:
            print(f"Failed to setup logging: {e}")
        
        return status

# Initialize configuration
config_status = Config.validate_config()