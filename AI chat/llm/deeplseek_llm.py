from typing import List, Dict, Any, Optional, Generator
import requests
from llm.base import LLMBase
from config import env_config
import logging
import json

logger = logging.getLogger("ai_chat_service.llm.deeplseek")

class DeepSeekLLM(LLMBase):
    """DeepSeek模型的实现"""
    
    def __init__(self):
        # 初始化DeepSeek配置
        self.api_key = env_config.DEEPSEEK_API_KEY
        self.model = env_config.DEEPSEEK_MODEL
        self.temperature = env_config.DEEPSEEK_TEMPERATURE
        self.api_base_url = env_config.DEEPSEEK_BASE_URL + "/chat/completions"
        self.backup_api_base_url = env_config.DEEPSEEK_BACKUP_BASE_URL + "/chat/completions"
        
        if not self.api_key:
            logger.error("DeepSeek API密钥未配置")
            raise ValueError("DeepSeek API密钥未配置")
            
    def generate_response(
        self, 
        prompt: str, 
        character_context: Dict[str, Any] = None,
        chat_history: List[Dict[str, str]] = None,
        **kwargs
    ) -> str:
        """
        生成DeepSeek模型的响应
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
            
            # 构建请求体
            request_body = {
                "model": self.model,
                "messages": messages,
                "temperature": self.temperature,
                **kwargs
            }
            
            # 设置请求头
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            # 调用DeepSeek API，带备用URL重试逻辑
            response = None
            api_urls = [self.api_base_url, self.backup_api_base_url]
            
            for url in api_urls:
                try:
                    logger.info(f"尝试调用DeepSeek API: {url}")
                    response = requests.post(
                        url,
                        headers=headers,
                        json=request_body,
                        timeout=30
                    )
                    
                    # 检查响应状态
                    response.raise_for_status()
                    logger.info(f"DeepSeek API调用成功: {url}")
                    break
                except requests.exceptions.RequestException as e:
                    logger.warning(f"DeepSeek API调用失败({url}): {str(e)}")
                    if url == api_urls[-1]:  # 如果是最后一个URL，抛出异常
                        raise
            
            # 解析响应
            response_json = response.json()
            
            # 返回生成的文本
            return response_json["choices"][0]["message"]["content"]
            
        except requests.exceptions.RequestException as e:
            logger.error(f"DeepSeek API调用失败: {str(e)}")
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_data = e.response.json()
                    logger.error(f"错误详情: {json.dumps(error_data)}")
                except:
                    logger.error(f"响应内容: {e.response.text}")
            raise
        except Exception as e:
            logger.error(f"DeepSeek模型处理异常: {str(e)}")
            raise
    
    def generate_streaming_response(
        self, 
        prompt: str, 
        character_context: Dict[str, Any] = None,
        chat_history: List[Dict[str, str]] = None,
        **kwargs
    ) -> Generator[str, None, None]:
        """
        生成DeepSeek模型的流式响应
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
            
            # 构建请求体（启用流式）
            request_body = {
                "model": self.model,
                "messages": messages,
                "temperature": self.temperature,
                "stream": True,
                **kwargs
            }
            
            # 设置请求头
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            # 调用DeepSeek API的流式响应，带备用URL重试逻辑
            response = None
            api_urls = [self.api_base_url, self.backup_api_base_url]
            
            for url in api_urls:
                try:
                    logger.info(f"尝试调用DeepSeek流式API: {url}")
                    response = requests.post(
                        url,
                        headers=headers,
                        json=request_body,
                        stream=True,
                        timeout=30
                    )
                    
                    # 检查响应状态
                    response.raise_for_status()
                    logger.info(f"DeepSeek流式API调用成功: {url}")
                    break
                except requests.exceptions.RequestException as e:
                    logger.warning(f"DeepSeek流式API调用失败({url}): {str(e)}")
                    if url == api_urls[-1]:  # 如果是最后一个URL，抛出异常
                        raise
            
            with response:
                
                # 处理流式响应
                for line in response.iter_lines():
                    if line:
                        # 移除前缀 "data: "
                        line = line.decode('utf-8')
                        if line.startswith('data: '):
                            line = line[6:]
                            
                        # 检查是否为结束标志
                        if line == '[DONE]':
                            break
                        
                        try:
                            # 解析JSON
                            chunk = json.loads(line)
                            
                            # 提取内容
                            if ('choices' in chunk and 
                                chunk['choices'] and 
                                'delta' in chunk['choices'][0] and 
                                'content' in chunk['choices'][0]['delta']):
                                
                                content = chunk['choices'][0]['delta']['content']
                                if content:
                                    yield content
                        except json.JSONDecodeError:
                            logger.warning(f"无法解析流式响应: {line}")
                            continue
                            
        except requests.exceptions.RequestException as e:
            logger.error(f"DeepSeek流式API调用失败: {str(e)}")
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_data = e.response.json()
                    logger.error(f"错误详情: {json.dumps(error_data)}")
                except:
                    logger.error(f"响应内容: {e.response.text}")
            raise
        except Exception as e:
            logger.error(f"DeepSeek模型流式处理异常: {str(e)}")
            raise