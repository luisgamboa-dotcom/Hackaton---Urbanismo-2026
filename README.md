# Green Tech — Landing Page

> **Recuperación de espacios urbanos inutilizados en sectores densos de Santiago**

Landing page modular MVC construida con **FastAPI + Python + Jinja2**, basada en el diseño "Minimalist Business Showcase" de Google Stitch. Implementa el modelo de negocio Canvas para la recuperación táctica de lotes baldíos y espacios residuales en la Región Metropolitana.

---

## 🚀 Inicio Rápido

### Prerrequisitos
- Python 3.11+
- Cuenta Supabase (PostgreSQL) - ver [Configuración DB](#configuración-de-base-de-datos)

### Instalación y ejecución

```bash
# 1. Clonar repositorio
git clone https://github.com/<tu-usuario>/hackaton-urbanismo-2026.git
cd hackaton-urbanismo-2026

# 2. Ejecutar script de inicio (crea venv, instala deps, inicializa DB, lanza servidor)
./start.sh

# 3. Abrir en navegador
# http://localhost:8000
```

El script `start.sh` automatiza:
1. ✅ Crear entorno virtual `.venv`
2. ✅ Instalar dependencias (`requirements.txt`)
3. ✅ Cargar variables de entorno (`.env`)
4. ✅ Inicializar base de datos (tablas + seed data)
5. ✅ Sincronizar tokens de diseño Stitch → CSS
6. ✅ Levantar servidor Uvicorn con hot-reload

---

## 🏗️ Arquitectura MVC Modular

```
trama-urbana-verde/
├── config/                 # Configuración centralizada
│   ├── settings.py         # Settings con Pydantic BaseSettings
│   ├── database.py         # SQLAlchemy async + Supabase
│   └── stitch_design.py    # Tokens de diseño (colores, tipografía, spacing)
├── controllers/            # Lógica de negocio
│   ├── base.py             # BaseController
│   ├── landing.py          # LandingController (home, secciones)
│   └── api.py              # APIController (futuro)
├── models/                 # Modelos de datos (SQLAlchemy)
│   ├── base.py             # BaseModel + timestamps
│   ├── space.py            # Espacio/Proyecto intervención
│   ├── partner.py          # Socio clave (municipalidad, empresa, ONG)
│   ├── community.py        # Comunidad/Junta de vecinos
│   └── impact_metric.py    # Métricas impacto (m², voluntarios)
├── views/                  # Templates Jinja2
│   ├── base.html           # Layout base + design system
│   ├── partials/           # Componentes reutilizables
│   │   ├── _header.html
│   │   ├── _footer.html
│   │   ├── _hero.html
│   │   ├── _value_prop.html
│   │   ├── _stats_bar.html
│   │   ├── _spaces_grid.html
│   │   ├── _partners.html
│   │   ├── _impact_meter.html
│   │   └── _cta_section.html
│   └── landing/
│       └── index.html      # Página principal
├── public/                 # Assets estáticos
│   ├── css/
│   │   ├── design-tokens.css  # Variables CSS desde Stitch
│   │   ├── components.css     # Botones, cards, chips, badges
│   │   ├── layout.css         # Grid, spacing, responsive
│   │   └── main.css           # Entry point
│   ├── js/
│   │   ├── main.js
│   │   ├── components/
│   │   │   ├── ImpactMeter.js
│   │   │   ├── SpaceCard.js
│   │   │   └── ScrollReveal.js
│   │   └── utils/
│   └── images/
├── sql/                    # Scripts SQL
│   ├── init.sql            # Schema inicial
│   └── seed.sql            # Datos semilla (Canvas)
├── utils/                  # Helpers
│   ├── stitch_sync.py      # Sync tokens Stitch → CSS
│   ├── formatters.py       # Formateo números, fechas
│   └── seo.py              # Meta tags, structured data
├── tests/                  # Tests pytest
├── main.py                 # Entry point FastAPI
├── start.sh                # Script inicio completo
└── pyproject.toml          # Configuración herramienta
```

---

## 🎨 Design System (desde Google Stitch)

| Token | Valor | Uso |
|-------|-------|-----|
| **Primary** | `#1B4332` | Tipografía principal, headers, estados primarios |
| **Secondary** | `#2D6A4F` | Fondos énfasis, badges ecológicos, hover states |
| **Tertiary/CTA** | `#E07A5F` | Botones acción crítica, alertas, marcadores |
| **Surface** | `#F3F4F1` | Fondo global (hormigón mineral) |
| **Card** | `#FFFFFF` | Tarjetas, superficies elevadas |
| **Border** | `#E5E7EB` | Divisores, bordes sutiles |
| **Font** | Plus Jakarta Sans | Toda la tipografía |
| **Radius Base** | `0.5rem` (8px) | Botones, inputs, chips |
| **Radius Card** | `1rem` (16px) | Tarjetas, paneles |

> **Sincronización automática:** `python -m utils.stitch_sync` lee `config/stitch_design.py` y genera `public/css/design-tokens.css`

---

## 🗄️ Configuración de Base de Datos

### Variables de entorno (`.env`)

```bash
# Copiar ejemplo y editar
cp .env.example .env
```

```env
# .env
APP_NAME="Green Tech"
APP_ENV=development
DEBUG=true

# Supabase / PostgreSQL
DATABASE_URL=postgresql+asyncpg://user:password@host:5432/dbname
# O para Supabase con connection pooling:
# DATABASE_URL=postgresql+asyncpg://postgres:[PASSWORD]@db.[PROJECT_REF].supabase.co:5432/postgres

# Stitch (opcional - para sync automático de design tokens)
STITCH_PROJECT_ID=17540452302289583695
```

### Schema Principal

```sql
-- Espacios / Proyectos de intervención
spaces (id, name, description, address, commune, lat/lng, area_m2, status, category, images...)

-- Métricas de impacto agregadas
impact_metrics (metric_key, value, label, icon)

-- Socios clave
partners (name, type, logo_url, website_url, description, display_order)

-- Comunidades / Juntas de vecinos
communities (name, commune, contact_info, member_count, space_id)
```

### Seed Data (desde Business Model Canvas)

- **9 Socios**: Municipalidades, Empresas RSE, ONGs, Viveros, Universidades, Juntas de Vecinos
- **3 Espacios ejemplo**: Plaza Pocket Yungay, Corredor Verde Matucana, Huerto Comunitario Brasil
- **4 Métricas**: 2.450 m² recuperados, 12 espacios, 340 voluntarios, 5 comunas

---

## 🧪 Testing & Calidad

```bash
# Activar entorno
source .venv/bin/activate

# Linting
ruff check .

# Type checking
mypy .

# Tests con coverage
pytest --cov=controllers --cov=models --cov=utils --cov=config

# Formateo automático
ruff format .
```

### CI Pipeline (GitHub Actions)

En cada PR a `develop` o `main`:
1. ✅ Ruff (lint + format check)
2. ✅ MyPy (type checking)
3. ✅ Pytest (unit tests + coverage)

---

## 📦 Deploy

### Desarrollo Local
```bash
./start.sh  # http://localhost:8000
```

### Staging/Producción (Docker)
```dockerfile
# Dockerfile incluido para deploy en Railway, Render, Fly.io, Cloud Run
docker build -t trama-urbana-verde .
docker run -p 8000:8000 --env-file .env trama-urbana-verde
```

Variables de producción requeridas:
- `APP_ENV=production`
- `DEBUG=false`
- `DATABASE_URL` (Supabase production pooler)
- `SECRET_KEY` (para sesiones futuras)

---

## 🤝 Contribución

1. Fork del repo
2. Crear branch: `git checkout -b feature/nueva-funcionalidad`
3. Commits convencionales: `feat:`, `fix:`, `chore:`, `docs:`
4. Push + Pull Request a `develop`
5. CI debe pasar + 1 approval

### Convenciones de Commits
```
feat: nueva sección hero con animación
fix: corrige cálculo m² en ImpactMeter
chore: actualiza dependencias
docs: agrega guía deploy a README
```

---

## 📄 Licencia

MIT License - ver [LICENSE](LICENSE)

---

## 🙋 Créditos

- **Diseño**: Google Stitch ("Minimalist Business Showcase" → adaptado a "Green Tech")
- **Modelo de Negocio**: Business Model Canvas - Hackatón Urbanismo 2026
- **Desarrollo**: Luis Gamboa (@luisgamboaretamal)
- **Inspiración**: Recuperación táctica de espacios urbanos en Santiago de Chile