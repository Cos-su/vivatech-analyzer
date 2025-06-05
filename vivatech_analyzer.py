#!/usr/bin/env python3
"""
VivaTech Startup Analyzer V2 - Version Parallélisée avec IA
Analyse et score les startups présentes à VivaTech avec performance optimisée
"""

import pandas as pd
import asyncio
import aiohttp
from bs4 import BeautifulSoup
import time
import re
import json
from urllib.parse import urljoin, urlparse
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from typing import Dict, List, Tuple, Optional
import warnings
from tqdm.asyncio import tqdm
import anthropic
from diskcache import Cache
import hashlib
from datetime import datetime, timedelta
import ssl
import certifi

warnings.filterwarnings('ignore')

class CacheManager:
    """Gestionnaire de cache intelligent pour éviter les re-scrapping"""
    
    def __init__(self, cache_dir='./cache', cache_duration_days=7):
        self.cache = Cache(cache_dir)
        self.cache_duration = timedelta(days=cache_duration_days)
    
    def get_cache_key(self, url: str) -> str:
        """Génère une clé de cache unique pour l'URL"""
        return hashlib.md5(url.encode()).hexdigest()
    
    def get_cached_content(self, url: str) -> Optional[Dict]:
        """Récupère le contenu en cache s'il est encore valide"""
        cache_key = self.get_cache_key(url)
        cached_data = self.cache.get(cache_key)
        
        if cached_data and 'timestamp' in cached_data:
            cached_time = datetime.fromisoformat(cached_data['timestamp'])
            if datetime.now() - cached_time < self.cache_duration:
                return cached_data['content']
        
        return None
    
    def cache_content(self, url: str, content: Dict):
        """Met en cache le contenu avec timestamp"""
        cache_key = self.get_cache_key(url)
        cache_data = {
            'content': content,
            'timestamp': datetime.now().isoformat()
        }
        self.cache.set(cache_key, cache_data)

