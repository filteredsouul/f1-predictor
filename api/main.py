"""
Application FastAPI principale pour F1 Predictor.

Cette API permet de faire des prédictions sur les résultats de F1.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
import os
from typing import Dict, Any

from api.endpoints import predict, health
from api.dependencies import get_model_pipeline

# Configuration du logging
logging.basicConfig(
    level=getattr(logging, os.getenv("LOG_LEVEL", "INFO")),
    format=os.getenv("LOG_FORMAT", "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
)

logger = logging.getLogger(__name__)

# Création de l'application FastAPI
app = FastAPI(
    title="F1 Predictor API",
    description="API de prédiction des résultats de Formule 1",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # À restreindre en production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Gestionnaire d'erreurs HTTP personnalisé."""
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail, "status_code": exc.status_code}
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Gestionnaire d'erreurs générales."""
    logger.error(f"Erreur non gérée: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Erreur interne du serveur", "status_code": 500}
    )


# Événements de démarrage et arrêt
@app.on_event("startup")
async def startup_event():
    """Actions à effectuer au démarrage de l'API."""
    logger.info("🚀 Démarrage de F1 Predictor API")
    
    # Chargement du modèle (optionnel au démarrage)
    try:
        pipeline = get_model_pipeline()
        if pipeline:
            logger.info("✅ Modèle chargé avec succès")
        else:
            logger.warning("⚠️ Aucun modèle trouvé - mode dégradé")
    except Exception as e:
        logger.error(f"❌ Erreur lors du chargement du modèle: {e}")


@app.on_event("shutdown")
async def shutdown_event():
    """Actions à effectuer à l'arrêt de l'API."""
    logger.info("🛑 Arrêt de F1 Predictor API")


# Routes principales
@app.get("/")
async def root() -> Dict[str, Any]:
    """Route racine avec informations sur l'API."""
    return {
        "message": "Bienvenue sur F1 Predictor API",
        "version": "1.0.0",
        "status": "active",
        "docs": "/docs",
        "health": "/health"
    }


# Inclusion des routers
app.include_router(health.router, prefix="/health", tags=["health"])
app.include_router(predict.router, prefix="/predict", tags=["prediction"])


if __name__ == "__main__":
    import uvicorn
    
    # Configuration par défaut pour le développement
    uvicorn.run(
        "api.main:app",
        host=os.getenv("API_HOST", "0.0.0.0"),
        port=int(os.getenv("API_PORT", 8000)),
        reload=os.getenv("RELOAD", "True").lower() == "true",
        log_level=os.getenv("LOG_LEVEL", "info").lower()
    ) 