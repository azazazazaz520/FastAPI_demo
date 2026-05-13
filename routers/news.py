from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from crud import news
from config.db_conf import get_db
#prefix路由前缀
#tags分组标签
router = APIRouter(prefix="/api/news",tags=["news"])


@router.get("/categories")
async def get_categories(skip:int=0,limit:int=100,db:AsyncSession = Depends(get_db)):
    categories = await news.get_categories(db,skip,limit)
    return{
        "code":200,
        "message":"获取新闻分类成功",
        "data":categories
    }

@router.get("/list")
async def get_news_list(
        category_id: int = Query(..., alias="categoryId"),
        page: int = 1,
        page_size: int = Query(10, alias="pageSize", le=100),#最大值100
        db: AsyncSession = Depends(get_db)
):
    
    # 思路：处理分页规则 → 查询新闻列表 → 计算总量 → 计算是否还有更多
    offset = (page - 1) * page_size
    news_list = await news.get_news_list(db, category_id, offset, page_size)
    total = await news.get_news_count(db, category_id)
    # (跳过的 + 当前列表里面的数量) < 总量
    has_more = (offset + len(news_list)) < total
    return {
        "code": 200,
        "message": "获取新闻列表成功",
        "data": {
            "list": news_list,
            "total": total,
            "hasMore": has_more
        }
    }