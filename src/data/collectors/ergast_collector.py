"""
Collecteur de données pour l'API Ergast.

Ce module permet de récupérer les données historiques de Formule 1
depuis l'API Ergast (résultats de courses, qualifications, pilotes, etc.).
"""

import logging
import time
from typing import Dict, List, Optional, Union

import pandas as pd
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

logger = logging.getLogger(__name__)


class ErgastCollector:
    """Collecteur de données pour l'API Ergast F1."""
    
    BASE_URL = "https://ergast.com/api/f1"
    
    def __init__(self, rate_limit: float = 1.0):
        """
        Initialise le collecteur Ergast.
        
        Args:
            rate_limit: Délai entre les requêtes (en secondes)
        """
        self.rate_limit = rate_limit
        self.session = self._create_session()
        
    def _create_session(self) -> requests.Session:
        """Crée une session HTTP avec retry et rate limiting."""
        session = requests.Session()
        
        # Configuration des retries
        retry_strategy = Retry(
            total=3,
            backoff_factor=2,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        return session
    
    def _make_request(self, endpoint: str, params: Optional[Dict] = None) -> Dict:
        """
        Effectue une requête à l'API Ergast.
        
        Args:
            endpoint: Endpoint de l'API
            params: Paramètres de la requête
            
        Returns:
            Réponse JSON de l'API
            
        Raises:
            requests.RequestException: Erreur de requête
        """
        url = f"{self.BASE_URL}/{endpoint}.json"
        
        if params is None:
            params = {}
        
        params.setdefault("limit", 1000)  # Limite par défaut
        
        try:
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            
            # Rate limiting
            time.sleep(self.rate_limit)
            
            return response.json()
            
        except requests.RequestException as e:
            logger.error(f"Erreur lors de la requête à {url}: {e}")
            raise
    
    def get_seasons(self, start_year: int = 1950, end_year: Optional[int] = None) -> List[int]:
        """
        Récupère la liste des saisons disponibles.
        
        Args:
            start_year: Première année
            end_year: Dernière année (par défaut: année courante)
            
        Returns:
            Liste des années de saisons
        """
        if end_year is None:
            end_year = pd.Timestamp.now().year
            
        try:
            response = self._make_request("seasons")
            seasons_data = response["MRData"]["SeasonTable"]["Seasons"]
            
            seasons = [
                int(season["season"]) 
                for season in seasons_data
                if start_year <= int(season["season"]) <= end_year
            ]
            
            logger.info(f"Trouvé {len(seasons)} saisons entre {start_year} et {end_year}")
            return sorted(seasons)
            
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des saisons: {e}")
            raise
    
    def get_races(self, season: Union[int, str]) -> pd.DataFrame:
        """
        Récupère les courses d'une saison.
        
        Args:
            season: Année de la saison
            
        Returns:
            DataFrame avec les informations des courses
        """
        try:
            response = self._make_request(f"{season}")
            races_data = response["MRData"]["RaceTable"]["Races"]
            
            races = []
            for race in races_data:
                race_info = {
                    "season": int(race["season"]),
                    "round": int(race["round"]),
                    "race_id": f"{race['season']}_{race['round']}",
                    "race_name": race["raceName"],
                    "circuit_id": race["Circuit"]["circuitId"],
                    "circuit_name": race["Circuit"]["circuitName"],
                    "country": race["Circuit"]["Location"]["country"],
                    "date": pd.to_datetime(race["date"]),
                    "url": race.get("url", "")
                }
                
                # Ajout de l'heure si disponible
                if "time" in race:
                    race_info["time"] = race["time"]
                
                races.append(race_info)
            
            df = pd.DataFrame(races)
            logger.info(f"Récupéré {len(df)} courses pour la saison {season}")
            
            return df
            
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des courses {season}: {e}")
            raise
    
    def get_results(self, season: Union[int, str], round_num: Optional[int] = None) -> pd.DataFrame:
        """
        Récupère les résultats de courses.
        
        Args:
            season: Année de la saison
            round_num: Numéro du round (optionnel, si None récupère toute la saison)
            
        Returns:
            DataFrame avec les résultats
        """
        try:
            if round_num:
                endpoint = f"{season}/{round_num}/results"
            else:
                endpoint = f"{season}/results"
            
            response = self._make_request(endpoint)
            races_data = response["MRData"]["RaceTable"]["Races"]
            
            results = []
            for race in races_data:
                race_info = {
                    "season": int(race["season"]),
                    "round": int(race["round"]),
                    "race_name": race["raceName"],
                    "circuit_id": race["Circuit"]["circuitId"],
                    "date": pd.to_datetime(race["date"])
                }
                
                for result in race["Results"]:
                    result_info = race_info.copy()
                    result_info.update({
                        "position": int(result["position"]) if result["position"].isdigit() else None,
                        "driver_id": result["Driver"]["driverId"],
                        "driver_name": f"{result['Driver']['givenName']} {result['Driver']['familyName']}",
                        "constructor_id": result["Constructor"]["constructorId"],
                        "constructor_name": result["Constructor"]["name"],
                        "grid": int(result["grid"]) if result["grid"].isdigit() else None,
                        "laps": int(result["laps"]),
                        "status": result["status"],
                        "points": float(result["points"])
                    })
                    
                    # Temps de course si disponible
                    if "Time" in result and "time" in result["Time"]:
                        result_info["race_time"] = result["Time"]["time"]
                    
                    # Temps au tour le plus rapide
                    if "FastestLap" in result:
                        fastest_lap = result["FastestLap"]
                        result_info["fastest_lap_rank"] = int(fastest_lap.get("rank", 0))
                        if "Time" in fastest_lap:
                            result_info["fastest_lap_time"] = fastest_lap["Time"]["time"]
                    
                    results.append(result_info)
            
            df = pd.DataFrame(results)
            logger.info(f"Récupéré {len(df)} résultats pour {season}" + 
                       (f" round {round_num}" if round_num else ""))
            
            return df
            
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des résultats: {e}")
            raise
    
    def get_qualifying(self, season: Union[int, str], round_num: Optional[int] = None) -> pd.DataFrame:
        """
        Récupère les résultats de qualifications.
        
        Args:
            season: Année de la saison
            round_num: Numéro du round (optionnel)
            
        Returns:
            DataFrame avec les résultats de qualifications
        """
        try:
            if round_num:
                endpoint = f"{season}/{round_num}/qualifying"
            else:
                endpoint = f"{season}/qualifying"
            
            response = self._make_request(endpoint)
            races_data = response["MRData"]["RaceTable"]["Races"]
            
            qualifying_results = []
            for race in races_data:
                race_info = {
                    "season": int(race["season"]),
                    "round": int(race["round"]),
                    "race_name": race["raceName"],
                    "circuit_id": race["Circuit"]["circuitId"],
                    "date": pd.to_datetime(race["date"])
                }
                
                for qual in race["QualifyingResults"]:
                    qual_info = race_info.copy()
                    qual_info.update({
                        "position": int(qual["position"]),
                        "driver_id": qual["Driver"]["driverId"],
                        "driver_name": f"{qual['Driver']['givenName']} {qual['Driver']['familyName']}",
                        "constructor_id": qual["Constructor"]["constructorId"],
                        "constructor_name": qual["Constructor"]["name"]
                    })
                    
                    # Temps de qualifications par session
                    for session in ["Q1", "Q2", "Q3"]:
                        if session in qual:
                            qual_info[f"{session.lower()}_time"] = qual[session]
                    
                    qualifying_results.append(qual_info)
            
            df = pd.DataFrame(qualifying_results)
            logger.info(f"Récupéré {len(df)} résultats de qualifs pour {season}" + 
                       (f" round {round_num}" if round_num else ""))
            
            return df
            
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des qualifications: {e}")
            raise
    
    def get_drivers(self, season: Optional[Union[int, str]] = None) -> pd.DataFrame:
        """
        Récupère les informations des pilotes.
        
        Args:
            season: Saison spécifique (optionnel)
            
        Returns:
            DataFrame avec les informations des pilotes
        """
        try:
            endpoint = f"{season}/drivers" if season else "drivers"
            response = self._make_request(endpoint)
            
            drivers_data = response["MRData"]["DriverTable"]["Drivers"]
            
            drivers = []
            for driver in drivers_data:
                driver_info = {
                    "driver_id": driver["driverId"],
                    "given_name": driver["givenName"],
                    "family_name": driver["familyName"],
                    "driver_name": f"{driver['givenName']} {driver['familyName']}",
                    "nationality": driver["nationality"],
                    "url": driver.get("url", "")
                }
                
                # Date de naissance si disponible
                if "dateOfBirth" in driver:
                    driver_info["date_of_birth"] = pd.to_datetime(driver["dateOfBirth"])
                
                drivers.append(driver_info)
            
            df = pd.DataFrame(drivers)
            logger.info(f"Récupéré {len(df)} pilotes" + 
                       (f" pour la saison {season}" if season else ""))
            
            return df
            
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des pilotes: {e}")
            raise
    
    def get_constructors(self, season: Optional[Union[int, str]] = None) -> pd.DataFrame:
        """
        Récupère les informations des constructeurs.
        
        Args:
            season: Saison spécifique (optionnel)
            
        Returns:
            DataFrame avec les informations des constructeurs
        """
        try:
            endpoint = f"{season}/constructors" if season else "constructors"
            response = self._make_request(endpoint)
            
            constructors_data = response["MRData"]["ConstructorTable"]["Constructors"]
            
            constructors = []
            for constructor in constructors_data:
                constructor_info = {
                    "constructor_id": constructor["constructorId"],
                    "constructor_name": constructor["name"],
                    "nationality": constructor["nationality"],
                    "url": constructor.get("url", "")
                }
                constructors.append(constructor_info)
            
            df = pd.DataFrame(constructors)
            logger.info(f"Récupéré {len(df)} constructeurs" + 
                       (f" pour la saison {season}" if season else ""))
            
            return df
            
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des constructeurs: {e}")
            raise 