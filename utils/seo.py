"""SEO helpers for meta tags, structured data, and social sharing."""

from dataclasses import dataclass
from urllib.parse import urljoin


@dataclass
class SEOData:
    """SEO metadata for a page."""
    title: str
    description: str
    canonical_url: str
    og_type: str = "website"
    og_image: str | None = None
    og_image_alt: str | None = None
    twitter_card: str = "summary_large_image"
    json_ld: dict | None = None
    noindex: bool = False
    nofollow: bool = False


def build_seo_data(
    title: str,
    description: str,
    path: str = "/",
    og_image: str | None = None,
    json_ld: dict | None = None,
) -> SEOData:
    """Build SEOData with defaults for the site."""
    base_url = "https://tramaurbanaverde.cl"  # Update for production
    canonical = urljoin(base_url, path)
    og_img = urljoin(base_url, og_image) if og_image else urljoin(base_url, "/images/og-default.jpg")

    return SEOData(
        title=f"{title} | Green Tech",
        description=description,
        canonical_url=canonical,
        og_image=og_img,
        og_image_alt=f"Green Tech - {title}",
        json_ld=json_ld,
    )


def render_meta_tags(seo: SEOData) -> str:
    """Render HTML meta tags from SEOData."""
    tags = [
        f'<title>{seo.title}</title>',
        f'<meta name="description" content="{seo.description}">',
        f'<link rel="canonical" href="{seo.canonical_url}">',
    ]

    # Robots
    robots = []
    if seo.noindex:
        robots.append("noindex")
    if seo.nofollow:
        robots.append("nofollow")
    if robots:
        tags.append(f'<meta name="robots" content="{", ".join(robots)}">')

    # Open Graph
    tags.extend([
        f'<meta property="og:type" content="{seo.og_type}">',
        f'<meta property="og:url" content="{seo.canonical_url}">',
        f'<meta property="og:title" content="{seo.title}">',
        f'<meta property="og:description" content="{seo.description}">',
        f'<meta property="og:image" content="{seo.og_image}">',
    ])
    if seo.og_image_alt:
        tags.append(f'<meta property="og:image:alt" content="{seo.og_image_alt}">')

    # Twitter
    tags.extend([
        f'<meta name="twitter:card" content="{seo.twitter_card}">',
        f'<meta name="twitter:title" content="{seo.title}">',
        f'<meta name="twitter:description" content="{seo.description}">',
        f'<meta name="twitter:image" content="{seo.og_image}">',
        f'<meta name="twitter:image:alt" content="{seo.og_image_alt or ""}">',
    ])

    # JSON-LD
    if seo.json_ld:
        import json
        tags.append(f'<script type="application/ld+json">{json.dumps(seo.json_ld, ensure_ascii=False)}</script>')

    return "\n    ".join(tags)


# Predefined JSON-LD schemas
def organization_schema() -> dict:
    """Organization schema for the project."""
    return {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": "Green Tech",
        "alternateName": "Recuperación Urbana Táctica",
        "url": "https://tramaurbanaverde.cl",
        "logo": "https://tramaurbanaverde.cl/images/logo.svg",
        "description": "Recuperación de espacios urbanos inutilizados en sectores densos de Santiago mediante urbanismo táctico participativo.",
        "foundingDate": "2026",
        "address": {
            "@type": "PostalAddress",
            "addressLocality": "Santiago",
            "addressRegion": "Región Metropolitana",
            "addressCountry": "CL",
        },
        "contactPoint": {
            "@type": "ContactPoint",
            "telephone": "+56-2-XXXX-XXXX",
            "contactType": "customer service",
            "availableLanguage": ["Spanish"],
        },
        "sameAs": [
            "https://www.instagram.com/tramaurbanaverde",
            "https://www.twitter.com/tramaurbanaverde",
            "https://www.linkedin.com/company/trama-urbana-verde",
        ],
    }


def web_site_schema() -> dict:
    """WebSite schema with search action."""
    return {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": "Green Tech",
        "url": "https://tramaurbanaverde.cl",
        "potentialAction": {
            "@type": "SearchAction",
            "target": {
                "@type": "EntryPoint",
                "urlTemplate": "https://tramaurbanaverde.cl/search?q={search_term_string}",
            },
            "query-input": "required name=search_term_string",
        },
    }


def project_schema(space_data: dict) -> dict:
    """Project schema for a specific space intervention."""
    return {
        "@context": "https://schema.org",
        "@type": "Project",
        "name": space_data.get("name", ""),
        "description": space_data.get("description", ""),
        "url": f"https://tramaurbanaverde.cl/espacios/{space_data.get('id', '')}",
        "image": space_data.get("image_url", ""),
        "location": {
            "@type": "Place",
            "address": {
                "@type": "PostalAddress",
                "streetAddress": space_data.get("address", ""),
                "addressLocality": space_data.get("commune", "Santiago"),
                "addressRegion": "Región Metropolitana",
                "addressCountry": "CL",
            },
            "geo": {
                "@type": "GeoCoordinates",
                "latitude": space_data.get("latitude", -33.45),
                "longitude": space_data.get("longitude", -70.65),
            },
        },
        "startDate": space_data.get("started_at", ""),
        "endDate": space_data.get("completed_at", ""),
        "projectStatus": space_data.get("status", "").replace("_", " ").title(),
        "keywords": ["urbanismo táctico", "recuperación urbana", "áreas verdes", "participación comunitaria", space_data.get("commune", "")],
    }


def breadcrumb_schema(items: list[dict]) -> dict:
    """BreadcrumbList schema."""
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": i + 1,
                "name": item["name"],
                "item": item["url"],
            }
            for i, item in enumerate(items)
        ],
    }
