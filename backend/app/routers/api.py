from fastapi import APIRouter

router = APIRouter(prefix="/api", tags=["api"])

@router.get("/hello")
async def hello():
    return {"message": "你好，世界！"} 