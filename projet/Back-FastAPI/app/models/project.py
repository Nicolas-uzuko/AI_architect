"""
Modèle SQLAlchemy — Project.

Table : projects
Relations :
  - Project N──1 User
  - Project 1──N Analysis
"""

import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, UUIDMixin, TimestampMixin


class Project(UUIDMixin, TimestampMixin, Base):
    """Table des projets analysés par l'IA."""

    __tablename__ = "projects"

    # ── Colonnes ─────────────────────────────────────────────────
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    title: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )
    idea: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="pending",   # pending | analyzing | completed | failed
        index=True,
    )

    # ── Relations ─────────────────────────────────────────────────
    user: Mapped["User"] = relationship(  # type: ignore[name-defined]
        "User",
        back_populates="projects",
        lazy="select",
    )
    analyses: Mapped[list["Analysis"]] = relationship(  # type: ignore[name-defined]
        "Analysis",
        back_populates="project",
        cascade="all, delete-orphan",
        lazy="select",
        order_by="Analysis.created_at.desc()",
    )

    def __repr__(self) -> str:
        return f"<Project id={self.id} title={self.title!r} status={self.status!r}>"
