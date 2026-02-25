from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from fastapi import Depends, Header, HTTPException

from app.models import Base, User
from app.services import service

import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://postgres:postgres@db:5432/tweetsdb"
)

engine = create_async_engine(
    DATABASE_URL,
    echo=True,           # Логирует SQL‑запросы
    pool_pre_ping=True,  # Проверяет соединения
    future=True
)


# Асинхронная функция для сброса и создания таблиц
async def init_models():
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)   # ← Асинхронный drop_all
        await conn.run_sync(Base.metadata.create_all)  # ← Асинхронный create_all


async_session_maker = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

async def get_current_user(api_key: str = Header(...), session: AsyncSession = Depends(get_session)) -> User:
    return await service.get_user_by_api_key(session, api_key)
