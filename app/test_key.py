from sqlalchemy import select

from app.models import User
from app.deps import async_session_maker



async def create_test_users():
    async with async_session_maker() as session:
        existing = await session.execute(select(User).where(User.api_key.in_(["testkey-alice", "testkey-bob"])))
        existing_keys = {user.api_key for user in existing.scalars().all()}

        to_add = []
        if "testkey-alice" not in existing_keys:
            to_add.append(User(name="Alice", api_key="testkey-alice"))
        if "testkey-bob" not in existing_keys:
            to_add.append(User(name="Bob", api_key="testkey-bob"))

        if to_add:
            session.add_all(to_add)
            await session.commit()