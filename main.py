from fastapi import FastAPI
from routers import news
app = FastAPI()

@app.get("/")   
def read_root():
    return {"Hello": "FastAPI", "Status": "Success"}


app.include_router(news.router)