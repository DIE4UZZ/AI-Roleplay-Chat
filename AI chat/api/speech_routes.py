from fastapi import APIRouter, HTTPException, UploadFile, File, Form, BackgroundTasks, Request
from fastapi.responses import FileResponse, StreamingResponse
import os
import tempfile
import logging
import uuid
import asyncio
from typing import Dict, Optional

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
from speech.audio_converter import audio_converter
from api.chat_routes import ModelManager

# 创建路由实例
router = APIRouter()

# 配置日志
logger = logging.getLogger("ai_chat_service.api.speech")

# 语音识别会话管理
recognition_sessions: Dict[str, Dict] = {}


# 音频格式转换接口
@router.post("/convert-audio", responses={400: {"model": ErrorResponse}, 500: {"model": ErrorResponse}})
async def convert_audio_format(
    file: UploadFile = File(...),
    target_format: str = Form("wav"),
    sample_rate: int = Form(None),
    channels: int = Form(None)
):
    """
    音频格式转换接口
    
    - **file**: 输入音频文件
    - **target_format**: 目标格式（支持的格式：wav, webm, mp3）
    - **sample_rate**: 目标采样率（可选）
    - **channels**: 目标声道数（可选）
    
    返回：转换后的音频文件
    """
    try:
        logger.info(f"接收到音频格式转换请求，原始文件: {file.filename}, 目标格式: {target_format}")
        
        # 读取音频文件内容
        audio_bytes = await file.read()
        
        # 检查目标格式
        if target_format.lower() not in ['wav', 'webm', 'mp3']:
            raise HTTPException(status_code=400, detail=f"不支持的目标格式: {target_format}，支持的格式: wav, webm, mp3")
        
        # 根据目标格式选择转换方法
        if target_format.lower() == 'wav':
            # 转换任意格式到WAV
            converted_path, error = audio_converter.convert_bytes_to_wav(
                audio_bytes=audio_bytes,
                original_filename=file.filename,
                sample_rate=sample_rate or env_config.AUDIO_SAMPLE_RATE,
                channels=channels or env_config.AUDIO_CHANNELS
            )
        elif target_format.lower() == 'webm':
            # 先转换为WAV，再转换为WebM
            # 第一步：转换为WAV
            wav_path, error1 = audio_converter.convert_bytes_to_wav(
                audio_bytes=audio_bytes,
                original_filename=file.filename,
                sample_rate=sample_rate or env_config.AUDIO_SAMPLE_RATE,
                channels=channels or env_config.AUDIO_CHANNELS
            )
            
            if wav_path:
                # 第二步：转换为WebM
                converted_path, error2 = audio_converter.wav_to_webm(
                    input_data=wav_path,
                    quality="medium"
                )
                error = error2
            else:
                converted_path = None
                error = error1
        else:  # mp3
            # 对于MP3格式，直接使用pydub进行转换
            import tempfile
            fd, temp_path = tempfile.mkstemp(suffix='.mp3')
            os.close(fd)
            
            try:
                from pydub import AudioSegment
                import io
                
                # 读取音频数据
                audio = AudioSegment.from_file(io.BytesIO(audio_bytes))
                
                # 应用采样率和声道数设置
                if sample_rate:
                    audio = audio.set_frame_rate(sample_rate)
                if channels:
                    audio = audio.set_channels(channels)
                
                # 导出为MP3
                audio.export(temp_path, format="mp3", bitrate="128k")
                converted_path = temp_path
                error = None
                
            except Exception as e:
                converted_path = None
                error = f"MP3转换失败: {str(e)}"
        
        if error:
            logger.error(f"音频格式转换失败: {error}")
            raise HTTPException(status_code=400, detail=error)
        
        logger.info(f"音频格式转换成功: {converted_path}")
        
        # 根据目标格式设置响应类型
        content_type_map = {
            'wav': 'audio/wav',
            'webm': 'audio/webm', 
            'mp3': 'audio/mpeg'
        }
        
        # 返回转换后的音频文件
        return FileResponse(
            path=converted_path,
            media_type=content_type_map[target_format.lower()],
            filename=f"converted_{file.filename.rsplit('.', 1)[0]}.{target_format}"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"音频格式转换处理失败: {str(e)}")
        raise HTTPException(status_code=500, detail="内部服务器错误")

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

# 语音识别会话接口 - 开始
@router.post("/start", responses={500: {"model": ErrorResponse}})
async def start_voice_recognition():
    """
    开始语音识别会话
    
    返回:
    - **id**: 会话ID
    """
    try:
        # 生成会话ID
        session_id = str(uuid.uuid4())
        
        logger.info(f"开始语音识别会话: {session_id}")
        
        # 在实际应用中，这里应该初始化实时语音识别会话
        # 目前我们只是创建一个会话记录
        recognition_sessions[session_id] = {
            "started_at": asyncio.get_event_loop().time(),
            "status": "active"
        }
        
        return {"id": session_id}
        
    except Exception as e:
        logger.error(f"启动语音识别会话失败: {str(e)}")
        raise HTTPException(status_code=500, detail="内部服务器错误")

# 语音识别会话接口 - 停止
@router.post("/stop", responses={400: {"model": ErrorResponse}, 500: {"model": ErrorResponse}})
async def stop_voice_recognition(request: Request):
    """
    停止语音识别会话并获取识别结果
    
    请求体参数:
    - **sessionId**: 会话ID
    
    返回:
    - **text**: 识别的文本
    """
    try:
        # 从请求体中获取sessionId
        body = await request.json()
        session_id = body.get("sessionId")
        
        if not session_id:
            raise HTTPException(status_code=400, detail="缺少sessionId参数")
        
        logger.info(f"停止语音识别会话: {session_id}")
        
        # 检查会话是否存在
        if session_id not in recognition_sessions:
            raise HTTPException(status_code=400, detail="无效的会话ID")
        
        # 更新会话状态
        recognition_sessions[session_id]["status"] = "completed"
        recognition_sessions[session_id]["completed_at"] = asyncio.get_event_loop().time()
        
        # 在实际应用中，这里应该获取实时语音识别的结果
        # 目前我们返回一个模拟的识别结果
        # 注意：在实际部署时，应该使用真实的语音识别功能
        simulated_text = "介绍下以自己"
        
        logger.info(f"语音识别会话完成，结果: {simulated_text}")
        
        return {"text": simulated_text}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"停止语音识别会话失败: {str(e)}")
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