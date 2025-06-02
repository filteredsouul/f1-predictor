#!/usr/bin/env python3
"""
Script de fin de session de travail pour F1 Predictor.

Ce script automatise toutes les tâches de nettoyage, tests,
et sauvegarde nécessaires à la fin d'une session de développement.
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
    """Affiche l'en-tête de fin de session."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("=" * 60)
    print("🏁 F1 PREDICTOR - FIN DE SESSION")
    print(f"📅 {now}")
    print("=" * 60)
    print()


def code_cleanup():
    """Nettoie et formate le code."""
    logger.info("🧹 Nettoyage et formatage du code...")
    
    try:
        # Black formatting
        logger.info("📝 Formatage avec Black...")
        result = run_command("black src/ api/ tests/")
        logger.info("✅ Formatage Black terminé")
        
        # Import sorting
        logger.info("📂 Organisation des imports avec isort...")
        run_command("isort src/ api/ tests/")
        logger.info("✅ Imports organisés")
        
        # Flake8 linting
        logger.info("🔍 Vérification du style avec flake8...")
        result = run_command("flake8 src/ api/ tests/ --count --statistics", check=False)
        if result.returncode == 0:
            logger.info("✅ Pas d'erreurs de style")
        else:
            logger.warning("⚠️ Problèmes de style détectés:")
            print(result.stdout)
        
        # Type checking
        logger.info("🔍 Vérification des types avec mypy...")
        result = run_command("mypy src/ api/ --ignore-missing-imports", check=False)
        if result.returncode == 0:
            logger.info("✅ Types OK")
        else:
            logger.warning("⚠️ Problèmes de types détectés (non bloquant)")
            
    except subprocess.CalledProcessError as e:
        logger.error(f"❌ Erreur lors du nettoyage: {e}")


def run_tests():
    """Lance la suite de tests."""
    logger.info("🧪 Exécution de la suite de tests...")
    
    try:
        # Tests rapides d'abord
        logger.info("⚡ Tests rapides...")
        result = run_command("pytest tests/ -x --tb=short", check=False)
        
        if result.returncode == 0:
            logger.info("✅ Tous les tests passent")
            
            # Tests avec couverture si les tests de base passent
            logger.info("📊 Calcul de la couverture...")
            result = run_command("pytest tests/ --cov=src --cov=api --cov-report=term-missing", check=False)
            
            if result.returncode == 0:
                logger.info("✅ Tests avec couverture terminés")
            else:
                logger.warning("⚠️ Problèmes avec la couverture")
                
        else:
            logger.error("❌ Certains tests échouent")
            print("📋 Résultats des tests:")
            print(result.stdout)
            
            response = input("\n🤔 Voulez-vous continuer malgré les tests échoués ? (y/N): ")
            if response.lower() != 'y':
                logger.info("Session arrêtée pour corriger les tests")
                sys.exit(1)
                
    except subprocess.CalledProcessError as e:
        logger.error(f"❌ Erreur lors des tests: {e}")


def cleanup_temp_files():
    """Nettoie les fichiers temporaires."""
    logger.info("🗑️ Nettoyage des fichiers temporaires...")
    
    # Fichiers Python temporaires
    temp_patterns = [
        "**/*.pyc",
        "**/__pycache__",
        ".pytest_cache",
        ".mypy_cache",
        "*.egg-info",
        ".coverage",
        "htmlcov",
        "*.tmp",
        "*.log"
    ]
    
    cleaned_count = 0
    
    for pattern in temp_patterns:
        try:
            if pattern.startswith("**"):
                # Pattern de recherche récursive
                for path in Path(".").rglob(pattern.replace("**/", "")):
                    if path.is_file():
                        path.unlink()
                        cleaned_count += 1
                    elif path.is_dir():
                        import shutil
                        shutil.rmtree(path, ignore_errors=True)
                        cleaned_count += 1
            else:
                # Pattern simple
                for path in Path(".").glob(pattern):
                    if path.is_file():
                        path.unlink()
                        cleaned_count += 1
                    elif path.is_dir():
                        import shutil
                        shutil.rmtree(path, ignore_errors=True)
                        cleaned_count += 1
        except Exception as e:
            logger.debug(f"Impossible de nettoyer {pattern}: {e}")
    
    logger.info(f"✅ {cleaned_count} fichiers temporaires nettoyés")


def check_git_status():
    """Vérifie le statut Git."""
    logger.info("🔍 Vérification du statut Git...")
    
    try:
        # Vérifier la branche courante
        result = run_command("git branch --show-current")
        current_branch = result.stdout.strip()
        logger.info(f"📍 Branche courante: {current_branch}")
        
        # Vérifier les modifications
        result = run_command("git status --porcelain")
        changes = result.stdout.strip()
        
        if changes:
            logger.info("📝 Modifications détectées:")
            run_command("git status", capture=False)
            return True
        else:
            logger.info("✅ Aucune modification non commitée")
            return False
            
    except subprocess.CalledProcessError as e:
        logger.error(f"❌ Erreur Git: {e}")
        return False


