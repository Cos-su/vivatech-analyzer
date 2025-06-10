#!/usr/bin/env python3
"""
Sample analysis script to demonstrate the Doxallia analysis on a few startups
This shows how the system would work without requiring 840 API calls
"""

import csv
import json
from datetime import datetime

def analyze_startup_sample():
    """
    This function demonstrates how to analyze a few sample startups
    In production, this would call Claude API for each startup
    """
    
    # Load a few sample startups
    sample_startups = []
    with open('startups_only.csv', 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for i, row in enumerate(reader):
            if i < 5:  # Just take first 5 for demonstration
                sample_startups.append(row)
            else:
                break
    
    print("Sample Startups for Analysis:")
    print("="*80)
    
    for startup in sample_startups:
        print(f"\nCompany: {startup['HOST COMPANY NAME']}")
        print(f"Website: {startup['WEBSITE']}")
        print(f"Sector: {startup['BUSINESS-SECTOR']}")
        print(f"Description: {startup['DESCRIPTION'][:150]}...")
        print("-"*80)
    
    # Create prompt template
    prompt_template = """
    You will analyze each startup using the Doxallia methodology.
    For each startup, you need to:
    
    1. Visit their website and gather information
    2. Search for additional information online
    3. Evaluate them on the 4 key criteria:
       - Souveraineté Numérique (25 points)
       - Antifraude Documentaire (25 points) 
       - Intelligence Documentaire (25 points)
       - Synergies Sectorielles (25 points)
    
    4. Provide a structured JSON response with scores and recommendations
    
    The startups to analyze are listed above.
    """
    
    # Save the sample analysis request
    analysis_request = {
        "analysis_date": datetime.now().isoformat(),
        "methodology": "Doxallia Deep Search",
        "sample_startups": [
            {
                "name": s['HOST COMPANY NAME'],
                "website": s['WEBSITE'],
                "sector": s['BUSINESS-SECTOR'],
                "description": s['DESCRIPTION']
            }
            for s in sample_startups
        ],
        "prompt_template": prompt_template
    }
    
    with open('sample_analysis_request.json', 'w', encoding='utf-8') as f:
        json.dump(analysis_request, f, ensure_ascii=False, indent=2)
    
    print("\nSample analysis request saved to: sample_analysis_request.json")
    print("\nTo perform the analysis:")
    print("1. Use the Task tool with the Doxallia prompt for each startup")
    print("2. Or use the Claude API with the analysis prompt")
    print("3. Save results in the structured JSON format")

if __name__ == "__main__":
    analyze_startup_sample()