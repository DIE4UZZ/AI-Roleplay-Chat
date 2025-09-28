import logging
import os
import tempfile
from typing import Optional, Tuple

import requests
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play

from config import env_config

logger = logging.getLogger("ai_chat_service.speech.tts")

class TextToSpeech:
    """文本转语音类，用于将文本转换为语音"""
    
    def __init__(self):
        # 基本配置
        self.lang = env_config.TTS_LANG
        self.slow = env_config.TTS_SLOW
        
        # API配置
        self.tts_engine = env_config.TTS_ENGINE or "gtts"  # gtts 或 api
        self.api_key = env_config.TTS_API_KEY
        self.api_base_url = env_config.TTS_BASE_URL
        self.api_backup_base_url = env_config.TTS_BACKUP_BASE_URL
        self.api_model = env_config.TTS_MODEL
        
        logger.info(f"初始化TTS引擎: {self.tts_engine}")
        logger.info(f"TTS API配置 - 基础URL: {self.api_base_url}, 模型: {self.api_model}")
        
        # 初始化API客户端
        if self.tts_engine == "api" and not self.api_key:
            logger.warning("TTS API密钥未配置，自动切换到gTTS")
            self.tts_engine = "gtts"
    
    def text_to_speech(self, text: str, save_path: str = None) -> Tuple[Optional[str], Optional[str]]:
        """
        将文本转换为语音并保存为文件
        
        参数:
            text: 要转换的文本
            save_path: 保存路径，如果为None则生成临时文件
        
        返回:
            (音频文件路径, 错误信息) 如果转换成功，错误信息为None；否则，文件路径为None
        """
        try:
            logger.info(f"正在将文本转换为语音，文本长度: {len(text)} 字符，引擎: {self.tts_engine}")
            
            # 确定保存路径
            if save_path is None:
                # 创建临时文件
                fd, temp_path = tempfile.mkstemp(suffix='.mp3')
                os.close(fd)
                save_path = temp_path
            else:
                # 确保目录存在
                os.makedirs(os.path.dirname(save_path), exist_ok=True)
            
            # 优先使用API，但如果API不可用，确保gTTS能工作
            if self.tts_engine == "api" and self.api_key:
                # 使用API转换
                success = self._text_to_speech_api(text, save_path)
                if success:
                    logger.info(f"语音文件保存成功(API): {save_path}")
                    return save_path, None
                else:
                    # API失败，回退到gTTS
                    logger.warning("TTS API调用失败，回退到gTTS")
                    
            # 强制使用gTTS作为备选
            logger.info(f"使用gTTS转换文本，语言: {self.lang}, 语速: {'慢速' if self.slow else '正常'}")
            tts = gTTS(text=text, lang=self.lang, slow=self.slow)
            tts.save(save_path)
            logger.info(f"语音文件保存成功(gTTS): {save_path}")
            
            return save_path, None
            
        except Exception as e:
            error = f"文本转语音失败: {str(e)}"
            logger.error(error)
            logger.exception("文本转语音异常详细信息")
            # 清理临时文件
            if save_path and os.path.exists(save_path):
                try:
                    os.remove(save_path)
                except:
                    pass
            return None, error
    
    def _text_to_speech_api(self, text: str, save_path: str) -> bool:
        """
        使用TTS API将文本转换为语音
        
        参数:
            text: 要转换的文本
            save_path: 保存路径
            
        返回:
            是否成功
        """
        try:
            # 构建请求参数
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            # 尝试不同的参数格式
            request_bodies = [
                # 格式1: 用户提供的七牛TTS API格式
                {
                    "audio": {
                        "voice_type": "zh_male_M392_conversation_wvae_bigtts",
                        "encoding": "mp3",
                        "speed_ratio": 1.0
                    },
                    "request": {
                        "text": text
                    }
                },
                # 格式2: 标准OpenAI格式
                {
                    "model": self.api_model,
                    "input": text,
                    "voice": "female",
                    "response_format": "mp3",
                    "speed": 1.0
                },
                # 格式3: 可能的DeepSeek TTS格式
                {
                    "text": text,
                    "model": self.api_model
                },
                # 格式4: 简化版参数
                {
                    "text": text
                }
            ]
            
            # 尝试不同的API端点格式
            base_urls = [self.api_base_url, self.api_backup_base_url]
            endpoint_paths = [
                "/voice/tts",  # 用户提供的七牛API端点
                "/audio/speech",
                "/speech/generate",
                "/tts/generate",
                "/tts",
                "/api/tts",
                "/api/speech"
            ]
            
            # 生成所有可能的API URL组合
            api_urls = []
            for base in base_urls:
                for path in endpoint_paths:
                    api_urls.append(base + path)
            
            # 去重
            api_urls = list(set(api_urls))
            logger.info(f"尝试所有可能的API URL组合，共{len(api_urls)}个URL")
            
            # 尝试所有URL和参数组合
            for url in api_urls:
                for request_body in request_bodies:
                    try:
                        logger.info(f"尝试调用TTS API: {url}，参数格式: {list(request_body.keys())}")
                        
                        # 发送请求
                        response = requests.post(
                            url,
                            headers=headers,
                            json=request_body,
                            timeout=30
                        )
                        
                        # 检查响应状态
                        if response.status_code == 200:
                            logger.info(f"TTS API调用成功: {url}")
                            
                            # 保存音频文件
                            with open(save_path, 'wb') as f:
                                f.write(response.content)
                            
                            return True
                        else:
                            status_code = response.status_code
                            logger.warning(f"TTS API调用失败({url}): {status_code} - {response.reason}")
                            try:
                                error_detail = response.json()
                                logger.warning(f"API错误详情: {error_detail}")
                            except:
                                logger.warning(f"API错误响应: {response.text}")
                        
                    except requests.exceptions.RequestException as e:
                        status_code = e.response.status_code if hasattr(e, 'response') and e.response else 'N/A'
                        logger.warning(f"TTS API调用异常({url}): {status_code} - {str(e)}")
                        if hasattr(e, 'response') and e.response is not None:
                            try:
                                error_detail = e.response.json()
                                logger.warning(f"API错误详情: {error_detail}")
                            except:
                                logger.warning(f"API错误响应: {e.response.text}")
                        
                        # 继续尝试下一个组合
                        continue
            
            # 所有组合都尝试失败
            logger.error(f"所有TTS API调用组合都失败，共尝试了{len(api_urls) * len(request_bodies)}种组合")
            logger.error(f"请检查TTS API配置是否正确: 基础URL={self.api_base_url}, 模型={self.api_model}")
            return False
            
        except Exception as e:
            logger.error(f"TTS API处理异常: {str(e)}")
            logger.exception("TTS API异常详细信息")
            return False
    
    def text_to_speech_bytes(self, text: str) -> Tuple[Optional[bytes], Optional[str]]:
        """
        将文本转换为语音并返回字节数据
        
        参数:
            text: 要转换的文本
        
        返回:
            (音频字节数据, 错误信息)
        """
        try:
            logger.info(f"正在将文本转换为语音字节数据，文本长度: {len(text)} 字符，引擎: {self.tts_engine}")
            
            # 创建临时文件
            fd, temp_path = tempfile.mkstemp(suffix='.mp3')
            os.close(fd)
            
            try:
                # 使用text_to_speech方法转换
                result, error = self.text_to_speech(text, temp_path)
                
                if result:
                    # 读取文件内容为字节数据
                    with open(temp_path, 'rb') as f:
                        audio_bytes = f.read()
                    logger.info(f"成功获取语音字节数据，大小: {len(audio_bytes)} 字节")
                    return audio_bytes, None
                else:
                    return None, error
            finally:
                # 清理临时文件
                if os.path.exists(temp_path):
                    try:
                        os.remove(temp_path)
                    except:
                        pass
            
        except Exception as e:
            error = f"文本转语音（字节数据）失败: {str(e)}"
            logger.error(error)
            logger.exception("文本转语音字节数据异常详细信息")
            return None, error
    
    def _text_to_speech_bytes_api(self, text: str) -> Optional[bytes]:
        """
        使用TTS API将文本转换为语音字节数据
        
        参数:
            text: 要转换的文本
            
        返回:
            音频字节数据，如果失败则返回None
        """
        try:
            # 构建请求参数
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            # 尝试不同的参数格式
            request_bodies = [
                # 格式1: 用户提供的七牛TTS API格式
                {
                    "audio": {
                        "voice_type": "zh_male_M392_conversation_wvae_bigtts",
                        "encoding": "mp3",
                        "speed_ratio": 1.0
                    },
                    "request": {
                        "text": text
                    }
                },
                # 格式2: 标准OpenAI格式
                {
                    "model": self.api_model,
                    "input": text,
                    "voice": "female",
                    "response_format": "mp3",
                    "speed": 1.0
                },
                # 格式3: 可能的DeepSeek TTS格式
                {
                    "text": text,
                    "model": self.api_model
                },
                # 格式4: 简化版参数
                {
                    "text": text
                }
            ]
            
            # 尝试不同的API端点格式
            base_urls = [self.api_base_url, self.api_backup_base_url]
            endpoint_paths = [
                "/voice/tts",  # 用户提供的七牛API端点
                "/audio/speech",
                "/speech/generate",
                "/tts/generate",
                "/tts",
                "/api/tts",
                "/api/speech"
            ]
            
            # 生成所有可能的API URL组合
            api_urls = []
            for base in base_urls:
                for path in endpoint_paths:
                    api_urls.append(base + path)
            
            # 去重
            api_urls = list(set(api_urls))
            
            # 尝试所有URL和参数组合
            for url in api_urls:
                for request_body in request_bodies:
                    try:
                        logger.info(f"尝试调用TTS API: {url}，参数格式: {list(request_body.keys())}")
                        
                        # 发送请求
                        response = requests.post(
                            url,
                            headers=headers,
                            json=request_body,
                            timeout=30
                        )
                        
                        # 检查响应状态
                        if response.status_code == 200:
                            logger.info(f"TTS API调用成功: {url}")
                            return response.content
                        else:
                            status_code = response.status_code
                            logger.warning(f"TTS API调用失败({url}): {status_code} - {response.reason}")
                            try:
                                error_detail = response.json()
                                logger.warning(f"API错误详情: {error_detail}")
                            except:
                                logger.warning(f"API错误响应: {response.text}")
                        
                    except requests.exceptions.RequestException as e:
                        status_code = e.response.status_code if hasattr(e, 'response') and e.response else 'N/A'
                        logger.warning(f"TTS API调用异常({url}): {status_code} - {str(e)}")
                        if hasattr(e, 'response') and e.response is not None:
                            try:
                                error_detail = e.response.json()
                                logger.warning(f"API错误详情: {error_detail}")
                            except:
                                logger.warning(f"API错误响应: {e.response.text}")
                        
                        # 继续尝试下一个组合
                        continue
            
            # 所有组合都尝试失败
            logger.error(f"所有TTS API调用组合都失败")
            return None
            
        except Exception as e:
            logger.error(f"TTS API处理异常: {str(e)}")
            return None
    
    def speak(self, text: str) -> Tuple[bool, Optional[str]]:
        """
        将文本转换为语音并播放
        
        参数:
            text: 要转换的文本
        
        返回:
            (是否成功, 错误信息)
        """
        try:
            # 创建临时文件
            fd, temp_path = tempfile.mkstemp(suffix='.mp3')
            os.close(fd)
            
            try:
                # 使用text_to_speech方法转换，该方法会自动选择引擎
                result, error = self.text_to_speech(text, temp_path)
                
                if result:
                    # 播放语音
                    logger.info("正在播放语音...")
                    audio = AudioSegment.from_mp3(temp_path)
                    play(audio)
                    return True, None
                else:
                    return False, error
                    
            finally:
                # 清理临时文件
                if os.path.exists(temp_path):
                    try:
                        os.remove(temp_path)
                    except:
                        pass
                        
        except Exception as e:
            error = f"语音播放失败: {str(e)}"
            logger.error(error)
            return False, error

# 创建全局实例
tts_engine = TextToSpeech()