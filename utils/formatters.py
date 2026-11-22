"""Formatters for numbers, dates, and other display values."""

from datetime import date, datetime


def format_number(value: int | float, decimals: int = 0) -> str:
    """Format number with thousand separators (Spanish format: 1.234,56)."""
    if value is None:
        return "—"
    if decimals == 0:
        return f"{int(value):,}".replace(",", ".")
    return f"{value:,.{decimals}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def format_area_m2(value: int | float | None) -> str:
    """Format area in square meters."""
    if value is None:
        return "—"
    if value >= 10000:
        return f"{format_number(value / 10000, 1)} ha"
    return f"{format_number(value)} m²"


def format_percentage(value: float, total: float, decimals: int = 1) -> str:
    """Format percentage."""
    if total == 0:
        return "0%"
    pct = (value / total) * 100
    return f"{pct:.{decimals}f}%".replace(".", ",")


def format_date(value: date | datetime | None, fmt: str = "%d/%m/%Y") -> str:
    """Format date in Spanish locale."""
    if value is None:
        return "—"
    if isinstance(value, datetime):
        value = value.date()
    return value.strftime(fmt)


def format_date_relative(value: date | datetime | None) -> str:
    """Format date as relative time (e.g., 'hace 3 meses')."""
    if value is None:
        return "—"
    if isinstance(value, datetime):
        value = value.date()

    today = date.today()
    delta = today - value

    if delta.days == 0:
        return "hoy"
    elif delta.days == 1:
        return "ayer"
    elif delta.days < 7:
        return f"hace {delta.days} días"
    elif delta.days < 30:
        weeks = delta.days // 7
        return f"hace {weeks} semana{'s' if weeks > 1 else ''}"
    elif delta.days < 365:
        months = delta.days // 30
        return f"hace {months} mes{'es' if months > 1 else ''}"
    else:
        years = delta.days // 365
        return f"hace {years} año{'s' if years > 1 else ''}"


def format_status_label(status: str) -> str:
    """Format space status for display."""
    labels = {
        "identified": "Identificado",
        "in_progress": "En Progreso",
        "completed": "Completado",
        "maintained": "En Mantenimiento",
    }
    return labels.get(status, status.capitalize())


def format_category_label(category: str | None) -> str:
    """Format space category for display."""
    if not category:
        return "Sin categoría"
    labels = {
        "pocket_park": "Plaza de Bolsillo",
        "green_corridor": "Corredor Verde",
        "community_garden": "Huerto Comunitario",
        "playground": "Área de Juegos",
        "resting_area": "Zona de Descanso",
        "urban_forest": "Mini Bosque Urbano",
    }
    return labels.get(category, category.replace("_", " ").title())


def format_partner_type(partner_type: str) -> str:
    """Format partner type for display."""
    labels = {
        "municipality": "Municipalidad",
        "company_rse": "Empresa RSE",
        "ngo": "ONG",
        "nursery": "Vivero",
        "university": "Universidad",
        "community": "Comunidad",
    }
    return labels.get(partner_type, partner_type.replace("_", " ").title())


def truncate_text(text: str | None, max_length: int = 100, suffix: str = "…") -> str:
    """Truncate text to max length."""
    if not text:
        return ""
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)].rstrip() + suffix


def slugify(text: str) -> str:
    """Convert text to URL-friendly slug."""
    import re
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_-]+", "-", text)
    text = re.sub(r"^-+|-+$", "", text)
    return text
