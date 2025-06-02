#!/usr/bin/env python3
"""
Script de début de session de travail pour F1 Predictor.

Ce script automatise toutes les vérifications et préparatifs
nécessaires au début d'une session de développement.
"""

import os
import sys
import subprocess
import logging
from datetime import datetime
from pathlib import Path

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def run_command(command: str, check: bool = True, capture: bool = True) -> subprocess.CompletedProcess:
    """Exécute une commande shell."""
    return subprocess.run(
        command, 
        shell=True, 
        check=check, 
        capture_output=capture, 
        text=True
    )


def print_header():
    """Affiche l'en-tête de début de session."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("=" * 60)
    print("🏎️  F1 PREDICTOR - DÉBUT DE SESSION")
    print(f"📅 {now}")
    print("=" * 60)
    print()


def check_git_status():
    """Vérifie le statut Git et met à jour."""
    logger.info("🔍 Vérification du statut Git...")
    
    try:
        # Vérifier la branche courante
        result = run_command("git branch --show-current")
        current_branch = result.stdout.strip()
        logger.info(f"📍 Branche courante: {current_branch}")
        
        # Vérifier s'il y a des modifications non commitées
        result = run_command("git status --porcelain")
        if result.stdout.strip():
            logger.warning("⚠️ Modifications non commitées détectées:")
            run_command("git status", capture=False)
            
            response = input("\n🤔 Voulez-vous continuer ? (y/N): ")
            if response.lower() != 'y':
                logger.info("Session annulée")
                sys.exit(0)
        
        # Fetch et pull
        logger.info("📥 Mise à jour depuis le repository distant...")
        run_command("git fetch origin")
        
        if current_branch in ['main', 'master', 'develop']:
            run_command("git pull origin " + current_branch)
            logger.info("✅ Repository mis à jour")
        else:
            logger.info(f"ℹ️ Sur branche feature '{current_branch}' - pull manuel si nécessaire")
            
    except subprocess.CalledProcessError as e:
        logger.error(f"❌ Erreur Git: {e}")
        sys.exit(1)


def check_python_environment():
    """Vérifie et active l'environnement Python."""
    logger.info("🐍 Vérification de l'environnement Python...")
    
    # Vérifier si on est dans un venv
    in_venv = hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
    
    if not in_venv:
        logger.warning("⚠️ Environnement virtuel non activé")
        print("💡 Pour activer l'environnement:")
        print("   source venv/bin/activate  # macOS/Linux")
        print("   venv\\Scripts\\activate     # Windows")
        print()
        
        response = input("🤔 Voulez-vous continuer sans venv ? (y/N): ")
        if response.lower() != 'y':
            sys.exit(0)
    else:
        logger.info(f"✅ Environnement virtuel actif: {sys.prefix}")
    
    # Vérifier la version Python
    if sys.version_info < (3, 10):
        logger.error("❌ Python 3.10+ requis")
        sys.exit(1)
    
    logger.info(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} OK")


def check_dependencies():
    """Vérifie les dépendances principales."""
    logger.info("📦 Vérification des dépendances...")
    
    critical_packages = [
        ('pandas', 'pd'),
        ('numpy', 'np'),
        ('sklearn', 'sklearn'),
        ('fastapi', 'fastapi'),
        ('src', 'src')
    ]
    
    failed_imports = []
    
    for package, import_name in critical_packages:
        try:
            __import__(import_name)
            logger.info(f"✅ {package} disponible")
        except ImportError:
            failed_imports.append(package)
            logger.warning(f"⚠️ {package} non trouvé")
    
    if failed_imports:
        logger.warning(f"🔧 Packages manquants: {', '.join(failed_imports)}")
        response = input("🤔 Voulez-vous installer les dépendances ? (Y/n): ")
        if response.lower() != 'n':
            try:
                run_command("pip install -r requirements-dev.txt")
                logger.info("✅ Dépendances installées")
            except subprocess.CalledProcessError as e:
                logger.error(f"❌ Erreur installation: {e}")


def check_project_state():
    """Vérifie l'état du projet."""
    logger.info("📊 Vérification de l'état du projet...")
    
    # Vérifier les dossiers de données
    data_folders = ['data/raw', 'data/processed', 'data/features']
    for folder in data_folders:
        path = Path(folder)
        if path.exists():
            count = len(list(path.iterdir()))
            logger.info(f"📁 {folder}: {count} fichiers")
        else:
            logger.warning(f"📁 {folder}: dossier non trouvé")
    
    # Vérifier les modèles
    models_path = Path('models/trained')
    if models_path.exists():
        model_count = len(list(models_path.glob('*.joblib')))
        logger.info(f"🤖 Modèles entraînés: {model_count}")
    
    # Vérifier les tests récents
    try:
        result = run_command("pytest tests/ --collect-only -q")
        test_count = len([line for line in result.stdout.split('\n') if 'test session starts' not in line and line.strip()])
        logger.info(f"🧪 Tests disponibles: ~{test_count}")
    except:
        logger.warning("⚠️ Impossible de compter les tests")


