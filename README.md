# Green Tech — Recuperación Urbana Táctica en Santiago

> **Plataforma web para postular, gestionar y transformar espacios urbanos inutilizados en sectores densos de Santiago mediante urbanismo táctico participativo.**

---

## Propósito del Proyecto

Green Tech es una plataforma que conecta a la comunidad con municipios, empresas, universidades y ONGs para **recuperar lotes baldíos, terrenos abandonados y vertederos ilegales** convirtiéndolos en plazas de bolsillo, corredores verdes, huertos comunitarios y zonas de descanso.

### Flujo principal
1. **Ciudadano** postula un espacio en `/postular` (ubicación en mapa + datos básicos + contacto)
2. **Sistema** valida y envía a moderación
3. **Moderador** aprueba/rechaza/solicita cambios
4. **Routing automático** deriva la solicitud: Municipalidad → Empresas → Escuelas → Universidades → Redes Sociales
5. **Ejecución** con voluntarios y socios, entrega a la comunidad

---

## Inicio Rápido

```bash
# 1. Clonar
git clone https://github.com/luisgamboa-dotcom/Hackaton---Urbanismo-2026.git
cd Hackaton---Urbanismo-2026

# 2. Configurar entorno
cp .env.example .env  # Editar con credenciales SMTP y DB

# 3. Ejecutar localmente
./start.sh
# http://localhost:8000
```

---

## Stack Tecnológico

| Capa | Tecnología |
|------|------------|
| **Backend** | FastAPI 0.115 + Python 3.12 |
| **DB** | PostgreSQL (Render) / SQLite (dev) + SQLAlchemy 2.0 |
| **Templates** | Jinja2 + herencia modular |
| **Frontend** | CSS custom properties (Design Tokens), Vanilla ES6 JS |
| **Mapas** | Leaflet 1.9.4 + MarkerCluster |
| **Deploy** | Docker + Render Blueprint (Web + Worker + PostgreSQL) |

---

## Estructura Clave

```
├── config/           # Settings, DB, Design Tokens (Stitch)
├── controllers/      # Lógica: requests, API, landing
├── models/           # SQLAlchemy: Space, Request, User, Partner, Community
├── views/            # Jinja2 templates (16 páginas + partials)
├── public/           # CSS/JS estáticos (componentes, mapa, utils)
├── sql/              # Schema + seed data (4 terrenos ejemplo)
├── utils/            # Email, background worker, formatters
├── main.py           # FastAPI app + 19 rutas
├── render.yaml       # Blueprint Render (Web + Worker + PG)
├── Dockerfile        # Multi-stage build
└── entrypoint.sh     # Inicio web/worker + migraciones
```

---

## Páginas Implementadas

| Ruta | Descripción |
|------|-------------|
| `/` | Landing con mapa interactivo (filtros: intervención, abandonado ⚠️, vertedero 🗑️) |
| `/postular` | Formulario 3 pasos: mapa/manual → detalles → contacto/fotos |
| `/espacios` | Listado de intervenciones con tarjetas |
| `/impacto` | Métricas animadas (m², espacios, voluntarios, comunas) |
| `/socios` | Red de partners (municipalidades, empresas, ONGs, universidades) |
| `/comunidades` | Juntas de vecinos y organizaciones |
| `/actividades` | Talleres, voluntariados, eventos |
| `/testimonios` | Experiencias de vecinos |
| `/nosotros` | Equipo, misión, metodología |
| `/contacto` | Formulario soporte |
| `/voluntariado` | Inscripción voluntarios |
| `/recursos` | Guías, normativa, materiales |
| `/transparencia` | Reportes, presupuesto, métricas |
| `/accesibilidad` | Declaración de accesibilidad |
| `/privacidad` `/terminos` `/cookies` | Legal |

---

## Funcionalidades Backend

- **Postulación espacios** con mapa picker (Leaflet) y subida de fotos (máx 5)
- **Registro usuarios** por email (identificación para soporte sin duplicados)
- **Sistema de soporte** con tickets y estados
- **Routing automático secuencial** (Municipalidad → Empresas → Escuelas → Universidades → RRSS) con deadlines
- **Panel municipal** para ver solicitudes por comuna
- **Cola de moderación** (aprobar/rechazar/solicitar cambios + emails)
- **Worker background** procesa routing y limpia drafts >30 días
- **Emails transaccionales** (Gmail SMTP) en cada cambio de estado

---

## Deploy en Render

1. **Agregar payment info** en Render Dashboard → Billing
2. **Crear Blueprint** desde repo: `render.yaml`
3. **Configurar env vars** en Dashboard tras deploy:
   - `SMTP_USERNAME` = luis.gamboa@puentemaipo.cl
   - `SMTP_PASSWORD` = Gmail App Password
   - `EMAIL_FROM` = Green Tech <noreply@tramaurbanaverde.cl>
   - `EMAIL_TO` = newcoolskeleton95@gmail.com

Servicios creados:
- **green-tech-api** (Web Service, Docker, puerto 8000)
- **green-tech-worker** (Background Worker, mismo Dockerfile)
- **green-tech-db** (PostgreSQL 16, plan free)

---

## Calidad

```bash
ruff check .      # Lint
mypy .            # Type check
pytest            # Tests
```

---

## Licencia

MIT — Desarrollado para Hackatón Urbanismo 2026 por Luis Gamboa, Vicente Cea y Benjamín Riquelme.