class ClaudeAnalyzer:
    """Analyseur sémantique utilisant l'API Claude"""
    
    def __init__(self, api_key: str = None):
        if api_key:
            self.client = anthropic.Anthropic(api_key=api_key)
            self.enabled = True
        else:
            self.client = None
            self.enabled = False
            print("⚠️ API Claude non configurée - utilisation scoring classique")
    
    def analyze_startup_relevance(self, content: str, description: str, company_name: str) -> Dict:
        """Analyse la pertinence d'une startup avec Claude"""
        if not self.enabled:
            return self._fallback_analysis(content, description)
        
        try:
            # Limitation du contenu pour rester dans les limites de tokens
            content_snippet = content[:2000] if content else ""
            description_snippet = description[:500] if description else ""
            
            prompt = f"""
Analysez cette startup selon ces 4 critères d'innovation (score 0-25 points chacun):

1. **Numérisation de documents** (OCR, scan, digitalisation, capture documentaire)
2. **Valorisation et extraction des données** (data mining, analytics, IA, traitement automatique)
3. **Certification et tiers de confiance** (blockchain, sécurité, authentification, audit, conformité)
4. **Mise à disposition des informations** (dashboards, APIs, portails, collaboration, partage)

**Startup:** {company_name}
**Description:** {description_snippet}
**Contenu site web:** {content_snippet}

Classifiez aussi selon ces tags (plusieurs possibles):
- Edge computing (calcul distribué, IoT, temps réel)
- RSE (durabilité, environnement, éthique, responsabilité)
- Risque augmenté (cybersécurité, fraude, monitoring, conformité)
- Game Changer (technologies disruptives, IA, quantum, innovation)
- Prospective (vision long terme, technologies émergentes)

Répondez UNIQUEMENT en JSON valide:
{{
    "scores": {{
        "numerisation": X,
        "extraction": Y,
        "certification": Z,
        "mise_disposition": W
    }},
    "total_score": SOMME,
    "tags": ["tag1", "tag2"],
    "justification": "Explication courte des scores",
    "keywords_found": ["mot1", "mot2"]
}}
"""
            
            response = self.client.messages.create(
                model="claude-3-haiku-20240307",  # Modèle plus rapide pour le volume
                max_tokens=500,
                messages=[{"role": "user", "content": prompt}]
            )
            
            # Parse de la réponse JSON
            response_text = response.content[0].text.strip()
            
            # Nettoyage pour extraire le JSON
            if response_text.startswith('```json'):
                response_text = response_text.replace('```json', '').replace('```', '').strip()
            
            analysis = json.loads(response_text)
            
            # Validation des scores
            for key in ['numerisation', 'extraction', 'certification', 'mise_disposition']:
                if key not in analysis['scores']:
                    analysis['scores'][key] = 0
                else:
                    analysis['scores'][key] = max(0, min(25, analysis['scores'][key]))
            
            analysis['total_score'] = sum(analysis['scores'].values())
            
            return analysis
            
        except Exception as e:
            print(f"⚠️ Erreur Claude pour {company_name}: {e}")
            return self._fallback_analysis(content, description)
    
    def _fallback_analysis(self, content: str, description: str) -> Dict:
        """Analyse de fallback si Claude n'est pas disponible"""
        combined_text = f"{content} {description}".lower()
        
        keywords_mapping = {
            "numerisation": ["ocr", "document", "scan", "digitization", "digitisation", "pdf", "paper", "archive", "capture", "recognition"],
            "extraction": ["data extraction", "data mining", "analytics", "intelligence", "etl", "data processing", "information extraction", "nlp", "text mining"],
            "certification": ["certification", "trust", "blockchain", "security", "authentication", "verification", "compliance", "audit", "identity"],
            "mise_disposition": ["dashboard", "portal", "api", "collaboration", "sharing", "access", "interface", "platform", "workspace"]
        }
        
        scores = {}
        keywords_found = []
        
        for criterion, keywords in keywords_mapping.items():
            score = 0
            criterion_keywords = []
            
            for keyword in keywords:
                count = combined_text.count(keyword.lower())
                if count > 0:
                    score += count
                    criterion_keywords.append(keyword)
            
            scores[criterion] = min(score * 2.5, 25)  # Normalisation
            keywords_found.extend(criterion_keywords)
        
        return {
            "scores": scores,
            "total_score": sum(scores.values()),
            "tags": self._assign_fallback_tags(combined_text),
            "justification": "Analyse par mots-clés (Claude indisponible)",
            "keywords_found": keywords_found[:10]
        }
    
    def _assign_fallback_tags(self, text: str) -> List[str]:
        """Attribution de tags de fallback"""
        tag_keywords = {
            "Edge computing": ["edge", "fog", "distributed", "iot", "real-time", "latency"],
            "RSE": ["sustainability", "esg", "carbon", "environment", "social", "governance", "ethics", "responsible", "green"],
            "Risque augmenté": ["cybersecurity", "fraud", "monitoring", "risk", "security", "compliance", "regulation"],
            "Game Changer": ["disruption", "innovation", "breakthrough", "revolutionary", "transformation", "ai", "quantum"],
            "Prospective": ["future", "vision", "roadmap", "strategy", "long-term", "emerging", "next-gen"]
        }
        
        assigned_tags = []
        for tag, keywords in tag_keywords.items():
            if any(keyword in text for keyword in keywords):
                assigned_tags.append(tag)
        
        return assigned_tags

