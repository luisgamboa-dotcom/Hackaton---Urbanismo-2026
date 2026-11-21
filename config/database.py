"""Database configuration and session management for SQLAlchemy async."""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from config.settings import get_settings


settings = get_settings()


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models."""

    pass


# Engine and session factory (initialized lazily)
_engine: AsyncEngine | None = None
_session_factory: async_sessionmaker[AsyncSession] | None = None


def get_engine() -> AsyncEngine:
    """Get or create the async database engine."""
    global _engine
    if _engine is None:
        if not settings.database_url:
            raise ValueError(
                "DATABASE_URL not configured. Set it in .env file or environment variables."
            )
        _engine = create_async_engine(
            settings.database_url,
            echo=settings.debug,
            pool_pre_ping=True,
            pool_size=5,
            max_overflow=10,
        )
    return _engine


def get_session_factory() -> async_sessionmaker[AsyncSession]:
    """Get or create the async session factory."""
    global _session_factory
    if _session_factory is None:
        _session_factory = async_sessionmaker(
            bind=get_engine(),
            class_=AsyncSession,
            expire_on_commit=False,
            autoflush=False,
        )
    return _session_factory


@asynccontextmanager
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Get a database session as async context manager.

    Usage:
        async with get_session() as session:
            result = await session.execute(select(Space))
            spaces = result.scalars().all()
    """
    factory = get_session_factory()
    async with factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db() -> None:
    """Initialize database: create all tables.

    This should be called once at application startup.
    In production, use Alembic migrations instead.
    """
    engine = get_engine()
    async with engine.begin() as conn:
        # Import all models to register them
        from models import (  # noqa: F401
            Space,
            Partner,
            ImpactMetric,
            Community,
        )
        await conn.run_sync(Base.metadata.create_all)


async def close_db() -> None:
    """Close database connections. Call on application shutdown."""
    global _engine, _session_factory
    if _engine is not None:
        await _engine.dispose()
        _engine = None
        _session_factory = None


# Dependency for FastAPI
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency for database session.

    Usage in routes:
        @app.get("/spaces")
        async def list_spaces(session: AsyncSession = Depends(get_db_session)):
            ...
    """
    async with get_session() as session:
        yield session