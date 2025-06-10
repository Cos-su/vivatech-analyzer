#!/usr/bin/env python3
"""
Setup project structure for Doxallia VivaTech Analysis
Creates directories and initial configuration files
"""

import os
from pathlib import Path

def create_directories():
    """Create project directory structure"""
    base_dirs = [
        # Source code
        'src/analyzers',
        'src/models', 
        'src/utils',
        
        # Configuration
        'config/prompts',
        
        # Data directories
        'data/raw',
        'data/processed',
        'data/temp',
        
        # Results directories
        'results/analyses',
        'results/summaries',
        'results/exports',
        
        # Test directories
        'tests/fixtures',
        'tests/unit',
        'tests/integration',
        
        # Scripts and logs
        'scripts',
        'logs'
    ]
    
    print("Creating directory structure...")
    for dir_path in base_dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        print(f"  ✓ Created {dir_path}")
    
    # Create __init__.py files for Python packages
    python_packages = [
        'src',
        'src/analyzers',
        'src/models',
        'src/utils',
        'config',
        'tests',
        'tests/unit',
        'tests/integration'
    ]
    
    print("\nCreating Python package files...")
    for package in python_packages:
        init_file = Path(package) / '__init__.py'
        init_file.touch()
        print(f"  ✓ Created {init_file}")
    
    # Create .gitkeep files for empty directories
    gitkeep_dirs = [
        'data/temp',
        'results/analyses',
        'results/summaries', 
        'results/exports',
        'logs'
    ]
    
    print("\nCreating .gitkeep files...")
    for dir_path in gitkeep_dirs:
        gitkeep_file = Path(dir_path) / '.gitkeep'
        gitkeep_file.touch()
        print(f"  ✓ Created {gitkeep_file}")

def create_config_files():
    """Create configuration files"""
    
    # Create .env.example
    env_example = """# API Configuration
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
"""
    
    print("\nCreating configuration files...")
    with open('.env.example', 'w') as f:
        f.write(env_example)
    print("  ✓ Created .env.example")
    
    # Create .gitignore
    gitignore = """# Python
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

# Results (keep summaries, ignore individual analyses)
results/analyses/*.json
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

# Project specific
aps_industry_analysis.json
sample_analysis_request.json
doxallia_analysis_*.json
doxallia_summary_*.csv
"""
    
    with open('.gitignore', 'w') as f:
        f.write(gitignore)
    print("  ✓ Created .gitignore")
    
    # Create requirements.txt
    requirements = """# Core dependencies
python-dotenv>=1.0.0
pandas>=2.0.0
numpy>=1.24.0
requests>=2.31.0

# Claude API (when available)
# anthropic>=0.3.0

# Data processing
openpyxl>=3.1.0
xlsxwriter>=3.1.0

# Testing
pytest>=7.4.0
pytest-cov>=4.1.0
pytest-mock>=3.11.0

# Logging and monitoring
loguru>=0.7.0

# Type checking
mypy>=1.5.0
types-requests>=2.31.0

# Code quality
black>=23.7.0
flake8>=6.1.0
isort>=5.12.0

# Documentation
mkdocs>=1.5.0
mkdocs-material>=9.2.0
"""
    
    with open('requirements.txt', 'w') as f:
        f.write(requirements)
    print("  ✓ Created requirements.txt")

def move_existing_files():
    """Move existing files to new structure"""
    
    print("\nOrganizing existing files...")
    
    # Move data files
    moves = [
        ('startup.csv', 'data/raw/startup.csv'),
        ('startups_only.csv', 'data/processed/startups_only.csv'),
        ('doxallia_analysis_prompt.md', 'config/prompts/doxallia_prompt.md'),
    ]
    
    for src, dst in moves:
        src_path = Path(src)
        dst_path = Path(dst)
        
        if src_path.exists():
            # Ensure destination directory exists
            dst_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Move file
            src_path.rename(dst_path)
            print(f"  ✓ Moved {src} → {dst}")
        else:
            print(f"  ⚠️  File not found: {src}")

def create_readme():
    """Create README.md file"""
    
    readme = """# Doxallia VivaTech Analysis System

## Overview
This system analyzes VivaTech startups for potential partnerships with Doxallia, evaluating them across four key domains:
- 🔐 Souveraineté Numérique (Digital Sovereignty)
- 🕵️ Antifraude Documentaire (Document Fraud Detection)
- 🧠 Intelligence Documentaire (Document Intelligence)
- 💼 Synergies Sectorielles (Sector Synergies)

## Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd simpleScoreVivaTech
   ```

2. **Run setup script**
   ```bash
   python setup_project.py
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and settings
   ```

## Usage

### Development Mode (Sample Analysis)
```bash
python scripts/run_sample.py
```

### Production Mode (Full Analysis)
```bash
python src/main.py --input data/processed/startups_only.csv
```

### Run Tests
```bash
pytest tests/
```

## Project Structure
See `project_structure.md` for detailed directory layout.

## Contributing
1. Create feature branch
2. Write tests
3. Ensure code quality (`black`, `flake8`)
4. Submit pull request

## License
Proprietary - Doxallia
"""
    
    with open('README.md', 'w') as f:
        f.write(readme)
    print("\n  ✓ Created README.md")

def main():
    """Main setup function"""
    print("🚀 Setting up Doxallia VivaTech Analysis Project")
    print("=" * 50)
    
    # Create directory structure
    create_directories()
    
    # Create configuration files
    create_config_files()
    
    # Move existing files
    move_existing_files()
    
    # Create README
    create_readme()
    
    print("\n✅ Project setup complete!")
    print("\nNext steps:")
    print("1. Copy .env.example to .env and add your API keys")
    print("2. Install dependencies: pip install -r requirements.txt")
    print("3. Run sample analysis: python scripts/run_sample.py")

if __name__ == "__main__":
    main()