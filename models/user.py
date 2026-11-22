"""User model - Registro e identificación de usuarios."""

from sqlalchemy import Boolean, DateTime, ForeignKey, Index, Integer, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base, TimestampMixin


class User(Base, TimestampMixin):
    """Model for registered users (ciudadanos)."""

    __tablename__ = "users"

    # Primary key
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # Basic info
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)

    # Profile
    phone: Mapped[str] = mapped_column(String(50), nullable=True)
    commune: Mapped[str] = mapped_column(String(100), nullable=True, index=True)
    avatar_url: Mapped[str] = mapped_column(String(500), nullable=True)

    # Auth & Security
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    verification_token: Mapped[str] = mapped_column(String(255), nullable=True)
    last_login_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=True)

    # Role (for future municipal panel access)
    role: Mapped[str] = mapped_column(String(50), default="citizen", nullable=False)  # citizen, municipal, admin

    # Constraints
    __table_args__ = (
        UniqueConstraint("email", name="uq_users_email"),
        Index("ix_users_commune_active", "commune", "is_active"),
    )

    # Relationships
    requests: Mapped[list["Request"]] = relationship("Request", back_populates="user")

    def __repr__(self) -> str:
        return f"<User(id={self.id}, name='{self.name}', email='{self.email}', role='{self.role}')>"


class RequestStatus(str):
    """Request status constants."""
    DRAFT = "draft"
    PENDING_MODERATION = "pending_moderation"
    REJECTED = "rejected"
    SENT = "sent"
    WAITING_RESPONSE = "waiting_response"
    RESPONDED = "responded"
    APPROVED = "approved"
    CLOSED = "closed"


class RequestCategory(str):
    """Request category constants (matches SpaceCategory)."""
    POCKET_PARK = "pocket_park"
    GREEN_CORRIDOR = "green_corridor"
    COMMUNITY_GARDEN = "community_garden"
    PLAYGROUND = "playground"
    RESTING_AREA = "resting_area"
    URBAN_FOREST = "urban_forest"


class Request(Base, TimestampMixin):
    """Model for citizen requests (solicitudes de recuperación)."""

    __tablename__ = "requests"

    # Primary key
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # Creator
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    # Location
    address: Mapped[str] = mapped_column(String(500), nullable=False)
    latitude: Mapped[float] = mapped_column(nullable=False, index=True)
    longitude: Mapped[float] = mapped_column(nullable=False, index=True)
    commune: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    reference: Mapped[str] = mapped_column(String(500), nullable=True)  # nearby landmarks

    # Media
    photo_url: Mapped[str] = mapped_column(String(500), nullable=True)
    photo_thumbnail_url: Mapped[str] = mapped_column(String(500), nullable=True)

    # Content
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)  # Text
    needs: Mapped[str] = mapped_column(nullable=False)  # Text

    # Classification
    category: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    estimated_area_m2: Mapped[int] = mapped_column(Integer, nullable=True)

    # Status & Workflow
    status: Mapped[str] = mapped_column(
        String(50),
        default=RequestStatus.DRAFT,
        nullable=False,
        index=True,
    )
    moderation_reason: Mapped[str] = mapped_column(String(500), nullable=True)
    moderated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=True)
    moderated_by: Mapped[int] = mapped_column(Integer, nullable=True)

    # Routing
    current_recipient_type: Mapped[str] = mapped_column(String(50), nullable=True)  # municipality, company, school, university, social_media
    current_recipient_id: Mapped[int] = mapped_column(Integer, nullable=True)
    current_recipient_name: Mapped[str] = mapped_column(String(255), nullable=True)
    current_recipient_email: Mapped[str] = mapped_column(String(255), nullable=True)

    # Timing
    sent_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=True)
    deadline_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=True, index=True)
    responded_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=True)

    # Response
    response_content: Mapped[str] = mapped_column(nullable=True)
    response_status: Mapped[str] = mapped_column(String(50), nullable=True)  # positive, negative, needs_info
    approved_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=True)

    # Counters
    support_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    view_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    # Constraints
    __table_args__ = (
        Index("ix_requests_commune_status", "commune", "status"),
        Index("ix_requests_user_status", "user_id", "status"),
        Index("ix_requests_deadline_status", "deadline_at", "status"),
    )

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="requests")
    submissions: Mapped[list["SubmissionHistory"]] = relationship("SubmissionHistory", back_populates="request")

    def __repr__(self) -> str:
        return f"<Request(id={self.id}, title='{self.title}', commune='{self.commune}', status='{self.status}')>"

    @property
    def coordinates(self) -> tuple[float, float]:
        """Return (lat, lng) tuple."""
        return (float(self.latitude), float(self.longitude))

    @property
    def is_active(self) -> bool:
        """Check if request is in active workflow."""
        return self.status in (
            RequestStatus.SENT,
            RequestStatus.WAITING_RESPONSE,
            RequestStatus.RESPONDED,
        )

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
        return labels.get(self.category, self.category)

    @property
    def status_label(self) -> str:
        """Human-readable status label."""
        labels = {
            "draft": "Borrador",
            "pending_moderation": "En Revisión",
            "rejected": "Rechazada",
            "sent": "Enviada",
            "waiting_response": "En Espera de Respuesta",
            "responded": "Respondida",
            "approved": "Aprobada",
            "closed": "Cerrada",
        }
        return labels.get(self.status, self.status)


