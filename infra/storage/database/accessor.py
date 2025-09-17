import logging
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from settings import settings
logger = logging.getLogger("vpn_service")


engine = create_async_engine(url=settings.db_url, future=True, echo=False, pool_pre_ping=True, query_cache_size=1200, )
AsyncSessionFactory = async_sessionmaker(
    engine,
    autoflush=False,
    expire_on_commit=False,
)


@asynccontextmanager
async def get_db_session() -> AsyncSession:
    try:
        async with AsyncSessionFactory() as session:
            yield session

    finally:
        await session.close()
