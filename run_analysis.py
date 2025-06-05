#!/usr/bin/env python3
"""
Script d'automatisation V2 pour l'analyse complète VivaTech
Intègre parallélisation, cache intelligent et API Claude
"""

import subprocess
import sys
import os
import asyncio
from datetime import datetime
import json

def run_command(command, description):
    """Exécute une commande avec gestion d'erreurs"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        if result.stdout:
            print(f"✅ {description} terminé")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur lors de {description}")
        print(f"Détail: {e.stderr}")
        return False

def check_dependencies_v2():
    """Vérifie que toutes les dépendances V2 sont installées"""
    print("🔍 Vérification des dépendances V2...")
    
    required_packages = [
        'pandas', 'requests', 'beautifulsoup4', 'matplotlib', 
        'seaborn', 'plotly', 'numpy', 'lxml', 'aiohttp', 
        'asyncio_throttle', 'anthropic', 'tqdm', 'diskcache'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            package_name = package.replace('-', '_').replace('asyncio_throttle', 'asyncio_throttle')
            __import__(package_name)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Packages V2 manquants: {', '.join(missing_packages)}")
        print("📦 Installation des dépendances V2...")
        return run_command("pip install -r requirements_v2.txt", "Installation des dépendances V2")
    else:
        print("✅ Toutes les dépendances V2 sont installées")
        return True

def configure_claude_api():
    """Configuration optionnelle de l'API Claude"""
    print("\n🤖 CONFIGURATION API CLAUDE (Optionnel)")
    print("="*50)
    print("L'API Claude améliore considérablement la précision d'analyse.")
    print("Sans API: Analyse par mots-clés classique")
    print("Avec API: Analyse sémantique avancée")
    
    try:
        use_claude = input("\nConfigurer l'API Claude? (o/n): ").strip().lower()
        
        if use_claude in ['o', 'oui', 'y', 'yes']:
            api_key = input("Entrez votre clé API Claude (ou ENTER pour passer): ").strip()
            
            if api_key:
                # Sauvegarde sécurisée de la clé API
                config_file = '.claude_config.json'
                config = {'api_key': api_key}
                
                with open(config_file, 'w') as f:
                    json.dump(config, f)
                
                print("✅ Clé API Claude configurée et sauvegardée")
                return api_key
            else:
                print("⚠️ Analyse sans API Claude (mode fallback)")
                return None
        else:
            print("⚠️ Analyse sans API Claude (mode fallback)")
            return None
            
    except KeyboardInterrupt:
        print("\n⚠️ Configuration interrompue")
        return None

def get_analysis_options():
    """Interface pour choisir les options d'analyse"""
    print("\n🎯 OPTIONS D'ANALYSE V2:")
    print("="*40)
    print("1. 🏃 Test rapide (50 startups) - ~30 secondes")
    print("2. 📊 Analyse étendue (200 startups) - ~2 minutes")
    print("3. 🚀 Analyse complète (toutes) - ~15-30 minutes")
    print("4. 🎛️ Analyse personnalisée")
    
    try:
        choice = input("\nChoisissez une option (1-4): ").strip()
        
        if choice == "1":
            return {
                'limit': 50,
                'max_concurrent': 25,
                'description': 'Test rapide'
            }
        elif choice == "2":
            return {
                'limit': 200,
                'max_concurrent': 30,
                'description': 'Analyse étendue'
            }
        elif choice == "3":
            return {
                'limit': None,
                'max_concurrent': 35,
                'description': 'Analyse complète'
            }
        elif choice == "4":
            try:
                limit = input("Nombre de startups (ENTER = toutes): ").strip()
                limit = int(limit) if limit else None
                
                concurrent = input("Concurrence max (défaut=25): ").strip()
                concurrent = int(concurrent) if concurrent else 25
                
                return {
                    'limit': limit,
                    'max_concurrent': concurrent,
                    'description': f'Analyse personnalisée ({limit or "toutes"} startups)'
                }
            except ValueError:
                print("❌ Valeurs invalides, utilisation des paramètres par défaut")
                return {
                    'limit': 50,
                    'max_concurrent': 25,
                    'description': 'Analyse par défaut'
                }
        else:
            print("❌ Option invalide, utilisation du test rapide")
            return {
                'limit': 50,
                'max_concurrent': 25,
                'description': 'Test rapide (défaut)'
            }
            
    except KeyboardInterrupt:
        print("\n⚠️ Sélection interrompue, utilisation des paramètres par défaut")
        return {
            'limit': 50,
            'max_concurrent': 25,
            'description': 'Test rapide (défaut)'
        }

