import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 导入配置
from config import env_config

# 创建FastAPI应用
app = FastAPI(
    title="AI角色聊天服务",
    description="提供LLM模型交互、语音识别和TTS功能的后端服务",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应限制为特定的域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 导入并配置日志
from utils.logger import get_logger
logger = get_logger("ai_chat_service")

# 异常处理
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"发生错误: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "内部服务器错误"}
    )

# 导入并注册路由
from api.chat_routes import router as chat_router
from api.speech_routes import router as speech_router
from api.character_routes import router as character_router

app.include_router(chat_router, prefix="/api/chat", tags=["聊天"])
app.include_router(speech_router, prefix="/api/speech", tags=["语音"])
app.include_router(character_router, prefix="/api", tags=["角色"])

# 测试接口
@app.get("/")
async def root():
    return {
        "message": "AI角色聊天服务运行中",
        "version": "1.0.0",
        "docs_url": "/docs",
        "default_provider": env_config.DEFAULT_LLM_PROVIDER
    }

# 启动服务
if __name__ == "__main__":
    logger.info(f"启动AI角色聊天服务，监听地址: http://{env_config.HOST}:{env_config.PORT}")
    logger.info(f"默认LLM提供商: {env_config.DEFAULT_LLM_PROVIDER}")
    
    uvicorn.run(
        "main:app",
        host=env_config.HOST,
        port=env_config.PORT,
        reload=env_config.DEBUG,
        log_level="info"
    )