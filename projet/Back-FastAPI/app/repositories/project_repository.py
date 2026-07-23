"""
Repository — Project.

Toutes les opérations de persistance liées aux projets.
Aucune logique métier ici — uniquement des accès DB.
"""

import uuid
import logging
from typing import Sequence

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.project import Project
from app.schemas.project_schema import ProjectCreate, ProjectUpdate

logger = logging.getLogger(__name__)


class ProjectRepository:
    """Accès aux données pour le modèle Project."""

    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    # ─────────────────────────── Create ─────────────────────────

    async def create_project(self, data: ProjectCreate) -> Project:
        """
        Crée un nouveau projet en base de données.

        Args:
            data: Payload validé par Pydantic (ProjectCreate)

        Returns:
            Instance Project persistée avec son UUID généré
        """
        project = Project(
            user_id=data.user_id,
            title=data.title,
            idea=data.idea,
            status="pending",
        )
        self.db.add(project)
        await self.db.flush()   # Obtenir l'ID sans committer
        await self.db.refresh(project)
        logger.debug(f"Project créé : {project.id}")
        return project

    # ─────────────────────────── Read ───────────────────────────

    async def get_project(self, project_id: uuid.UUID) -> Project | None:
        """
        Récupère un projet par son UUID.

        Args:
            project_id: UUID du projet

        Returns:
            Instance Project ou None si introuvable
        """
        stmt = select(Project).where(Project.id == project_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_projects(
        self,
        user_id: uuid.UUID,
        skip: int = 0,
        limit: int = 20,
    ) -> tuple[Sequence[Project], int]:
        """
        Récupère la liste des projets d'un utilisateur avec pagination.

        Args:
            user_id: UUID de l'utilisateur
            skip:    Nombre d'éléments à ignorer (offset)
            limit:   Nombre maximum d'éléments à retourner

        Returns:
            Tuple (liste de projets, total)
        """
        # Total count
        count_stmt = (
            select(func.count())
            .select_from(Project)
            .where(Project.user_id == user_id)
        )
        total_result = await self.db.execute(count_stmt)
        total = total_result.scalar_one()

        # Projets paginés, triés par date de création décroissante
        stmt = (
            select(Project)
            .where(Project.user_id == user_id)
            .order_by(Project.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        result = await self.db.execute(stmt)
        projects = result.scalars().all()

        return projects, total

    # ─────────────────────────── Update ─────────────────────────

    async def update_project(
        self,
        project_id: uuid.UUID,
        data: ProjectUpdate,
    ) -> Project | None:
        """
        Met à jour les champs non-nuls d'un projet.

        Args:
            project_id: UUID du projet à modifier
            data:       Payload de mise à jour (champs optionnels)

        Returns:
            Instance Project mise à jour ou None si introuvable
        """
        project = await self.get_project(project_id)
        if not project:
            return None

        update_data = data.model_dump(exclude_none=True)
        for field, value in update_data.items():
            setattr(project, field, value)

        await self.db.flush()
        await self.db.refresh(project)
        return project

    # ─────────────────────────── Delete ─────────────────────────

    async def delete_project(self, project_id: uuid.UUID) -> bool:
        """
        Supprime un projet (cascade sur ses analyses).

        Args:
            project_id: UUID du projet

        Returns:
            True si supprimé, False si introuvable
        """
        project = await self.get_project(project_id)
        if not project:
            return False

        await self.db.delete(project)
        await self.db.flush()
        return True
