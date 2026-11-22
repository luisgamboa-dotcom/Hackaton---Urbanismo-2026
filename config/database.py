"""Database configuration and session management for SQLAlchemy sync."""

from collections.abc import Generator
from contextlib import contextmanager

from sqlalchemy import Engine, create_engine, text
from sqlalchemy.orm import Session, sessionmaker

from config.settings import get_settings
from models.base import Base

settings = get_settings()


_engine: Engine | None = None
_session_factory: sessionmaker[Session] | None = None


def get_engine() -> Engine:
    """Get or create the database engine."""
    global _engine
    if _engine is None:
        if not settings.database_url:
            raise ValueError(
                "DATABASE_URL not configured. Set it in .env file or environment variables."
            )
        db_url = settings.database_url


        if db_url.startswith("sqlite://"):

            connect_args = {"check_same_thread": False} if db_url.startswith("sqlite:///") else {}
            _engine = create_engine(
                db_url,
                echo=settings.debug,
                connect_args=connect_args,
            )
        else:


            if db_url.startswith("postgresql+asyncpg://"):
                db_url = db_url.replace("postgresql+asyncpg://", "postgresql+psycopg2://")
            elif db_url.startswith("postgresql://"):
                db_url = db_url.replace("postgresql://", "postgresql+psycopg2://")


            pool_size = 5
            max_overflow = 10
            if settings.is_production:
                pool_size = 10
                max_overflow = 20

            _engine = create_engine(
                db_url,
                echo=settings.debug,
                pool_pre_ping=True,
                pool_size=pool_size,
                max_overflow=max_overflow,
                pool_recycle=1800,
            )
    return _engine


def get_session_factory() -> sessionmaker[Session]:
    """Get or create the session factory."""
    global _session_factory
    if _session_factory is None:
        _session_factory = sessionmaker(
            bind=get_engine(),
            class_=Session,
            expire_on_commit=False,
            autoflush=False,
        )
    return _session_factory


@contextmanager
def get_session() -> Generator[Session, None, None]:
    """Get a database session as context manager.

    Usage:
        with get_session() as session:
            result = session.execute(select(Space))
            spaces = result.scalars().all()
    """
    factory = get_session_factory()
    with factory() as session:
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()


def init_db() -> None:
    """Initialize database: create all tables.

    This should be called once at application startup.
    In production, use Alembic migrations instead.
    """
    engine = get_engine()

    from models import (
        Community,
        ImpactMetric,
        ModerationQueue,
        Organization,
        Partner,
        Request,
        Space,
        SubmissionHistory,
        Support,
        User,
    )
    Base.metadata.create_all(engine)


def seed_db() -> None:
    """Seed database with initial data from SQL files."""
    import sqlite3
    from contextlib import suppress
    from pathlib import Path

    db_url = settings.database_url


    seed_files = [
        "seed_sqlite.sql",
        "seed_user_tables.sql",
    ]

    if db_url.startswith("sqlite://"):
        db_path = db_url.replace("sqlite:///", "")

        for seed_filename in seed_files:
            seed_file = Path(__file__).parent.parent / "sql" / seed_filename

            if not seed_file.exists():
                print(f"Seed file not found: {seed_filename}")
                continue


            sqlite_conn = sqlite3.connect(db_path)
            try:
                sql_content = seed_file.read_text(encoding="utf-8")

                lines = sql_content.split('\n')
                filtered = [line for line in lines if not line.strip().startswith('--')]
                clean_sql = '\n'.join(filtered)
                sqlite_conn.executescript(clean_sql)
                sqlite_conn.commit()
                print(f"Seeded: {seed_filename}")
            except Exception as e:
                print(f"Seed warning ({seed_filename}): {e}")
            finally:
                sqlite_conn.close()
    else:

        engine = get_engine()

        for seed_filename in seed_files:
            seed_file = Path(__file__).parent.parent / "sql" / seed_filename

            if not seed_file.exists():
                print(f"Seed file not found: {seed_filename}")
                continue

            with engine.begin() as pg_conn:
                sql_content = seed_file.read_text(encoding="utf-8")
                statements = [stmt.strip() for stmt in sql_content.split(";") if stmt.strip()]
                for statement in statements:
                    if statement.startswith("--"):
                        continue
                    with suppress(Exception):
                        pg_conn.execute(text(statement))
                print(f"Seeded: {seed_filename}")


def init_and_seed_db() -> None:
    """Initialize database and seed with initial data."""
    init_db()
    seed_db()


def close_db() -> None:
    """Close database connections. Call on application shutdown."""
    global _engine, _session_factory
    if _engine is not None:
        _engine.dispose()
        _engine = None
        _session_factory = None



def get_db_session() -> Generator[Session, None, None]:
    """FastAPI dependency for database session.

    Usage in routes:
        @app.get("/spaces")
        async def list_spaces(session: Session = Depends(get_db_session)):
            ...
    """
    with get_session() as session:
        yield session
