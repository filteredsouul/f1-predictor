# 🚀 Guide de Démarrage Rapide - F1 Predictor

Ce guide vous permet de démarrer rapidement avec le projet F1 Predictor, de l'installation à votre première session de développement.

## ⚡ Installation Express (5 minutes)

### 1. Clone et Installation Automatique
```bash
# Cloner le projet
git clone https://github.com/filteredsouul/f1-predictor
cd f1-predictor

# Installation automatique
python scripts/setup_project.py
```

### 2. Activation de l'Environnement
```bash
# macOS/Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. Vérification
```bash
# Test rapide
python -c "import src; print('✅ Prêt!')"
```

## 🔄 Workflow de Session Standard

### 🚀 Début de Session (2 minutes)
```bash
# Script automatisé (recommandé)
python scripts/start_session.py

# OU manuellement:
git pull origin main
source venv/bin/activate
python -c "import src; print('OK')"
```

### 💻 Pendant la Session

**Commandes fréquentes :**
```bash
# Tests continus
pytest tests/ -v

# Formatage du code
black src/ api/ tests/

# Commits fréquents (toutes les 30-60 min)
git add . && git commit -m "feat: description"
```

### 🏁 Fin de Session (3 minutes)
```bash
# Script automatisé (recommandé)
python scripts/end_session.py

# OU manuellement:
black src/ api/ tests/        # Formater
pytest tests/                 # Tester
git add . && git commit -m "..." # Sauvegarder
git push origin branche       # Publier
deactivate                    # Sortir du venv
```

## 📋 Checklists Ultra-Rapides

### ✅ Checklist Début (30 secondes)
- [ ] `cd f1-predictor`
- [ ] `python scripts/start_session.py`
- [ ] Objectif défini
- [ ] Branche active

### ✅ Checklist Fin (1 minute)
- [ ] `python scripts/end_session.py`
- [ ] Tests passent
- [ ] Code commité
- [ ] Branche pushée

## 🎯 Premiers Pas de Développement

### Phase 1 : Exploration des Données
```bash
# Lancer Jupyter
jupyter notebook notebooks/01_data_exploration.ipynb

# Tester le collecteur Ergast
python -c "
from src.data.collectors.ergast_collector import ErgastCollector
collector = ErgastCollector()
print(collector.get_seasons(2020, 2023))
"
```

### Phase 2 : Développement API
```bash
# Démarrer l'API en mode développement
uvicorn api.main:app --reload

# Tester l'API
curl http://localhost:8000/
curl http://localhost:8000/health
```

### Phase 3 : Interface Web
```bash
# Lancer Streamlit (quand disponible)
streamlit run web/streamlit/app.py
```

## 🔧 Commandes Essentielles

### Développement
```bash
# Tests
pytest tests/                 # Tous les tests
pytest tests/test_data/ -v    # Tests spécifiques
pytest --cov=src tests/       # Avec couverture

# Code Quality
black src/ api/ tests/        # Formatage
flake8 src/ api/ tests/       # Linting
isort src/ api/ tests/        # Imports
mypy src/ api/                # Types

# Git
git status                    # État
git add . && git commit -m ""  # Commit rapide
git push origin branche       # Push
git checkout -b feature/nom   # Nouvelle branche
```

### Données
```bash
# Explorer les données disponibles
ls -la data/raw/ data/processed/

# Lancer la collecte (quand implémentée)
python scripts/collect_data.py

# Entraîner un modèle (quand implémenté)
python scripts/train_model.py
```

## 📚 Documentation Rapide

| Document | Usage | Temps |
|----------|-------|-------|
| `README.md` | Vue d'ensemble du projet | 5 min |
| `docs/installation.md` | Installation détaillée | 10 min |
| `docs/workflow-session.md` | Guide de workflow complet | 15 min |
| `CONTRIBUTING.md` | Contribution au projet | 10 min |
| `QUICKSTART.md` | Ce guide ! | 3 min |

## 🆘 Aide Rapide

### Problèmes Courants

**Environnement virtuel :**
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements-dev.txt
```

**Imports qui échouent :**
```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
pip install -e .
```

**Tests échouent :**
```bash
pip install -r requirements-dev.txt
pytest tests/ -v --tb=short
```

**Git issues :**
```bash
git status
git add .
git commit -m "fix: problème résolu"
```

### Contacts et Support

- 🐛 **Issues** : [GitHub Issues](https://github.com/filteredsouul/f1-predictor/issues)
- 💬 **Discussions** : [GitHub Discussions](https://github.com/filteredsouul/f1-predictor/discussions)
- 📧 **Email** : contact@f1predictor.com

## 🎉 Félicitations !

Vous êtes maintenant prêt à contribuer au projet F1 Predictor ! 

### 🎯 Prochaines étapes suggérées :

1. **Explorer** : `jupyter notebook notebooks/01_data_exploration.ipynb`
2. **Développer** : Choisir une issue GitHub ou fonctionnalité
3. **Tester** : `pytest tests/` après chaque modification
4. **Contribuer** : Faire une Pull Request

### 🏎️ Objectifs par Phase :

**Phase 1 - Modèle** (Actuelle)
- [ ] Collecteur de données complet
- [ ] Feature engineering avancé
- [ ] Modèles ML entraînés
- [ ] Pipeline de prédiction

**Phase 2 - API**
- [ ] API REST fonctionnelle
- [ ] Documentation Swagger
- [ ] Tests d'intégration
- [ ] Déploiement cloud

**Phase 3 - Interface**
- [ ] Interface Streamlit
- [ ] Version React
- [ ] Simulation interactive
- [ ] Visualisations avancées

---

**⭐ N'oubliez pas de star le projet sur GitHub !**

**🚀 Bon développement avec F1 Predictor !** 