class Support(Base, TimestampMixin):
    """Model for citizen support/apoyo to requests."""

    __tablename__ = "supports"

    # Primary key
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # Relations
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )
    request_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("requests.id"),
        nullable=False,
        index=True,
    )

    # Constraints
    __table_args__ = (
        UniqueConstraint("user_id", "request_id", name="uq_support_user_request"),
        Index("ix_supports_request_created", "request_id", "created_at"),
    )

    def __repr__(self) -> str:
        return f"<Support(id={self.id}, user_id={self.user_id}, request_id={self.request_id})>"


class OrganizationType(str):
    """Organization type constants for routing."""
    MUNICIPALITY = "municipality"
    COMPANY = "company"
    SCHOOL = "school"
    UNIVERSITY = "university"
    SOCIAL_MEDIA = "social_media"


class Organization(Base, TimestampMixin):
    """Model for organizations/contacts for request routing."""

    __tablename__ = "organizations"

    # Primary key
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # Basic info
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    type: Mapped[str] = mapped_column(String(50), nullable=False, index=True)

    # Contact
    email: Mapped[str] = mapped_column(String(255), nullable=True)
    phone: Mapped[str] = mapped_column(String(50), nullable=True)
    contact_person: Mapped[str] = mapped_column(String(255), nullable=True)
    website_url: Mapped[str] = mapped_column(String(500), nullable=True)

    # Geographic scope
    commune: Mapped[str] = mapped_column(String(100), nullable=True, index=True)  # for municipalities
    region: Mapped[str] = mapped_column(String(100), nullable=True)  # for broader orgs

    # Routing config
    priority_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)  # within type
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
    auto_send: Mapped[bool] = mapped_column(default=False, nullable=False)  # whether to auto-send

    # Email template customization
    custom_subject: Mapped[str] = mapped_column(String(255), nullable=True)
    custom_message: Mapped[str] = mapped_column(nullable=True)

    # Constraints
    __table_args__ = (
        Index("ix_organizations_type_active", "type", "is_active"),
        Index("ix_organizations_type_commune", "type", "commune"),
    )

    # Relationships
    submissions: Mapped[list["SubmissionHistory"]] = relationship("SubmissionHistory", back_populates="organization")

    def __repr__(self) -> str:
        return f"<Organization(id={self.id}, name='{self.name}', type='{self.type}', commune='{self.commune}')>"

    @property
    def type_label(self) -> str:
        """Human-readable type label."""
        labels = {
            "municipality": "Municipalidad",
            "company": "Empresa",
            "school": "Colegio",
            "university": "Universidad",
            "social_media": "Redes Sociales",
        }
        return labels.get(self.type, self.type)


class SubmissionHistory(Base, TimestampMixin):
    """Model for tracking request submissions to organizations."""

    __tablename__ = "submission_history"

    # Primary key
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # Relations
    request_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("requests.id"),
        nullable=False,
        index=True,
    )
    organization_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("organizations.id"),
        nullable=False,
        index=True,
    )

    # Submission details
    sent_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    sent_by: Mapped[str] = mapped_column(String(50), default="auto", nullable=False)  # auto, manual
    message_subject: Mapped[str] = mapped_column(String(255), nullable=True)
    message_body: Mapped[str] = mapped_column(nullable=True)
    message_recipient: Mapped[str] = mapped_column(String(255), nullable=True)

    # Result
    status: Mapped[str] = mapped_column(String(50), default="sent", nullable=False)  # sent, delivered, failed, bounced
    external_id: Mapped[str] = mapped_column(String(255), nullable=True)  # email message ID, etc.
    error_message: Mapped[str] = mapped_column(String(500), nullable=True)

    # Response tracking
    responded_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=True)
    response_content: Mapped[str] = mapped_column(nullable=True)
    response_status: Mapped[str] = mapped_column(String(50), nullable=True)  # positive, negative, needs_info

    # Constraints
    __table_args__ = (
        Index("ix_submission_request_org", "request_id", "organization_id"),
        Index("ix_submission_status_date", "status", "sent_at"),
    )

    # Relationships
    request: Mapped["Request"] = relationship("Request", back_populates="submissions")
    organization: Mapped["Organization"] = relationship("Organization", back_populates="submissions")

    def __repr__(self) -> str:
        return f"<SubmissionHistory(id={self.id}, request_id={self.request_id}, org_id={self.organization_id}, status='{self.status}')>"


class ModerationAction(str):
    """Moderation action constants."""
    APPROVE = "approve"
    REJECT = "reject"
    REQUEST_CHANGES = "request_changes"


class ModerationQueue(Base, TimestampMixin):
    """Model for moderation queue of requests."""

    __tablename__ = "moderation_queue"

    # Primary key
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # Relations
    request_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("requests.id"),
        nullable=False,
        unique=True,
        index=True,
    )
    moderator_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=True)

    # Status
    status: Mapped[str] = mapped_column(String(50), default="pending", nullable=False, index=True)  # pending, in_review, resolved
    action: Mapped[str] = mapped_column(String(50), nullable=True)  # approve, reject, request_changes
    reason: Mapped[str] = mapped_column(String(500), nullable=True)

    # Timing
    reviewed_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=True)

    # Constraints
    __table_args__ = (
        Index("ix_moderation_status_date", "status", "created_at"),
    )

    def __repr__(self) -> str:
        return f"<ModerationQueue(id={self.id}, request_id={self.request_id}, status='{self.status}')>"
