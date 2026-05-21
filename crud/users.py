from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.users import User
from schemas.users import UserResquest


async def get_user_by_username(db: AsyncSession, username: str):
    stmt = select(User).where(User.username == username)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

async def create_user(db: AsyncSession, user_data:UserResquest):
    new_user = User(username=user_data.username, password=user_data.password)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user