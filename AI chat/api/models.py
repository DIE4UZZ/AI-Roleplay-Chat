from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
from datetime import datetime

class CharacterContext(BaseModel):
    """角色上下文信息"""
    name: str = Field(..., description="角色名称")
    description: str = Field("", description="角色描述")
    avatar: str = Field("🎭", description="角色头像")
    category: str = Field("", description="角色分类")
    other_info: Optional[Dict[str, Any]] = Field(None, description="其他信息")

class Message(BaseModel):
    """聊天消息"""
    id: Optional[int] = Field(None, description="消息ID")
    text: str = Field(..., description="消息文本")
    sender: str = Field("user", description="发送者", pattern="^(user|ai)$")
    timestamp: Optional[datetime] = Field(default_factory=datetime.now, description="时间戳")

class ChatRequest(BaseModel):
    """聊天请求"""
    prompt: str = Field(..., description="用户输入的提示文本")
    character_id: Optional[int] = Field(None, description="角色ID")
    character_context: Optional[CharacterContext] = Field(None, description="角色上下文")
    chat_history: Optional[List[Dict[str, str]]] = Field(None, description="聊天历史")
    stream: bool = Field(False, description="是否使用流式响应")
    model_provider: Optional[str] = Field(None, description="模型提供商")
    model_name: Optional[str] = Field(None, description="模型名称")

class ChatResponse(BaseModel):
    """聊天响应"""
    reply: str = Field(..., description="AI的回复")
    character_id: Optional[int] = Field(None, description="角色ID")
    timestamp: datetime = Field(default_factory=datetime.now, description="时间戳")
    model_provider: str = Field(..., description="使用的模型提供商")
    model_name: str = Field(..., description="使用的模型名称")

class SpeechRecognitionRequest(BaseModel):
    """语音识别请求"""
    # 注意：实际的音频数据通常通过multipart/form-data上传
    # 这里只定义元数据
    language: str = Field("zh-CN", description="语言代码")
    sample_rate: int = Field(16000, description="采样率")

class SpeechRecognitionResponse(BaseModel):
    """语音识别响应"""
    text: str = Field(..., description="识别的文本")
    confidence: Optional[float] = Field(None, description="置信度")
    language: str = Field("zh-CN", description="使用的语言代码")

class TTSRequest(BaseModel):
    """文本转语音请求"""
    text: str = Field(..., description="要转换的文本")
    language: str = Field("zh-cn", description="语言代码")
    slow: bool = Field(False, description="是否使用慢速语音")

class TTSResponse(BaseModel):
    """文本转语音响应"""
    audio_url: Optional[str] = Field(None, description="音频文件URL")
    # 注意：实际的音频数据通常通过HTTP响应的二进制数据返回
    # 这里只定义元数据
    language: str = Field("zh-cn", description="使用的语言代码")
    duration: Optional[float] = Field(None, description="音频时长（秒）")

class VoiceChatRequest(BaseModel):
    """语音聊天请求（结合语音识别和TTS）"""
    # 音频数据通过multipart/form-data上传
    character_id: Optional[int] = Field(None, description="角色ID")
    character_context: Optional[CharacterContext] = Field(None, description="角色上下文")
    language: str = Field("zh-CN", description="语言代码")
    sample_rate: int = Field(16000, description="采样率")

class ErrorResponse(BaseModel):
    """错误响应"""
    error: str = Field(..., description="错误信息")
    code: int = Field(..., description="错误代码")
    details: Optional[str] = Field(None, description="错误详情")