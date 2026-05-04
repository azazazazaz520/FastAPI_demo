from fastapi import FastAPI

# 创建应用实例
app = FastAPI()

# 定义一个简单的 GET 接口
@app.get("/")
def read_root():
    return {"Hello": "FastAPI", "Status": "Success"}

# 定义一个带路径参数的接口
@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "query": q}