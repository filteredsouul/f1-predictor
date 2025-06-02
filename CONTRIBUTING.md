# Guide de Contribution

Merci de votre intérêt pour contribuer au projet F1 Predictor ! 🏎️

## 🚀 Démarrage rapide

1. **Fork** le repository
2. **Clone** votre fork
3. **Créer** une branche pour votre feature
4. **Développer** vos modifications
5. **Tester** vos changements
6. **Soumettre** une Pull Request

## 🔧 Configuration de l'environnement de développement

```bash
# Cloner le repo
git clone https://github.com/votre-username/f1-predictor.git
cd f1-predictor

# Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/Mac

# Installer les dépendances de développement
pip install -r requirements-dev.txt

# Installer les pre-commit hooks
pre-commit install
```

## 📝 Standards de code

### Style de code
- **Black** pour le formatage Python
- **flake8** pour le linting
- **isort** pour l'organisation des imports
- **mypy** pour le type checking

```bash
# Formater le code
black src/ api/ tests/

# Vérifier le style
flake8 src/ api/ tests/

# Organiser les imports
isort src/ api/ tests/

# Type checking
mypy src/ api/
```

### Conventions de nommage
- **Classes** : PascalCase (`F1Pipeline`, `DataCollector`)
- **Fonctions/méthodes** : snake_case (`predict_race`, `load_data`)
- **Variables** : snake_case (`race_data`, `model_path`)
- **Constantes** : UPPER_SNAKE_CASE (`API_URL`, `DEFAULT_MODEL`)

## 🧪 Tests

```bash
# Lancer tous les tests
pytest

# Tests avec couverture
pytest --cov=src --cov-report=html

# Tests spécifiques
pytest tests/test_models/
pytest tests/test_api/
```

### Structure des tests
```python
def test_fonction_description():
    # Arrange
    data = create_test_data()
    
    # Act
    result = function_to_test(data)
    
    # Assert
    assert result == expected_value
```

## 📊 Types de contributions

### 🐛 Corrections de bugs
- Créer une issue détaillée
- Référencer l'issue dans votre PR
- Inclure des tests de régression

### ✨ Nouvelles fonctionnalités
- Discuter de la fonctionnalité dans une issue
- Suivre l'architecture existante
- Documenter les nouvelles APIs

### 📚 Documentation
- Améliorer la clarté des README
- Ajouter des exemples d'utilisation
- Corriger les typos

### 🔬 Amélioration des modèles
- Tester de nouveaux algorithmes
- Améliorer le feature engineering
- Optimiser les hyperparamètres

## 📋 Checklist Pull Request

- [ ] Mon code respecte le style du projet
- [ ] J'ai ajouté des tests pour mes modifications
- [ ] Tous les tests passent
- [ ] J'ai mis à jour la documentation si nécessaire
- [ ] Ma PR a un titre descriptif
- [ ] J'ai lié les issues correspondantes

## 🏷️ Convention de commit

Utilisez des messages de commit clairs :

```
type(scope): description courte

Description plus détaillée si nécessaire.

Fixes #123
```

**Types** :
- `feat`: nouvelle fonctionnalité
- `fix`: correction de bug
- `docs`: documentation
- `style`: formatage
- `refactor`: refactoring
- `test`: ajout de tests
- `chore`: maintenance

**Exemples** :
```
feat(models): add CatBoost ensemble model
fix(api): handle missing race data gracefully
docs(readme): update installation instructions
test(features): add tests for rolling averages
```

## 🔄 Processus de review

1. **Automated checks** : CI/CD, tests, linting
2. **Code review** : Un maintainer review le code
3. **Discussion** : Échanges constructifs
4. **Merge** : Après approbation

## 💡 Bonnes pratiques

### Code
- Suivre le principe DRY (Don't Repeat Yourself)
- Écrire des fonctions pures quand possible
- Documenter les fonctions complexes
- Gérer les erreurs proprement

### Git
- Commits atomiques et logiques
- Branches courtes et focalisées
- Rebase avant de merger si nécessaire

### Machine Learning
- Valider les modèles sur des données de test
- Documenter les expériences
- Versionner les datasets
- Tracer la reproductibilité

## 🆘 Besoin d'aide ?

- **Issues** : Poser une question
- **Discussions** : Conversations générales
- **Email** : contact@f1predictor.com

## 🙏 Reconnaissance

Toutes les contributions sont valorisées et reconnues :
- Ajout dans les contributors
- Mention dans les release notes
- Badges de reconnaissance

---

Merci de contribuer à F1 Predictor ! 🏁 