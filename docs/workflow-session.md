# 🔄 Guide de Workflow - Sessions de Travail

Ce guide détaille les étapes à suivre au début et à la fin de chaque session de développement pour maintenir un workflow efficace et reproductible.

## 🚀 Début de Session de Travail

### 1. 🔧 Préparation de l'Environnement

```bash
# Naviguer vers le répertoire du projet
cd /chemin/vers/f1-predictor

# Vérifier le statut Git
git status
git branch

# Mettre à jour depuis le repository distant
git fetch origin
git pull origin main  # ou votre branche de travail
```

### 2. 🐍 Activation de l'Environnement Python

```bash
# Activer l'environnement virtuel
# macOS/Linux:
source venv/bin/activate

# Windows:
venv\Scripts\activate

# Vérifier l'activation (doit afficher le chemin du venv)
which python
python --version
```

### 3. 📦 Mise à Jour des Dépendances (si nécessaire)

```bash
# Vérifier s'il y a de nouvelles dépendances
git diff HEAD~1 requirements*.txt

# Si des changements, mettre à jour
pip install -r requirements-dev.txt

# Vérifier l'installation
pip list | grep -E "(pandas|numpy|scikit-learn|fastapi)"
```

### 4. 🧪 Tests de Santé de l'Environnement

```bash
# Test des imports principaux
python -c "
import src
import pandas as pd
import numpy as np
import sklearn
print('✅ Environnement prêt')
"

# Test de l'API (optionnel)
python -c "
try:
    from api.main import app
    print('✅ API importée')
except Exception as e:
    print(f'⚠️ Problème API: {e}')
"
```

### 5. 📊 Vérification de l'État du Projet

```bash
# Vérifier les données disponibles
ls -la data/raw/ data/processed/

# Vérifier les modèles existants
ls -la models/trained/

# Vérifier les logs récents (si applicable)
ls -la logs/ 2>/dev/null || echo "Pas de logs"
```

### 6. 🎯 Planification de la Session

**Checklist personnelle :**
- [ ] Objectif de la session défini
- [ ] Issue GitHub assignée (si applicable)
- [ ] Branche de travail créée/mise à jour
- [ ] Temps estimé de travail

```bash
# Créer une nouvelle branche si nécessaire
git checkout -b feature/nom-de-la-fonctionnalite

# Ou basculer sur une branche existante
git checkout nom-de-la-branche
```

---

## 💾 Pendant la Session de Travail

### 🔄 Commits Fréquents

```bash
# Commits atomiques toutes les 30-60 minutes
git add .
git commit -m "type(scope): description courte

- Détail 1
- Détail 2"

# Types de commits :
# feat: nouvelle fonctionnalité
# fix: correction de bug
# docs: documentation
# style: formatage
# refactor: refactoring
# test: ajout de tests
# chore: maintenance
```

### 🧪 Tests Continus

```bash
# Lancer les tests régulièrement
pytest tests/ -v

# Tests spécifiques au module en cours
pytest tests/test_data/ -v
pytest tests/test_models/ -v

# Tests avec couverture
pytest --cov=src tests/
```

### 📝 Logging et Documentation

```bash
# Garder un log de session (dans un fichier ou mentalement)
echo "$(date): Travail sur feature X - status Y" >> session.log

# Mettre à jour la documentation si nécessaire
# - Docstrings des nouvelles fonctions
# - README.md si nouvelles fonctionnalités
# - CHANGELOG.md pour les modifications importantes
```

---

## 🏁 Fin de Session de Travail

### 1. 🧹 Nettoyage du Code

```bash
# Formatage automatique
black src/ api/ tests/
isort src/ api/ tests/

# Vérification du style
flake8 src/ api/ tests/

# Type checking
mypy src/ api/ --ignore-missing-imports
```

### 2. 🧪 Tests Finaux

```bash
# Suite complète de tests
pytest tests/ --cov=src --cov=api

# Tests d'intégration (si applicable)
pytest tests/ -m integration

# Vérification que tout fonctionne
python -c "
import src
from src.data.collectors.ergast_collector import ErgastCollector
print('✅ Imports OK')
"
```

### 3. 📚 Documentation

```bash
# Mettre à jour les docstrings manquantes
# Vérifier que les nouvelles fonctions sont documentées

# Mettre à jour CHANGELOG.md si nécessaire
# Ajouter des exemples dans notebooks/ si nouvelle fonctionnalité majeure
```

### 4. 💾 Sauvegarde et Versioning

```bash
# Vérifier les fichiers modifiés
git status

# Ajouter tous les fichiers pertinents
git add .

# Commit final de session avec résumé
git commit -m "feat(session): résumé des modifications de la session

- Fonctionnalité A implémentée
- Bug B corrigé  
- Tests C ajoutés
- Documentation D mise à jour"

# Push vers le repository distant
git push origin nom-de-la-branche
```

### 5. 🔍 Vérification Finale

