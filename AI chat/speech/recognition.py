import speech_recognition as sr
import pyaudio
import wave
import io
import tempfile
import os
import hashlib
import logging
from config import env_config
from typing import Optional, Tuple
from speech.audio_converter import audio_converter

logger = logging.getLogger("ai_chat_service.speech.recognition")

class SpeechRecognizer:
    """语音识别类，用于将语音转换为文本"""
    
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.language = env_config.SPEECH_RECOGNITION_LANGUAGE
        
        # 优化识别器配置以提高准确性
        self.recognizer.energy_threshold = 400  # 稍微提高以减少噪音干扰
        self.recognizer.dynamic_energy_threshold = True  # 动态调整阈值
        self.recognizer.pause_threshold = 1.0  # 增加暂停阈值，适应不同语速
        self.recognizer.phrase_threshold = 0.3  # 短语识别阈值
        self.recognizer.non_speaking_duration = 0.5  # 静音检测
        
        # 添加识别超时限制
        self.recognition_timeout = 10
        
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
                logger.info(f"当前能量阈值: {self.recognizer.energy_threshold}")
                logger.info("请说话...")
                
                audio_data = self.recognizer.listen(source, timeout=timeout)
                logger.info(f"录制音频长度: {len(audio_data.get_raw_data())} 字节")
                logger.info("正在识别语音...")
                
                # 使用Google的语音识别服务
                try:
                    text = self.recognizer.recognize_google(audio_data, language=self.language)
                    logger.info(f"识别成功，置信度较高")
                except sr.UnknownValueError:
                    logger.warning("Google语音识别无法理解音频，尝试备用识别")
                    text = self.recognizer.recognize_sphinx(audio_data, language=self.language)
                except sr.RequestError as e:
                    logger.error(f"Google语音识别服务错误: {e}")
                    return None, f"识别服务错误: {str(e)}"
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
    
    def recognize_from_audio_file(self, file_path: str, auto_convert: bool = True) -> Tuple[Optional[str], Optional[str]]:
        """
        从音频文件识别语音
        
        参数:
            file_path: 音频文件路径
            auto_convert: 是否自动转换音频格式（默认为True）
        
        返回:
            (识别的文本, 错误信息)
        """
        try:
            # 检查是否需要格式转换
            actual_file_path = file_path
            file_extension = os.path.splitext(file_path)[1].lower()
            
            if auto_convert and file_extension in ('.webm', '.mp3', '.ogg', '.flac', '.m4a'):
                logger.info(f"检测到需要格式转换的音频文件: {file_path} (格式: {file_extension})")
                converted_path, error = audio_converter.webm_to_wav(file_path)
                if converted_path:
                    actual_file_path = converted_path
                    logger.info(f"音频格式转换成功: {actual_file_path}")
                else:
                    logger.error(f"音频格式转换失败，使用原始文件: {error}")
            
            # 检查文件是否存在
            if not os.path.exists(actual_file_path):
                error = f"音频文件不存在: {actual_file_path}"
                logger.error(error)
                return None, error
            
            # 检查文件大小
            file_size = os.path.getsize(actual_file_path)
            logger.info(f"音频文件大小: {file_size} 字节")
            
            if file_size < 1000:  # 小于1KB的音频文件可能无法识别
                logger.warning(f"音频文件过小 ({file_size} 字节)，可能识别效果不佳")
            
            try:
                with sr.AudioFile(actual_file_path) as source:
                    logger.info(f"正在识别音频文件: {actual_file_path}")
                    audio_data = self.recognizer.record(source)
                    logger.info(f"读取音频数据长度: {len(audio_data.get_raw_data())} 字节")
                    
                    # 使用Google的语音识别服务
                    try:
                        text = self.recognizer.recognize_google(audio_data, language=self.language)
                        logger.info(f"语音识别成功: {text}")
                    except sr.UnknownValueError:
                        logger.warning("Google语音识别无法理解音频，尝试备用识别")
                        text = self.recognizer.recognize_sphinx(audio_data)
                        logger.info(f"备用识别结果: {text}")
                    except sr.RequestError as e:
                        logger.error(f"语音识别服务错误: {e}")
                        return None, f"识别服务错误: {str(e)}"
                    
                    return text, None
            except Exception as e:
                error = f"音频文件读取失败: {str(e)}"
                logger.error(error)
                return None, error
                
        except Exception as e:
            error = f"从文件识别语音出错: {str(e)}"
            logger.error(error)
            return None, error
    
    def recognize_from_audio_bytes(
        self, 
        audio_bytes: bytes, 
        original_filename: str = "audio.unknown",
        auto_convert: bool = True
    ) -> Tuple[Optional[str], Optional[str]]:
        """
        从音频字节数据识别语音
        
        参数:
            audio_bytes: 音频字节数据
            original_filename: 原始文件名（用于检测格式）
            auto_convert: 是否自动转换音频格式（默认为True）
        
        返回:
            (识别的文本, 错误信息)
        """
        try:
            # 检查是否需要格式转换
            actual_audio_bytes = audio_bytes
            converted_file_path = None
            
            if auto_convert and any(file_ext in original_filename.lower() for file_ext in ['.webm', '.mp3', '.ogg', '.flac', '.m4a']):
                logger.info(f"检测到需要格式转换的音频文件: {original_filename}")
                converted_file_path, error = audio_converter.convert_bytes_to_wav(
                    audio_bytes=audio_bytes,
                    original_filename=original_filename,
                    sample_rate=env_config.AUDIO_SAMPLE_RATE,
                    channels=env_config.AUDIO_CHANNELS
                )
                
                if converted_file_path:
                    logger.info(f"音频格式转换成功: {converted_file_path}")
                    # 读取转换后的文件
                    try:
                        with open(converted_file_path, 'rb') as f:
                            actual_audio_bytes = f.read()
                    except Exception as e:
                        logger.error(f"读取转换后的文件失败: {e}")
                        logger.info("使用原始音频数据")
                        actual_audio_bytes = audio_bytes
                else:
                    logger.error(f"音频格式转换失败，使用原始数据: {error}")
            
            # 将字节数据转换为AudioFile对象
            audio_file = io.BytesIO(actual_audio_bytes)
            with sr.AudioFile(audio_file) as source:
                logger.info(f"正在识别音频字节数据，文件名: {original_filename}")
                audio_data = self.recognizer.record(source)
                text = self.recognizer.recognize_google(audio_data, language=self.language)
                logger.info(f"语音识别成功: {text}")
                return text, None
                
        except Exception as e:
            error = f"从字节数据识别语音出错: {str(e)}"
            logger.error(error)
            return None, error
        
        finally:
            # 清理临时转换文件
            if converted_file_path and converted_file_path.startswith(tempfile.gettempdir()):
                try:
                    import os
                    if os.path.exists(converted_file_path):
                        os.remove(converted_file_path)
                        logger.info(f"清理临时转换文件: {converted_file_path}")
                except Exception as e:
                    logger.warning(f"清理临时文件失败: {e}")

# 创建全局实例
speech_recognizer = SpeechRecognizer()