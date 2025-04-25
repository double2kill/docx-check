from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from pathlib import Path
from app.routers.api import router as api_router
from app.config import settings

app = FastAPI(title=settings.APP_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 添加API路由
app.include_router(api_router, prefix=settings.API_PREFIX)

# 挂载静态文件目录
static_dir = Path(__file__).parent / "app" / "static"
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

@app.get("/")
async def root():
    return {"message": "欢迎使用FastAPI!"}

if __name__ == "__main__":
    import uvicorn
    import threading
    import time
    import logging
    
    def print_docs_url():
        time.sleep(1)  # 等待服务器启动
        # 直接使用标准的 logging，但模拟 Uvicorn 的格式
        log_format = "\033[32mINFO\033[0m:     %(message)s"
        logging.basicConfig(level=logging.INFO, format=log_format, force=True)
        logging.info("API文档地址: http://localhost:8000/docs")
        logging.info("文档上传测试页面: http://localhost:8000/static/upload.html")
    
    # 在新线程中打印文档URL
    threading.Thread(target=print_docs_url, daemon=True).start()
    
    # 正常启动服务器
    uvicorn.run("main:app", host="localhost", port=8000, reload=True) 