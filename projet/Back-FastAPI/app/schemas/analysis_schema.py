"""
Schémas Pydantic pour l'analyse de projet IA.
Prêt pour : PostgreSQL, Auth JWT, Export PDF, Génération UML.
"""

from pydantic import BaseModel, Field
from typing import Any, Optional


# ─────────────────────────── Request ────────────────────────────

class AnalysisRequest(BaseModel):
    """Payload envoyé par le frontend pour analyser une idée de projet."""
    idea: str = Field(
        ...,
        min_length=10,
        max_length=5000,
        description="Description textuelle de l'idée de projet",
        examples=["Créer une application web de gestion de vente de chaussures"],
    )


# ─────────────────────────── Sub-models ─────────────────────────

class CahierDesCharges(BaseModel):
    """Cahier des charges structuré du projet."""
    description: str = Field(
        default="",
        description="Description générale du projet",
    )
    objectifs: list[str] = Field(
        default_factory=list,
        description="Objectifs principaux du projet",
    )
    utilisateurs: list[str] = Field(
        default_factory=list,
        description="Types d'utilisateurs cibles",
    )
    fonctionnalites: list[str] = Field(
        default_factory=list,
        description="Liste des fonctionnalités principales",
    )
    contraintes: list[str] = Field(
        default_factory=list,
        description="Contraintes techniques et métier",
    )
    technologies: list[str] = Field(
        default_factory=list,
        description="Stack technologique recommandée",
    )


class AnalysisData(BaseModel):
    """Données complètes retournées par l'IA."""
    cahier_des_charges: CahierDesCharges = Field(
        default_factory=CahierDesCharges,
        description="Cahier des charges complet du projet",
    )
    diagramme_simple: str = Field(
        default="",
        description="Représentation textuelle du diagramme d'architecture",
    )
    taches_github: list[str] = Field(
        default_factory=list,
        description="Liste des issues/tâches GitHub à créer",
    )
    squelette_code: dict[str, Any] = Field(
        default_factory=dict,
        description="Structure de fichiers et squelette du projet",
    )


# ─────────────────────────── Response ───────────────────────────

class AnalysisResponse(BaseModel):
    """Réponse standard de l'API d'analyse."""
    success: bool = Field(
        default=True,
        description="Indique si l'analyse s'est déroulée avec succès",
    )
    data: Optional[AnalysisData] = Field(
        default=None,
        description="Données de l'analyse (null en cas d'erreur)",
    )
    error: Optional[str] = Field(
        default=None,
        description="Message d'erreur (null en cas de succès)",
    )


class ErrorResponse(BaseModel):
    """Réponse en cas d'erreur."""
    success: bool = False
    data: None = None
    error: str
