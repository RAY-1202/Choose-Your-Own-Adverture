from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# 导入配置设置
from core.config import settings
from routers import story, job
from db.database import create_tables

create_tables()

# 创建 FastAPI 应用实例
app = FastAPI(
    title="Choose Your Own Adventure Game API",
    description="API to generate cool stories",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# 配置 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(story.router, prefix = settings.API_PREFIX)
app.include_router(job.router, prefix = settings.API_PREFIX)

# 只有当作为主程序运行时，才启动服务器
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host = "localhost", port = 8000, reload = True)