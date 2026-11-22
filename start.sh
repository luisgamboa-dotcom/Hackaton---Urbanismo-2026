set -euo pipefail
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}
log_success() {
    echo -e "${GREEN}[OK]${NC} $1"
}
log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}
log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_ROOT"
log_info "Starting Trama Urbana Verde..."
log_info "Project root: $PROJECT_ROOT"
if [ ! -d ".venv" ]; then
    log_info "Creating virtual environment..."
    python3 -m venv .venv
    log_success "Virtual environment created"
else
    log_info "Virtual environment already exists"
fi
log_info "Activating virtual environment..."
source .venv/bin/activate
log_info "Upgrading pip and installing dependencies..."
pip install --upgrade pip > /dev/null 2>&1
pip install -r requirements.txt > /dev/null 2>&1
log_success "Dependencies installed"
if [ -f ".env" ]; then
    log_info "Loading environment variables from .env..."
    set -a
    source .env
    set +a
    log_success "Environment variables loaded"
else
    log_warn "No .env file found. Copy .env.example to .env and configure DATABASE_URL"
    log_warn "Continuing without database initialization..."
fi
if [ -n "${DATABASE_URL:-}" ]; then
    log_info "Initializing database..."
    python -c "
from config.database import init_and_seed_db
init_and_seed_db()
" && log_success "Database initialized and seeded" || {
        log_error "Database initialization failed"
        exit 1
    }
else
    log_warn "DATABASE_URL not set, skipping database initialization"
fi
log_info "Syncing design tokens..."
python -m utils.stitch_sync > /dev/null 2>&1 && log_success "Design tokens synced" || {
    log_warn "Design token sync failed (utils/stitch_sync.py not yet implemented)"
}
log_info "Starting Uvicorn server on http://localhost:8000"
log_info "Press Ctrl+C to stop"
echo ""
exec uvicorn main:app --host 0.0.0.0 --port 8000 --reload