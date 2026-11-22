"""Partner model - Socios clave del proyecto."""

import enum

from sqlalchemy import Boolean, Index, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base, TimestampMixin


class PartnerType(enum.StrEnum):
    """Type of partner organization."""

    MUNICIPALITY = "municipality"       # Municipalidad
    COMPANY_RSE = "company_rse"         # Empresa con RSE
    NGO = "ngo"                         # ONG ambiental/urbanista
    NURSERY = "nursery"                 # Vivero
    UNIVERSITY = "university"           # Universidad
    COMMUNITY = "community"             # Junta de vecinos / comunidad


class Partner(Base, TimestampMixin):
    """Model for key partners (socios clave)."""

    __tablename__ = "partners"

    # Primary key
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # Basic info
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
    )
    description: Mapped[str] = mapped_column(Text, nullable=True)

    # Contact & Links
    logo_url: Mapped[str] = mapped_column(String(500), nullable=True)
    website_url: Mapped[str] = mapped_column(String(500), nullable=True)

    # Display
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    display_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    # Table indexes
    __table_args__ = (
        Index("ix_partners_type_active", "type", "is_active"),
        Index("ix_partners_display_order", "display_order"),
    )

    def __repr__(self) -> str:
        return f"<Partner(id={self.id}, name='{self.name}', type={self.type})>"

    @property
    def type_label(self) -> str:
        """Human-readable partner type label."""
        labels = {
            "municipality": "Municipalidad",
            "company_rse": "Empresa RSE",
            "ngo": "ONG",
            "nursery": "Vivero",
            "university": "Universidad",
            "community": "Comunidad",
        }
        return labels.get(self.type, self.type)

    @property
    def type_icon(self) -> str:
        """Icon name for partner type."""
        icons = {
            "municipality": "building-2",
            "company_rse": "briefcase",
            "ngo": "heart",
            "nursery": "leaf",
            "university": "graduation-cap",
            "community": "users",
        }
        return icons.get(self.type, "building")
