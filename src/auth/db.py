from collections.abc import Generator

from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from src.config import settings

engine = create_async_engine(settings.DATABASE_URL, future=True, echo=True)
async_session = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)


async def get_db_session() -> Generator:
    try:
        session: AsyncSession = async_session()
        yield session
    finally:
        await session.close()


async def get_redis_connection():
    try:
        r = Redis(
            host=settings.REDIS_HOST, port=6379, db=0, decode_responses=True
        )
        yield r
    finally:
        await r.close()
