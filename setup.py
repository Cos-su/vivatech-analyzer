#!/usr/bin/env python3
"""
Setup script for VivaTech Startup Analyzer
Handles installation and initial configuration
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(command, description):
    """Execute a command with error handling"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error during {description}")
        print(f"Details: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python 3.8+ required, found {version.major}.{version.minor}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible")
    return True

def install_dependencies():
    """Install required dependencies"""
    requirements_file = Path("requirements.txt")
    
    if not requirements_file.exists():
        print("❌ requirements.txt not found")
        return False
    
    print("📦 Installing dependencies...")
    return run_command(
        f"{sys.executable} -m pip install -r requirements.txt",
        "Installing Python packages"
    )

def create_sample_config():
    """Create sample configuration files"""
    print("📝 Creating sample configuration...")
    
    # Sample Claude config (template)
    claude_config_sample = {
        "api_key": "your-claude-api-key-here",
        "model": "claude-3-haiku-20240307",
        "max_tokens": 500
    }
    
    sample_file = Path(".claude_config.json.sample")
    if not sample_file.exists():
        import json
        with open(sample_file, 'w') as f:
            json.dump(claude_config_sample, f, indent=2)
        print("✅ Created .claude_config.json.sample")
    
    # Create example data directory
    examples_dir = Path("examples")
    examples_dir.mkdir(exist_ok=True)
    
    # Create example CSV header
    example_csv = examples_dir / "example_data.csv"
    if not example_csv.exists():
        csv_content = """PARTNER_ID;HOST COMPANY NAME;PLACE;HALL;DAYS OF PRESENCE;DESCRIPTION;WEBSITE;BUSINESS-SECTOR;COUNTRY
EXAMPLE_STARTUP;Example Host;A01-001;hall1;wed,thu,fri;Example startup description;https://example.com;informationtechnologies;france"""
        with open(example_csv, 'w') as f:
            f.write(csv_content)
        print("✅ Created example CSV format")
    
    return True

def check_csv_file():
    """Check for VivaTech CSV file"""
    csv_file = Path("VivaTech.csv")
    if csv_file.exists():
        print("✅ VivaTech.csv found")
        return True
    else:
        print("⚠️ VivaTech.csv not found")
        print("   Please place your VivaTech CSV file in this directory")
        print("   You can use examples/example_data.csv as a reference")
        return False

def setup_git_hooks():
    """Setup git hooks for development"""
    if Path(".git").exists():
        print("📋 Setting up git hooks...")
        
        # Pre-commit hook to run basic checks
        hooks_dir = Path(".git/hooks")
        hooks_dir.mkdir(exist_ok=True)
        
        pre_commit_hook = hooks_dir / "pre-commit"
        hook_content = """#!/bin/bash
# Basic pre-commit checks
echo "Running pre-commit checks..."

# Check Python syntax
python -m py_compile vivatech_analyzer.py
if [ $? -ne 0 ]; then
    echo "❌ Python syntax error in vivatech_analyzer.py"
    exit 1
fi

echo "✅ Pre-commit checks passed"
"""
        
        with open(pre_commit_hook, 'w') as f:
            f.write(hook_content)
        
        # Make executable
        os.chmod(pre_commit_hook, 0o755)
        print("✅ Git hooks configured")
        return True
    
    return False

def run_quick_test():
    """Run a quick test to verify installation"""
    print("🧪 Running quick installation test...")
    
    try:
        # Test imports
        import pandas
        import aiohttp
        import beautifulsoup4
        import plotly
        print("✅ Core dependencies import successfully")
        
        # Test analyzer import
        from vivatech_analyzer import VivaTechAnalyzerV2
        print("✅ VivaTech analyzer imports successfully")
        
        return True
    
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 VivaTech Startup Analyzer - Setup")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        print("\n💡 Please upgrade to Python 3.8 or higher")
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("\n❌ Failed to install dependencies")
        sys.exit(1)
    
    # Create configuration files
    create_sample_config()
    
    # Check for CSV file
    csv_exists = check_csv_file()
    
    # Setup git hooks (optional)
    setup_git_hooks()
    
    # Run quick test
    if not run_quick_test():
        print("\n❌ Installation test failed")
        sys.exit(1)
    
    # Final instructions
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    
    if not csv_exists:
        print("1. 📁 Place your VivaTech.csv file in this directory")
    
    print("2. 🚀 Run analysis: python run_analysis.py")
    print("3. 📖 Read usage guide: cat USAGE.md")
    print("4. 🤖 (Optional) Configure Claude AI for better accuracy")
    
    print("\n💡 Quick start command:")
    print("   python run_analysis.py")
    
    print("\n🔗 For more information:")
    print("   📖 README.md - Full documentation")
    print("   📖 USAGE.md - Usage examples")
    print("   📁 examples/ - Sample files")

if __name__ == "__main__":
    main()