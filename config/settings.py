"""
Configuration settings for Doxallia VivaTech Analysis
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Base configuration"""
    BASE_DIR = Path(__file__).parent.parent
    DATA_DIR = BASE_DIR / "data"
    RESULTS_DIR = BASE_DIR / "results"
    LOGS_DIR = BASE_DIR / "logs"
    CONFIG_DIR = BASE_DIR / "config"
    
    # Ensure directories exist
    for dir_path in [DATA_DIR, RESULTS_DIR, LOGS_DIR]:
        dir_path.mkdir(parents=True, exist_ok=True)
    
    # API Settings
    CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")
    CLAUDE_MODEL = os.getenv("CLAUDE_MODEL", "claude-3-opus-20240229")
    
    # Analysis Settings
    BATCH_SIZE = int(os.getenv("BATCH_SIZE", 10))
    DELAY_BETWEEN_BATCHES = int(os.getenv("DELAY_BETWEEN_BATCHES", 5))
    MAX_RETRIES = int(os.getenv("MAX_RETRIES", 3))
    
    # File paths
    RAW_DATA_PATH = DATA_DIR / "raw"
    PROCESSED_DATA_PATH = DATA_DIR / "processed"
    TEMP_DATA_PATH = DATA_DIR / "temp"
    
    ANALYSES_PATH = RESULTS_DIR / "analyses"
    SUMMARIES_PATH = RESULTS_DIR / "summaries"
    EXPORTS_PATH = RESULTS_DIR / "exports"
    
    # Prompt paths
    DOXALLIA_PROMPT_PATH = CONFIG_DIR / "prompts" / "doxallia_prompt.md"
    
    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    ENVIRONMENT = "development"
    
    # Use sample data in development
    USE_SAMPLE_DATA = True
    MAX_COMPANIES_TO_ANALYZE = 5
    
    # Shorter delays for testing
    DELAY_BETWEEN_BATCHES = 2
    
    # More verbose logging
    LOG_LEVEL = "DEBUG"

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    ENVIRONMENT = "production"
    
    # Use full dataset in production
    USE_SAMPLE_DATA = False
    MAX_COMPANIES_TO_ANALYZE = None
    
    # Production delays
    DELAY_BETWEEN_BATCHES = 5
    
    # Less verbose logging
    LOG_LEVEL = "INFO"

class TestConfig(Config):
    """Test configuration"""
    DEBUG = True
    ENVIRONMENT = "test"
    
    # Test specific settings
    USE_SAMPLE_DATA = True
    MAX_COMPANIES_TO_ANALYZE = 3
    DELAY_BETWEEN_BATCHES = 0
    
    # Test data paths
    TEST_FIXTURES_PATH = Config.BASE_DIR / "tests" / "fixtures"
    
    # Use temp directory for test results
    ANALYSES_PATH = Config.TEMP_DATA_PATH / "test_analyses"
    SUMMARIES_PATH = Config.TEMP_DATA_PATH / "test_summaries"
    
    # Debug logging for tests
    LOG_LEVEL = "DEBUG"

# Configuration factory
def get_config():
    """Get configuration based on environment"""
    env = os.getenv("ENVIRONMENT", "development").lower()
    
    configs = {
        "development": DevelopmentConfig(),
        "production": ProductionConfig(),
        "test": TestConfig()
    }
    
    config = configs.get(env, DevelopmentConfig())
    
    # Validate critical settings
    if env == "production" and not config.CLAUDE_API_KEY:
        raise ValueError("CLAUDE_API_KEY must be set in production environment")
    
    return config

# Global config instance
config = get_config()