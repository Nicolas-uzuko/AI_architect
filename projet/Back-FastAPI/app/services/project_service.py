"""
Service — Project.

Orchestration de la logique métier pour les projets.
Utilise ProjectRepository pour toutes les opérations DB.
"""

import uuid
import logging

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.project_repository import ProjectRepository
from app.schemas.project_schema import (
    ProjectCreate,
    ProjectList,
    ProjectRead,
    ProjectUpdate,
)

logger = logging.getLogger(__name__)


class ProjectService:
    """Service métier pour la gestion des projets."""

    def __init__(self, db: AsyncSession) -> None:
        self.repo = ProjectRepository(db)

    # ─────────────────────────── create_project ──────────────────

    async def create_project(self, data: ProjectCreate) -> ProjectRead:
        """
        Crée un nouveau projet et le persiste en base de données.

        Args:
            data: Payload validé (titre, idée, user_id)

        Returns:
            ProjectRead — représentation publique du projet créé

        Raises:
            HTTPException 400 : Données invalides
        """
        logger.info(f"Création projet '{data.title}' pour user={data.user_id}")

        project = await self.repo.create_project(data)
        return ProjectRead.model_validate(project)

    # ─────────────────────────── get_project ─────────────────────

    async def get_project(self, project_id: uuid.UUID) -> ProjectRead:
        """
        Récupère un projet par son UUID.

        Args:
            project_id: UUID du projet

        Returns:
            ProjectRead

        Raises:
            HTTPException 404 : Projet introuvable
        """
        project = await self.repo.get_project(project_id)

        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Projet {project_id} introuvable",
            )

        return ProjectRead.model_validate(project)

    # ─────────────────────────── get_projects ────────────────────

    async def get_projects(
        self,
        user_id: uuid.UUID,
        page: int = 1,
        page_size: int = 20,
    ) -> ProjectList:
        """
        Récupère la liste paginée des projets d'un utilisateur.

        Args:
            user_id:   UUID de l'utilisateur
            page:      Numéro de page (commence à 1)
            page_size: Nombre d'éléments par page

        Returns:
            ProjectList — liste paginée avec total
        """
        skip = (page - 1) * page_size
        projects, total = await self.repo.get_projects(
            user_id=user_id,
            skip=skip,
            limit=page_size,
        )

        logger.info(f"get_projects user={user_id} → {len(projects)}/{total}")

        return ProjectList(
            items=[ProjectRead.model_validate(p) for p in projects],
            total=total,
            page=page,
            page_size=page_size,
        )

    # ─────────────────────────── update_project ──────────────────

    async def update_project(
        self,
        project_id: uuid.UUID,
        data: ProjectUpdate,
    ) -> ProjectRead:
        """
        Met à jour un projet existant.

        Args:
            project_id: UUID du projet
            data:       Champs à mettre à jour (partiels)

        Returns:
            ProjectRead mis à jour

        Raises:
            HTTPException 404 : Projet introuvable
        """
        project = await self.repo.update_project(project_id, data)

        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Projet {project_id} introuvable",
            )

        return ProjectRead.model_validate(project)
