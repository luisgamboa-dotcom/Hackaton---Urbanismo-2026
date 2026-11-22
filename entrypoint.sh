#!/bin/bash
# Entrypoint for Green Tech Docker container
# Can run as web service or worker based on COMMAND

set -euo pipefail

# Run database migrations/initialization
echo "Initializing database..."
python -c "
from config.database import init_and_seed_db
try:
    init_and_seed_db()
    print('Database initialized and seeded successfully')
except Exception as e:
    print(f'Database initialization warning: {e}')
"

# Sync design tokens
echo "Syncing design tokens..."
python -m utils.stitch_sync 2>/dev/null && echo "Design tokens synced" || echo "Design token sync skipped"

# Determine command to run
COMMAND="${1:-web}"

case "$COMMAND" in
    web)
        echo "Starting web service on port 8000..."
        exec uvicorn main:app --host 0.0.0.0 --port 8000
        ;;
    worker)
        echo "Starting background worker..."
        exec python -m utils.background_worker
        ;;
    *)
        echo "Unknown command: $COMMAND"
        echo "Usage: entrypoint.sh [web|worker]"
        exit 1
        ;;
esac