class AsyncWebScraper:
    """Scraper web asynchrone haute performance"""
    
    def __init__(self, max_concurrent=20, cache_manager=None, timeout=10):
        self.max_concurrent = max_concurrent
        self.cache_manager = cache_manager
        self.timeout = timeout
        self.session = None
        
        # Configuration SSL pour éviter les erreurs de certificat
        self.ssl_context = ssl.create_default_context(cafile=certifi.where())
        
    async def __aenter__(self):
        """Entrée du context manager"""
        connector = aiohttp.TCPConnector(
            limit=self.max_concurrent,
            ssl=self.ssl_context,
            enable_cleanup_closed=True
        )
        
        timeout = aiohttp.ClientTimeout(total=self.timeout)
        
        self.session = aiohttp.ClientSession(
            connector=connector,
            timeout=timeout,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'fr-FR,fr;q=0.9,en;q=0.8',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
            }
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Sortie du context manager"""
        if self.session:
            await self.session.close()
    
    async def scrape_single_website(self, url: str, semaphore: asyncio.Semaphore) -> Dict:
        """Scrape un site web unique avec limitation de concurrence"""
        if not url or pd.isna(url):
            return {"content": "", "title": "", "error": "URL manquante", "url": url, "status": "failed"}
        
        # Vérification du cache d'abord
        if self.cache_manager:
            cached_content = self.cache_manager.get_cached_content(url)
            if cached_content:
                return {**cached_content, "status": "cached"}
        
        # Nettoyage de l'URL
        url = str(url).strip()
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        async with semaphore:  # Limitation de concurrence
            try:
                async with self.session.get(url) as response:
                    if response.status == 200:
                        content = await response.text()
                        
                        # Parsing avec BeautifulSoup
                        soup = BeautifulSoup(content, 'html.parser')
                        
                        # Extraction du titre
                        title = soup.find('title')
                        title_text = title.get_text().strip() if title else ""
                        
                        # Suppression des scripts et styles
                        for script in soup(["script", "style", "nav", "footer", "header"]):
                            script.decompose()
                        
                        # Extraction du texte principal
                        main_content = soup.get_text()
                        main_content = re.sub(r'\s+', ' ', main_content).strip()
                        
                        result = {
                            "content": main_content[:3000],  # Limitation pour les performances
                            "title": title_text,
                            "url": url,
                            "status": "success",
                            "scraped_at": datetime.now().isoformat()
                        }
                        
                        # Mise en cache
                        if self.cache_manager:
                            self.cache_manager.cache_content(url, result)
                        
                        return result
                    
                    else:
                        return {
                            "content": "", 
                            "title": "", 
                            "error": f"HTTP {response.status}", 
                            "url": url, 
                            "status": "failed"
                        }
                        
            except asyncio.TimeoutError:
                return {"content": "", "title": "", "error": "Timeout", "url": url, "status": "timeout"}
            except Exception as e:
                return {"content": "", "title": "", "error": str(e), "url": url, "status": "failed"}
    
    async def scrape_websites_batch(self, urls: List[str], progress_callback=None) -> List[Dict]:
        """Scrape une liste d'URLs en parallèle avec barre de progression"""
        semaphore = asyncio.Semaphore(self.max_concurrent)
        
        # Création des tâches
        tasks = [self.scrape_single_website(url, semaphore) for url in urls]
        
        # Exécution avec barre de progression
        if progress_callback:
            results = []
            for coro in tqdm.as_completed(tasks, desc="Scraping sites web"):
                result = await coro
                results.append(result)
                if progress_callback:
                    progress_callback(len(results), len(urls))
        else:
            results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Gestion des exceptions
        processed_results = []
        for result in results:
            if isinstance(result, Exception):
                processed_results.append({
                    "content": "", 
                    "title": "", 
                    "error": str(result), 
                    "status": "exception"
                })
            else:
                processed_results.append(result)
        
        return processed_results

