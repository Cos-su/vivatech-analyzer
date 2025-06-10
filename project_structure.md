# Project Structure - Doxallia VivaTech Analysis

## Recommended Directory Structure

```
simpleScoreVivaTech/
├── README.md                    # Project documentation
├── requirements.txt             # Python dependencies
├── .gitignore                  # Git ignore file
├── .env.example                # Example environment variables
├── config/                     # Configuration files
│   ├── __init__.py
│   ├── settings.py            # Application settings
│   └── prompts/               # Analysis prompts
│       └── doxallia_prompt.md
│
├── src/                        # Source code
│   ├── __init__.py
│   ├── analyzers/             # Analysis modules
│   │   ├── __init__.py
│   │   ├── base_analyzer.py
│   │   ├── doxallia_analyzer.py
│   │   └── startup_scorer.py
│   │
│   ├── models/                # Data models
│   │   ├── __init__.py
│   │   ├── startup.py
│   │   └── analysis_result.py
│   │
│   ├── utils/                 # Utility functions
│   │   ├── __init__.py
│   │   ├── csv_handler.py
│   │   ├── json_handler.py
│   │   └── api_client.py
│   │
│   └── main.py               # Main application entry
│
├── data/                      # Data directory
│   ├── raw/                  # Original data files
│   │   └── startup.csv       # Original VivaTech data
│   │
│   ├── processed/            # Processed data
│   │   └── startups_only.csv
│   │
│   └── temp/                 # Temporary files (git ignored)
│       └── .gitkeep
│
├── results/                   # Analysis results
│   ├── analyses/             # Individual analysis JSON files
│   │   └── .gitkeep
│   │
│   ├── summaries/            # Summary reports
│   │   └── .gitkeep
│   │
│   └── exports/              # Export files
│       └── .gitkeep
│
├── tests/                     # Test files
│   ├── __init__.py
│   ├── conftest.py           # Pytest configuration
│   ├── fixtures/             # Test data
│   │   ├── sample_startups.csv
│   │   └── expected_results.json
│   │
│   ├── unit/                 # Unit tests
│   │   ├── test_analyzers.py
│   │   ├── test_models.py
│   │   └── test_utils.py
│   │
│   └── integration/          # Integration tests
│       └── test_full_analysis.py
│
├── scripts/                   # Utility scripts
│   ├── setup_project.py      # Project setup script
│   ├── run_sample.py         # Run sample analysis
│   └── batch_analyze.py      # Batch analysis script
│
└── logs/                      # Log files (git ignored)
    └── .gitkeep
```

## Best Practices Implementation

### 1. Environment Configuration

**.env.example**
```
# API Configuration
CLAUDE_API_KEY=your_api_key_here
CLAUDE_MODEL=claude-3-opus-20240229

# Analysis Settings
BATCH_SIZE=10
DELAY_BETWEEN_BATCHES=5
MAX_RETRIES=3

# Paths
DATA_PATH=./data
RESULTS_PATH=./results
LOG_PATH=./logs

# Environment
ENVIRONMENT=development  # development, staging, production
```

### 2. Configuration Management

**config/settings.py**
```python
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
    
    # API Settings
    CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")
    CLAUDE_MODEL = os.getenv("CLAUDE_MODEL", "claude-3-opus-20240229")
    
    # Analysis Settings
    BATCH_SIZE = int(os.getenv("BATCH_SIZE", 10))
    DELAY_BETWEEN_BATCHES = int(os.getenv("DELAY_BETWEEN_BATCHES", 5))
    MAX_RETRIES = int(os.getenv("MAX_RETRIES", 3))

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    USE_SAMPLE_DATA = True
    MAX_COMPANIES_TO_ANALYZE = 5

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    USE_SAMPLE_DATA = False
    MAX_COMPANIES_TO_ANALYZE = None

# Select config based on environment
ENV = os.getenv("ENVIRONMENT", "development")
config = DevelopmentConfig() if ENV == "development" else ProductionConfig()
```

### 3. Git Ignore File

**.gitignore**
```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
.venv

# Environment
.env
.env.local
.env.*.local

# Data
data/temp/
*.tmp
*.bak

# Results (optional - depend on your needs)
results/analyses/*.json
results/summaries/*.csv
results/exports/*

# Logs
logs/*.log
logs/*.txt

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Testing
.pytest_cache/
.coverage
htmlcov/
.tox/
.nox/

# Jupyter
.ipynb_checkpoints
*.ipynb
```

### 4. Data Model Example

