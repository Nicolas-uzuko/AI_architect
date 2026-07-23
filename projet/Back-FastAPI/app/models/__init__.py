"""Models package — expose tous les modèles pour Alembic autogenerate."""

from app.models.base import Base
from app.models.user import User
from app.models.project import Project
from app.models.analysis import Analysis

__all__ = ["Base", "User", "Project", "Analysis"]
