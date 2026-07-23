"""
Service — Analysis.

Orchestration de la logique métier pour la sauvegarde et la consultation
des analyses IA en base de données.
"""

import uuid
import logging
from typing import Any

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.analysis_repository import AnalysisRepository
from app.repositories.project_repository import ProjectRepository
from app.schemas.analysis_schema_db import (
    AnalysisCreate,
    AnalysisHistory,
    AnalysisRead,
)

logger = logging.getLogger(__name__)


class AnalysisService:
    """Service métier pour la persistance des analyses IA."""

    def __init__(self, db: AsyncSession) -> None:
        self.repo = AnalysisRepository(db)
        self.project_repo = ProjectRepository(db)

    # ─────────────────────────── save_analysis ───────────────────

    async def save_analysis(self, data: AnalysisCreate) -> AnalysisRead:
        """
        Persiste le résultat d'une analyse IA liée à un projet.

        Vérifie l'existence du projet avant de sauvegarder.

        Args:
            data: AnalysisCreate contenant project_id, result_json, model_used

        Returns:
            AnalysisRead — représentation publique de l'analyse sauvegardée

        Raises:
            HTTPException 404 : Projet introuvable
        """
        # Vérifier que le projet existe
        project = await self.project_repo.get_project(data.project_id)
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Projet {data.project_id} introuvable — impossible de sauvegarder l'analyse",
            )

        analysis = await self.repo.save_analysis(
            project_id=data.project_id,
            result_json=data.result_json,
            model_used=data.model_used,
        )

        # Mettre à jour le statut du projet à "completed"
        from app.schemas.project_schema import ProjectUpdate
        await self.project_repo.update_project(
            data.project_id,
            ProjectUpdate(status="completed"),
        )

        logger.info(f"Analyse sauvegardée : {analysis.id} → projet {data.project_id}")
        return AnalysisRead.model_validate(analysis)

    # ─────────────────────────── get_analysis_history ────────────

    async def get_analysis_history(
        self,
        project_id: uuid.UUID,
        page: int = 1,
        page_size: int = 20,
    ) -> AnalysisHistory:
        """
        Récupère l'historique paginé des analyses d'un projet.

        Args:
            project_id: UUID du projet
            page:       Numéro de page (commence à 1)
            page_size:  Nombre d'analyses par page

        Returns:
            AnalysisHistory — liste paginée avec total

        Raises:
            HTTPException 404 : Projet introuvable
        """
        # Vérifier que le projet existe
        project = await self.project_repo.get_project(project_id)
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Projet {project_id} introuvable",
            )

        skip = (page - 1) * page_size
        analyses, total = await self.repo.get_analysis_history(
            project_id=project_id,
            skip=skip,
            limit=page_size,
        )

        logger.info(f"get_analysis_history project={project_id} → {len(analyses)}/{total}")

        return AnalysisHistory(
            project_id=project_id,
            analyses=[AnalysisRead.model_validate(a) for a in analyses],
            total=total,
        )

    # ─────────────────────────── get_latest ──────────────────────

    async def get_latest_analysis(self, project_id: uuid.UUID) -> AnalysisRead | None:
        """
        Récupère la dernière analyse d'un projet.

        Args:
            project_id: UUID du projet

        Returns:
            AnalysisRead ou None si aucune analyse n'existe
        """
        analysis = await self.repo.get_latest_analysis(project_id)
        if not analysis:
            return None
        return AnalysisRead.model_validate(analysis)
