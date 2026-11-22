"""Community model - Comunidades / Juntas de vecinos."""

from __future__ import annotations

from sqlalchemy import ForeignKey, Index, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base, TimestampMixin
from models.space import Space


class Community(Base, TimestampMixin):
    """Model for community organizations (juntas de vecinos, comunidades de edificios)."""

    __tablename__ = "communities"

    # Primary key
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # Basic info
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    commune: Mapped[str] = mapped_column(String(100), nullable=True, index=True)

    # Contact
    contact_email: Mapped[str] = mapped_column(String(255), nullable=True)
    contact_phone: Mapped[str] = mapped_column(String(50), nullable=True)
    contact_person: Mapped[str] = mapped_column(String(255), nullable=True)

    # Metrics
    member_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    # Relationship to space (optional - a community can be linked to a space)
    space_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("spaces.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    # Relationship
    space: Mapped[Space] = relationship("Space", backref="communities")

    # Table indexes
    __table_args__ = (
        Index("ix_communities_commune_space", "commune", "space_id"),
    )

    def __repr__(self) -> str:
        return f"<Community(id={self.id}, name='{self.name}', commune='{self.commune}')>"
