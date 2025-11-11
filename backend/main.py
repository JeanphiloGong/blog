# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import posts
from infra.db import Base, engine
app = FastAPI(
        title="日志系统",
        description="日志系统",
        version="1.0.0",
        )

# 创建所有orm表
Base.metadata.create_all(bind=engine)

# 允许的前端地址（开发环境）
origins = [
    "http://localhost:5173",  # SvelteKit dev server
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,          # 或 ["*"] 先图省事，生产再收紧
    allow_credentials=True,
    allow_methods=["*"],            # 允许所有方法：GET/POST/PUT/OPTIONS...
    allow_headers=["*"],            # 允许所有头
)

app.include_router(posts.router, tags=["posts"])
