from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from crud import news
from config.db_conf import get_db
#prefix路由前缀
#tags分组标签
router = APIRouter(prefix="/api/news",tags=["news"])


@router.get("/catagories")

async def get_catagories(skip:int=0,limit:int=100,db:AsyncSession = Depends(get_db)):
    catagories = await news.get_catagories(db,skip,limit)
    return{
        "code":200,
        "message":"获取新闻分类成功",
        "data":catagories
    }