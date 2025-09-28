from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional

class LLMBase(ABC):
    """LLM模型的基础接口类"""
    
    @abstractmethod
    def generate_response(
        self, 
        prompt: str, 
        character_context: Dict[str, Any] = None,
        chat_history: List[Dict[str, str]] = None,
        **kwargs
    ) -> str:
        """
        生成模型响应
        
        参数:
            prompt: 用户输入的提示文本
            character_context: 角色上下文信息
            chat_history: 聊天历史记录
            **kwargs: 其他参数
        
        返回:
            模型生成的响应文本
        """
        pass
    
    @abstractmethod
    def generate_streaming_response(
        self, 
        prompt: str, 
        character_context: Dict[str, Any] = None,
        chat_history: List[Dict[str, str]] = None,
        **kwargs
    ):
        """
        生成流式响应
        
        参数:
            prompt: 用户输入的提示文本
            character_context: 角色上下文信息
            chat_history: 聊天历史记录
            **kwargs: 其他参数
        
        返回:
            流式响应生成器
        """
        pass
    
    @staticmethod
    def create_prompt(
        prompt: str, 
        character_context: Dict[str, Any] = None,
        chat_history: List[Dict[str, str]] = None
    ) -> str:
        """
        构建完整的提示文本
        
        参数:
            prompt: 用户输入的提示文本
            character_context: 角色上下文信息
            chat_history: 聊天历史记录
        
        返回:
            构建好的完整提示文本
        """
        full_prompt = []
        
        # 添加角色上下文
        if character_context:
            name = character_context.get('name', 'AI')
            description = character_context.get('description', '')
            
            system_prompt = f"你是{name}。"
            if description:
                system_prompt += f" {description}"
            
            full_prompt.append(system_prompt)
        
        # 添加聊天历史
        if chat_history:
            for message in chat_history:
                role = message.get('role', 'user')
                content = message.get('content', '')
                
                if role == 'user':
                    full_prompt.append(f"用户: {content}")
                else:
                    full_prompt.append(f"{name}: {content}")
        
        # 添加当前用户输入
        full_prompt.append(f"用户: {prompt}")
        full_prompt.append(f"{name}:")
        
        return '\n'.join(full_prompt)