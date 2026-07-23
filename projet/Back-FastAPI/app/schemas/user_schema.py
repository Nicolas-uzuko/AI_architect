"""
Schémas Pydantic v2 — User.

Séparation claire Create / Read / Update.
"""

import uuid
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


# ─────────────────────────── Create ─────────────────────────────

class UserCreate(BaseModel):
    """Payload pour créer un nouvel utilisateur."""

    name: str = Field(
        ...,
        min_length=2,
        max_length=255,
        description="Nom complet de l'utilisateur",
        examples=["Alice Dupont"],
    )
    email: EmailStr = Field(
        ...,
        description="Adresse email unique",
        examples=["alice@example.com"],
    )
    password: str = Field(
        ...,
        min_length=8,
        max_length=128,
        description="Mot de passe en clair (sera hashé côté serveur)",
    )


# ─────────────────────────── Read ───────────────────────────────

class UserRead(BaseModel):
    """Représentation publique d'un utilisateur (sans password_hash)."""

    model_config = {"from_attributes": True}

    id: uuid.UUID
    name: str
    email: str
    created_at: datetime


# ─────────────────────────── Update ─────────────────────────────

class UserUpdate(BaseModel):
    """Payload de mise à jour partielle d'un utilisateur."""

    name: str | None = Field(default=None, min_length=2, max_length=255)
    email: EmailStr | None = None
