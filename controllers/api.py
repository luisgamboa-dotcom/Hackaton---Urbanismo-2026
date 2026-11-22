"""API Controller for future REST endpoints."""

from contextlib import suppress
from typing import Any

from sqlalchemy.sql.elements import ColumnElement

from controllers.base import BaseController
from models import Community, ImpactMetric, Partner, Space
from models.partner import PartnerType
from models.space import SpaceCategory, SpaceStatus


class APIController(BaseController):
    """Controller for API endpoints (JSON responses)."""





    async def list_spaces(
        self,
        status: SpaceStatus | None = None,
        category: SpaceCategory | None = None,
        commune: str | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> dict[str, Any]:
        """List spaces with filters and pagination."""
        filters: list[ColumnElement[bool]] = []
        if status:
            filters.append(Space.status == status.value)
        if category:
            filters.append(Space.category == category.value)
        if commune:
            filters.append(Space.commune.ilike(f"%{commune}%"))

        spaces = self.get_all(
            Space,
            *filters,
            order_by=Space.created_at.desc(),
            limit=limit,
            offset=offset,
        )
        total = self.count(Space, *filters)

        return {
            "data": spaces,
            "total": total,
            "limit": limit,
            "offset": offset,
        }

    async def get_space(self, space_id: int) -> Space | None:
        """Get a single space by ID."""
        return self.get_one(Space, Space.id == space_id)





    async def list_partners(
        self,
        type_: str | None = None,
        active_only: bool = True,
    ) -> list[Partner]:
        """List partners with optional type filter."""
        filters: list[ColumnElement[bool]] = []
        if active_only:
            filters.append(Partner.is_active == True)
        if type_:
            with suppress(ValueError):
                filters.append(Partner.type == PartnerType(type_).value)
        return self.get_all(
            Partner,
            *filters,
            order_by=Partner.display_order,
        )





    async def get_metrics(self) -> list[ImpactMetric]:
        """Get all impact metrics."""
        return self.get_all(ImpactMetric, order_by=ImpactMetric.display_order)

    async def get_metric(self, metric_key: str) -> ImpactMetric | None:
        """Get a single metric by key."""
        return self.get_one(ImpactMetric, ImpactMetric.metric_key == metric_key)





    async def list_communities(
        self,
        commune: str | None = None,
        space_id: int | None = None,
    ) -> list[Community]:
        """List communities with optional filters."""
        filters: list[ColumnElement[bool]] = []
        if commune:
            filters.append(Community.commune.ilike(f"%{commune}%"))
        if space_id:
            filters.append(Community.space_id == space_id)
        return self.get_all(Community, *filters, order_by=Community.name)





    async def get_dashboard_stats(self) -> dict[str, Any]:
        """Get aggregated statistics for dashboard."""


        metrics = await self.get_metrics()
        metrics_dict = {m.metric_key: m.value for m in metrics}


        spaces_by_status = {}
        for status in SpaceStatus:
            count = self.count(Space, Space.status == status.value)
            spaces_by_status[status.value] = count

        spaces_by_category = {}
        for category in SpaceCategory:
            count = self.count(Space, Space.category == category.value)
            spaces_by_category[category.value] = count

        partners_by_type = {}
        for ptype in PartnerType:
            count = self.count(Partner, Partner.type == ptype.value, Partner.is_active == True)
            partners_by_type[ptype.value] = count

        return {
            "metrics": metrics_dict,
            "spaces_by_status": spaces_by_status,
            "spaces_by_category": spaces_by_category,
            "partners_by_type": partners_by_type,
            "total_communities": self.count(Community),
        }





    def get_map_spaces(
        self,
        category: str | None = None,
        status: str | None = None,
        commune: str | None = None,
    ) -> dict[str, Any]:
        """Get spaces with coordinates for map markers (GeoJSON-like format)."""
        filters: list[ColumnElement[bool]] = [
            Space.latitude.is_not(None),
            Space.longitude.is_not(None)
        ]

        if category:
            filters.append(Space.category == category)
        if status:
            filters.append(Space.status == status)
        if commune:
            filters.append(Space.commune.ilike(f"%{commune}%"))

        spaces = self.get_all(
            Space,
            *filters,
            order_by=Space.created_at.desc(),
        )

        return {
            "spaces": [
                {
                    "id": s.id,
                    "name": s.name,
                    "description": s.description,
                    "commune": s.commune,
                    "category": s.category,
                    "category_label": s.category_label,
                    "status": s.status.value if hasattr(s.status, 'value') else s.status,
                    "status_label": s.status_label,
                    "area_m2": s.area_m2,
                    "latitude": float(s.latitude) if s.latitude else None,
                    "longitude": float(s.longitude) if s.longitude else None,
                    "image_url": s.image_url,
                    "before_image_url": s.before_image_url
                }
                for s in spaces
            ]
        }
