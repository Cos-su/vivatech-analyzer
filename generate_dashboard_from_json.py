#!/usr/bin/env python3
"""
Script pour générer le dashboard HTML à partir du JSON existant
"""
import json
import os
from datetime import datetime
import plotly.express as px
import numpy as np

def generate_dashboard_from_json(json_file: str, output_file: str = "dashboard_vivatech.html"):
    """Génère un dashboard HTML à partir du fichier JSON V2"""
    
    # Lecture du fichier JSON
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    startups = data['top_startups']
    metadata = data['metadata']
    
    # Préparation des données pour Plotly
    top_20 = startups[:20]
    names = [s['name'][:30] + '...' if len(s['name']) > 30 else s['name'] for s in top_20]
    scores = [s['total_score'] for s in top_20]
    
    # Graphique des top startups
    fig_top = px.bar(
        x=scores[::-1], 
        y=names[::-1],
        orientation='h',
        title="🏆 Top 20 Startups VivaTech V2",
        labels={'x': 'Score', 'y': 'Startup'},
        color=scores[::-1],
        color_continuous_scale='viridis'
    )
    fig_top.update_layout(height=800, showlegend=False)
    
    # Distribution des tags
    tag_distribution = metadata.get('tag_distribution', {})
    
    if tag_distribution:
        fig_tags = px.pie(
            values=list(tag_distribution.values()),
            names=list(tag_distribution.keys()),
            title="📊 Distribution des Tags d'Innovation"
        )
    else:
        fig_tags = None
    
    # Statistiques de performance
    stats = {
        'total_analyzed': metadata['total_analyzed'],
        'avg_score': data['summary_stats']['avg_score'],
        'successful_scrapes': metadata['scraping_performance']['successful_scrapes'],
        'cache_hits': metadata['scraping_performance']['cached_results'],
        'claude_enabled': metadata['claude_ai_enabled']
    }
    
    # Template HTML
    html_template = f"""
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>VivaTech Analyzer V2 - Dashboard</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        .header h1 {{
            margin: 0;
            font-size: 2.5em;
            font-weight: 300;
        }}
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            padding: 30px;
            background: #f8f9fa;
        }}
        .stat-card {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }}
        .stat-value {{
            font-size: 2em;
            font-weight: bold;
            color: #667eea;
        }}
        .chart-container {{
            padding: 30px;
        }}
        .startup-list {{
            padding: 30px;
            background: #f8f9fa;
        }}
        .startup-item {{
            background: white;
            margin: 10px 0;
            padding: 20px;
            border-radius: 10px;
            border-left: 5px solid #667eea;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .startup-name {{
            font-size: 1.2em;
            font-weight: bold;
            color: #333;
        }}
        .startup-score {{
            font-size: 1.5em;
            font-weight: bold;
            color: #667eea;
            float: right;
        }}
        .startup-details {{
            margin-top: 10px;
            color: #666;
        }}
        .tags {{
            margin-top: 10px;
        }}
        .tag {{
            display: inline-block;
            background: #667eea;
            color: white;
            padding: 3px 8px;
            border-radius: 15px;
            font-size: 0.8em;
            margin: 2px;
        }}
        .version-badge {{
            background: #28a745;
            color: white;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.9em;
            margin-left: 10px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 VivaTech Analyzer V2<span class="version-badge">Haute Performance</span></h1>
            <p>Analyse intelligente des startups VivaTech avec IA et cache</p>
            <p>📅 Généré le {datetime.now().strftime('%d/%m/%Y à %H:%M:%S')}</p>
        </div>
        
        <div class="stats">
            <div class="stat-card">
                <div class="stat-value">{stats['total_analyzed']}</div>
                <div>Startups analysées</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{stats['avg_score']:.1f}</div>
                <div>Score moyen</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{stats['successful_scrapes']}</div>
                <div>Sites scrapés</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{'✅' if stats['claude_enabled'] else '❌'}</div>
                <div>Claude AI</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{stats['cache_hits']}</div>
                <div>Cache utilisé</div>
            </div>
        </div>
        
        <div class="chart-container">
            <div id="top-startups-chart"></div>
        </div>
        
        {"<div class='chart-container'><div id='tags-chart'></div></div>" if fig_tags else ""}
        
        <div class="startup-list">
            <h2>🏆 Top Startups Détaillées</h2>
"""

    # Ajout des startups
    for i, startup in enumerate(top_20, 1):
        tags_html = ""
        if startup['claude_analysis'].get('tags'):
            tags_html = "".join([f'<span class="tag">{tag}</span>' for tag in startup['claude_analysis']['tags']])
        
        html_template += f"""
            <div class="startup-item">
                <div class="startup-score">{startup['total_score']:.1f}</div>
                <div class="startup-name">{i}. {startup['name']}</div>
                <div class="startup-details">
                    <strong>Site:</strong> <a href="{startup['website']}" target="_blank">{startup['website']}</a><br>
                    <strong>Hall:</strong> {startup.get('hall', 'N/A')} | 
                    <strong>Présence:</strong> {startup.get('days_presence', 'N/A')}<br>
                    <strong>Description:</strong> {startup['description'][:200]}...
                </div>
                <div class="tags">{tags_html}</div>
            </div>
"""

    html_template += """
        </div>
    </div>
    
    <script>
"""

    # Ajout du graphique top startups
    html_template += f"""
        var topStartupsData = {fig_top.to_json()};
        Plotly.newPlot('top-startups-chart', topStartupsData.data, topStartupsData.layout);
"""

    # Ajout du graphique des tags si disponible
    if fig_tags:
        html_template += f"""
        var tagsData = {fig_tags.to_json()};
        Plotly.newPlot('tags-chart', tagsData.data, tagsData.layout);
"""

    html_template += """
    </script>
</body>
</html>
"""

    # Écriture du fichier
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_template)
    
    print(f"📊 Dashboard V2 généré: {output_file}")
    return output_file

if __name__ == "__main__":
    # Recherche du fichier JSON le plus récent
    json_files = [f for f in os.listdir('.') if f.startswith('vivatech_analysis_v2_') and f.endswith('.json')]
    
    if not json_files:
        print("❌ Aucun fichier JSON V2 trouvé")
        exit(1)
    
    # Prendre le plus récent
    latest_json = max(json_files, key=lambda x: os.path.getmtime(x))
    print(f"📁 Utilisation du fichier: {latest_json}")
    
    # Génération du dashboard
    dashboard_file = generate_dashboard_from_json(latest_json)
    
    # Ouverture automatique
    import sys
    if sys.platform.startswith('darwin'):  # macOS
        os.system(f'open {dashboard_file}')
    elif sys.platform.startswith('win'):   # Windows
        os.system(f'start {dashboard_file}')
    else:  # Linux
        os.system(f'xdg-open {dashboard_file}')