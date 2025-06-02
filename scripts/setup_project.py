#!/usr/bin/env python3
"""
Script d'initialisation du projet F1 Predictor.

Ce script configure l'environnement de développement et vérifie les dépendances.
"""

import os
import sys
import subprocess
import logging
from pathlib import Path

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def run_command(command: str, check: bool = True) -> subprocess.CompletedProcess:
    """Exécute une commande shell."""
    logger.info(f"Exécution: {command}")
    return subprocess.run(
        command, 
        shell=True, 
        check=check, 
        capture_output=True, 
        text=True
    )


def check_python_version():
    """Vérifie la version de Python."""
    logger.info("🐍 Vérification de la version Python...")
    
    if sys.version_info < (3, 10):
        logger.error("❌ Python 3.10+ requis")
        sys.exit(1)
    
    logger.info(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} détecté")


def create_virtual_environment():
    """Crée un environnement virtuel."""
    logger.info("🔧 Création de l'environnement virtuel...")
    
    venv_path = Path("venv")
    if venv_path.exists():
        logger.info("⚠️ Environnement virtuel existant détecté")
        return
    
    try:
        run_command("python -m venv venv")
        logger.info("✅ Environnement virtuel créé")
    except subprocess.CalledProcessError as e:
        logger.error(f"❌ Erreur lors de la création du venv: {e}")
        sys.exit(1)


def install_dependencies():
    """Installe les dépendances."""
    logger.info("📦 Installation des dépendances...")
    
    # Détection de l'OS pour l'activation du venv
    if os.name == 'nt':  # Windows
        pip_path = "venv\\Scripts\\pip"
    else:  # Unix/Linux/macOS
        pip_path = "venv/bin/pip"
    
    try:
        # Mise à jour de pip
        run_command(f"{pip_path} install --upgrade pip")
        
        # Installation des dépendances de développement
        run_command(f"{pip_path} install -r requirements-dev.txt")
        
        # Installation du package en mode développement
        run_command(f"{pip_path} install -e .")
        
        logger.info("✅ Dépendances installées")
    except subprocess.CalledProcessError as e:
        logger.error(f"❌ Erreur lors de l'installation: {e}")
        sys.exit(1)


def setup_pre_commit():
    """Configure les hooks pre-commit."""
    logger.info("🔗 Configuration des hooks pre-commit...")
    
    if os.name == 'nt':  # Windows
        precommit_path = "venv\\Scripts\\pre-commit"
    else:  # Unix/Linux/macOS
        precommit_path = "venv/bin/pre-commit"
    
    try:
        run_command(f"{precommit_path} install")
        logger.info("✅ Hooks pre-commit configurés")
    except subprocess.CalledProcessError as e:
        logger.warning(f"⚠️ Erreur lors de la configuration pre-commit: {e}")


def create_env_file():
    """Crée le fichier .env à partir de .env.example."""
    logger.info("⚙️ Configuration du fichier d'environnement...")
    
    env_example = Path(".env.example")
    env_file = Path(".env")
    
    if env_file.exists():
        logger.info("⚠️ Fichier .env existant détecté")
        return
    
    if env_example.exists():
        try:
            env_file.write_text(env_example.read_text())
            logger.info("✅ Fichier .env créé à partir de .env.example")
        except Exception as e:
            logger.warning(f"⚠️ Erreur lors de la création du .env: {e}")
    else:
        logger.warning("⚠️ Fichier .env.example non trouvé")


def verify_installation():
    """Vérifie l'installation."""
    logger.info("🔍 Vérification de l'installation...")
    
    if os.name == 'nt':  # Windows
        python_path = "venv\\Scripts\\python"
    else:  # Unix/Linux/macOS
        python_path = "venv/bin/python"
    
    try:
        # Test d'import du package principal
        result = run_command(f"{python_path} -c 'import src; print(\"✅ Package src importé\")'")
        logger.info(result.stdout.strip())
        
        # Test des dépendances principales
        result = run_command(f"{python_path} -c 'import pandas, numpy, sklearn; print(\"✅ Dépendances ML importées\")'")
        logger.info(result.stdout.strip())
        
        logger.info("✅ Installation vérifiée avec succès")
    except subprocess.CalledProcessError as e:
        logger.error(f"❌ Erreur lors de la vérification: {e}")


def print_next_steps():
    """Affiche les prochaines étapes."""
    logger.info("\n🎉 Configuration terminée !")
    
    activation_cmd = "venv\\Scripts\\activate" if os.name == 'nt' else "source venv/bin/activate"
    
    print(f"""
📋 Prochaines étapes:

1. Activer l'environnement virtuel:
   {activation_cmd}

2. Lancer l'exploration des données:
   jupyter notebook notebooks/01_data_exploration.ipynb

3. Démarrer l'API de développement:
   uvicorn api.main:app --reload

4. Lancer l'interface Streamlit:
   streamlit run web/streamlit/app.py

5. Exécuter les tests:
   pytest tests/

📚 Documentation:
   - README.md pour le guide général
   - CONTRIBUTING.md pour contribuer
   - docs/ pour la documentation détaillée

🚀 Bon développement !
""")


def main():
    """Fonction principale."""
    logger.info("🏎️ Initialisation du projet F1 Predictor")
    
    try:
        check_python_version()
        create_virtual_environment()
        install_dependencies()
        setup_pre_commit()
        create_env_file()
        verify_installation()
        print_next_steps()
        
    except KeyboardInterrupt:
        logger.info("\n⚠️ Installation interrompue par l'utilisateur")
        sys.exit(1)
    except Exception as e:
        logger.error(f"❌ Erreur inattendue: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 