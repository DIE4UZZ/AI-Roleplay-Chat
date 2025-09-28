from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from typing import List, Dict, Any, Optional
from fastapi.responses import StreamingResponse
import logging

# 导入数据模型
from api.models import (
    ChatRequest, 
    ChatResponse, 
    Message, 
    CharacterContext,
    ErrorResponse
)



# 导入LLM模型
from llm.openai_llm import OpenAILLM
from llm.deeplseek_llm import DeepSeekLLM
from config import env_config

# 创建路由实例
router = APIRouter()

# 配置日志
logger = logging.getLogger("ai_chat_service.api.chat")

# 模型管理器
class ModelManager:
    """管理不同的LLM模型实例"""
    _instance = None
    _models = {}
    
    @classmethod
    def get_model(cls, provider: str = None, model_name: str = None):
        """获取指定的模型实例"""
        # 如果没有提供提供商，使用默认值
        provider = provider or env_config.DEFAULT_LLM_PROVIDER
        model_key = f"{provider}:{model_name}" if model_name else provider
        
        # 如果模型实例不存在，创建一个
        if model_key not in cls._models:
            if provider == 'openai':
                cls._models[model_key] = OpenAILLM()
            # 可以在这里添加其他模型提供商的实现
            elif provider == 'deepseek':
                cls._models[model_key] = DeepSeekLLM()
            # elif provider == 'ollama':
            #     cls._models[model_key] = OllamaLLM(model_name=model_name)
            # elif provider == 'anthropic':
            #     cls._models[model_key] = AnthropicLLM(model_name=model_name)
            else:
                raise ValueError(f"不支持的模型提供商: {provider}")
        
        return cls._models[model_key]

# 处理聊天请求
@router.post("/send", response_model=ChatResponse, responses={400: {"model": ErrorResponse}, 500: {"model": ErrorResponse}})
async def send_chat_message(request: ChatRequest):
    """
    发送聊天消息并获取AI回复
    
    - **prompt**: 用户输入的消息文本
    - **character_id**: 角色ID（可选）
    - **character_context**: 角色上下文信息（可选）
    - **chat_history**: 聊天历史记录（可选）
    - **stream**: 是否使用流式响应（可选，默认为False）
    - **model_provider**: 模型提供商（可选）
    - **model_name**: 模型名称（可选）
    
    响应：
    - **reply**: AI的回复文本
    - **character_id**: 角色ID
    - **timestamp**: 时间戳
    - **model_provider**: 使用的模型提供商
    - **model_name**: 使用的模型名称
    """
    try:
        logger.info(f"接收到聊天请求，角色ID: {request.character_id}")
        
        # 如果使用流式响应
        if request.stream:
            # 流式响应需要特殊处理
            # 注意：FastAPI的流式响应需要使用异步生成器
            # 由于时间限制，这里暂时不实现完整的流式响应
            raise HTTPException(status_code=400, detail="流式响应暂未实现")
        
        # 获取模型实例
        model = ModelManager.get_model(request.model_provider, request.model_name)
        provider = request.model_provider or env_config.DEFAULT_LLM_PROVIDER
        model_name = request.model_name or getattr(env_config, f"{provider.upper()}_MODEL", "default")
        
        # 调用模型生成响应
        reply = model.generate_response(
            prompt=request.prompt,
            character_context=request.character_context.dict() if request.character_context else None,
            chat_history=request.chat_history
        )
        
        logger.info(f"聊天请求处理完成，回复长度: {len(reply)} 字符")
        
        # 返回响应
        return ChatResponse(
            reply=reply,
            character_id=request.character_id,
            model_provider=provider,
            model_name=model_name
        )
        
    except ValueError as e:
        logger.error(f"模型错误: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"聊天请求处理失败: {str(e)}")
        raise HTTPException(status_code=500, detail="内部服务器错误")

# 流式聊天接口（暂时不实现）
@router.post("/stream")
async def stream_chat_message(request: ChatRequest):
    """
    流式获取AI回复（暂未实现）
    """
    raise HTTPException(status_code=400, detail="流式响应暂未实现")

# 为了兼容前端现有的API调用（/chat/send）
@router.post("/send/legacy", response_model=ChatResponse)
async def legacy_send_chat_message(characterId: int = None, message: str = None, prompt: str = None):
    """
    兼容前端现有调用的聊天接口
    
    这是为了兼容前端现有的API调用格式，通过查询参数传递
    调用格式：POST /api/chat/send/legacy?characterId=1&message=Hello
    """
    # 确定使用的消息内容
    text = message or prompt
    if not text:
        raise HTTPException(status_code=400, detail="消息内容不能为空")
    
    # 构建请求对象
    chat_request = ChatRequest(
        prompt=text,
        character_id=characterId
    )
    
    # 调用主聊天接口
    return await send_chat_message(chat_request)

# 创建一个单独的角色聊天接口，专门处理前端通过请求体发送的角色聊天请求
@router.post("/character/send", response_model=ChatResponse)
async def character_chat_message(request: dict):
    """
    角色聊天接口，处理前端发送的角色聊天请求
    
    前端调用格式：POST /api/chat/character/send { characterId, message }
    """
    # 从请求体中获取数据
    character_id = request.get('characterId')
    message = request.get('message')
    
    if not message:
        raise HTTPException(status_code=400, detail="消息内容不能为空")
    
    # 构建请求对象
    chat_request = ChatRequest(
        prompt=message,
        character_id=character_id
    )
    
    # 调用主聊天接口
    return await send_chat_message(chat_request)

# 获取聊天历史（模拟实现）
@router.get("/history/{character_id}", response_model=List[Message])
async def get_chat_history(character_id: int):
    """
    获取与指定角色的聊天历史
    
    - **character_id**: 角色ID
    """
    # 注意：实际应用中应该从数据库或其他存储中获取历史记录
    # 这里仅返回模拟数据
    logger.info(f"获取角色 {character_id} 的聊天历史")
    
    # 模拟历史记录（实际应该从数据库获取）
    return []

# 清除聊天历史（模拟实现）
@router.delete("/history/{character_id}")
async def clear_chat_history(character_id: int):
    """
    清除与指定角色的聊天历史
    
    - **character_id**: 角色ID
    """
    # 注意：实际应用中应该从数据库或其他存储中删除历史记录
    logger.info(f"清除角色 {character_id} 的聊天历史")
    
    return {"status": "success", "message": "聊天历史已清除"}