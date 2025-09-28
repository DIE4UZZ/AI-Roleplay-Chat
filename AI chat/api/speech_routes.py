from fastapi import APIRouter, HTTPException, UploadFile, File, Form, BackgroundTasks
from fastapi.responses import FileResponse, StreamingResponse
import os
import tempfile
import logging

# 导入数据模型
from api.models import (
    SpeechRecognitionRequest, 
    SpeechRecognitionResponse, 
    TTSRequest, 
    TTSResponse,
    VoiceChatRequest,
    ErrorResponse
)

# 导入语音处理模块
from speech.recognition import speech_recognizer
from speech.tts import tts_engine
from speech.audio_utils import audio_utils
from api.chat_routes import ModelManager

# 创建路由实例
router = APIRouter()

# 配置日志
logger = logging.getLogger("ai_chat_service.api.speech")

# 语音识别接口
@router.post("/recognize", response_model=SpeechRecognitionResponse, responses={400: {"model": ErrorResponse}, 500: {"model": ErrorResponse}})
async def recognize_speech(
    file: UploadFile = File(...),
    language: str = Form("zh-CN"),
    sample_rate: int = Form(16000)
):
    """
    语音识别接口
    
    - **file**: 音频文件（支持wav、mp3等格式）
    - **language**: 语言代码（默认：zh-CN）
    - **sample_rate**: 采样率（默认：16000）
    
    响应：
    - **text**: 识别的文本
    - **language**: 使用的语言代码
    """
    try:
        logger.info(f"接收到语音识别请求，文件: {file.filename}")
        
        # 读取音频文件内容
        audio_bytes = await file.read()
        
        # 调用语音识别模块
        text, error = speech_recognizer.recognize_from_audio_bytes(audio_bytes)
        
        if error:
            logger.error(f"语音识别失败: {error}")
            raise HTTPException(status_code=400, detail=error)
        
        logger.info(f"语音识别成功，结果: {text}")
        
        # 返回识别结果
        return SpeechRecognitionResponse(
            text=text,
            language=language
        )
        
    except Exception as e:
        logger.error(f"语音识别处理失败: {str(e)}")
        raise HTTPException(status_code=500, detail="内部服务器错误")

# 文本转语音接口
@router.post("/tts", responses={400: {"model": ErrorResponse}, 500: {"model": ErrorResponse}})
async def text_to_speech(
    request: TTSRequest
):
    """
    文本转语音接口
    
    - **text**: 要转换的文本
    - **language**: 语言代码（默认：zh-cn）
    - **slow**: 是否使用慢速语音（默认：False）
    
    返回：音频文件（mp3格式）
    """
    try:
        logger.info(f"接收到文本转语音请求，文本长度: {len(request.text)} 字符")
        
        # 创建临时文件保存音频
        fd, temp_path = tempfile.mkstemp(suffix='.mp3')
        os.close(fd)
        
        try:
            # 调用TTS模块
            audio_path, error = tts_engine.text_to_speech(
                text=request.text,
                save_path=temp_path,
            )
            
            if error:
                logger.error(f"文本转语音失败: {error}")
                raise HTTPException(status_code=400, detail=error)
            
            # 返回音频文件
            return FileResponse(
                path=audio_path,
                media_type="audio/mpeg",
                filename=f"tts_output.mp3"
            )
            
        finally:
            # 注册后台任务清理临时文件
            # 注意：由于FastAPI的限制，这里不能直接传递temp_path给background_tasks
            # 实际应用中应该使用一个更复杂的清理机制
            pass
            
    except Exception as e:
        logger.error(f"文本转语音处理失败: {str(e)}")
        raise HTTPException(status_code=500, detail="内部服务器错误")

# 语音聊天接口（结合语音识别和LLM回复）
@router.post("/voice-chat", responses={400: {"model": ErrorResponse}, 500: {"model": ErrorResponse}})
async def voice_chat(
    file: UploadFile = File(...),
    character_id: int = Form(None),
    character_name: str = Form(None),
    character_description: str = Form(None),
    language: str = Form("zh-CN")
):
    """
    语音聊天接口（结合语音识别和AI回复）
    
    - **file**: 语音输入文件
    - **character_id**: 角色ID（可选）
    - **character_name**: 角色名称（可选）
    - **character_description**: 角色描述（可选）
    - **language**: 语言代码（默认：zh-CN）
    
    返回：AI回复的语音文件
    """
    try:
        logger.info(f"接收到语音聊天请求")
        
        # 1. 语音识别
        audio_bytes = await file.read()
        text, error = speech_recognizer.recognize_from_audio_bytes(audio_bytes)
        
        if error:
            logger.error(f"语音识别失败: {error}")
            raise HTTPException(status_code=400, detail=error)
        
        logger.info(f"语音识别结果: {text}")
        
        # 2. 构建角色上下文
        character_context = None
        if character_name:
            character_context = {
                "name": character_name,
                "description": character_description or ""
            }
        
        # 3. 调用LLM生成回复
        model = ModelManager.get_model()
        reply = model.generate_response(
            prompt=text,
            character_context=character_context
        )
        
        logger.info(f"AI回复生成完成: {reply}")
        
        # 4. 将回复转换为语音
        fd, temp_path = tempfile.mkstemp(suffix='.mp3')
        os.close(fd)
        
        try:
            audio_path, error = tts_engine.text_to_speech(
                text=reply,
                save_path=temp_path
            )
            
            if error:
                logger.error(f"文本转语音失败: {error}")
                raise HTTPException(status_code=400, detail=error)
            
            # 返回音频文件
            return FileResponse(
                path=audio_path,
                media_type="audio/mpeg",
                filename=f"ai_reply.mp3"
            )
            
        finally:
            # 注册后台任务清理临时文件
            pass
            
    except Exception as e:
        logger.error(f"语音聊天处理失败: {str(e)}")
        raise HTTPException(status_code=500, detail="内部服务器错误")

# 清理临时文件的后台任务（实际应用中需要更完善的实现）
def cleanup_temp_file(file_path: str):
    """\清理临时文件"""
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            logger.info(f"临时文件已清理: {file_path}")
    except Exception as e:
        logger.error(f"清理临时文件失败: {str(e)}")