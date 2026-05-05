from fastapi import FastAPI,Path,Query,HTTPException,Depends
from pydantic import BaseModel,Field
from fastapi.responses import HTMLResponse,FileResponse
# 创建应用实例
app = FastAPI()

# @app.middleware("http")
# async def middleware1(request,call_next):
#     print("中间件1start")
#     response = await call_next(request)
#     print("中间件1end")
#     return response
    

# 定义一个简单的 GET 接口
@app.get("/")   #get请求方法
def read_root():
    return {"Hello": "FastAPI", "Status": "Success"}

# # 定义一个带路径参数的接口
# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: str = None):
#     return {"item_id": item_id, "query": q}

# @app.get("/hello/{id}")

# async def get_hello(id:int = Path(...,gt=0,lt=100,description="1-100之间")):
#     return {"msg":"FastAPI","id":id}


# @app.get("/author/{name}")

# async def get_author(name:str = Path(...,min_length=2,max_length=10)):
#     return {"msg":f"这是{name}的信息"}

# @app.get("/news/news_list")
# async def get_news_list(skip:int= Query(0,description="跳过的记录数",lt=100),
#                         limit:int = Query(10,description="返回的记录数")):
#     return {"skip":skip,"limit":limit}

#注册
class User(BaseModel):
    username:str = Field(...,description="用户名")
    password:str

class news(BaseModel):
    id:int
    title:str
    content:str

@app.post("/register")
async def register(user:User):
    return user

@app.get("/html",response_class= HTMLResponse)
async def get_html():
    return "<h1>hellow</h1>"


@app.get("/files",response_class=FileResponse)
async def get_file():
    path = "./files/1.jpg"
    return FileResponse(path)

# @app.get("/news/{id}",response_model=news)
# async def get_news(id:int):
#     return {
#         "id":id,
#         "title":f"这是第{id}本书",
#         "content":"这是一本书"
#     }
# @app.get("/news/{id}")
# async def get_news(id:int):
#     id_list = [1,2,3,4,5,6]
#     if id not in id_list:
#         raise HTTPException(status_code=404,detail="查找的新闻不存在")
    
async def common_parameters(skip:int = Query(0,ge=0),limit:int = Query(0,le=60)):
    return {
        "skip":skip,
        "limit":limit
    }

@app.get("/news/news_list")
async def get_news_list(commons = Depends(common_parameters)):
    return commons