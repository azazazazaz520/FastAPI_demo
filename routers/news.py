from fastapi import APIRouter

#prefix路由前缀
#tags分组标签
router = APIRouter(prefix="/api/news",tags=["news"])


@router.get("/catagories")

async def get_catagories():
    return{"msg":"hello"}