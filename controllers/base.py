"""Base controller with common functionality."""

from typing import Any, Generic, TypeVar

from sqlalchemy import func, select
from sqlalchemy.orm import Session
from sqlalchemy.sql.elements import ColumnElement

from models import ImpactMetric, Partner, Space

ModelType = TypeVar("ModelType")


class BaseController(Generic[ModelType]):
    """Base controller with common database operations."""

    def __init__(self, session: Session):
        self.session = session

    def get_all(
        self,
        model: type[ModelType],
        *filters: ColumnElement[bool],
        order_by: Any = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> list[ModelType]:
        """Get all records with optional filters, ordering, and pagination."""
        stmt = select(model)
        for f in filters:
            stmt = stmt.where(f)
        if order_by is not None:
            stmt = stmt.order_by(order_by)
        if limit:
            stmt = stmt.limit(limit)
        if offset:
            stmt = stmt.offset(offset)
        result = self.session.execute(stmt)
        return list(result.scalars().all())

    def get_one(
        self,
        model: type[ModelType],
        *filters: ColumnElement[bool],
        order_by: Any = None,
    ) -> ModelType | None:
        """Get a single record matching filters."""
        stmt = select(model)
        for f in filters:
            stmt = stmt.where(f)
        if order_by is not None:
            stmt = stmt.order_by(order_by)
        result = self.session.execute(stmt)
        return result.scalar_one_or_none()

    def count(self, model: type[ModelType], *filters: ColumnElement[bool]) -> int:
        """Count records matching filters."""
        stmt = select(func.count()).select_from(model)
        for f in filters:
            stmt = stmt.where(f)
        result = self.session.execute(stmt)
        return result.scalar() or 0


class LandingController(BaseController):
    """Controller for landing page data."""

    def get_hero_space(self) -> Space | None:
        """Get featured space for hero section (first completed space with images)."""
        results = self.get_all(
            Space,
            Space.status == "completed",
            Space.image_url.is_not(None),
            Space.before_image_url.is_not(None),
            order_by=Space.completed_at.desc(),
            limit=1,
        )
        return results[0] if results else None

    def get_value_props(self) -> list[dict]:
        """Get data for value proposition section (3 pillars)."""
        # These are static content based on the business model canvas
        return [
            {
                "icon": "leaf",
                "title": "Espacios Vivos",
                "description": "Recuperamos lotes baldíos y espacios residuales transformándolos en áreas verdes, plazas de bolsillo y huertos comunitarios que regeneran el suelo y la biodiversidad urbana.",
                "metric_key": "total_m2_recovered",
            },
            {
                "icon": "users",
                "title": "Comunidad Activa",
                "description": "Fomentamos la participación vecinal en el diseño, construcción y cuidado de los espacios. Juntas de vecinos, colegios y voluntarios son los verdaderos protagonistas.",
                "metric_key": "total_communities",
            },
            {
                "icon": "trending-up",
                "title": "Impacto Medible",
                "description": "Cada metro cuadrado recuperado se monitorea: biodiversidad, uso social, bienestar comunitario. Transparencia total en la gestión de recursos públicos y privados.",
                "metric_key": "total_spaces",
            },
        ]

    def get_stats(self) -> list[ImpactMetric]:
        """Get impact metrics for stats bar."""
        return self.get_all(
            ImpactMetric,
            order_by=ImpactMetric.display_order,
        )

    def get_featured_spaces(self, limit: int = 6) -> list[Space]:
        """Get featured spaces for grid (completed + in_progress, with images)."""
        return self.get_all(
            Space,
            Space.status.in_(["completed", "in_progress"]),
            Space.image_url.is_not(None),
            order_by=Space.created_at.desc(),
            limit=limit,
        )

    def get_all_spaces(self) -> list[Space]:
        """Get all spaces for map/filter view."""
        return self.get_all(
            Space,
            order_by=(Space.commune, Space.name),
        )

    def get_active_partners(self) -> list[Partner]:
        """Get active partners ordered by display_order."""
        return self.get_all(
            Partner,
            Partner.is_active == True,  # noqa: E712
            order_by=Partner.display_order,
        )

    def get_partners_by_type(self) -> dict[str, list[Partner]]:
        """Get partners grouped by type."""
        partners = self.get_active_partners()
        grouped: dict[str, list[Partner]] = {}
        for p in partners:
            key = p.type
            if key not in grouped:
                grouped[key] = []
            grouped[key].append(p)
        return grouped

    def get_home_data(self) -> dict[str, Any]:
        """Get all data needed for the landing page in one call."""
        hero_space = self.get_hero_space()
        value_props = self.get_value_props()
        stats = self.get_stats()
        featured_spaces = self.get_featured_spaces(limit=6)
        partners = self.get_active_partners()
        partners_by_type = self.get_partners_by_type()

        # Enrich value props with actual metric values
        stats_dict = {s.metric_key: s for s in stats}
        for vp in value_props:
            if vp["metric_key"] in stats_dict:
                vp["metric_value"] = stats_dict[vp["metric_key"]].formatted_value
                vp["metric_label"] = stats_dict[vp["metric_key"]].label

        # Spaces with coordinates for map fallback
        spaces_with_coords = self.get_all(
            Space,
            Space.latitude.is_not(None),
            Space.longitude.is_not(None),
        )
        spaces_for_map = [
            {
                "id": s.id,
                "name": s.name,
                "description": s.description,
                "commune": s.commune,
                "category": s.category,
                "category_label": s.category_label,
                "status": s.status,
                "status_label": s.status_label,
                "area_m2": s.area_m2,
                "latitude": float(s.latitude) if s.latitude else None,
                "longitude": float(s.longitude) if s.longitude else None,
            }
            for s in spaces_with_coords
        ]

        return {
            "hero_space": hero_space,
            "value_props": value_props,
            "stats": stats,
            "featured_spaces": featured_spaces,
            "partners": partners,
            "partners_by_type": partners_by_type,
            "spaces_for_map": spaces_for_map,
            "site_name": "Green Tech",
            "site_tagline": "Recuperación Urbana Táctica en Santiago",
        }