```bash
# Vérifier que le push s'est bien passé
git log --oneline -5

# Vérifier l'état de la branche
git status

# S'assurer qu'il n'y a pas de fichiers oubliés
git clean -n  # dry run pour voir ce qui serait supprimé
```

### 6. 📝 Log de Session

```bash
# Créer un résumé de session (dans un fichier ou issue GitHub)
cat > session_summary.md << EOF
# Session du $(date +%Y-%m-%d)

## 🎯 Objectifs
- [ ] Objectif 1 (✅/❌)
- [ ] Objectif 2 (✅/❌)

## ✅ Réalisations
- Fonctionnalité X implémentée
- Tests Y ajoutés
- Bug Z corrigé

## 🔄 À faire prochaine session
- Continuer fonctionnalité A
- Tester intégration B
- Documenter module C

## 📊 Métriques
- Commits: X
- Tests ajoutés: Y
- Couverture: Z%
EOF
```

### 7. 🧹 Nettoyage de l'Environnement

```bash
# Nettoyer les fichiers temporaires
find . -name "*.pyc" -delete
find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true

# Nettoyer les caches (optionnel)
rm -rf .pytest_cache/
rm -rf .mypy_cache/

# Désactiver l'environnement virtuel
deactivate
```

---

## 📋 Checklists Rapides

### ✅ Checklist Début de Session (5 min)

- [ ] `cd` vers projet
- [ ] `git pull origin main`
- [ ] `source venv/bin/activate`
- [ ] Test imports: `python -c "import src; print('OK')"`
- [ ] Objectif de session défini
- [ ] Branche de travail active

### ✅ Checklist Fin de Session (10 min)

- [ ] Code formaté: `black src/ api/ tests/`
- [ ] Tests passent: `pytest tests/`
- [ ] Changements commités: `git commit -m "..."`
- [ ] Push effectué: `git push origin branche`
- [ ] Documentation mise à jour
- [ ] Résumé de session créé
- [ ] Environnement désactivé: `deactivate`

---

## 🔧 Outils et Raccourcis Utiles

### Aliases Git Recommandés

```bash
# Ajouter à votre ~/.gitconfig ou ~/.zshrc
git config --global alias.st status
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.cm "commit -m"
git config --global alias.log1 "log --oneline -10"
git config --global alias.pushup "push -u origin HEAD"
```

### Scripts Utiles

```bash
# Script de début de session
echo '#!/bin/bash
cd /chemin/vers/f1-predictor
source venv/bin/activate
git pull origin main
python -c "import src; print(\"✅ Prêt à travailler\")"
' > ~/start_f1.sh && chmod +x ~/start_f1.sh

# Script de fin de session
echo '#!/bin/bash
black src/ api/ tests/
pytest tests/ --tb=short
git status
echo "💾 N\'oubliez pas de commit et push!"
deactivate
' > ~/end_f1.sh && chmod +x ~/end_f1.sh
```

### Variables d'Environnement Utiles

```bash
# Ajouter à votre ~/.zshrc ou ~/.bashrc
export F1_PROJECT_PATH="/chemin/vers/f1-predictor"
export LOG_LEVEL=INFO
export PYTHONPATH="$F1_PROJECT_PATH:$PYTHONPATH"

# Fonction pour aller rapidement au projet
f1cd() {
    cd "$F1_PROJECT_PATH"
    source venv/bin/activate
    echo "🏎️ F1 Predictor activé!"
}
```

---

## 🎯 Bonnes Pratiques

### 💡 Tips de Productivité

1. **Sessions courtes** : 1-3 heures max avec pauses
2. **Objectifs clairs** : 1-3 objectifs spécifiques par session
3. **Commits fréquents** : Toutes les 30-60 minutes
4. **Tests continus** : Lancer les tests après chaque modification importante
5. **Documentation au fur et à mesure** : Ne pas reporter à plus tard

### ⚠️ Choses à Éviter

- ❌ Travailler sans environnement virtuel activé
- ❌ Oublier de pull avant de commencer
- ❌ Commits trop gros (>100 lignes changées)
- ❌ Push sans avoir testé
- ❌ Laisser des `print()` de debug dans le code
- ❌ Travailler directement sur `main`

### 🔄 Workflow Git Recommandé

```
main branch
    ↓
  git pull
    ↓
feature/ma-fonctionnalite
    ↓
commits fréquents
    ↓
tests + formatting
    ↓
git push origin feature/ma-fonctionnalite
    ↓
Pull Request
    ↓
Code Review
    ↓
Merge vers main
```

---

## 🆘 Dépannage Rapide

### Problèmes Courants

**Environnement virtuel non trouvé :**
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements-dev.txt
```

**Imports qui ne fonctionnent pas :**
```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
pip install -e .
```

**Tests qui échouent après pull :**
```bash
pip install -r requirements-dev.txt
pytest tests/ -v
```

**Problèmes de formatage :**
```bash
pip install black isort flake8
black --check src/ api/ tests/
```

---

🎉 **Workflow établi !** Utilisez ce guide pour maintenir une productivité constante et un code de qualité tout au long du développement du projet F1 Predictor. 