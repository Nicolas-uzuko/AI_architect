"""
Schémas Pydantic v2 — Analysis (couche DB).

Distinct de analysis_schema.py (qui gère les requêtes/réponses IA).
Ce fichier gère la persistance PostgreSQL des analyses.
"""

import uuid
from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


# ─────────────────────────── Create ─────────────────────────────

class AnalysisCreate(BaseModel):
    """Payload pour sauvegarder une analyse en base de données."""

    project_id: uuid.UUID = Field(
        ...,
        description="UUID du projet auquel cette analyse est liée",
    )
    result_json: dict[str, Any] = Field(
        ...,
        description="Résultat complet de l'analyse IA (stocké en JSONB)",
    )
    model_used: str = Field(
        default="llama-3.3-70b-versatile",
        max_length=100,
        description="Identifiant du modèle IA utilisé",
        examples=["llama-3.3-70b-versatile", "gpt-4o"],
    )


# ─────────────────────────── Read ───────────────────────────────

class AnalysisRead(BaseModel):
    """Représentation complète d'une analyse persistée."""

    model_config = {"from_attributes": True}

    id: uuid.UUID
    project_id: uuid.UUID
    result_json: dict[str, Any]
    model_used: str
    created_at: datetime


# ─────────────────────────── History ────────────────────────────

class AnalysisHistory(BaseModel):
    """Historique des analyses d'un projet."""

    project_id: uuid.UUID
    analyses: list[AnalysisRead]
    total: int
