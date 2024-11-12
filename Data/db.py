from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from .config import settings

async_engine = create_async_engine(
    url=settings.Database_URL_asyncpg,
)

async_session = sessionmaker(
    async_engine,
    class_=AsyncSession
)

sync_engine = create_engine (
    url=settings.Database_URL_psycopg,
)