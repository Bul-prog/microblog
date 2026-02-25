import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.models import Base, User
from app.deps import get_session


# SQLite in-memory shared между соединениями
TEST_DB_URL = "sqlite+aiosqlite://"

engine_test = create_async_engine(
    TEST_DB_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

SessionTest = async_sessionmaker(engine_test, class_=AsyncSession, expire_on_commit=False)


async def override_get_session():
    async with SessionTest() as session:
        yield session


app.dependency_overrides[get_session] = override_get_session


@pytest.fixture(scope="session", autouse=True)
async def prepare_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # seed users
    async with SessionTest() as session:
        session.add_all(
            [
                User(name="alice", api_key="alice-key"),
                User(name="bob", api_key="bob-key"),
                User(name="carol", api_key="carol-key"),
            ]
        )
        await session.commit()

    yield

    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