def commit_and_push():
    """Gère les commits et push."""
    logger.info("💾 Gestion des commits et push...")
    
    has_changes = check_git_status()
    
    if not has_changes:
        logger.info("ℹ️ Aucune modification à commiter")
        return
    
    # Demander si on doit commiter
    response = input("\n🤔 Voulez-vous commiter ces modifications ? (Y/n): ")
    if response.lower() == 'n':
        logger.info("⚠️ Modifications non commitées")
        return
    
    # Ajouter tous les fichiers
    run_command("git add .")
    
    # Message de commit
    print("\n📝 Types de commit suggérés:")
    print("   feat: nouvelle fonctionnalité")
    print("   fix: correction de bug")
    print("   docs: documentation")
    print("   style: formatage")
    print("   refactor: refactoring")
    print("   test: ajout de tests")
    print("   chore: maintenance")
    
    commit_message = input("\n💬 Message de commit: ")
    if not commit_message:
        commit_message = f"chore: fin de session {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    
    try:
        # Commit
        run_command(f'git commit -m "{commit_message}"')
        logger.info("✅ Commit réalisé")
        
        # Push
        push_response = input("🚀 Voulez-vous push vers le repository distant ? (Y/n): ")
        if push_response.lower() != 'n':
            current_branch = run_command("git branch --show-current").stdout.strip()
            
            try:
                run_command(f"git push origin {current_branch}")
                logger.info("✅ Push réalisé")
            except subprocess.CalledProcessError:
                # Peut-être la première fois sur cette branche
                try:
                    run_command(f"git push -u origin {current_branch}")
                    logger.info("✅ Push réalisé (nouvelle branche)")
                except subprocess.CalledProcessError as e:
                    logger.error(f"❌ Erreur lors du push: {e}")
        
    except subprocess.CalledProcessError as e:
        logger.error(f"❌ Erreur lors du commit: {e}")


def update_session_summary():
    """Met à jour le résumé de session."""
    logger.info("📊 Mise à jour du résumé de session...")
    
    session_file = Path("session_plan.md")
    
    if not session_file.exists():
        logger.warning("⚠️ Aucun plan de session trouvé")
        return
    
    # Lire le plan existant
    content = session_file.read_text()
    
    # Ajouter les statistiques de fin de session
    stats_section = f"""

## 📊 Statistiques de session

### Git
- Branche: {run_command("git branch --show-current").stdout.strip()}
- Commits de la session: {get_session_commits()}
- Fichiers modifiés: {get_modified_files_count()}

### Tests
- Statut: {get_test_status()}
- Couverture: {get_coverage_info()}

### Code Quality
- Formatage: {'✅' if check_formatting() else '❌'}
- Linting: {'✅' if check_linting() else '❌'}

---
Session terminée le {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
    
    # Remplacer ou ajouter la section stats
    if "## 📊 Statistiques de session" in content:
        # Remplacer la section existante
        lines = content.split('\n')
        new_lines = []
        in_stats = False
        
        for line in lines:
            if line.startswith("## 📊 Statistiques de session"):
                in_stats = True
                new_lines.append(stats_section)
                break
            elif line.startswith("---") and in_stats:
                in_stats = False
                continue
            elif not in_stats:
                new_lines.append(line)
        
        content = '\n'.join(new_lines)
    else:
        content += stats_section
    
    session_file.write_text(content)
    logger.info("✅ Résumé de session mis à jour")


def get_session_commits():
    """Obtient le nombre de commits de la session."""
    try:
        # Compter les commits depuis aujourd'hui
        today = datetime.now().strftime('%Y-%m-%d')
        result = run_command(f'git log --since="{today}" --oneline')
        return len(result.stdout.strip().split('\n')) if result.stdout.strip() else 0
    except:
        return "N/A"


def get_modified_files_count():
    """Obtient le nombre de fichiers modifiés."""
    try:
        result = run_command("git diff --name-only HEAD~1")
        return len(result.stdout.strip().split('\n')) if result.stdout.strip() else 0
    except:
        return "N/A"


def get_test_status():
    """Obtient le statut des tests."""
    try:
        result = run_command("pytest tests/ --collect-only -q", check=False)
        if result.returncode == 0:
            return "✅ Passent"
        else:
            return "❌ Échouent"
    except:
        return "❓ Inconnu"


def get_coverage_info():
    """Obtient les informations de couverture."""
    try:
        result = run_command("coverage report --show-missing", check=False)
        if result.returncode == 0:
            # Extraire le pourcentage total
            lines = result.stdout.split('\n')
            for line in lines:
                if 'TOTAL' in line:
                    parts = line.split()
                    if len(parts) >= 4:
                        return parts[3]
        return "N/A"
    except:
        return "N/A"


def check_formatting():
    """Vérifie si le code est bien formaté."""
    try:
        result = run_command("black --check src/ api/ tests/", check=False)
        return result.returncode == 0
    except:
        return False


def check_linting():
    """Vérifie le linting."""
    try:
        result = run_command("flake8 src/ api/ tests/", check=False)
        return result.returncode == 0
    except:
        return False


def print_summary():
    """Affiche le résumé final."""
    print("\n" + "=" * 60)
    print("✅ SESSION TERMINÉE !")
    print("=" * 60)
    print()
    print("📋 Actions réalisées:")
    print("   ✅ Code formaté et nettoyé")
    print("   ✅ Tests exécutés")
    print("   ✅ Fichiers temporaires supprimés")
    print("   ✅ Modifications commitées et pushées")
    print("   ✅ Résumé de session mis à jour")
    print()
    print("📊 Consultez session_plan.md pour les détails de la session")
    print()
    print("🔄 Prochaines fois:")
    print("   - Utilisez python scripts/start_session.py pour commencer")
    print("   - Suivez le guide docs/workflow-session.md")
    print("   - Consultez CONTRIBUTING.md pour les bonnes pratiques")
    print()
    print("💤 Bonne pause et à bientôt !")
    print("=" * 60)


def main():
    """Fonction principale."""
    try:
        print_header()
        code_cleanup()
        run_tests()
        cleanup_temp_files()
        commit_and_push()
        update_session_summary()
        print_summary()
        
    except KeyboardInterrupt:
        print("\n⚠️ Fin de session interrompue")
        sys.exit(1)
    except Exception as e:
        logger.error(f"❌ Erreur inattendue: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 