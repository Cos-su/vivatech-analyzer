# Doxallia VivaTech Analysis System

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