class VivaTechAnalyzerV2:
    """Analyseur VivaTech V2 avec performances optimisées"""
    
    def __init__(self, csv_file_path: str, claude_api_key: str = None):
        self.csv_file_path = csv_file_path
        self.df = None
        self.scored_startups = []
        
        # Composants
        self.cache_manager = CacheManager()
        self.claude_analyzer = ClaudeAnalyzer(claude_api_key)
        
        print(f"🚀 VivaTech Analyzer V2 initialisé")
        print(f"   Cache: {'✅ Activé' if self.cache_manager else '❌ Désactivé'}")
        print(f"   Claude AI: {'✅ Activé' if self.claude_analyzer.enabled else '❌ Désactivé'}")
    
    def load_data(self) -> bool:
        """Charge et nettoie les données du CSV"""
        try:
            encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
            
            for encoding in encodings:
                try:
                    self.df = pd.read_csv(self.csv_file_path, sep=';', encoding=encoding, skiprows=1)
                    print(f"✅ Données chargées avec l'encodage {encoding}")
                    break
                except UnicodeDecodeError:
                    continue
            
            if self.df is None:
                raise Exception("Impossible de lire le fichier avec les encodages testés")
            
            # Nettoyage des données
            required_cols = ['HOST COMPANY NAME', 'WEBSITE']
            missing_cols = [col for col in required_cols if col not in self.df.columns]
            
            if missing_cols:
                print(f"❌ Colonnes manquantes: {missing_cols}")
                return False
            
            # Filtrage
            initial_count = len(self.df)
            self.df = self.df.dropna(subset=['HOST COMPANY NAME', 'WEBSITE'])
            self.df = self.df[self.df['WEBSITE'].str.strip() != '']
            
            print(f"📊 {len(self.df)} startups avec sites web (sur {initial_count} totales)")
            return True
            
        except Exception as e:
            print(f"❌ Erreur lors du chargement des données: {e}")
            return False
    
    async def analyze_startups_async(self, limit: int = None, max_concurrent: int = 20):
        """Analyse asynchrone des startups avec performances optimisées"""
        if self.df is None:
            print("❌ Veuillez d'abord charger les données")
            return
        
        # Limitation pour les tests
        df_to_analyze = self.df.head(limit) if limit else self.df
        urls_to_scrape = df_to_analyze['WEBSITE'].tolist()
        
        print(f"🚀 Analyse asynchrone de {len(df_to_analyze)} startups")
        print(f"   Concurrence: {max_concurrent} requêtes simultanées")
        print(f"   Cache: {'utilisé' if self.cache_manager else 'désactivé'}")
        
        # Callback pour progression
        def progress_callback(completed, total):
            if completed % 10 == 0 or completed == total:
                print(f"   📊 Progression: {completed}/{total} sites analysés ({completed/total*100:.1f}%)")
        
        # Scraping parallèle
        start_time = time.time()
        
        async with AsyncWebScraper(max_concurrent, self.cache_manager) as scraper:
            website_results = await scraper.scrape_websites_batch(urls_to_scrape, progress_callback)
        
        scraping_time = time.time() - start_time
        print(f"⚡ Scraping terminé en {scraping_time:.1f}s (vs ~{len(df_to_analyze)*2:.0f}s en séquentiel)")
        
        # Analyse sémantique
        print("🧠 Analyse sémantique en cours...")
        analysis_start = time.time()
        
        self.scored_startups = []
        
        for idx, (row_idx, row) in enumerate(df_to_analyze.iterrows()):
            website_data = website_results[idx] if idx < len(website_results) else {}
            
            # Analyse avec Claude ou fallback
            description = str(row.get('DESCRIPTION', '')) if pd.notna(row.get('DESCRIPTION')) else ''
            content = website_data.get('content', '')
            company_name = row['HOST COMPANY NAME']
            
            # Analyse sémantique
            analysis = self.claude_analyzer.analyze_startup_relevance(content, description, company_name)
            
            # Compilation des résultats
            startup_data = {
                "name": company_name,
                "website": row['WEBSITE'],
                "description": description,
                "country": row.get('COUNTRY', ''),
                "business_sector": row.get('BUSINESS-SECTOR', ''),
                "hall": row.get('HALL', ''),
                "days_presence": row.get('DAYS OF PRESENCE', ''),
                "website_content": content[:500],
                "website_title": website_data.get('title', ''),
                "scraping_status": website_data.get('status', 'unknown'),
                "total_score": analysis['total_score'],
                "claude_analysis": analysis,
                "raw_data": row.to_dict()
            }
            
            self.scored_startups.append(startup_data)
            
            # Progression
            if (idx + 1) % 10 == 0:
                print(f"   🧠 Analysées: {idx + 1}/{len(df_to_analyze)}")
        
        analysis_time = time.time() - analysis_start
        total_time = time.time() - start_time
        
        print(f"✅ Analyse terminée!")
        print(f"   📊 Temps total: {total_time:.1f}s")
        print(f"   ⚡ Scraping: {scraping_time:.1f}s")
        print(f"   🧠 Analyse: {analysis_time:.1f}s")
        print(f"   🚀 Gain vs V1: ~{((len(df_to_analyze)*2)/total_time):.1f}x plus rapide")
    
    def run_analysis(self, limit: int = None, max_concurrent: int = 20):
        """Point d'entrée principal pour l'analyse"""
        try:
            # Exécution de l'analyse asynchrone
            asyncio.run(self.analyze_startups_async(limit, max_concurrent))
        except Exception as e:
            print(f"❌ Erreur lors de l'analyse: {e}")
            raise
    
    def print_top_recommendations(self, top_n: int = 10):
        """Affiche les meilleures recommandations avec analyse Claude"""
        if not self.scored_startups:
            print("❌ Aucune startup analysée")
            return
        
        sorted_startups = sorted(self.scored_startups, key=lambda x: x['total_score'], reverse=True)
        
        print(f"\n🏆 TOP {top_n} DES STARTUPS LES PLUS PERTINENTES (V2):")
        print("=" * 80)
        
        for i, startup in enumerate(sorted_startups[:top_n], 1):
            analysis = startup['claude_analysis']
            
            print(f"\n{i}. {startup['name']}")
            print(f"   Score: {startup['total_score']:.1f}/100")
            print(f"   Site: {startup['website']}")
            print(f"   Hall: {startup.get('hall', 'N/A')} | Présence: {startup.get('days_presence', 'N/A')}")
            
            if analysis.get('tags'):
                print(f"   Tags: {', '.join(analysis['tags'])}")
            
            print(f"   Description: {startup['description'][:150]}...")
            
            # Scores détaillés
            scores = analysis['scores']
            print("   Scores détaillés:")
            print(f"     • Numérisation documents: {scores.get('numerisation', 0):.1f}/25")
            print(f"     • Extraction données: {scores.get('extraction', 0):.1f}/25")
            print(f"     • Certification/confiance: {scores.get('certification', 0):.1f}/25")
            print(f"     • Mise à disposition info: {scores.get('mise_disposition', 0):.1f}/25")
            
            if analysis.get('justification'):
                print(f"   💡 Analyse: {analysis['justification']}")
            
            print(f"   🔍 Status scraping: {startup['scraping_status']}")
            print("-" * 80)
    
    def export_results_v2(self, filename: str = None):
        """Exporte les résultats V2 avec métadonnées enrichies"""
        if not self.scored_startups:
            print("❌ Aucune startup analysée")
            return
        
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"vivatech_analysis_v2_{timestamp}.json"
        
        # Tri par score décroissant
        sorted_startups = sorted(self.scored_startups, key=lambda x: x['total_score'], reverse=True)
        
        # Statistiques de performance
        scraping_stats = {
            'total_analyzed': len(sorted_startups),
            'successful_scrapes': len([s for s in sorted_startups if s['scraping_status'] == 'success']),
            'cached_results': len([s for s in sorted_startups if s['scraping_status'] == 'cached']),
            'failed_scrapes': len([s for s in sorted_startups if s['scraping_status'] in ['failed', 'timeout', 'exception']])
        }
        
        # Analyse des tags
        all_tags = []
        for startup in sorted_startups:
            tags = startup['claude_analysis'].get('tags', [])
            all_tags.extend(tags)
        
        tag_distribution = {}
        for tag in all_tags:
            tag_distribution[tag] = tag_distribution.get(tag, 0) + 1
        
        results = {
            "metadata": {
                "version": "2.0",
                "analysis_date": datetime.now().isoformat(),
                "total_analyzed": len(sorted_startups),
                "claude_ai_enabled": self.claude_analyzer.enabled,
                "cache_enabled": self.cache_manager is not None,
                "scraping_performance": scraping_stats,
                "tag_distribution": tag_distribution
            },
            "top_startups": sorted_startups[:100],  # Top 100
            "summary_stats": {
                "avg_score": np.mean([s['total_score'] for s in sorted_startups]),
                "max_score": max([s['total_score'] for s in sorted_startups]),
                "min_score": min([s['total_score'] for s in sorted_startups]),
                "std_score": np.std([s['total_score'] for s in sorted_startups])
            }
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        print(f"📄 Résultats V2 exportés vers {filename}")
        print(f"   📊 Performance scraping: {scraping_stats['successful_scrapes']}/{scraping_stats['total_analyzed']} succès")
        if scraping_stats['cached_results'] > 0:
            print(f"   ⚡ Cache utilisé: {scraping_stats['cached_results']} résultats")
        
        return filename

    def generate_dashboard_v2(self, output_file: str = "dashboard_vivatech.html"):
        """Génère un dashboard HTML interactif avec les résultats V2"""
        if not self.scored_startups:
            print("❌ Aucune startup analysée pour générer le dashboard")
            return False
        
        sorted_startups = sorted(self.scored_startups, key=lambda x: x['total_score'], reverse=True)
        
        # Préparation des données pour Plotly
        top_20 = sorted_startups[:20]
        names = [s['name'][:30] + '...' if len(s['name']) > 30 else s['name'] for s in top_20]
        scores = [s['total_score'] for s in top_20]
        websites = [s['website'] for s in top_20]
        
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
        all_tags = []
        for startup in sorted_startups:
            tags = startup['claude_analysis'].get('tags', [])
            all_tags.extend(tags)
        
        tag_counts = {}
        for tag in all_tags:
            tag_counts[tag] = tag_counts.get(tag, 0) + 1
        
        if tag_counts:
            fig_tags = px.pie(
                values=list(tag_counts.values()),
                names=list(tag_counts.keys()),
                title="📊 Distribution des Tags d'Innovation"
            )
        else:
            fig_tags = None
        
        # Statistiques de performance
        stats = {
            'total_analyzed': len(sorted_startups),
            'avg_score': np.mean([s['total_score'] for s in sorted_startups]),
            'successful_scrapes': len([s for s in sorted_startups if s['scraping_status'] == 'success']),
            'cache_hits': len([s for s in sorted_startups if s['scraping_status'] == 'cached']),
            'claude_enabled': self.claude_analyzer.enabled
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

async def main():
    """Fonction principale pour la démonstration"""
    print("🚀 VIVATECH ANALYZER V2 - VERSION HAUTE PERFORMANCE")
    print("=" * 60)
    
    # Configuration
    CLAUDE_API_KEY = None  # À définir si vous avez une clé API
    CSV_FILE = '/Users/cos/Documents/GitHub/extractVivaTech/VivaTech.csv'
    
    # Initialisation
    analyzer = VivaTechAnalyzerV2(CSV_FILE, CLAUDE_API_KEY)
    
    # Chargement des données
    if not analyzer.load_data():
        return
    
    # Choix du mode d'analyse
    print("\n🎯 OPTIONS D'ANALYSE V2:")
    print("1. Test rapide (20 startups)")
    print("2. Analyse moyenne (100 startups)")  
    print("3. Analyse complète (toutes les startups)")
    
    try:
        choice = input("\nChoisissez une option (1-3): ").strip()
        
        if choice == "1":
            limit = 20
            print(f"🚀 Test rapide avec {limit} startups...")
        elif choice == "2":
            limit = 100
            print(f"🚀 Analyse moyenne avec {limit} startups...")
        elif choice == "3":
            limit = None
            print("🚀 Analyse complète de toutes les startups...")
            print("⚠️  Cela peut prendre 30-60 minutes selon le nombre total")
        else:
            limit = 20
            print("🚀 Choix par défaut: test rapide")
        
        # Analyse
        start_time = time.time()
        await analyzer.analyze_startups_async(limit=limit, max_concurrent=25)
        total_time = time.time() - start_time
        
        # Affichage des résultats
        analyzer.print_top_recommendations(15)
        
        # Export JSON
        json_file = analyzer.export_results_v2()
        
        # Génération du dashboard HTML
        html_file = analyzer.generate_dashboard_v2()
        
        print(f"\n✅ Analyse V2 terminée en {total_time:.1f}s!")
        print("🎉 Performances optimisées - prêt pour la production!")
        
        return html_file
        
    except KeyboardInterrupt:
        print("\n⚠️ Analyse interrompue par l'utilisateur")
    except Exception as e:
        print(f"\n❌ Erreur: {e}")

if __name__ == "__main__":
    asyncio.run(main())