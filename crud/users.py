from datetime import datetime, timedelta
import uuid

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.users import User, UserToken
from schemas.users import UserRequest
from utils import security

async def get_user_by_username(db: AsyncSession, username: str):
    stmt = select(User).where(User.username == username)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

async def create_user(db: AsyncSession, user_data:UserRequest):
    hashed_password = security.get_hash_password(user_data.password)
    user = User(username=user_data.username, password=hashed_password)
    db.add(user)
    await db.commit()
    await db.refresh(user) #从数据库读回最新的user
    return user

#生成token
async def create_token(db:AsyncSession,user_id:int):
    #生成token+过期时间
    #查询当前用户是否有token
    token = str(uuid.uuid4())
    expires_at = datetime.now() + timedelta(days=7) #设置过期时间为7天
    query = select(UserToken).where(UserToken.user_id == user_id)
    result = await db.execute(query)
    user_token = result.scalar_one_or_none()
    if user_token:
        #更新token和过期时间
        user_token.token = token
        user_token.expires_at = expires_at
    else:
        user_token = UserToken(user_id=user_id, token=token, expires_at=expires_at)
        db.add(user_token)
        await db.commit()

    return token