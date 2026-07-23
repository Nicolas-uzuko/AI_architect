"""
Point d'entrée principal de l'application FastAPI.

Extensible pour :
    - Authentification JWT (middleware)
    - Rate limiting (slowapi)
    - Monitoring (Prometheus / Sentry)
    - Versioning API (/api/v1, /api/v2)
"""

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from app.routers.analysis import router as analysis_router
from app.core.database import init_db, close_db

# ─────────────────────────── Logging ────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


# ─────────────────────────── Lifespan ───────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Événements de démarrage et d'arrêt de l'application."""
    logger.info("🚀 AI Project Architect API — Démarrage")
    await init_db()          # ✅ Connexion PostgreSQL vérifiée au démarrage
    # TODO: Initialiser le client Redis ici
    yield
    logger.info("🛑 AI Project Architect API — Arrêt")
    await close_db()         # ✅ Fermeture propre du pool de connexions


# ─────────────────────────── App ────────────────────────────────
app = FastAPI(
    title="AI Project Architect API",
    description=(
        "API backend pour la plateforme SaaS AI Project Architect. "
        "Analyse des idées de projets via IA et génère des cahiers des charges, "
        "diagrammes, tâches GitHub et squelettes de code."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
    contact={
        "name": "AI Project Architect",
        "url": "http://localhost:3000",
    },
)


# ─────────────────────────── CORS ───────────────────────────────
# Origines autorisées — adapter selon l'environnement de déploiement
ALLOWED_ORIGINS = [
    "http://localhost:3000",       # Next.js dev
    "http://localhost:3001",       # Alternate dev port
    "https://ai-project-architect.vercel.app",  # Production (à adapter)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
    allow_headers=["*"],
)


# ─────────────────────────── Routers ────────────────────────────
app.include_router(analysis_router)

from app.routers.projects import router as projects_router
app.include_router(projects_router)

# TODO: Décommenter au fur et à mesure des développements futurs
# from app.routers.auth import router as auth_router
# from app.routers.export import router as export_router
# app.include_router(auth_router)
# app.include_router(projects_router)
# app.include_router(export_router)


# ─────────────────────────── Root ───────────────────────────────
@app.get("/", tags=["Root"], summary="Racine de l'API")
async def root():
    return {
        "name": "AI Project Architect API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs",
        "health": "/api/health",
    }
