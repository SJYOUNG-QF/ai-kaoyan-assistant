"""
FastAPI 主入口
这是整个后端的启动文件
"""

import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import health, pdf, chat

# 创建 FastAPI 应用实例
app = FastAPI(
    title="AI考研助手 API",
    description="考研学习助手后端服务",
    version="0.1.0",
)

# 配置 CORS (允许前端跨域访问)
# 部署时通过 FRONTEND_URL 环境变量指定前端地址
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(health.router)
app.include_router(pdf.router)
app.include_router(chat.router)
