"""
Routeur d'analyse de projet.
Route : POST /api/analyze
"""

import logging
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, HTTPException, status, Depends
from app.schemas.analysis_schema import (
    AnalysisRequest,
    AnalysisResponse,
    ErrorResponse,
)
from app.services.ai_service import analyze_project
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.services.project_service import ProjectService
from app.services.analysis_service import AnalysisService
from app.schemas.project_schema import ProjectCreate
from app.schemas.analysis_schema_db import AnalysisCreate

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api",
    tags=["Analysis"],
)


@router.post(
    "/analyze",
    response_model=AnalysisResponse,
    status_code=status.HTTP_200_OK,
    summary="Analyser une idée de projet",
    description=(
        "Reçoit une idée de projet en texte libre, crée le projet en base de données, "
        "retourne un rapport structuré généré par l'IA et le sauvegarde en DB."
    ),
)
async def analyze_project_route(
    request: AnalysisRequest,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> AnalysisResponse:
    """
    Analyse une idée de projet via l'IA et retourne un rapport complet.
    Sauvegarde l'analyse et le projet en base de données.
    """
    logger.info(f"Analyse demandée pour : {request.idea[:80]}...")
    
    proj_service = ProjectService(db)
    analysis_service = AnalysisService(db)

    try:
        # 1. Créer le projet "en cours d'analyse"
        project_title = request.idea[:50] + "..." if len(request.idea) > 50 else request.idea
        project = await proj_service.create_project(
            ProjectCreate(
                title=project_title,
                idea=request.idea,
                user_id=user.id
            )
        )
        
        # 2. Lancer l'analyse IA
        analysis_data = analyze_project(idea=request.idea)

        # 3. Sauvegarder l'analyse en DB
        await analysis_service.save_analysis(
            AnalysisCreate(
                project_id=project.id,
                result_json=analysis_data.model_dump(),
                model_used="llama-3.3-70b-versatile"
            )
        )

        logger.info(f"Analyse terminée avec succès pour le projet {project.id}")
        
        # On inclut l'ID du projet dans la réponse (si le frontend le veut)
        # Mais AnalysisData de analysis_schema ne l'a pas. 
        # On peut le renvoyer tel quel car le front s'attend à AnalysisData
        return AnalysisResponse(
            success=True,
            data=analysis_data,
            error=None,
        )

    except ValueError as exc:
        logger.warning(f"Données invalides : {exc}")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        )

    except Exception as exc:
        logger.error(f"Erreur lors de l'analyse : {exc}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Une erreur interne est survenue. Veuillez réessayer.",
        )


@router.get(
    "/health",
    tags=["Health"],
    summary="Health check",
    description="Vérifie que l'API est opérationnelle.",
)
async def health_check():
    return {"status": "ok", "service": "AI Project Architect API"}
