# 🏎️ F1 Predictor

[![CI](https://github.com/filteredsouul/f1-predictor/workflows/CI/badge.svg)](https://github.com/filteredsouul/f1-predictor/actions)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://python.org)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

> Modèle de Machine Learning pour prédire les résultats des Grands Prix de Formule 1

## 🎯 Objectif

Développer un modèle de Machine Learning pour prédire les résultats des Grands Prix de Formule 1. Le projet est orienté "model-first" : la priorité est donnée à la construction d'un modèle robuste avant d'envisager l'interface ou la mise en production.

## 🚀 Démarrage Ultra-Rapide (3 minutes)

```bash
# 1. Cloner et installer
git clone https://github.com/filteredsouul/f1-predictor.git
cd f1-predictor
python scripts/setup_project.py

# 2. Activer l'environnement
source venv/bin/activate  # Linux/Mac

# 3. Commencer à développer
python scripts/start_session.py
```

📖 **Guide détaillé** : [QUICKSTART.md](QUICKSTART.md)

## 📊 Utilisation

### Prédiction simple
```python
from src.models.pipeline import F1Pipeline

# Charger le modèle pré-entraîné
pipeline = F1Pipeline.load('models/trained/best_model.joblib')

# Faire une prédiction
prediction = pipeline.predict(race_data)
print(f"Classement prédit: {prediction}")
```

### API REST
```bash
# Lancer l'API
uvicorn api.main:app --reload

# Faire une prédiction via API
curl -X POST "http://localhost:8000/predict" \
     -H "Content-Type: application/json" \
     -d @examples/sample_request.json
```

### Interface Streamlit
```bash
streamlit run web/streamlit/app.py
```

## 🏗️ Architecture du projet

```
f1-predictor/
├── src/                    # Code source principal
│   ├── data/              # Collecte et traitement des données
│   ├── features/          # Feature engineering
│   ├── models/            # Modèles ML et pipelines
│   └── evaluation/        # Métriques et validation
├── api/                   # API REST FastAPI
├── web/                   # Interfaces utilisateur
├── notebooks/             # Exploration et prototypage
├── scripts/               # Scripts d'automatisation
└── docs/                  # Documentation
```

## 📈 Phases du projet

### Phase 1 - Construction du modèle ✅
- [x] Collecte de données (Ergast API, FastF1)
- [x] Feature engineering (moyennes glissantes, historiques)
- [x] Modélisation (XGBoost, CatBoost, RandomForest)
- [x] Évaluation (LogLoss, MAE, Accuracy @Top3)

### Phase 2 - Déploiement du modèle 🚧
- [ ] API REST avec FastAPI
- [ ] Containerisation Docker
- [ ] Déploiement cloud (Render/Railway)

### Phase 3 - Interface Web 📅
- [ ] MVP Streamlit
- [ ] Version React/Next.js
- [ ] Simulation interactive

## 🔄 Workflow de Développement

### Sessions de Travail Automatisées

```bash
# 🚀 Début de session (2 minutes)
python scripts/start_session.py

# 💻 Pendant la session
pytest tests/ -v              # Tests continus
black src/ api/ tests/        # Formatage
git add . && git commit -m "feat: ..."  # Commits fréquents

# 🏁 Fin de session (3 minutes)
python scripts/end_session.py
```

**📋 Guides détaillés :**
- [Workflow de Session](docs/workflow-session.md) - Guide complet (15 min)
- [QUICKSTART.md](QUICKSTART.md) - Démarrage rapide (3 min)

## 🔧 Développement

Voir [CONTRIBUTING.md](CONTRIBUTING.md) pour le guide de contribution.

```bash
# Installation en mode développement
pip install -r requirements-dev.txt

# Lancer les tests
pytest tests/

# Formatage du code
black src/ api/ tests/
flake8 src/ api/ tests/

# Pre-commit hooks
pre-commit install
```

## 📚 Documentation

| Guide | Description | Temps |
|-------|-------------|-------|
| [QUICKSTART.md](QUICKSTART.md) | Démarrage rapide | 3 min |
| [Installation](docs/installation.md) | Guide d'installation détaillé | 10 min |
| [Workflow](docs/workflow-session.md) | Sessions de travail | 15 min |
| [Contribution](CONTRIBUTING.md) | Guide de contribution | 10 min |
| [API](docs/api.md) | Documentation API | 5 min |
| [Modèles](docs/model.md) | Architecture des modèles | 10 min |

## 🤝 Contribution

Les contributions sont les bienvenues ! 

### Démarrage Express
1. **Fork** le repository
2. **Clone** : `git clone https://github.com/votre-username/f1-predictor.git`
3. **Setup** : `python scripts/setup_project.py`
4. **Développer** : `python scripts/start_session.py`
5. **Terminer** : `python scripts/end_session.py`
6. **PR** : Créer une Pull Request

Voir [CONTRIBUTING.md](CONTRIBUTING.md) pour plus de détails.

## 📊 Scripts d'Automatisation

Le projet inclut des scripts pour automatiser les tâches répétitives :

| Script | Usage | Description |
|--------|-------|-------------|
| `setup_project.py` | Installation initiale | Configure l'environnement complet |
| `start_session.py` | Début de session | Prépare l'environnement de travail |
| `end_session.py` | Fin de session | Nettoie, teste et sauvegarde |
| `collect_data.py` | Collecte de données | Récupère les données F1 |
| `train_model.py` | Entraînement | Lance l'entraînement des modèles |

## 📄 Licence

Ce projet est sous licence MIT. Voir [LICENSE](LICENSE) pour plus de détails.

## 🙏 Remerciements

- [Ergast API](https://ergast.com/mrd/) pour les données historiques F1
- [FastF1](https://github.com/theOehrly/Fast-F1) pour les données télémétrie
- Communauté F1 pour l'inspiration et les discussions

---

⭐ N'hésitez pas à star le projet si vous le trouvez utile !

🚀 **Prêt à commencer ?** → [QUICKSTART.md](QUICKSTART.md) 