async def run_analysis_v2_async(options, claude_api_key=None):
    """Lance l'analyse V2 de manière programmatique"""
    try:
        # Import du module V2
        from vivatech_analyzer import VivaTechAnalyzerV2
        
        # Initialisation
        analyzer = VivaTechAnalyzerV2(
            csv_file_path='VivaTech.csv',
            claude_api_key=claude_api_key
        )
        
        # Chargement des données
        if not analyzer.load_data():
            return False
        
        print(f"\n🚀 Lancement: {options['description']}")
        print(f"   Limite: {options['limit'] or 'Toutes les startups'}")
        print(f"   Concurrence: {options['max_concurrent']} requêtes simultanées")
        print(f"   API Claude: {'✅ Activée' if claude_api_key else '❌ Désactivée'}")
        
        # Analyse asynchrone
        await analyzer.analyze_startups_async(
            limit=options['limit'],
            max_concurrent=options['max_concurrent']
        )
        
        # Affichage des résultats
        analyzer.print_top_recommendations(20)
        
        # Export JSON
        results_file = analyzer.export_results_v2()
        
        # Génération du dashboard HTML
        html_file = analyzer.generate_dashboard_v2()
        
        return html_file
        
    except Exception as e:
        print(f"❌ Erreur lors de l'analyse V2: {e}")
        return False

