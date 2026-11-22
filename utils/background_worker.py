"""Background worker for Green Tech - handles async tasks."""

import time
import signal
import sys
from datetime import UTC, datetime
from contextlib import contextmanager

from config.database import get_db_session
from controllers.requests import RequestsController
from models import RequestStatus


class BackgroundWorker:
    """Background worker for processing async tasks."""

    def __init__(self, poll_interval: int = 60):
        self.poll_interval = poll_interval
        self.running = False

    def start(self):
        """Start the worker loop."""
        self.running = True
        print(f"Background worker started (poll interval: {self.poll_interval}s)")

        # Handle graceful shutdown
        signal.signal(signal.SIGTERM, self._signal_handler)
        signal.signal(signal.SIGINT, self._signal_handler)

        while self.running:
            try:
                self._process_pending_tasks()
            except Exception as e:
                print(f"Worker error: {e}")

            # Sleep with early exit check
            for _ in range(self.poll_interval):
                if not self.running:
                    break
                time.sleep(1)

        print("Background worker stopped")

    def _signal_handler(self, signum, frame):
        """Handle shutdown signals."""
        print(f"Received signal {signum}, shutting down...")
        self.running = False

    def _process_pending_tasks(self):
        """Process pending routing and other tasks."""
        with get_db_session() as session:
            controller = RequestsController(session)

            # Process automatic routing for requests past deadline
            result = controller.process_routing_all()
            if result.get("processed", 0) > 0:
                print(f"Processed routing for {result['processed']} requests")

            # Clean up old draft requests (older than 30 days)
            self._cleanup_old_drafts(controller)

    def _cleanup_old_drafts(self, controller: RequestsController):
        """Remove draft requests older than 30 days."""
        from datetime import timedelta
        from sqlalchemy import select, delete

        from models import Request

        cutoff = datetime.now(UTC) - timedelta(days=30)
        stmt = delete(Request).where(
            Request.status == RequestStatus.DRAFT,
            Request.created_at < cutoff
        )
        result = controller.session.execute(stmt)
        if result.rowcount > 0:
            print(f"Cleaned up {result.rowcount} old draft requests")


def process_routing_all(controller: RequestsController) -> dict:
    """Process automatic routing for all pending requests."""
    from datetime import datetime, UTC
    from sqlalchemy import select

    from models import Request

    # Get all requests that are sent or waiting and past deadline
    stmt = select(Request).where(
        Request.status.in_([RequestStatus.SENT, RequestStatus.WAITING_RESPONSE]),
        Request.deadline_at.is_not(None),
        Request.deadline_at < datetime.now(UTC),
    )
    result = controller.session.execute(stmt)
    requests = result.scalars().all()

    processed = 0
    for req in requests:
        if controller.process_routing(req.id):
            processed += 1

    return {"processed": processed, "total_checked": len(requests)}


# Add method to RequestsController for use in worker
RequestsController.process_routing_all = process_routing_all


if __name__ == "__main__":
    # Get poll interval from environment (default 60s)
    import os
    poll_interval = int(os.getenv("WORKER_POLL_INTERVAL", "60"))

    worker = BackgroundWorker(poll_interval=poll_interval)
    worker.start()