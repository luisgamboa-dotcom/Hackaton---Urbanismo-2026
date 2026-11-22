"""Main entry point for Green Tech - FastAPI application."""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager, suppress
from datetime import UTC
from pathlib import Path
from typing import Any

from fastapi import Depends, FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from config.database import close_db, get_db_session, init_and_seed_db
from config.settings import get_settings
from controllers import APIController, LandingController, RequestsController
from models import ImpactMetric, Organization, Partner, RequestStatus, Space
from models import Request as RequestModel
from models.space import SpaceCategory, SpaceStatus
from utils.formatters import (
    format_area_m2,
    format_category_label,
    format_date,
    format_date_relative,
    format_number,
    format_partner_type,
    format_status_label,
    slugify,
    truncate_text,
)
from utils.stitch_sync import sync_tokens

settings = get_settings()


BASE_DIR = Path(__file__).parent
TEMPLATES_DIR = BASE_DIR / "views"
STATIC_DIR = BASE_DIR / "public"


templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


templates.env.filters["format_number"] = format_number
templates.env.filters["format_area_m2"] = format_area_m2
templates.env.filters["format_date"] = format_date
templates.env.filters["format_date_relative"] = format_date_relative
templates.env.filters["format_status_label"] = format_status_label
templates.env.filters["format_category_label"] = format_category_label
templates.env.filters["format_partner_type"] = format_partner_type
templates.env.filters["truncate"] = truncate_text
templates.env.filters["slugify"] = slugify


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Application lifespan handler."""

    if settings.database_url:
        try:
            init_and_seed_db()
            print("Database initialized and seeded")
        except Exception as e:
            print(f"Database initialization failed: {e}")
    else:
        print("DATABASE_URL not set, skipping database initialization")


    try:
        sync_tokens()
        print("Design tokens synced")
    except Exception as e:
        print(f"Design token sync failed: {e}")

    yield


    close_db()
    print("Application shutdown complete")


app = FastAPI(
    title=settings.app_name,
    description="Landing page para recuperación urbana táctica en Santiago",
    version="0.1.0",
    lifespan=lifespan,
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None,
)


app.mount("/public", StaticFiles(directory=str(STATIC_DIR)), name="public")
app.mount("/images", StaticFiles(directory=str(STATIC_DIR / "images")), name="images")







@app.get("/", response_class=HTMLResponse, name="home")
async def home(request: Request, session: Session = Depends(get_db_session)) -> HTMLResponse:
    """Landing page - Main route."""
    controller = LandingController(session)
    data = controller.get_home_data()

    return templates.TemplateResponse(
        request,
        "landing/index.html",
        data,
    )


@app.get("/espacios", response_class=HTMLResponse, name="spaces_list")
async def spaces_list(
    request: Request,
    session: Session = Depends(get_db_session),
    status: str | None = None,
    category: str | None = None,
    commune: str | None = None,
) -> HTMLResponse:
    """List all spaces with filters."""
    controller = APIController(session)


    status_filter = None
    if status:
        with suppress(ValueError):
            status_filter = SpaceStatus(status)

    category_filter = None
    if category:
        with suppress(ValueError):
            category_filter = SpaceCategory(category)

    result = await controller.list_spaces(
        status=status_filter,
        category=category_filter,
        commune=commune,
        limit=50,
    )


    from sqlalchemy import distinct, select


    communes_result = session.execute(
        select(distinct(Space.commune)).where(Space.commune.is_not(None)).order_by(Space.commune)
    )
    communes = [c for c in communes_result.scalars().all() if c]

    categories = [c.value for c in SpaceCategory]
    statuses = [s.value for s in SpaceStatus]

    return templates.TemplateResponse(
        request,
        "spaces/list.html",
        {
            "spaces": result["data"],
            "total": result["total"],
            "filters": {
                "status": status,
                "category": category,
                "commune": commune,
            },
            "communes": communes,
            "categories": categories,
            "statuses": statuses,
            "site_name": "Green Tech",
        },
    )


@app.get("/espacios/{space_id}", response_class=HTMLResponse, name="space_detail")
async def space_detail(
    request: Request,
    space_id: int,
    session: Session = Depends(get_db_session),
) -> HTMLResponse:
    """Space detail page."""
    controller = APIController(session)
    space = await controller.get_space(space_id)

    if not space:
        return templates.TemplateResponse(
            request,
            "errors/404.html",
            {"site_name": "Green Tech"},
            status_code=404,
        )

    return templates.TemplateResponse(
        request,
        "spaces/detail.html",
        {
            "space": space,
            "site_name": "Green Tech",
        },
    )


@app.get("/postular", response_class=HTMLResponse, name="propose_space")
async def propose_space_page(
    request: Request,
    session: Session = Depends(get_db_session),
) -> HTMLResponse:
    """Postular espacio page - standalone page."""
    controller = LandingController(session)
    data = controller.get_home_data()
    return templates.TemplateResponse(
        request,
        "propose.html",
        data,
    )


@app.get("/socios", response_class=HTMLResponse, name="partners_page")
async def partners_page(
    request: Request,
    session: Session = Depends(get_db_session),
) -> HTMLResponse:
    """Socios y aliados page."""
    controller = LandingController(session)
    data = controller.get_home_data()
    return templates.TemplateResponse(
        request,
        "partners.html",
        data,
    )


@app.get("/impacto", response_class=HTMLResponse, name="impact_page")
async def impact_page(
    request: Request,
    session: Session = Depends(get_db_session),
) -> HTMLResponse:
    """Impacto y métricas page."""
    controller = LandingController(session)
    data = controller.get_home_data()

    stats = controller.get_stats()
    data["stats"] = stats
    return templates.TemplateResponse(
        request,
        "impact.html",
        data,
    )


@app.get("/actividades", response_class=HTMLResponse, name="activities_page")
async def activities_page(
    request: Request,
    session: Session = Depends(get_db_session),
) -> HTMLResponse:
    """Actividades y talleres page."""
    controller = LandingController(session)
    data = controller.get_home_data()
    return templates.TemplateResponse(
        request,
        "activities.html",
        data,
    )


@app.get("/comunidades", response_class=HTMLResponse, name="communities_page")
async def communities_page(
    request: Request,
    session: Session = Depends(get_db_session),
) -> HTMLResponse:
    """Red de comunidades y juntas de vecinos page."""
    controller = LandingController(session)
    data = controller.get_home_data()
    return templates.TemplateResponse(
        request,
        "communities.html",
        data,
    )


@app.get("/contacto", response_class=HTMLResponse, name="contact_page")
async def contact_page(
    request: Request,
    session: Session = Depends(get_db_session),
) -> HTMLResponse:
    """Contacto page."""
    controller = LandingController(session)
    data = controller.get_home_data()
    return templates.TemplateResponse(
        request,
        "contact.html",
        data,
    )


@app.get("/privacidad", response_class=HTMLResponse, name="privacy_page")
async def privacy_page(
    request: Request,
    session: Session = Depends(get_db_session),
) -> HTMLResponse:
    """Política de privacidad page."""
    controller = LandingController(session)
    data = controller.get_home_data()
    return templates.TemplateResponse(
        request,
        "privacy.html",
        data,
    )


@app.get("/terminos", response_class=HTMLResponse, name="terms_page")
async def terms_page(
    request: Request,
    session: Session = Depends(get_db_session),
) -> HTMLResponse:
    """Términos y condiciones page."""
    controller = LandingController(session)
    data = controller.get_home_data()
    return templates.TemplateResponse(
        request,
        "terms.html",
        data,
    )


@app.get("/cookies", response_class=HTMLResponse, name="cookies_page")
async def cookies_page(
    request: Request,
    session: Session = Depends(get_db_session),
) -> HTMLResponse:
    """Política de cookies page."""
    controller = LandingController(session)
    data = controller.get_home_data()
    return templates.TemplateResponse(
        request,
        "cookies.html",
        data,
    )


@app.get("/accesibilidad", response_class=HTMLResponse, name="accessibility_page")
async def accessibility_page(
    request: Request,
    session: Session = Depends(get_db_session),
) -> HTMLResponse:
    """Declaración de accesibilidad page."""
    controller = LandingController(session)
    data = controller.get_home_data()
    return templates.TemplateResponse(
        request,
        "accessibility.html",
        data,
    )


@app.get("/transparencia", response_class=HTMLResponse, name="transparency_page")
async def transparency_page(
    request: Request,
    session: Session = Depends(get_db_session),
) -> HTMLResponse:
    """Transparencia y rendición de cuentas page."""
    controller = LandingController(session)
    data = controller.get_home_data()
    return templates.TemplateResponse(
        request,
        "transparency.html",
        data,
    )


@app.get("/voluntariado", response_class=HTMLResponse, name="volunteer_page")
async def volunteer_page(
    request: Request,
    session: Session = Depends(get_db_session),
) -> HTMLResponse:
    """Voluntariado page."""
    controller = LandingController(session)
    data = controller.get_home_data()
    return templates.TemplateResponse(
        request,
        "volunteer.html",
        data,
    )


@app.get("/recursos", response_class=HTMLResponse, name="resources_page")
async def resources_page(
    request: Request,
    session: Session = Depends(get_db_session),
) -> HTMLResponse:
    """Recursos y guías page."""
    controller = LandingController(session)
    data = controller.get_home_data()
    return templates.TemplateResponse(
        request,
        "recursos.html",
        data,
    )


@app.get("/testimonios", response_class=HTMLResponse, name="testimonials_page")
async def testimonials_page(
    request: Request,
    session: Session = Depends(get_db_session),
) -> HTMLResponse:
    """Testimonios page."""
    controller = LandingController(session)
    data = controller.get_home_data()
    return templates.TemplateResponse(
        request,
        "testimonios.html",
        data,
    )


@app.get("/nosotros", response_class=HTMLResponse, name="about_page")
async def about_page(
    request: Request,
    session: Session = Depends(get_db_session),
) -> HTMLResponse:
    """Nosotros page."""
    controller = LandingController(session)
    data = controller.get_home_data()
    return templates.TemplateResponse(
        request,
        "nosotros.html",
        data,
    )


@app.get("/health", name="health_check")
async def health_check() -> dict[str, str]:
    """Health check endpoint."""
    return {
        "status": "ok",
        "app": settings.app_name,
        "version": "0.1.0",
        "environment": settings.app_env,
    }







@app.get("/api/spaces", name="api_spaces_list")
async def api_spaces_list(
    session: Session = Depends(get_db_session),
    status: str | None = None,
    category: str | None = None,
    commune: str | None = None,
    limit: int = 20,
    offset: int = 0,
) -> dict[str, Any]:
    """API: List spaces with filters."""
    controller = APIController(session)

    status_filter = None
    if status:
        with suppress(ValueError):
            status_filter = SpaceStatus(status)

    category_filter = None
    if category:
        with suppress(ValueError):
            category_filter = SpaceCategory(category)

    return await controller.list_spaces(
        status=status_filter,
        category=category_filter,
        commune=commune,
        limit=limit,
        offset=offset,
    )


@app.get("/api/spaces/{space_id}", name="api_space_detail", response_model=None)
async def api_space_detail(
    space_id: int,
    session: Session = Depends(get_db_session),
) -> Space | dict[str, str]:
    """API: Get single space."""
    controller = APIController(session)
    space = await controller.get_space(space_id)

    if not space:
        return {"error": "Not found"}

    return space


@app.get("/api/metrics", name="api_metrics_list", response_model=None)
async def api_metrics_list(session: Session = Depends(get_db_session)) -> list[ImpactMetric]:
    """API: Get all impact metrics."""
    controller = APIController(session)
    return await controller.get_metrics()


@app.get("/api/partners", name="api_partners_list", response_model=None)
async def api_partners_list(
    session: Session = Depends(get_db_session),
    type: str | None = None,
) -> list[Partner]:
    """API: List partners."""
    controller = APIController(session)
    return await controller.list_partners(type_=type)


@app.get("/api/dashboard/stats", name="api_dashboard_stats")
async def api_dashboard_stats(session: Session = Depends(get_db_session)) -> dict[str, Any]:
    """API: Get dashboard statistics."""
    controller = APIController(session)
    return await controller.get_dashboard_stats()


@app.get("/api/map/spaces", name="api_map_spaces")
async def api_map_spaces(
    session: Session = Depends(get_db_session),
    category: str | None = None,
    status: str | None = None,
    commune: str | None = None,
) -> dict[str, Any]:
    """API: Get spaces with coordinates for map markers."""
    controller = APIController(session)
    return controller.get_map_spaces(
        category=category,
        status=status,
        commune=commune,
    )







@app.post("/api/requests", name="api_create_request")
async def api_create_request(
    request_data: dict,
    session: Session = Depends(get_db_session),
) -> dict[str, Any]:
    """API: Create a new citizen request."""
    controller = RequestsController(session)


    user = controller.get_or_create_user(
        name=request_data.get("user_name", ""),
        email=request_data.get("user_email", ""),
        phone=request_data.get("user_phone"),
        commune=request_data.get("user_commune"),
    )


    request = controller.create_request(
        user_id=user.id,
        address=request_data.get("address", ""),
        latitude=float(request_data.get("latitude", 0)),
        longitude=float(request_data.get("longitude", 0)),
        commune=request_data.get("commune", ""),
        title=request_data.get("title", ""),
        description=request_data.get("description", ""),
        needs=request_data.get("needs", ""),
        category=request_data.get("category", "pocket_park"),
        reference=request_data.get("reference"),
        estimated_area_m2=request_data.get("estimated_area_m2"),
        photo_url=request_data.get("photo_url"),
    )

    return {
        "success": True,
        "request_id": request.id,
        "status": request.status,
        "message": "Solicitud creada y enviada a moderación",
    }


@app.get("/api/requests", name="api_list_requests")
async def api_list_requests(
    session: Session = Depends(get_db_session),
    user_id: int | None = None,
    commune: str | None = None,
    status: str | None = None,
    category: str | None = None,
    limit: int = 20,
    offset: int = 0,
) -> dict[str, Any]:
    """API: List requests with filters."""
    controller = RequestsController(session)
    return controller.get_requests(
        user_id=user_id,
        commune=commune,
        status=status,
        category=category,
        limit=limit,
        offset=offset,
    )


@app.get("/api/requests/{request_id}", name="api_get_request", response_model=None)
async def api_get_request(
    request_id: int,
    session: Session = Depends(get_db_session),
) -> RequestModel | dict[str, str]:
    """API: Get single request."""
    controller = RequestsController(session)
    request = controller.get_request_by_id(request_id)

    if not request:
        return {"error": "Not found"}

    return request


@app.get("/api/requests/{request_id}/supports", name="api_get_request_supports")
async def api_get_request_supports(
    request_id: int,
    session: Session = Depends(get_db_session),
) -> dict[str, Any]:
    """API: Get support count and user's support status for a request."""
    controller = RequestsController(session)
    request = controller.get_request_by_id(request_id)

    if not request:
        return {"error": "Not found"}


    return {
        "request_id": request_id,
        "support_count": request.support_count,
        "has_user_supported": False,
    }


