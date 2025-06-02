"""
F1 Predictor - Modèle de Machine Learning pour prédire les résultats de Formule 1.

Ce package contient tous les modules nécessaires pour :
- Collecter et traiter les données F1
- Effectuer le feature engineering
- Entraîner et évaluer les modèles
- Faire des prédictions
"""

__version__ = "1.0.0"
__author__ = "Charles-François Fouti-Loemba"
__email__ = "contact@f1predictor.com"

from src.models.pipeline import F1Pipeline

__all__ = ["F1Pipeline"] 