from typing import List, Dict, Any, Optional, Generator
import openai
from openai import OpenAI
from llm.base import LLMBase
from config import env_config
import logging

logger = logging.getLogger("ai_chat_service.llm.openai")

class OpenAILLM(LLMBase):
    """OpenAI模型的实现"""
    
    def __init__(self):
        # 初始化OpenAI客户端
        if env_config.OPENAI_API_KEY:
            self.client = OpenAI(api_key=env_config.OPENAI_API_KEY)
        else:
            # 如果没有API密钥，尝试使用环境变量或默认配置
            self.client = OpenAI()
            
        self.model = env_config.OPENAI_MODEL
        self.temperature = env_config.OPENAI_TEMPERATURE
        
    def generate_response(
        self, 
        prompt: str, 
        character_context: Dict[str, Any] = None,
        chat_history: List[Dict[str, str]] = None,
        **kwargs
    ) -> str:
        """
        生成OpenAI模型的响应
        """
        try:
            # 构建messages格式
            messages = []
            
            # 添加系统消息（角色上下文）
            if character_context:
                system_content = f"你是{character_context.get('name', 'AI')}"
                if 'description' in character_context:
                    system_content += f": {character_context['description']}"
                messages.append({"role": "system", "content": system_content})
            
            # 添加聊天历史
            if chat_history:
                for message in chat_history:
                    role = message.get('role', 'user')
                    content = message.get('content', '')
                    messages.append({"role": role, "content": content})
            
            # 添加用户消息
            messages.append({"role": "user", "content": prompt})
            
            # 调用OpenAI API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                **kwargs
            )
            
            # 返回生成的文本
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"OpenAI API调用失败: {str(e)}")
            raise
    
    def generate_streaming_response(
        self, 
        prompt: str, 
        character_context: Dict[str, Any] = None,
        chat_history: List[Dict[str, str]] = None,
        **kwargs
    ) -> Generator[str, None, None]:
        """
        生成OpenAI模型的流式响应
        """
        try:
            # 构建messages格式
            messages = []
            
            # 添加系统消息（角色上下文）
            if character_context:
                system_content = f"你是{character_context.get('name', 'AI')}"
                if 'description' in character_context:
                    system_content += f": {character_context['description']}"
                messages.append({"role": "system", "content": system_content})
            
            # 添加聊天历史
            if chat_history:
                for message in chat_history:
                    role = message.get('role', 'user')
                    content = message.get('content', '')
                    messages.append({"role": role, "content": content})
            
            # 添加用户消息
            messages.append({"role": "user", "content": prompt})
            
            # 调用OpenAI API的流式响应
            stream = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                stream=True,
                **kwargs
            )
            
            # 流式返回生成的文本
            for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    yield chunk.choices[0].delta.content
                    
        except Exception as e:
            logger.error(f"OpenAI流式API调用失败: {str(e)}")
            raise