**src/models/startup.py**
```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class Startup:
    """Startup data model"""
    company_name: str
    website: str
    description: str
    hall: Optional[str]
    booth_number: Optional[str]
    days_of_presence: Optional[str]
    business_sector: str
    country: str
    pavilion: Optional[str]
    
    @classmethod
    def from_csv_row(cls, row: dict) -> 'Startup':
        """Create Startup instance from CSV row"""
        return cls(
            company_name=row['HOST COMPANY NAME'],
            website=row['WEBSITE'],
            description=row['DESCRIPTION'],
            hall=row.get('HALL'),
            booth_number=row.get('BOOTH NUMBER'),
            days_of_presence=row.get('DAYS OF PRESENCE'),
            business_sector=row['BUSINESS-SECTOR'],
            country=row['COUNTRY'],
            pavilion=row.get('PAVILION')
        )
```

### 5. Base Analyzer Class

**src/analyzers/base_analyzer.py**
```python
from abc import ABC, abstractmethod
from typing import Dict, Any
import logging

class BaseAnalyzer(ABC):
    """Base class for all analyzers"""
    
    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger(self.__class__.__name__)
    
    @abstractmethod
    def analyze(self, startup: 'Startup') -> Dict[str, Any]:
        """Analyze a startup and return results"""
        pass
    
    @abstractmethod
    def validate_results(self, results: Dict[str, Any]) -> bool:
        """Validate analysis results"""
        pass
    
    def save_results(self, results: Dict[str, Any], filename: str):
        """Save results to file"""
        # Implementation here
        pass
```

### 6. Testing Structure

**tests/conftest.py**
```python
import pytest
from pathlib import Path

@pytest.fixture
def sample_startup_data():
    """Provide sample startup data for testing"""
    return {
        'HOST COMPANY NAME': 'Test Company',
        'WEBSITE': 'https://test.com',
        'DESCRIPTION': 'Test description',
        'BUSINESS-SECTOR': 'informationtechnologies',
        'COUNTRY': 'france'
    }

@pytest.fixture
def test_data_path():
    """Path to test data"""
    return Path(__file__).parent / "fixtures"
```

### 7. Main Application Entry

**src/main.py**
```python
#!/usr/bin/env python3
"""
Doxallia VivaTech Analysis System
Main application entry point
"""

import argparse
import logging
from pathlib import Path
from config.settings import config
from analyzers.doxallia_analyzer import DoxalliaAnalyzer
from utils.csv_handler import load_startups

def setup_logging():
    """Configure logging"""
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    log_file = config.LOGS_DIR / 'analysis.log'
    
    logging.basicConfig(
        level=logging.DEBUG if config.DEBUG else logging.INFO,
        format=log_format,
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )

def main():
    """Main application logic"""
    parser = argparse.ArgumentParser(description='Analyze VivaTech startups')
    parser.add_argument('--input', type=str, default='data/processed/startups_only.csv')
    parser.add_argument('--batch-size', type=int, default=config.BATCH_SIZE)
    parser.add_argument('--test', action='store_true', help='Run in test mode')
    
    args = parser.parse_args()
    
    # Setup
    setup_logging()
    logger = logging.getLogger(__name__)
    
    # Load data
    input_file = Path(args.input)
    if args.test:
        input_file = Path('tests/fixtures/sample_startups.csv')
    
    logger.info(f"Loading startups from {input_file}")
    startups = load_startups(input_file)
    
    # Initialize analyzer
    analyzer = DoxalliaAnalyzer(config)
    
    # Run analysis
    logger.info(f"Analyzing {len(startups)} startups")
    results = analyzer.batch_analyze(startups, batch_size=args.batch_size)
    
    logger.info("Analysis complete")

if __name__ == "__main__":
    main()
```

### 8. Development vs Production Separation

**Key Principles:**

1. **Environment Variables**: Use `.env` files for configuration
2. **Data Separation**: Keep test data in `tests/fixtures/`, production data in `data/`
3. **Results Isolation**: Store test results in `data/temp/` (gitignored)
4. **Configuration Classes**: Use different configs for dev/prod
5. **Logging**: Different log levels and destinations per environment
6. **Sample Mode**: Use `USE_SAMPLE_DATA` flag for testing

### 9. Setup Script

**scripts/setup_project.py**
```python
#!/usr/bin/env python3
"""Setup project structure and dependencies"""

import os
from pathlib import Path

def create_directories():
    """Create project directories"""
    dirs = [
        'data/raw', 'data/processed', 'data/temp',
        'results/analyses', 'results/summaries', 'results/exports',
        'logs', 'config/prompts'
    ]
    
    for dir_path in dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        
    # Create .gitkeep files
    for dir_path in ['data/temp', 'results/analyses', 'logs']:
        (Path(dir_path) / '.gitkeep').touch()

if __name__ == "__main__":
    create_directories()
    print("Project structure created successfully!")
```

This architecture provides:
- Clear separation between test and production
- Modular, testable code
- Configuration management
- Proper logging
- Easy deployment and maintenance