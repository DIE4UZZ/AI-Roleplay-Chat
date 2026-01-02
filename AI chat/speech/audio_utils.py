import pyaudio
import wave
import os
import io
import numpy as np
from typing import Optional, Tuple
import logging
from config import env_config

logger = logging.getLogger("ai_chat_service.speech.audio_utils")

class AudioUtils:
    """音频处理工具类"""
    
    @staticmethod
    def record_audio(
        duration: int = 5, 
        output_file: str = None,
        sample_rate: int = None,
        channels: int = None,
        chunk_size: int = None
    ) -> Tuple[Optional[bytes], Optional[str]]:
        """
        录制音频
        
        参数:
            duration: 录制时长（秒）
            output_file: 输出文件路径，如果为None则只返回字节数据
            sample_rate: 采样率，如果为None则使用配置值
            channels: 声道数，如果为None则使用配置值
            chunk_size: 块大小，如果为None则使用配置值
        
        返回:
            (音频字节数据, 错误信息)
        """
        try:
            # 使用配置值或默认值
            sample_rate = sample_rate or env_config.AUDIO_SAMPLE_RATE
            channels = channels or env_config.AUDIO_CHANNELS
            chunk_size = chunk_size or env_config.AUDIO_CHUNK_SIZE
            
            audio_format = pyaudio.paInt16
            
            logger.info(f"开始录制音频，时长: {duration}秒")
            
            # 初始化PyAudio
            p = pyaudio.PyAudio()
            
            # 打开音频流
            stream = p.open(
                format=audio_format,
                channels=channels,
                rate=sample_rate,
                input=True,
                frames_per_buffer=chunk_size
            )
            
            # 录制音频
            frames = []
            for i in range(0, int(sample_rate / chunk_size * duration)):
                data = stream.read(chunk_size)
                frames.append(data)
            
            # 停止录制
            stream.stop_stream()
            stream.close()
            p.terminate()
            
            logger.info(f"音频录制完成，共录制 {len(frames)} 帧")
            
            # 合并音频数据
            audio_bytes = b''.join(frames)
            
            # 如果指定了输出文件，保存到文件
            if output_file:
                # 确保目录存在
                os.makedirs(os.path.dirname(output_file), exist_ok=True)
                
                wf = wave.open(output_file, 'wb')
                wf.setnchannels(channels)
                wf.setsampwidth(p.get_sample_size(audio_format))
                wf.setframerate(sample_rate)
                wf.writeframes(audio_bytes)
                wf.close()
                
                logger.info(f"音频文件保存成功: {output_file}")
            
            return audio_bytes, None
            
        except Exception as e:
            error = f"音频录制失败: {str(e)}"
            logger.error(error)
            return None, error
    
    @staticmethod
    def save_wav(audio_bytes: bytes, output_file: str, sample_rate: int = None, channels: int = None) -> Tuple[bool, Optional[str]]:
        """
        将音频字节数据保存为WAV文件
        
        参数:
            audio_bytes: 音频字节数据
            output_file: 输出文件路径
            sample_rate: 采样率
            channels: 声道数
        
        返回:
            (是否成功, 错误信息)
        """
        try:
            # 使用配置值或默认值
            sample_rate = sample_rate or env_config.AUDIO_SAMPLE_RATE
            channels = channels or env_config.AUDIO_CHANNELS
            
            # 检查输出文件路径
            output_dir = os.path.dirname(output_file)
            
            # 只有当目录不为空时才创建目录
            if output_dir:
                # 确保目录存在
                os.makedirs(output_dir, exist_ok=True)
            
            wf = wave.open(output_file, 'wb')
            wf.setnchannels(channels)
            wf.setsampwidth(2)  # 16位
            wf.setframerate(sample_rate)
            wf.writeframes(audio_bytes)
            wf.close()
            
            logger.info(f"WAV文件保存成功: {output_file}")
            return True, None
            
        except Exception as e:
            error = f"WAV文件保存失败: {str(e)}"
            logger.error(error)
            return False, error
    
    @staticmethod
    def read_wav(file_path: str) -> Tuple[Optional[bytes], Optional[dict], Optional[str]]:
        """
        读取WAV文件
        
        参数:
            file_path: 文件路径
        
        返回:
            (音频字节数据, 音频信息, 错误信息)
        """
        try:
            wf = wave.open(file_path, 'rb')
            
            # 获取音频信息
            audio_info = {
                'nchannels': wf.getnchannels(),
                'sampwidth': wf.getsampwidth(),
                'framerate': wf.getframerate(),
                'nframes': wf.getnframes(),
                'comptype': wf.getcomptype(),
                'compname': wf.getcompname()
            }
            
            # 读取音频数据
            audio_bytes = wf.readframes(audio_info['nframes'])
            wf.close()
            
            logger.info(f"WAV文件读取成功: {file_path}")
            return audio_bytes, audio_info, None
            
        except Exception as e:
            error = f"WAV文件读取失败: {str(e)}"
            logger.error(error)
            return None, None, error
    
    @staticmethod
    def bytes_to_numpy(audio_bytes: bytes, dtype=np.int16) -> np.ndarray:
        """
        将音频字节数据转换为NumPy数组
        
        参数:
            audio_bytes: 音频字节数据
            dtype: 数据类型
        
        返回:
            NumPy数组
        """
        return np.frombuffer(audio_bytes, dtype=dtype)
    
    @staticmethod
    def numpy_to_bytes(audio_array: np.ndarray) -> bytes:
        """
        将NumPy数组转换为音频字节数据
        
        参数:
            audio_array: NumPy数组
        
        返回:
            音频字节数据
        """
        return audio_array.tobytes()

# 创建全局实例
audio_utils = AudioUtils()