@app.post("/api/requests/{request_id}/support", name="api_add_support")
async def api_add_support(
    request_id: int,
    support_data: dict,
    session: Session = Depends(get_db_session),
) -> dict[str, Any]:
    """API: Add support to a request."""
    controller = RequestsController(session)

    user_email = support_data.get("user_email")
    user_name = support_data.get("user_name")
    user_phone = support_data.get("user_phone")
    user_commune = support_data.get("user_commune")

    if not user_email:
        return {"success": False, "error": "Email requerido"}


    user = controller.get_or_create_user(
        name=user_name or "Vecino",
        email=user_email,
        phone=user_phone,
        commune=user_commune,
    )


    support = controller.add_support(user.id, request_id)

    if support is None:

        if controller.has_user_supported(user.id, request_id):
            return {"success": False, "error": "Ya has apoyado esta solicitud"}
        return {"success": False, "error": "No se pudo agregar el apoyo"}


    request = controller.get_request_by_id(request_id)

    return {
        "success": True,
        "support_count": request.support_count if request else 0,
        "message": "¡Gracias por tu apoyo!",
    }


@app.delete("/api/requests/{request_id}/support", name="api_remove_support")
async def api_remove_support(
    request_id: int,
    user_email: str,
    session: Session = Depends(get_db_session),
) -> dict[str, Any]:
    """API: Remove support from a request."""
    controller = RequestsController(session)

    user = controller.get_user_by_email(user_email)
    if not user:
        return {"success": False, "error": "Usuario no encontrado"}

    success = controller.remove_support(user.id, request_id)

    if not success:
        return {"success": False, "error": "No se encontró el apoyo"}

    request = controller.get_request_by_id(request_id)

    return {
        "success": True,
        "support_count": request.support_count if request else 0,
        "message": "Apoyo retirado",
    }