def run_health_checks():
    """Lance des tests de santé rapides."""
    logger.info("🏥 Tests de santé...")
    
    # Test import principal
    try:
        result = run_command("python -c \"import src; print('✅ Package principal OK')\"")
        logger.info(result.stdout.strip())
    except subprocess.CalledProcessError:
        logger.error("❌ Problème avec le package principal")
    
    # Test API (optionnel)
    try:
        result = run_command("python -c \"from api.main import app; print('✅ API OK')\"")
        logger.info(result.stdout.strip())
    except subprocess.CalledProcessError:
        logger.warning("⚠️ API non accessible (normal si pas encore implémentée)")
    
    # Test rapide des imports ML
    try:
        result = run_command("python -c \"import pandas as pd, numpy as np; print('✅ ML libs OK')\"")
        logger.info(result.stdout.strip())
    except subprocess.CalledProcessError:
        logger.error("❌ Problème avec les librairies ML")


def plan_session():
    """Aide à planifier la session."""
    print("\n" + "=" * 60)
    print("🎯 PLANIFICATION DE SESSION")
    print("=" * 60)
    
    print("\n📋 Questions de planification:")
    
    # Objectifs de la session
    print("\n1. Quels sont vos objectifs pour cette session ?")
    print("   Exemples:")
    print("   - Implémenter le collecteur FastF1")
    print("   - Créer les features de moyennes glissantes")
    print("   - Tester le modèle XGBoost")
    print("   - Documenter l'API")
    
    objectives = input("\n🎯 Vos objectifs (séparez par des virgules): ")
    
    # Estimation du temps
    duration = input("⏱️  Durée estimée de la session (ex: 2h): ")
    
    # Branche de travail
    current_branch = run_command("git branch --show-current").stdout.strip()
    print(f"\n🌿 Branche courante: {current_branch}")
    
    if current_branch in ['main', 'master']:
        create_branch = input("❓ Voulez-vous créer une nouvelle branche ? (Y/n): ")
        if create_branch.lower() != 'n':
            branch_name = input("📝 Nom de la branche (ex: feature/collecteur-fastf1): ")
            if branch_name:
                try:
                    run_command(f"git checkout -b {branch_name}")
                    logger.info(f"✅ Branche '{branch_name}' créée et activée")
                except subprocess.CalledProcessError as e:
                    logger.error(f"❌ Erreur création branche: {e}")
    
    # Sauvegarde du plan
    session_plan = f"""# Session du {datetime.now().strftime('%Y-%m-%d %H:%M')}

## 🎯 Objectifs
{chr(10).join(['- [ ] ' + obj.strip() for obj in objectives.split(',') if obj.strip()])}

## ⏱️ Durée estimée
{duration}

## 🌿 Branche
{run_command("git branch --show-current").stdout.strip()}

## 📝 Notes
[À remplir pendant la session]

---
Généré automatiquement par start_session.py
"""
    
    with open('session_plan.md', 'w') as f:
        f.write(session_plan)
    
    logger.info("📝 Plan de session sauvegardé dans session_plan.md")


def print_summary():
    """Affiche le résumé final."""
    print("\n" + "=" * 60)
    print("✅ SESSION PRÊTE !")
    print("=" * 60)
    print()
    print("📋 Prochaines actions suggérées:")
    print("   1. Consultez session_plan.md pour vos objectifs")
    print("   2. Lancez votre IDE/éditeur préféré")
    print("   3. Ouvrez un terminal pour les commandes")
    print("   4. Commencez par les tests: pytest tests/")
    print()
    print("🔧 Commandes utiles:")
    print("   pytest tests/                    # Lancer les tests")
    print("   jupyter notebook notebooks/      # Explorer les données")
    print("   uvicorn api.main:app --reload    # Démarrer l'API")
    print("   black src/ api/ tests/           # Formater le code")
    print()
    print("📚 Documentation:")
    print("   docs/workflow-session.md         # Guide de workflow")
    print("   docs/installation.md             # Guide d'installation")
    print("   CONTRIBUTING.md                  # Guide de contribution")
    print()
    print("🎉 Bon développement !")
    print("=" * 60)


def main():
    """Fonction principale."""
    try:
        print_header()
        check_git_status()
        check_python_environment()
        check_dependencies()
        check_project_state()
        run_health_checks()
        plan_session()
        print_summary()
        
    except KeyboardInterrupt:
        print("\n⚠️ Session d'initialisation interrompue")
        sys.exit(1)
    except Exception as e:
        logger.error(f"❌ Erreur inattendue: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 