"""Impact Metric model - Métricas de impacto agregadas."""

from sqlalchemy import BigInteger, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base, TimestampMixin


class ImpactMetric(Base, TimestampMixin):
    """Model for aggregated impact metrics (KPIs)."""

    __tablename__ = "impact_metrics"

    # Primary key
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # Metric identifier (unique key)
    metric_key: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
        index=True,
    )

    # Value and display
    value: Mapped[int] = mapped_column(BigInteger, default=0, nullable=False)
    label: Mapped[str] = mapped_column(String(255), nullable=False)
    icon: Mapped[str] = mapped_column(String(100), nullable=True)

    # Display order
    display_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    # Constraints
    __table_args__ = (
        UniqueConstraint("metric_key", name="uq_impact_metrics_key"),
    )

    def __repr__(self) -> str:
        return f"<ImpactMetric(key='{self.metric_key}', value={self.value}, label='{self.label}')>"

    @property
    def formatted_value(self) -> str:
        """Format value with thousand separators."""
        return f"{self.value:,}".replace(",", ".")


# Predefined metric keys (constants for consistency)
class MetricKeys:
    """Standard metric keys used across the application."""

    TOTAL_M2_RECOVERED = "total_m2_recovered"
    TOTAL_SPACES = "total_spaces"
    TOTAL_VOLUNTEERS = "total_volunteers"
    TOTAL_COMMUNES = "total_communes"
    TOTAL_PARTNERS = "total_partners"
    TOTAL_COMMUNITIES = "total_communities"

    @classmethod
    def all_keys(cls) -> list[str]:
        """Return all predefined metric keys."""
        return [
            cls.TOTAL_M2_RECOVERED,
            cls.TOTAL_SPACES,
            cls.TOTAL_VOLUNTEERS,
            cls.TOTAL_COMMUNES,
            cls.TOTAL_PARTNERS,
            cls.TOTAL_COMMUNITIES,
        ]


# Default metric configurations
DEFAULT_METRICS = [
    {
        "metric_key": MetricKeys.TOTAL_M2_RECOVERED,
        "value": 2450,
        "label": "m² de suelo vivo recuperados",
        "icon": "leaf",
        "display_order": 1,
    },
    {
        "metric_key": MetricKeys.TOTAL_SPACES,
        "value": 12,
        "label": "Espacios intervenidos",
        "icon": "map-pin",
        "display_order": 2,
    },
    {
        "metric_key": MetricKeys.TOTAL_VOLUNTEERS,
        "value": 340,
        "label": "Voluntarios activos",
        "icon": "users",
        "display_order": 3,
    },
    {
        "metric_key": MetricKeys.TOTAL_COMMUNES,
        "value": 5,
        "label": "Comunas de Santiago",
        "icon": "building-2",
        "display_order": 4,
    },
    {
        "metric_key": MetricKeys.TOTAL_PARTNERS,
        "value": 9,
        "label": "Socios estratégicos",
        "icon": "handshake",
        "display_order": 5,
    },
    {
        "metric_key": MetricKeys.TOTAL_COMMUNITIES,
        "value": 8,
        "label": "Comunidades organizadas",
        "icon": "users-round",
        "display_order": 6,
    },
]