@app.get("/api/organizations", name="api_list_organizations", response_model=None)
async def api_list_organizations(
    session: Session = Depends(get_db_session),
    type: str | None = None,
    commune: str | None = None,
) -> list[Organization]:
    """API: List organizations."""
    controller = RequestsController(session)
    return controller.get_organizations(type_=type, commune=commune)


@app.get("/api/organizations/municipality/{commune}", name="api_get_municipality", response_model=None)
async def api_get_municipality(
    commune: str,
    session: Session = Depends(get_db_session),
) -> Organization | dict[str, str]:
    """API: Get municipality for a commune."""
    controller = RequestsController(session)
    org = controller.get_municipality_for_commune(commune)

    if not org:
        return {"error": "Not found"}

    return org







@app.get("/api/moderation/queue", name="api_moderation_queue")
async def api_moderation_queue(
    session: Session = Depends(get_db_session),
    status: str = "pending",
    limit: int = 50,
    offset: int = 0,
) -> dict[str, Any]:
    """API: Get moderation queue."""
    controller = RequestsController(session)
    return controller.get_moderation_queue(status=status, limit=limit, offset=offset)


@app.post("/api/moderation/{request_id}", name="api_moderate_request")
async def api_moderate_request(
    request_id: int,
    moderation_data: dict,
    session: Session = Depends(get_db_session),
) -> dict[str, Any]:
    """API: Moderate a request."""
    controller = RequestsController(session)

    moderator_id = moderation_data.get("moderator_id", 1)
    action = moderation_data.get("action")
    reason = moderation_data.get("reason")

    if action not in ("approve", "reject", "request_changes"):
        return {"success": False, "error": "Acción inválida"}

    request = controller.moderate_request(request_id, moderator_id, action, reason)

    if not request:
        return {"success": False, "error": "Solicitud no encontrada"}

    return {
        "success": True,
        "request_id": request.id,
        "status": request.status,
        "message": f"Solicitud {action}ada correctamente",
    }







