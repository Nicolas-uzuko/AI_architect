"""
Environnement Alembic — support async (psycopg v3 / SQLAlchemy 2.x).

Charge la DATABASE_URL depuis les Settings Pydantic (fichier .env).
Importe tous les modèles pour que autogenerate détecte les changements.
"""

import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context

# ── Import Settings pour DATABASE_URL ─────────────────────────────────────
from app.core.config import get_settings

# ── Import Base + tous les modèles pour autogenerate ─────────────────────
from app.models.base import Base
from app.models.user import User       # noqa: F401
from app.models.project import Project  # noqa: F401
from app.models.analysis import Analysis  # noqa: F401

# ─────────────────────────────────────────────────────────────────────────
# Configuration Alembic
# ─────────────────────────────────────────────────────────────────────────

config = context.config

# Interpréter la section [loggers] de alembic.ini
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Surcharger l'URL depuis les Settings Pydantic (priorité sur alembic.ini)
settings = get_settings()
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

# Metadata cible pour autogenerate
target_metadata = Base.metadata


# ─────────────────────────────────────────────────────────────────────────
# Mode offline (génération SQL sans connexion réelle)
# ─────────────────────────────────────────────────────────────────────────

def run_migrations_offline() -> None:
    """
    Mode offline : génère le SQL sans connexion DB active.
    Utile pour inspecter les migrations avant application.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()


# ─────────────────────────────────────────────────────────────────────────
# Mode online async (connexion réelle via psycopg v3)
# ─────────────────────────────────────────────────────────────────────────

def do_run_migrations(connection: Connection) -> None:
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
        compare_server_default=True,
        # Inclure les schémas PostgreSQL si nécessaire
        # include_schemas=True,
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """Crée l'engine async et exécute les migrations."""
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,  # Pas de pool pour les migrations
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """Point d'entrée online — lance la boucle asyncio."""
    import sys
    if sys.platform == "win32":
        # Windows : ProactorEventLoop (défaut Python 3.8+) incompatible avec psycopg async
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(run_async_migrations())


# ─────────────────────────── Dispatch ────────────────────────────────────

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
