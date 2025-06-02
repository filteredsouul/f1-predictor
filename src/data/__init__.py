"""
Module de collecte et traitement des données F1.

Ce module contient :
- Collecteurs pour Ergast API et FastF1
- Processeurs pour nettoyer les données
- Loaders pour charger les données de manière uniforme
"""

from src.data.loaders import DataLoader
from src.data.processors import DataProcessor

__all__ = ["DataLoader", "DataProcessor"] 