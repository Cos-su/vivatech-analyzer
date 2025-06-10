#!/usr/bin/env python3
"""
Run sample analysis for testing/development
This script demonstrates the test/production separation
"""

import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

import json
import csv
from datetime import datetime
from config.settings import get_config

def create_sample_data():
    """Create sample data for testing"""
    config = get_config()
    
    # Ensure test fixtures directory exists
    fixtures_dir = Path(__file__).parent.parent / "tests" / "fixtures"
    fixtures_dir.mkdir(parents=True, exist_ok=True)
    
    # Create sample startups CSV
    sample_file = fixtures_dir / "sample_startups.csv"
    
    if not sample_file.exists():
        print(f"Creating sample data file: {sample_file}")
        
        # Read first 5 entries from processed data
        source_file = config.PROCESSED_DATA_PATH / "startups_only.csv"
        
        if source_file.exists():
            with open(source_file, 'r', encoding='utf-8') as infile:
                reader = csv.DictReader(infile)
                fieldnames = reader.fieldnames
                
                with open(sample_file, 'w', newline='', encoding='utf-8') as outfile:
                    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
                    writer.writeheader()
                    
                    for i, row in enumerate(reader):
                        if i < 5:
                            writer.writerow(row)
                        else:
                            break
            
            print(f"✓ Created sample data with 5 startups")
        else:
            print(f"✗ Source file not found: {source_file}")
            return None
    
    return sample_file

def run_sample_analysis():
    """Run analysis on sample data"""
    # Force development environment
    os.environ["ENVIRONMENT"] = "development"
    config = get_config()
    
    print("=" * 60)
    print("DOXALLIA VIVATECH ANALYSIS - SAMPLE RUN")
    print("=" * 60)
    print(f"Environment: {config.ENVIRONMENT}")
    print(f"Debug Mode: {config.DEBUG}")
    print(f"Max Companies: {config.MAX_COMPANIES_TO_ANALYZE}")
    print(f"Batch Delay: {config.DELAY_BETWEEN_BATCHES}s")
    print("=" * 60)
    
    # Create sample data if needed
    sample_file = create_sample_data()
    if not sample_file:
        print("Failed to create sample data")
        return
    
    # Load sample data
    print(f"\nLoading sample data from: {sample_file}")
    
    with open(sample_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        startups = list(reader)
    
    print(f"Loaded {len(startups)} startups for analysis")
    
    # Display startups
    print("\nStartups to analyze:")
    print("-" * 60)
    for i, startup in enumerate(startups, 1):
        print(f"{i}. {startup['HOST COMPANY NAME']}")
        print(f"   Website: {startup['WEBSITE']}")
        print(f"   Sector: {startup['BUSINESS-SECTOR']}")
        print(f"   Country: {startup['COUNTRY']}")
    
    # Create results directory for this run
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_dir = config.TEMP_DATA_PATH / f"sample_run_{timestamp}"
    results_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"\nResults will be saved to: {results_dir}")
    
    # Simulate analysis
    print("\nSimulating analysis...")
    print("(In production, this would call the Claude API)")
    
    # Create mock results
    mock_results = {
        "run_info": {
            "timestamp": timestamp,
            "environment": config.ENVIRONMENT,
            "total_startups": len(startups)
        },
        "analyses": {}
    }
    
    for startup in startups:
        company_name = startup['HOST COMPANY NAME']
        print(f"\n→ Analyzing {company_name}...")
        
        # Mock analysis result
        mock_results["analyses"][company_name] = {
            "company_info": {
                "name": company_name,
                "website": startup['WEBSITE'],
                "sector": startup['BUSINESS-SECTOR'],
                "country": startup['COUNTRY']
            },
            "scores_expertise": {
                "souverainete_numerique": 15,
                "antifraude_documentaire": 10,
                "intelligence_documentaire": 12,
                "synergies_sectorielles": 8
            },
            "score_total": 45,
            "niveau_confiance": 0.7,
            "recommandation_finale": {
                "approche": "Veille",
                "priorite": "Moyenne",
                "timeline": "12 mois"
            }
        }
        
        print(f"  Score: 45/100")
        print(f"  Recommandation: Veille")
    
    # Save results
    results_file = results_dir / "sample_analysis_results.json"
    with open(results_file, 'w', encoding='utf-8') as f:
        json.dump(mock_results, f, ensure_ascii=False, indent=2)
    
    print(f"\n✓ Results saved to: {results_file}")
    
    # Create summary CSV
    summary_file = results_dir / "sample_summary.csv"
    with open(summary_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['company_name', 'score_total', 'recommandation', 'priorite']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for company, analysis in mock_results["analyses"].items():
            writer.writerow({
                'company_name': company,
                'score_total': analysis['score_total'],
                'recommandation': analysis['recommandation_finale']['approche'],
                'priorite': analysis['recommandation_finale']['priorite']
            })
    
    print(f"✓ Summary saved to: {summary_file}")
    
    print("\n" + "=" * 60)
    print("SAMPLE RUN COMPLETE")
    print("=" * 60)
    print("\nNote: This was a sample run with mock data.")
    print("In production, real API calls would be made to analyze each startup.")
    print(f"\nTo run in production mode, set ENVIRONMENT=production in .env")

if __name__ == "__main__":
    run_sample_analysis()