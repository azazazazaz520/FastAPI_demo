from fastapi import APIRouter, Depends, Query, HTTPException


router = APIRouter(prefix="/api/users", tags=["users"])

@router.get("/register")

async def register():
    return {
        "code": 200,
        "message": "注册成功",
        "data": {
            "token": "用户访问令牌",
            "userInfo": {
            "id": 1,
            "username": "example_user",
            "bio": "这个人很懒，什么都没留下",
            "avatar": "https://fastly.jsdelivr.net/npm/@vant/assets/cat.jpeg"
            }
        }
    }