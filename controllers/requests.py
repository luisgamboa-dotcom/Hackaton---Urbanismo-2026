"""Requests Controller - Handles citizen requests, supports, and routing."""

from datetime import UTC, datetime, timedelta
from typing import Any

from sqlalchemy import desc, func, select
from sqlalchemy.sql.elements import ColumnElement

from config.settings import get_settings
from controllers.base import BaseController
from models import (
    ModerationQueue,
    Organization,
    OrganizationType,
    Request,
    RequestStatus,
    SubmissionHistory,
    Support,
    User,
)
from utils.email import email_service

settings = get_settings()


class RequestsController(BaseController):
    """Controller for citizen requests and related functionality."""





    def get_user_by_email(self, email: str) -> User | None:
        """Get user by email."""
        return self.get_one(User, User.email == email.lower().strip())

    def get_user_by_id(self, user_id: int) -> User | None:
        """Get user by ID."""
        return self.get_one(User, User.id == user_id)

    def create_user(self, name: str, email: str, phone: str | None = None, commune: str | None = None) -> User:
        """Create a new user."""
        user = User(
            name=name.strip(),
            email=email.lower().strip(),
            phone=phone.strip() if phone else None,
            commune=commune.strip() if commune else None,
            role="citizen",
        )
        self.session.add(user)
        self.session.flush()
        return user

    def get_or_create_user(self, name: str, email: str, phone: str | None = None, commune: str | None = None) -> User:
        """Get existing user or create new one."""
        user = self.get_user_by_email(email)
        if user:

            user.last_login_at = datetime.now(UTC)
            if phone and not user.phone:
                user.phone = phone.strip()
            if commune and not user.commune:
                user.commune = commune.strip()
            self.session.flush()
            return user
        return self.create_user(name, email, phone, commune)





    def create_request(
        self,
        user_id: int,
        address: str,
        latitude: float,
        longitude: float,
        commune: str,
        title: str,
        description: str,
        needs: str,
        category: str,
        reference: str | None = None,
        estimated_area_m2: int | None = None,
        photo_url: str | None = None,
    ) -> Request:
        """Create a new citizen request."""
        request = Request(
            user_id=user_id,
            address=address.strip(),
            latitude=latitude,
            longitude=longitude,
            commune=commune.strip(),
            reference=reference.strip() if reference else None,
            title=title.strip(),
            description=description.strip(),
            needs=needs.strip(),
            category=category,
            estimated_area_m2=estimated_area_m2,
            photo_url=photo_url,
            status=RequestStatus.PENDING_MODERATION,
        )
        self.session.add(request)
        self.session.flush()


        moderation = ModerationQueue(request_id=request.id)
        self.session.add(moderation)
        self.session.flush()


        try:
            user = self.get_user_by_id(user_id)
            email_service.send_request_notification({
                "title": request.title,
                "category": request.category_label,
                "address": request.address,
                "commune": request.commune,
                "latitude": request.latitude,
                "longitude": request.longitude,
                "estimated_area_m2": request.estimated_area_m2,
                "description": request.description,
                "needs": request.needs,
                "user_name": user.name if user else "Anónimo",
                "user_email": user.email if user else "No disponible",
                "user_phone": user.phone if user else "No disponible",
                "user_commune": user.commune if user else "No disponible",
                "support_count": 0,
            })
        except Exception as e:
            print(f"Failed to send request notification email: {e}")

        return request

    def get_request_by_id(self, request_id: int) -> Request | None:
        """Get request by ID."""
        return self.get_one(Request, Request.id == request_id)

    def get_requests(
        self,
        user_id: int | None = None,
        commune: str | None = None,
        status: str | None = None,
        category: str | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> dict[str, Any]:
        """List requests with filters."""
        filters: list[ColumnElement[bool]] = []

        if user_id:
            filters.append(Request.user_id == user_id)
        if commune:
            filters.append(Request.commune.ilike(f"%{commune}%"))
        if status:
            filters.append(Request.status == status)
        if category:
            filters.append(Request.category == category)


        if not status:
            filters.append(Request.status.not_in([RequestStatus.DRAFT, RequestStatus.REJECTED]))

        requests = self.get_all(
            Request,
            *filters,
            order_by=desc(Request.created_at),
            limit=limit,
            offset=offset,
        )
        total = self.count(Request, *filters)

        return {
            "data": requests,
            "total": total,
            "limit": limit,
            "offset": offset,
        }

    def get_user_requests(self, user_id: int, limit: int = 20, offset: int = 0) -> dict[str, Any]:
        """Get requests created by a specific user (including drafts)."""
        filters = [Request.user_id == user_id]
        requests = self.get_all(
            Request,
            *filters,
            order_by=desc(Request.created_at),
            limit=limit,
            offset=offset,
        )
        total = self.count(Request, *filters)
        return {"data": requests, "total": total, "limit": limit, "offset": offset}

    def update_request_status(
        self, request_id: int, status: str, **kwargs: Any
    ) -> Request | None:
        """Update request status and related fields."""
        request = self.get_request_by_id(request_id)
        if not request:
            return None

        request.status = status
        for key, value in kwargs.items():
            if hasattr(request, key):
                setattr(request, key, value)

        self.session.flush()
        return request





    def add_support(self, user_id: int, request_id: int) -> Support | None:
        """Add user support to a request. Returns None if already supported."""

        existing = self.get_one(Support, Support.user_id == user_id, Support.request_id == request_id)
        if existing:
            return None


        request = self.get_request_by_id(request_id)
        if not request or request.status in (RequestStatus.DRAFT, RequestStatus.REJECTED, RequestStatus.CLOSED):
            return None

        support = Support(user_id=user_id, request_id=request_id)
        self.session.add(support)


        request.support_count += 1
        self.session.flush()


        try:
            user = self.get_user_by_id(user_id)
            if user and user.email:
                email_service.send_support_confirmation({
                    "title": request.title,
                    "support_count": request.support_count,
                }, user.email, user.name)
        except Exception as e:
            print(f"Failed to send support confirmation email: {e}")

        return support

    def remove_support(self, user_id: int, request_id: int) -> bool:
        """Remove user support from a request."""
        support = self.get_one(Support, Support.user_id == user_id, Support.request_id == request_id)
        if not support:
            return False

        request = self.get_request_by_id(request_id)
        if request:
            request.support_count = max(0, request.support_count - 1)

        self.session.delete(support)
        self.session.flush()
        return True

    def has_user_supported(self, user_id: int, request_id: int) -> bool:
        """Check if user has supported a request."""
        return self.get_one(Support, Support.user_id == user_id, Support.request_id == request_id) is not None

    def get_support_count(self, request_id: int) -> int:
        """Get support count for a request."""
        return self.count(Support, Support.request_id == request_id)

    def get_user_supports(self, user_id: int, limit: int = 20, offset: int = 0) -> dict[str, Any]:
        """Get requests supported by a user."""
        supports = self.get_all(
            Support,
            Support.user_id == user_id,
            order_by=desc(Support.created_at),
            limit=limit,
            offset=offset,
        )
        total = self.count(Support, Support.user_id == user_id)
        return {"data": supports, "total": total, "limit": limit, "offset": offset}





    def get_organizations(
        self,
        type_: str | None = None,
        commune: str | None = None,
        active_only: bool = True,
    ) -> list[Organization]:
        """Get organizations with filters."""
        filters: list[ColumnElement[bool]] = []
        if active_only:
            filters.append(Organization.is_active == True)
        if type_:
            filters.append(Organization.type == type_)
        if commune:
            filters.append(Organization.commune == commune)
        return self.get_all(Organization, *filters, order_by=Organization.priority_order)

    def get_municipality_for_commune(self, commune: str) -> Organization | None:
        """Get the municipality organization for a specific commune."""
        return self.get_one(
            Organization,
            Organization.type == OrganizationType.MUNICIPALITY,
            Organization.commune == commune,
            Organization.is_active == True,
        )

    def get_next_routing_organizations(
        self,
        current_type: str | None,
        commune: str | None = None,
    ) -> list[Organization]:
        """Get the next organizations in the routing sequence."""

        routing_order = [
            OrganizationType.MUNICIPALITY,
            OrganizationType.COMPANY,
            OrganizationType.SCHOOL,
            OrganizationType.UNIVERSITY,
            OrganizationType.SOCIAL_MEDIA,
        ]

        if current_type is None:

            if commune:
                muni = self.get_municipality_for_commune(commune)
                if muni:
                    return [muni]

            return self.get_organizations(type_=OrganizationType.MUNICIPALITY, active_only=True)[:1]

        try:
            current_idx = routing_order.index(current_type)
            next_idx = current_idx + 1
        except ValueError:
            return []

        if next_idx >= len(routing_order):
            return []

        next_type = routing_order[next_idx]

        if next_type == OrganizationType.MUNICIPALITY and commune:
            muni = self.get_municipality_for_commune(commune)
            return [muni] if muni else []

        return self.get_organizations(type_=next_type, active_only=True)

    def get_organization_by_id(self, org_id: int) -> Organization | None:
        """Get organization by ID."""
        return self.get_one(Organization, Organization.id == org_id)





    def get_wait_days(self) -> int:
        """Get configured wait days from system config or default."""


        return 15

    def calculate_deadline(self, sent_at: datetime | None = None) -> datetime:
        """Calculate deadline for response."""
        base = sent_at or datetime.now(UTC)
        return base + timedelta(days=self.get_wait_days())

    def submit_to_organization(
        self,
        request_id: int,
        organization_id: int,
        sent_by: str = "auto",
    ) -> SubmissionHistory | None:
        """Record a submission to an organization."""
        request = self.get_request_by_id(request_id)
        organization = self.get_organization_by_id(organization_id)

        if not request or not organization:
            return None


        existing = self.get_one(
            SubmissionHistory,
            SubmissionHistory.request_id == request_id,
            SubmissionHistory.organization_id == organization_id,
            SubmissionHistory.status == "sent",
        )
        if existing:
            return existing


        subject = organization.custom_subject or f"Solicitud de recuperación urbana: {request.title}"
        body = self.generate_request_message(request, organization)

        submission = SubmissionHistory(
            request_id=request_id,
            organization_id=organization_id,
            sent_by=sent_by,
            message_subject=subject,
            message_body=body,
            message_recipient=organization.email,
            status="sent",
            sent_at=datetime.now(UTC),
        )
        self.session.add(submission)


        request.current_recipient_type = organization.type
        request.current_recipient_id = organization.id
        request.current_recipient_name = organization.name
        request.current_recipient_email = organization.email
        request.sent_at = datetime.now(UTC)
        request.deadline_at = self.calculate_deadline(datetime.now(UTC))
        request.status = RequestStatus.SENT

        self.session.flush()


        try:
            email_service.send_routing_notification({
                "title": request.title,
            }, {
                "name": organization.name,
                "type": organization.type.value,
                "email": organization.email,
            })
        except Exception as e:
            print(f"Failed to send routing notification email: {e}")

        return submission

    def generate_request_message(self, request: Request, organization: Organization) -> str:
        """Generate formal message for request submission."""
        if organization.custom_message:
            return organization.custom_message.format(
                request_title=request.title,
                request_address=request.address,
                request_commune=request.commune,
                request_description=request.description,
                request_needs=request.needs,
                request_category=request.category_label,
                request_supports=request.support_count,
                request_user_name=request.user.name if request.user else "Ciudadano",
                request_photo_url=request.photo_url or "No disponible",
                organization_name=organization.name,
            )

        return f"""
Estimados {organization.name}:

Por medio de la presente, la plataforma Green Tech les hace llegar una solicitud ciudadana para la recuperación de un espacio urbano en la comuna de {request.commune}.

DETALLES DE LA SOLICITUD:
- Título: {request.title}
- Categoría: {request.category_label}
- Dirección/Referencia: {request.address}
- Comuna: {request.commune}
- Coordenadas: {request.latitude}, {request.longitude}
- Área estimada: {request.estimated_area_m2 or 'No especificada'} m²

DESCRIPCIÓN DEL ESPACIO:
{request.description}

NECESIDADES IDENTIFICADAS:
{request.needs}

APOYO CIUDADANO:
Esta solicitud cuenta con {request.support_count} apoyo(s) de vecinos registrados en la plataforma.

SOLICITANTE:
Nombre: {request.user.name if request.user else 'Ciudadano anónimo'}
Correo: {request.user.email if request.user else 'No disponible'}

FOTOGRAFÍA:
{request.photo_url or 'No disponible'}

SOLICITAMOS:
Evaluar la factibilidad de intervenir este espacio para transformarlo en un área verde comunitaria (plaza de bolsillo, corredor verde, huerto comunitario, zona de descanso, área de juegos o mini bosque urbano), de acuerdo con las competencias y recursos de su institución.

Quedamos a disposición para coordinar una visita a terreno y proporcionar información adicional.

Atentamente,
Equipo Green Tech
https://tramaurbanaverde.cl
        """.strip()

    def process_routing(self, request_id: int) -> bool:
        """Process automatic routing for a request."""
        request = self.get_request_by_id(request_id)
        if not request:
            return False


        if (
            request.current_recipient_id
            and request.status in (RequestStatus.SENT, RequestStatus.WAITING_RESPONSE)
            and request.deadline_at
            and datetime.now(UTC) > request.deadline_at
        ):

            return self.advance_routing(request_id)


        if not request.current_recipient_id:
            return self.start_routing(request_id)

        return False

    def start_routing(self, request_id: int) -> bool:
        """Start the routing process for a request."""
        request = self.get_request_by_id(request_id)
        if not request:
            return False

        next_orgs = self.get_next_routing_organizations(None, request.commune)
        if not next_orgs:
            return False

        self.submit_to_organization(request_id, next_orgs[0].id)
        return True

    def advance_routing(self, request_id: int) -> bool:
        """Advance request to next organization in routing sequence."""
        request = self.get_request_by_id(request_id)
        if not request or not request.current_recipient_type:
            return False

        next_orgs = self.get_next_routing_organizations(request.current_recipient_type, request.commune)
        if not next_orgs:

            request.status = RequestStatus.CLOSED
            self.session.flush()
            return False

        self.submit_to_organization(request_id, next_orgs[0].id)
        return True

    def record_response(
        self,
        request_id: int,
        organization_id: int,
        response_content: str,
        response_status: str,
    ) -> SubmissionHistory | None:
        """Record a response from an organization."""
        submission = self.get_one(
            SubmissionHistory,
            SubmissionHistory.request_id == request_id,
            SubmissionHistory.organization_id == organization_id,
        )
        if not submission:
            return None

        submission.responded_at = datetime.now(UTC)
        submission.response_content = response_content
        submission.response_status = response_status
        submission.status = "responded"

        request = self.get_request_by_id(request_id)
        if request:
            request.responded_at = datetime.now(UTC)
            request.response_content = response_content
            request.response_status = response_status
            request.status = RequestStatus.RESPONDED

            if response_status == "positive":
                request.status = RequestStatus.APPROVED
                request.approved_at = datetime.now(UTC)

        self.session.flush()
        return submission





    def get_moderation_queue(self, status: str = "pending", limit: int = 50, offset: int = 0) -> dict[str, Any]:
        """Get moderation queue."""
        filters = [ModerationQueue.status == status]
        items = self.get_all(
            ModerationQueue,
            *filters,
            order_by=ModerationQueue.created_at,
            limit=limit,
            offset=offset,
        )
        total = self.count(ModerationQueue, *filters)
        return {"data": items, "total": total, "limit": limit, "offset": offset}

    def moderate_request(
        self,
        request_id: int,
        moderator_id: int,
        action: str,
        reason: str | None = None,
    ) -> Request | None:
        """Moderate a request."""
        request = self.get_request_by_id(request_id)
        moderation = self.get_one(ModerationQueue, ModerationQueue.request_id == request_id)

        if not request or not moderation:
            return None

        moderation.moderator_id = moderator_id
        moderation.action = action
        moderation.reason = reason
        moderation.reviewed_at = datetime.now(UTC)
        moderation.status = "resolved"

        if action == "approve":
            request.status = RequestStatus.SENT
            request.moderated_at = datetime.now(UTC)
            request.moderated_by = moderator_id

            self.start_routing(request_id)
        elif action == "reject":
            request.status = RequestStatus.REJECTED
            request.moderation_reason = reason
            request.moderated_at = datetime.now(UTC)
            request.moderated_by = moderator_id
        elif action == "request_changes":
            request.status = RequestStatus.DRAFT
            request.moderation_reason = reason
            request.moderated_at = datetime.now(UTC)
            request.moderated_by = moderator_id

        self.session.flush()


        try:
            user = self.get_user_by_id(request.user_id)
            email_service.send_moderation_notification({
                "title": request.title,
                "category": request.category_label,
                "commune": request.commune,
                "support_count": request.support_count,
            }, action, reason, user.email if user else None)
        except Exception as e:
            print(f"Failed to send moderation notification email: {e}")

        return request





    def get_municipal_requests(
        self,
        commune: str,
        status: str | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> dict[str, Any]:
        """Get requests for a specific municipality (commune)."""
        filters = [Request.commune == commune]

        if status:
            filters.append(Request.status == status)
        else:

            filters.append(Request.status.in_([
                RequestStatus.SENT,
                RequestStatus.WAITING_RESPONSE,
                RequestStatus.RESPONDED,
                RequestStatus.APPROVED,
            ]))

        requests = self.get_all(
            Request,
            *filters,
            order_by=desc(Request.created_at),
            limit=limit,
            offset=offset,
        )
        total = self.count(Request, *filters)

        return {"data": requests, "total": total, "limit": limit, "offset": offset}





    def get_request_stats(self) -> dict[str, Any]:
        """Get request statistics."""
        total = self.count(Request)
        pending_moderation = self.count(Request, Request.status == RequestStatus.PENDING_MODERATION)
        active = self.count(Request, Request.status.in_([
            RequestStatus.SENT,
            RequestStatus.WAITING_RESPONSE,
            RequestStatus.RESPONDED,
        ]))
        approved = self.count(Request, Request.status == RequestStatus.APPROVED)
        rejected = self.count(Request, Request.status == RequestStatus.REJECTED)


        stmt = select(Request.commune, func.count(Request.id)).where(
            Request.status.not_in([RequestStatus.DRAFT, RequestStatus.REJECTED])
        ).group_by(Request.commune).order_by(desc(func.count(Request.id)))
        result = self.session.execute(stmt)
        by_commune = {row[0]: row[1] for row in result.all()}


        stmt2 = select(Request.category, func.count(Request.id)).where(
            Request.status.not_in([RequestStatus.DRAFT, RequestStatus.REJECTED])
        ).group_by(Request.category).order_by(desc(func.count(Request.id)))
        result2 = self.session.execute(stmt2)
        by_category = {row[0]: row[1] for row in result2.all()}

        return {
            "total": total,
            "pending_moderation": pending_moderation,
            "active": active,
            "approved": approved,
            "rejected": rejected,
            "by_commune": by_commune,
            "by_category": by_category,
        }
