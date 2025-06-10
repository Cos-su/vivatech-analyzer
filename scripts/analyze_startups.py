#!/usr/bin/env python3
"""
Doxallia Strategic Analysis System
Analyzes startups for potential partnerships using multi-agent deep research
"""

import csv
import json
import time
from datetime import datetime
import os

def load_startups(file_path):
    """Load startups from CSV file"""
    startups = []
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            startups.append(row)
    return startups

def save_analysis_results(results, output_file):
    """Save analysis results to JSON file"""
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

def create_analysis_prompt(startup):
    """Create analysis prompt for a startup"""
    prompt = f"""
    Analyse cette startup selon la méthodologie Doxallia :
    
    - Nom : {startup['HOST COMPANY NAME']}
    - Description : {startup['DESCRIPTION']}
    - Site web : {startup['WEBSITE']}
    - Secteur : {startup['BUSINESS-SECTOR']}
    - Pays : {startup['COUNTRY']}
    
    Effectue une recherche approfondie et fournis une analyse complète selon le format JSON structuré.
    """
    return prompt

def create_summary_csv(results, output_file):
    """Create a summary CSV with key scores and recommendations"""
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = [
            'company_name', 'website', 'sector', 'country',
            'score_total', 'niveau_confiance',
            'souverainete_numerique', 'antifraude_documentaire',
            'intelligence_documentaire', 'synergies_sectorielles',
            'recommandation', 'priorite', 'positionnement'
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for company, analysis in results.items():
            if isinstance(analysis, dict) and 'scores_expertise' in analysis:
                row = {
                    'company_name': company,
                    'website': analysis.get('website', ''),
                    'sector': analysis.get('sector', ''),
                    'country': analysis.get('country', ''),
                    'score_total': analysis.get('score_total', 0),
                    'niveau_confiance': analysis.get('niveau_confiance', 0),
                    'souverainete_numerique': analysis['scores_expertise'].get('souverainete_numerique', 0),
                    'antifraude_documentaire': analysis['scores_expertise'].get('antifraude_documentaire', 0),
                    'intelligence_documentaire': analysis['scores_expertise'].get('intelligence_documentaire', 0),
                    'synergies_sectorielles': analysis['scores_expertise'].get('synergies_sectorielles', 0),
                    'recommandation': analysis.get('recommandation_finale', {}).get('approche', ''),
                    'priorite': analysis.get('recommandation_finale', {}).get('priorite', ''),
                    'positionnement': analysis.get('intelligence_competitive', {}).get('positionnement_vs_doxallia', '')
                }
                writer.writerow(row)

def main():
    # Configuration
    input_file = 'startups_only.csv'
    output_json = f'doxallia_analysis_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
    output_csv = f'doxallia_summary_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    
    # Load startups
    print(f"Loading startups from {input_file}...")
    startups = load_startups(input_file)
    print(f"Loaded {len(startups)} startups")
    
    # Analysis configuration
    batch_size = 10  # Process in batches to avoid overwhelming the system
    delay_between_batches = 5  # seconds
    
    results = {}
    
    print("\nStarting analysis process...")
    print("This will take some time as we perform deep research on each startup.")
    
    # Process startups in batches
    for i in range(0, len(startups), batch_size):
        batch = startups[i:i+batch_size]
        print(f"\nProcessing batch {i//batch_size + 1} ({i+1}-{min(i+batch_size, len(startups))} of {len(startups)})")
        
        for startup in batch:
            company_name = startup['HOST COMPANY NAME']
            print(f"  Analyzing: {company_name}")
            
            # Create analysis prompt
            prompt = create_analysis_prompt(startup)
            
            # Here you would normally call the Claude API or use the Task tool
            # For now, we'll create a placeholder structure
            results[company_name] = {
                'website': startup['WEBSITE'],
                'sector': startup['BUSINESS-SECTOR'],
                'country': startup['COUNTRY'],
                'description': startup['DESCRIPTION'],
                'analysis_timestamp': datetime.now().isoformat(),
                'status': 'pending_analysis'
            }
        
        # Delay between batches
        if i + batch_size < len(startups):
            print(f"  Waiting {delay_between_batches} seconds before next batch...")
            time.sleep(delay_between_batches)
    
    # Save results
    print(f"\nSaving results to {output_json}")
    save_analysis_results(results, output_json)
    
    print(f"Creating summary CSV: {output_csv}")
    create_summary_csv(results, output_csv)
    
    print("\nAnalysis complete!")
    print(f"- Full results: {output_json}")
    print(f"- Summary CSV: {output_csv}")

if __name__ == "__main__":
    main()