"""Community model - Comunidades / Juntas de vecinos."""

from __future__ import annotations

from sqlalchemy import ForeignKey, Index, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base, TimestampMixin
from models.space import Space


class Community(Base, TimestampMixin):
    """Model for community organizations (juntas de vecinos, comunidades de edificios)."""

    __tablename__ = "communities"


    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)


    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    commune: Mapped[str] = mapped_column(String(100), nullable=True, index=True)


    contact_email: Mapped[str] = mapped_column(String(255), nullable=True)
    contact_phone: Mapped[str] = mapped_column(String(50), nullable=True)
    contact_person: Mapped[str] = mapped_column(String(255), nullable=True)


    member_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)


    space_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("spaces.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )


    space: Mapped[Space] = relationship("Space", backref="communities")


    __table_args__ = (
        Index("ix_communities_commune_space", "commune", "space_id"),
    )

    def __repr__(self) -> str:
        return f"<Community(id={self.id}, name='{self.name}', commune='{self.commune}')>"
