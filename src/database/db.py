from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.config import settings

async_engine = create_async_engine(
    url=settings.DB_URL,
    echo=False,
    future=True,
)

async_session_maker = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
