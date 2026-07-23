"""
Couche de connexion à la base de données PostgreSQL.

- Engine async SQLAlchemy 2.x (psycopg v3)
- Session factory async
- Dependency FastAPI `get_db()`
- Fonctions lifespan : init_db() / close_db()
"""

import logging
from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.config import get_settings

logger = logging.getLogger(__name__)

settings = get_settings()

# ─────────────────────────── Engine ─────────────────────────────

engine: AsyncEngine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DATABASE_ECHO,
    pool_size=settings.DATABASE_POOL_SIZE,
    max_overflow=settings.DATABASE_MAX_OVERFLOW,
    pool_pre_ping=True,        # Vérifie la connexion avant utilisation
    pool_recycle=3600,         # Recycle les connexions toutes les heures
)

# ─────────────────────────── Session Factory ─────────────────────

AsyncSessionLocal: async_sessionmaker[AsyncSession] = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,    # Evite les requêtes lazy post-commit
    autocommit=False,
    autoflush=False,
)


# ─────────────────────────── Dependency ─────────────────────────

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency FastAPI — injecte une session DB dans les routes/services.

    Usage :
        async def my_route(db: AsyncSession = Depends(get_db)):
            ...
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


# ─────────────────────────── Lifespan Hooks ─────────────────────

async def init_db() -> None:
    """
    Appelé au démarrage de l'application.
    Vérifie la connexion à PostgreSQL et logue le statut.
    Note : Les tables sont gérées par Alembic, pas ici.
    """
    try:
        async with engine.connect() as conn:
            await conn.execute(__import__("sqlalchemy").text("SELECT 1"))
        logger.info("✅ PostgreSQL — Connexion établie avec succès")
    except Exception as exc:
        logger.error(f"❌ PostgreSQL — Échec de connexion : {exc}")
        raise


async def close_db() -> None:
    """Appelé à l'arrêt de l'application. Ferme toutes les connexions."""
    await engine.dispose()
    logger.info("🔌 PostgreSQL — Connexions fermées")
