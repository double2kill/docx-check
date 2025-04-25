from fastapi import APIRouter
from app.routers.files import router as files_router

router = APIRouter(tags=["api"])

@router.get("/hello")
async def hello():
    return {"message": "你好，世界！"}

# 包含文件处理路由器
router.include_router(files_router, prefix="/files", tags=["files"]) 