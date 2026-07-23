"""
Modèle SQLAlchemy — Analysis.

Table : analyses
Relations : Analysis N──1 Project

Stockage du résultat JSON de l'IA en colonne JSONB PostgreSQL.
"""

import uuid
from datetime import datetime
from typing import Any

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, UUIDMixin


class Analysis(UUIDMixin, Base):
    """Table des analyses IA liées aux projets."""

    __tablename__ = "analyses"

    # ── Colonnes ─────────────────────────────────────────────────
    project_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    result_json: Mapped[dict[str, Any]] = mapped_column(
        JSONB,
        nullable=False,
        comment="Résultat complet de l'analyse IA en format JSON",
    )
    model_used: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        default="llama-3.3-70b-versatile",
        comment="Modèle IA utilisé pour générer l'analyse",
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        index=True,
    )

    # ── Relations ─────────────────────────────────────────────────
    project: Mapped["Project"] = relationship(  # type: ignore[name-defined]
        "Project",
        back_populates="analyses",
        lazy="select",
    )

    def __repr__(self) -> str:
        return f"<Analysis id={self.id} project_id={self.project_id} model={self.model_used!r}>"
