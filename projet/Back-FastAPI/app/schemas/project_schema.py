"""
Schémas Pydantic v2 — Project.

Séparation claire Create / Read / Update / List.
"""

import uuid
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field

# Statuts possibles d'un projet
ProjectStatus = Literal["pending", "analyzing", "completed", "failed"]


# ─────────────────────────── Create ─────────────────────────────

class ProjectCreate(BaseModel):
    """Payload pour créer un nouveau projet."""

    title: str = Field(
        ...,
        min_length=3,
        max_length=500,
        description="Titre court du projet",
        examples=["Plateforme de vente en ligne"],
    )
    idea: str = Field(
        ...,
        min_length=10,
        max_length=5000,
        description="Description complète de l'idée de projet",
        examples=["Créer une application web de gestion de vente de chaussures"],
    )
    user_id: uuid.UUID = Field(
        ...,
        description="UUID de l'utilisateur propriétaire du projet",
    )


# ─────────────────────────── Read ───────────────────────────────

class ProjectRead(BaseModel):
    """Représentation complète d'un projet."""

    model_config = {"from_attributes": True}

    id: uuid.UUID
    user_id: uuid.UUID
    title: str
    idea: str
    status: str
    created_at: datetime
    updated_at: datetime


# ─────────────────────────── Update ─────────────────────────────

class ProjectUpdate(BaseModel):
    """Payload de mise à jour partielle d'un projet."""

    title: str | None = Field(default=None, min_length=3, max_length=500)
    idea: str | None = Field(default=None, min_length=10, max_length=5000)
    status: ProjectStatus | None = None


# ─────────────────────────── List ───────────────────────────────

class ProjectList(BaseModel):
    """Réponse paginée pour la liste des projets."""

    model_config = {"from_attributes": True}

    items: list[ProjectRead]
    total: int
    page: int = 1
    page_size: int = 20
