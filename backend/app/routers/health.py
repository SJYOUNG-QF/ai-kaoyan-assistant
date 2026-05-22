"""
健康检查路由
用于确认后端服务是否正常运行
"""

from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/health")
def health_check():
    """
    健康检查接口
    访问 http://localhost:8000/health
    如果返回 {"status": "ok"} 说明服务正常运行
    """
    return {"status": "ok", "message": "AI考研助手后端运行中"}