@app.get("/api/municipal/requests", name="api_municipal_requests")
async def api_municipal_requests(
    session: Session = Depends(get_db_session),
    commune: str | None = None,
    status: str | None = None,
    limit: int = 50,
    offset: int = 0,
) -> dict[str, Any]:
    """API: Get requests for a municipality (requires auth in production)."""
    controller = RequestsController(session)



    if not commune:
        return {"error": "Comuna requerida"}

    return controller.get_municipal_requests(
        commune=commune,
        status=status,
        limit=limit,
        offset=offset,
    )


@app.get("/api/municipal/stats", name="api_municipal_stats")
async def api_municipal_stats(
    session: Session = Depends(get_db_session),
    commune: str | None = None,
) -> dict[str, Any]:
    """API: Get statistics for municipal panel."""
    controller = RequestsController(session)

    if not commune:
        return {"error": "Comuna requerida"}


    from models import Request

    total = controller.count(Request, Request.commune == commune)
    pending = controller.count(Request, Request.commune == commune, Request.status == RequestStatus.PENDING_MODERATION)
    sent = controller.count(Request, Request.commune == commune, Request.status == RequestStatus.SENT)
    waiting = controller.count(Request, Request.commune == commune, Request.status == RequestStatus.WAITING_RESPONSE)
    responded = controller.count(Request, Request.commune == commune, Request.status == RequestStatus.RESPONDED)
    approved = controller.count(Request, Request.commune == commune, Request.status == RequestStatus.APPROVED)

    return {
        "commune": commune,
        "total": total,
        "pending_moderation": pending,
        "sent": sent,
        "waiting_response": waiting,
        "responded": responded,
        "approved": approved,
    }







