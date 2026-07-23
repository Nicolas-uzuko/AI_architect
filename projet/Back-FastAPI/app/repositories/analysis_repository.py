"""
Repository — Analysis.

Toutes les opérations de persistance liées aux analyses IA.
Aucune logique métier ici — uniquement des accès DB.
"""

import uuid
import logging
from typing import Any, Sequence

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.analysis import Analysis

logger = logging.getLogger(__name__)


class AnalysisRepository:
    """Accès aux données pour le modèle Analysis."""

    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    # ─────────────────────────── Create ─────────────────────────

    async def save_analysis(
        self,
        project_id: uuid.UUID,
        result_json: dict[str, Any],
        model_used: str = "llama-3.3-70b-versatile",
    ) -> Analysis:
        """
        Persiste le résultat d'une analyse IA en base de données.

        Args:
            project_id:  UUID du projet associé
            result_json: Dictionnaire complet du résultat IA (stocké en JSONB)
            model_used:  Identifiant du modèle IA utilisé

        Returns:
            Instance Analysis persistée avec son UUID généré
        """
        analysis = Analysis(
            project_id=project_id,
            result_json=result_json,
            model_used=model_used,
        )
        self.db.add(analysis)
        await self.db.flush()
        await self.db.refresh(analysis)
        logger.debug(f"Analysis sauvegardée : {analysis.id} (project={project_id})")
        return analysis

    # ─────────────────────────── Read ───────────────────────────

    async def get_analysis(self, analysis_id: uuid.UUID) -> Analysis | None:
        """
        Récupère une analyse par son UUID.

        Args:
            analysis_id: UUID de l'analyse

        Returns:
            Instance Analysis ou None si introuvable
        """
        stmt = select(Analysis).where(Analysis.id == analysis_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_analysis_history(
        self,
        project_id: uuid.UUID,
        skip: int = 0,
        limit: int = 20,
    ) -> tuple[Sequence[Analysis], int]:
        """
        Récupère l'historique des analyses d'un projet, triées du plus récent au plus ancien.

        Args:
            project_id: UUID du projet
            skip:       Offset de pagination
            limit:      Nombre max d'analyses à retourner

        Returns:
            Tuple (liste d'analyses, total)
        """
        # Total count
        count_stmt = (
            select(func.count())
            .select_from(Analysis)
            .where(Analysis.project_id == project_id)
        )
        total_result = await self.db.execute(count_stmt)
        total = total_result.scalar_one()

        # Analyses paginées, triées par date décroissante
        stmt = (
            select(Analysis)
            .where(Analysis.project_id == project_id)
            .order_by(Analysis.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        result = await self.db.execute(stmt)
        analyses = result.scalars().all()

        return analyses, total

    # ─────────────────────────── Latest ─────────────────────────

    async def get_latest_analysis(self, project_id: uuid.UUID) -> Analysis | None:
        """
        Récupère la dernière analyse d'un projet.

        Args:
            project_id: UUID du projet

        Returns:
            Dernière instance Analysis ou None
        """
        stmt = (
            select(Analysis)
            .where(Analysis.project_id == project_id)
            .order_by(Analysis.created_at.desc())
            .limit(1)
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()
