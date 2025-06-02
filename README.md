# 🏎️ F1 Predictor

[![CI](https://github.com/username/f1-predictor/workflows/CI/badge.svg)](https://github.com/username/f1-predictor/actions)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://python.org)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

> Modèle de Machine Learning pour prédire les résultats des Grands Prix de Formule 1

## 🎯 Objectif

Développer un modèle de Machine Learning pour prédire les résultats des Grands Prix de Formule 1. Le projet est orienté "model-first" : la priorité est donnée à la construction d'un modèle robuste avant d'envisager l'interface ou la mise en production.

## 🚀 Installation rapide

```bash
# Cloner le repository
git clone https://github.com/username/f1-predictor.git
cd f1-predictor

# Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou venv\Scripts\activate  # Windows

# Installer les dépendances
pip install -r requirements.txt
```

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

- [Installation](docs/installation.md)
- [Guide d'utilisation](docs/usage.md)
- [Documentation API](docs/api.md)
- [Architecture du modèle](docs/model.md)
- [Guide de déploiement](docs/deployment.md)

## 🤝 Contribution

Les contributions sont les bienvenues ! Voir [CONTRIBUTING.md](CONTRIBUTING.md) pour plus de détails.

## 📄 Licence

Ce projet est sous licence MIT. Voir [LICENSE](LICENSE) pour plus de détails.

## 🙏 Remerciements

- [Ergast API](https://ergast.com/mrd/) pour les données historiques F1
- [FastF1](https://github.com/theOehrly/Fast-F1) pour les données télémétrie
- Communauté F1 pour l'inspiration et les discussions

---

⭐ N'hésitez pas à star le projet si vous le trouvez utile ! 