"""Space model - Espacio/Proyecto de intervención urbana."""

import enum
from datetime import date

from sqlalchemy import Date, Index, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base, TimestampMixin


# Status and category constants (as strings for DB)
class SpaceStatus(enum.StrEnum):
    IDENTIFIED = "identified"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    MAINTAINED = "maintained"


class SpaceCategory(enum.StrEnum):
    POCKET_PARK = "pocket_park"
    GREEN_CORRIDOR = "green_corridor"
    COMMUNITY_GARDEN = "community_garden"
    PLAYGROUND = "playground"
    RESTING_AREA = "resting_area"
    URBAN_FOREST = "urban_forest"
    ABANDONED_LAND = "abandoned_land"
    DUMPING_GROUND = "dumping_ground"


class Space(Base, TimestampMixin):
    """Model for urban space recovery projects."""

    __tablename__ = "spaces"

    # Primary key
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # Basic info
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    address: Mapped[str] = mapped_column(String(500), nullable=True)
    commune: Mapped[str] = mapped_column(String(100), nullable=True, index=True)

    # Geolocation
    latitude: Mapped[float] = mapped_column(Numeric(10, 8), nullable=True)
    longitude: Mapped[float] = mapped_column(Numeric(11, 8), nullable=True)

    # Metrics
    area_m2: Mapped[int] = mapped_column(Integer, nullable=True)

    # Status & Category
    status: Mapped[str] = mapped_column(
        String(50),
        default=SpaceStatus.IDENTIFIED,
        nullable=False,
        index=True,
    )
    category: Mapped[str] = mapped_column(
        String(50),
        nullable=True,
        index=True,
    )

    # Images
    image_url: Mapped[str] = mapped_column(String(500), nullable=True)
    before_image_url: Mapped[str] = mapped_column(String(500), nullable=True)

    # Timeline
    started_at: Mapped[date] = mapped_column(Date, nullable=True)
    completed_at: Mapped[date] = mapped_column(Date, nullable=True)

    # Table indexes
    __table_args__ = (
        Index("ix_spaces_commune_status", "commune", "status"),
        Index("ix_spaces_status_category", "status", "category"),
    )

    def __repr__(self) -> str:
        return f"<Space(id={self.id}, name='{self.name}', commune='{self.commune}', status={self.status})>"

    @property
    def coordinates(self) -> tuple[float, float] | None:
        """Return (lat, lng) tuple if both coordinates exist."""
        if self.latitude is not None and self.longitude is not None:
            return (float(self.latitude), float(self.longitude))
        return None

    @property
    def is_active(self) -> bool:
        """Check if space is currently being worked on."""
        return self.status in (SpaceStatus.IN_PROGRESS, SpaceStatus.MAINTAINED)

    @property
    def status_label(self) -> str:
        """Human-readable status label."""
        labels = {
            "identified": "Identificado",
            "in_progress": "En Progreso",
            "completed": "Completado",
            "maintained": "En Mantenimiento",
        }
        return labels.get(self.status, self.status)

    @property
    def category_label(self) -> str:
        """Human-readable category label."""
        labels = {
            "pocket_park": "Plaza de Bolsillo",
            "green_corridor": "Corredor Verde",
            "community_garden": "Huerto Comunitario",
            "playground": "Área de Juegos",
            "resting_area": "Zona de Descanso",
            "urban_forest": "Mini Bosque Urbano",
        }
        return labels.get(self.category, self.category if self.category else "Sin categoría")
