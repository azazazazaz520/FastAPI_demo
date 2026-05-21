from pydantic import BaseModel,ConfigDict,Field
from typing import Optional
class UserRequest(BaseModel):
    username: str
    password: str

# user_info 对应的类：基础类 + Info 类（id、用户名）
class UserInfoBase(BaseModel):
    """
    用户信息基础数据模型
    """
    nickname: Optional[str] = Field(None, max_length=50, description="昵称")
    avatar: Optional[str] = Field(None, max_length=255, description="头像URL")
    gender: Optional[str] = Field(None, max_length=10, description="性别")
    bio: Optional[str] = Field(None, max_length=500, description="个人简介")

class UserInfoResponse(UserInfoBase):
    id: int
    username: str

    #模型类兼容
    model_config = ConfigDict(
        from_attributes=True       #允许从ORM对象中取值
    )
    

class UserAuthResponse(BaseModel):
    token: str
    user_info: UserInfoResponse = Field(..., alias="userInfo")

    #模型类兼容
    model_config = ConfigDict(
        populate_by_name=True,     #字段名兼容
        from_attributes=True       #允许从ORM对象中取值
    )