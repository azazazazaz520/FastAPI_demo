from fastapi import FastAPI,Path,Query,HTTPException,Depends
from pydantic import BaseModel,Field
from fastapi.responses import HTMLResponse,FileResponse
from sqlalchemy.ext.asyncio import create_async_engine,async_sessionmaker,AsyncSession
from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column
from datetime import datetime
from sqlalchemy import DateTime,func,String,Float,select
# 创建应用实例
app = FastAPI()
ASYNC_DATABASE_URL = "mysql+aiomysql://root:123456@localhost:3306/FastAPI_first?charset=utf8"
async_engine = create_async_engine(
    ASYNC_DATABASE_URL,
    echo = True,
    pool_size = 10,
    max_overflow = 20
)
class Base(DeclarativeBase):
    create_time:Mapped[datetime] = mapped_column(DateTime,insert_default=func.now(),default=func.now,comment="创建时间")    
    update_time:Mapped[datetime] = mapped_column(DateTime,insert_default=func.now(),default=func.now,onupdate=func.now(),comment="修改时间")
class Book(Base):
    __tablename__ = "Book"
    id:Mapped[int] = mapped_column(primary_key=True,comment="书籍id")
    book_name:Mapped[str] = mapped_column(String(255),comment="书名")
    author:Mapped[str] = mapped_column(String(255),comment="作者")
    price:Mapped[float] = mapped_column(Float,comment="价格")
    publisher:Mapped[str] = mapped_column(String(255),comment="出版社")

async def create_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.on_event("startup")
async def startup_event():
    await create_tables()


# 定义一个简单的 GET 接口
@app.get("/")   #get请求方法
def read_root():
    return {"Hello": "FastAPI", "Status": "Success"}


asyncSessionLocal = async_sessionmaker(
    bind= async_engine,     #绑定数据库引擎
    class_=AsyncSession,    #指定会话类
    expire_on_commit=False  #回话不过期
)

async def get_database():
    async with asyncSessionLocal() as session:
        try:
            yield session   #返回数据库会话给路由处理函数
            await session.commit()  #提交事务
        except Exception:
            await session.rollback()    #回滚
            raise
        finally:
            await session.close()   #关闭会话


@app.get("/book/books")
async def get_book_list(db:AsyncSession = Depends(get_database)):
    result = await db.execute(select(Book))
    book = result.scalars().all()
    return book