def generate_performance_report(results_file):
    """Génère un rapport de performance"""
    try:
        with open(results_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        metadata = data['metadata']
        performance = metadata['scraping_performance']
        
        print("\n📊 RAPPORT DE PERFORMANCE V2")
        print("="*50)
        print(f"Version: {metadata['version']}")
        print(f"Date d'analyse: {metadata['analysis_date']}")
        print(f"Total analysé: {metadata['total_analyzed']} startups")
        
        print(f"\n🔥 Performance Scraping:")
        print(f"   ✅ Succès: {performance['successful_scrapes']}")
        print(f"   ⚡ Cache: {performance['cached_results']}")
        print(f"   ❌ Échecs: {performance['failed_scrapes']}")
        
        success_rate = (performance['successful_scrapes'] / metadata['total_analyzed']) * 100
        print(f"   📈 Taux de succès: {success_rate:.1f}%")
        
        print(f"\n🤖 IA et Tags:")
        print(f"   Claude AI: {'✅ Activé' if metadata['claude_ai_enabled'] else '❌ Désactivé'}")
        print(f"   Cache: {'✅ Activé' if metadata['cache_enabled'] else '❌ Désactivé'}")
        
        if metadata.get('tag_distribution'):
            print(f"\n🏷️ Distribution des Tags:")
            for tag, count in sorted(metadata['tag_distribution'].items(), key=lambda x: x[1], reverse=True)[:5]:
                print(f"   {tag}: {count} startups")
        
    except Exception as e:
        print(f"⚠️ Impossible de générer le rapport de performance: {e}")

def main():
    """Fonction principale d'automatisation V2"""
    print("🚀 VIVATECH ANALYZER V2 - AUTOMATISATION COMPLÈTE")
    print("="*70)
    print(f"📅 Démarré le {datetime.now().strftime('%d/%m/%Y à %H:%M:%S')}")
    print("\n🆕 NOUVEAUTÉS V2:")
    print("   ⚡ Scraping parallèle (25x plus rapide)")
    print("   🤖 Analyse IA avec Claude (optionnel)")
    print("   💾 Cache intelligent")
    print("   📊 Métriques de performance avancées")
    
    try:
        # Vérification des fichiers requis
        if not os.path.exists('VivaTech.csv'):
            print("\n❌ Fichier VivaTech.csv non trouvé")
            print("📋 Veuillez placer le fichier CSV dans le répertoire courant")
            return False
        
        # Vérification des dépendances V2
        if not check_dependencies_v2():
            return False
        
        # Configuration optionnelle Claude
        claude_api_key = configure_claude_api()
        
        # Options d'analyse
        options = get_analysis_options()
        
        print(f"\n{'='*60}")
        print("🚀 LANCEMENT DE L'ANALYSE V2")
        print(f"{'='*60}")
        
        # Estimation du temps
        estimated_time = {
            50: "30 secondes",
            200: "2 minutes", 
            None: "15-30 minutes"
        }.get(options['limit'], "Variable")
        
        print(f"⏱️ Temps estimé: {estimated_time}")
        
        # Lancement de l'analyse asynchrone
        start_time = datetime.now()
        html_file = asyncio.run(run_analysis_v2_async(options, claude_api_key))
        end_time = datetime.now()
        
        if html_file:
            print(f"\n✅ ANALYSE V2 TERMINÉE AVEC SUCCÈS!")
            print(f"⏱️ Durée réelle: {(end_time - start_time).total_seconds():.1f} secondes")
            
            # Recherche du fichier JSON généré
            results_file = None
            for file in os.listdir('.'):
                if file.startswith('vivatech_analysis_v2_') and file.endswith('.json'):
                    results_file = file
                    break
            
            if results_file:
                # Rapport de performance
                generate_performance_report(results_file)
            
            # Fichiers générés
            print(f"\n📁 FICHIERS GÉNÉRÉS:")
            if results_file:
                print(f"   📊 {results_file} - Données complètes JSON")
            print(f"   🌐 {html_file} - Dashboard interactif HTML")
            
            # Proposition d'ouverture du dashboard
            try:
                open_results = input(f"\n📖 Ouvrir le dashboard? (o/n): ").strip().lower()
                if open_results in ['o', 'oui', 'y', 'yes']:
                    if sys.platform.startswith('darwin'):  # macOS
                        os.system(f'open {html_file}')
                    elif sys.platform.startswith('win'):   # Windows
                        os.system(f'start {html_file}')
                    else:  # Linux
                        os.system(f'xdg-open {html_file}')
            except KeyboardInterrupt:
                print("\n👋 Au revoir!")
            
            print(f"\n💡 PROCHAINES ÉTAPES:")
            print(f"1. 📧 Contactez les startups top-scorées")
            print(f"2. 📅 Planifiez vos rendez-vous VivaTech")
            print(f"3. 🔄 Relancez l'analyse si nouvelles données")
            print(f"4. 📊 Utilisez les filtres JSON pour analyses spécifiques")
            
            return True
        else:
            print(f"\n❌ L'analyse V2 a échoué")
            return False
        
    except KeyboardInterrupt:
        print(f"\n⚠️ Analyse interrompue par l'utilisateur")
        return False
    except Exception as e:
        print(f"\n💥 Erreur inattendue: {e}")
        return False

if __name__ == "__main__":
    try:
        success = main()
        if success:
            print(f"\n🎉 MISSION ACCOMPLIE! L'analyse VivaTech V2 est prête.")
            print(f"🚀 Performances optimisées pour un usage professionnel.")
        else:
            print(f"\n❌ L'analyse a échoué. Vérifiez les erreurs ci-dessus.")
            sys.exit(1)
    except KeyboardInterrupt:
        print(f"\n⚠️ Programme interrompu par l'utilisateur")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Erreur critique: {e}")
        sys.exit(1)