import speech_recognition as sr
import pyaudio
import wave
import io
import logging
from config import env_config
from typing import Optional, Tuple

logger = logging.getLogger("ai_chat_service.speech.recognition")

class SpeechRecognizer:
    """语音识别类，用于将语音转换为文本"""
    
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.language = env_config.SPEECH_RECOGNITION_LANGUAGE
        
        # 配置 recognizer
        self.recognizer.energy_threshold = 300  # 调整麦克风灵敏度
        self.recognizer.dynamic_energy_threshold = True
        
    def recognize_from_microphone(self, timeout: int = 10) -> Tuple[Optional[str], Optional[str]]:
        """
        从麦克风识别语音
        
        参数:
            timeout: 超时时间（秒）
        
        返回:
            (识别的文本, 错误信息) 如果识别成功，错误信息为None；否则，文本为None
        """
        try:
            with sr.Microphone() as source:
                logger.info("正在调整麦克风以适应环境噪音...")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                logger.info("请说话...")
                
                audio_data = self.recognizer.listen(source, timeout=timeout)
                logger.info("正在识别语音...")
                
                # 使用Google的语音识别服务
                text = self.recognizer.recognize_google(audio_data, language=self.language)
                logger.info(f"识别结果: {text}")
                return text, None
                
        except sr.WaitTimeoutError:
            error = "识别超时，请重试"
            logger.error(error)
            return None, error
        except sr.UnknownValueError:
            error = "无法识别语音，请清晰说话"
            logger.error(error)
            return None, error
        except sr.RequestError as e:
            error = f"无法连接到语音识别服务: {str(e)}"
            logger.error(error)
            return None, error
        except Exception as e:
            error = f"语音识别出错: {str(e)}"
            logger.error(error)
            return None, error
    
    def recognize_from_audio_file(self, file_path: str) -> Tuple[Optional[str], Optional[str]]:
        """
        从音频文件识别语音
        
        参数:
            file_path: 音频文件路径
        
        返回:
            (识别的文本, 错误信息)
        """
        try:
            with sr.AudioFile(file_path) as source:
                audio_data = self.recognizer.record(source)
                text = self.recognizer.recognize_google(audio_data, language=self.language)
                return text, None
                
        except Exception as e:
            error = f"从文件识别语音出错: {str(e)}"
            logger.error(error)
            return None, error
    
    def recognize_from_audio_bytes(self, audio_bytes: bytes) -> Tuple[Optional[str], Optional[str]]:
        """
        从音频字节数据识别语音
        
        参数:
            audio_bytes: 音频字节数据
        
        返回:
            (识别的文本, 错误信息)
        """
        try:
            # 将字节数据转换为AudioFile对象
            audio_file = io.BytesIO(audio_bytes)
            with sr.AudioFile(audio_file) as source:
                audio_data = self.recognizer.record(source)
                text = self.recognizer.recognize_google(audio_data, language=self.language)
                return text, None
                
        except Exception as e:
            error = f"从字节数据识别语音出错: {str(e)}"
            logger.error(error)
            return None, error

# 创建全局实例
speech_recognizer = SpeechRecognizer()