@app.post("/api/admin/process-routing", name="api_process_routing")
async def api_process_routing(
    session: Session = Depends(get_db_session),
) -> dict[str, Any]:
    """API: Process automatic routing for all pending requests (cron job)."""
    controller = RequestsController(session)


    from datetime import datetime

    from sqlalchemy import select

    from models import Request

    stmt = select(Request).where(
        Request.status.in_([RequestStatus.SENT, RequestStatus.WAITING_RESPONSE]),
        Request.deadline_at.is_not(None),
        Request.deadline_at < datetime.now(UTC),
    )
    result = session.execute(stmt)
    requests = result.scalars().all()

    processed = 0
    for req in requests:
        if controller.process_routing(req.id):
            processed += 1

    return {
        "success": True,
        "processed": processed,
        "total_checked": len(requests),
    }


@app.post("/api/admin/requests/{request_id}/respond", name="api_record_response")
async def api_record_response(
    request_id: int,
    response_data: dict,
    session: Session = Depends(get_db_session),
) -> dict[str, Any]:
    """API: Record organization response (for webhook/email processing)."""
    controller = RequestsController(session)

    org_id = response_data.get("organization_id")
    content = response_data.get("content", "")
    status = response_data.get("status")

    if not org_id or not status:
        return {"success": False, "error": "organization_id y status requeridos"}

    submission = controller.record_response(request_id, org_id, content, status)

    if not submission:
        return {"success": False, "error": "Envío no encontrado"}

    return {
        "success": True,
        "request_status": submission.request.status if submission.request else "unknown",
    }







@app.get("/api/requests/stats", name="api_request_stats")
async def api_request_stats(
    session: Session = Depends(get_db_session),
) -> dict[str, Any]:
    """API: Get request statistics."""
    controller = RequestsController(session)
    return controller.get_request_stats()







@app.exception_handler(404)
async def not_found_handler(request: Request, exc: Exception) -> HTMLResponse:
    """404 handler."""
    return templates.TemplateResponse(
        request,
        "errors/404.html",
        {"site_name": "Green Tech"},
        status_code=404,
    )


@app.exception_handler(500)
async def server_error_handler(request: Request, exc: Exception) -> HTMLResponse:
    """500 handler."""
    return templates.TemplateResponse(
        request,
        "errors/500.html",
        {"site_name": "Green Tech"},
        status_code=500,
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
    )
