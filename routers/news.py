from fastapi import APIRouter

#prefix路由前缀
#tags分组标签
router = APIRouter(prefix="/api/news",tags=["news"])


@router.get("/catagories")

async def get_catagories(skip:int=0,limit:int=100):
    return{
        "code":200,
        "message":"获取新闻分类成功",
        "data":"新闻分类列表"
    }