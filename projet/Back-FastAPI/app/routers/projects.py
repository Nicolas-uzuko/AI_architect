"""
Routeur pour la gestion des projets (Historique).
"""
import uuid
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas.project_schema import ProjectList, ProjectRead
from app.schemas.analysis_schema_db import AnalysisRead
from app.services.project_service import ProjectService
from app.services.analysis_service import AnalysisService
from pydantic import BaseModel

router = APIRouter(
    prefix="/api/projects",
    tags=["Projects"],
)

class ProjectDetailsResponse(BaseModel):
    project: ProjectRead
    latest_analysis: AnalysisRead | None = None

@router.get(
    "/",
    response_model=ProjectList,
    summary="Lister les projets de l'utilisateur",
)
async def list_projects(
    page: int = 1,
    page_size: int = 20,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Récupère l'historique des projets pour l'utilisateur actuel."""
    service = ProjectService(db)
    return await service.get_projects(user_id=user.id, page=page, page_size=page_size)


@router.get(
    "/{project_id}",
    response_model=ProjectDetailsResponse,
    summary="Obtenir les détails d'un projet",
)
async def get_project_details(
    project_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """
    Récupère un projet spécifique et sa dernière analyse.
    Idéal pour recharger un ancien projet dans le chat.
    """
    proj_service = ProjectService(db)
    analysis_service = AnalysisService(db)
    
    project = await proj_service.get_project(project_id)
    if project.user_id != user.id:
        raise HTTPException(status_code=403, detail="Accès refusé à ce projet")
        
    latest_analysis = await analysis_service.get_latest_analysis(project_id)
    
    return ProjectDetailsResponse(
        project=project,
        latest_analysis=latest_analysis
    )
