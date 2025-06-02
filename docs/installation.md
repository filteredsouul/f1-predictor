# 📦 Guide d'Installation

Ce guide vous accompagne dans l'installation et la configuration du projet F1 Predictor.

## 🔧 Prérequis

### Système
- **Python 3.10+** (recommandé: 3.11)
- **Git** pour le versioning
- **4GB RAM minimum** pour les modèles ML
- **2GB d'espace disque** pour les données et modèles

### Optionnel
- **Docker** pour la containerisation
- **Node.js 18+** pour l'interface React (Phase 3)

## 🚀 Installation Rapide

### Option 1: Script automatique (Recommandé)

```bash
# Cloner le repository
git clone https://github.com/votre-username/f1-predictor.git
cd f1-predictor

# Lancer le script d'installation
python scripts/setup_project.py
```

Le script configure automatiquement :
- ✅ Environnement virtuel Python
- ✅ Installation des dépendances
- ✅ Configuration pre-commit
- ✅ Fichier d'environnement
- ✅ Vérification de l'installation

### Option 2: Installation manuelle

```bash
# 1. Cloner le repository
git clone https://github.com/votre-username/f1-predictor.git
cd f1-predictor

# 2. Créer l'environnement virtuel
python -m venv venv

# 3. Activer l'environnement
# Sur macOS/Linux:
source venv/bin/activate
# Sur Windows:
venv\Scripts\activate

# 4. Mettre à jour pip
pip install --upgrade pip

# 5. Installer les dépendances
pip install -r requirements-dev.txt

# 6. Installer le package en mode développement
pip install -e .

# 7. Configurer pre-commit (optionnel)
pre-commit install

# 8. Créer le fichier d'environnement
cp .env.example .env
```

## 🔍 Vérification de l'Installation

### Test des imports
```bash
python -c "import src; print('✅ Package principal OK')"
python -c "import pandas, numpy, sklearn; print('✅ Dépendances ML OK')"
python -c "import fastapi, uvicorn; print('✅ Dépendances API OK')"
```

### Test de l'API
```bash
# Démarrer l'API
uvicorn api.main:app --reload

# Dans un autre terminal, tester
curl http://localhost:8000/
curl http://localhost:8000/health
```

### Test des notebooks
```bash
jupyter notebook notebooks/01_data_exploration.ipynb
```

## 🐳 Installation avec Docker

### Build de l'image
```bash
docker build -t f1-predictor .
```

### Lancement du conteneur
```bash
# API seulement
docker run -p 8000:8000 f1-predictor

# Avec volumes pour le développement
docker run -p 8000:8000 -v $(pwd):/app f1-predictor
```

### Docker Compose (développement)
```bash
docker-compose up --build
```

## ⚙️ Configuration

### Variables d'environnement

Éditez le fichier `.env` créé :

```bash
# API Configuration
ERGAST_API_URL=https://ergast.com/api/f1
FASTF1_CACHE_DIR=./cache/fastf1

# Model Configuration
MODEL_VERSION=v1.0.0
MODEL_PATH=models/trained/best_model.joblib

# API Settings
API_HOST=0.0.0.0
API_PORT=8000
API_DEBUG=True

# Logging
LOG_LEVEL=INFO
```

### Configuration des outils de développement

Le fichier `pyproject.toml` contient la configuration pour :
- **Black** (formatage)
- **flake8** (linting)
- **isort** (imports)
- **mypy** (type checking)
- **pytest** (tests)

## 🔧 Dépannage

### Erreurs courantes

#### Python version incorrecte
```bash
# Vérifier la version
python --version

# Installer Python 3.11 si nécessaire
# macOS avec Homebrew:
brew install python@3.11

# Ubuntu/Debian:
sudo apt update && sudo apt install python3.11
```

#### Erreurs d'installation de packages
```bash
# Mettre à jour pip et setuptools
pip install --upgrade pip setuptools wheel

# Installer avec verbose pour diagnostiquer
pip install -v -r requirements.txt
```

#### Problèmes avec FastF1
```bash
# FastF1 nécessite parfois des dépendances système
# Ubuntu/Debian:
sudo apt install python3-dev build-essential

# macOS:
xcode-select --install
```

#### Erreurs de permissions
```bash
# Donner les permissions d'exécution
chmod +x scripts/*.py

# Problèmes de cache pip
pip cache purge
```

### Logs et debugging

```bash
# Activer les logs détaillés
export LOG_LEVEL=DEBUG

# Vérifier les imports problématiques
python -c "import sys; print(sys.path)"
python -c "import src; print(src.__file__)"
```

## 📚 Prochaines étapes

Une fois l'installation terminée :

1. **Exploration** : `jupyter notebook notebooks/01_data_exploration.ipynb`
2. **Développement** : Voir [CONTRIBUTING.md](../CONTRIBUTING.md)
3. **API** : Consulter [api.md](api.md)
4. **Modèles** : Voir [model.md](model.md)

## 🆘 Support

- **Issues GitHub** : [Créer une issue](https://github.com/votre-username/f1-predictor/issues)
- **Discussions** : [GitHub Discussions](https://github.com/votre-username/f1-predictor/discussions)
- **Email** : contact@f1predictor.com

---

✅ **Installation réussie ?** Passez au [Guide d'utilisation](usage.md) ! 