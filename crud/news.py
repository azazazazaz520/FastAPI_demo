from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, update
from models.news import Category,News
async def get_categories(db:AsyncSession,skip:int = 0,limit:int = 100):
    stmt = select(Category).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()

async def get_news_list(db:AsyncSession,category_id:int,skip:int=0,limit:int=10):
    stmt = select(News).where(News.category_id == category_id).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()

async def get_news_count(db:AsyncSession,category_id:int):#查询指定分类下的新闻总量
    stmt = select(func.count(News.id)).where(News.category_id == category_id)
    db_result = await db.execute(stmt)
    return db_result.scalar_one()

async def get_news_detail(db:AsyncSession,news_id:int):
    stmt = select(News).where(News.id == news_id)
    result = await db.execute(stmt)
    news_detail = result.scalar_one_or_none()
    return news_detail

async def increase_news_views(db:AsyncSession,news_id:int):
    stmt = update(News).where(News.id == news_id).values(views=News.views + 1)
    await db.execute(stmt)
    await db.commit()