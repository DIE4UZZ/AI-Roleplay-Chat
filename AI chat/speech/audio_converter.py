"""
音频格式转换工具类
支持WebM、MP3、WAV等音频格式之间的相互转换
特别优化WebM到WAV的转换，确保适合TTS处理
"""

import os
import tempfile
import logging
from typing import Optional, Tuple, Union
from pathlib import Path
import io

try:
    from pydub import AudioSegment
    from pydub.utils import mediainfo
    PYDUB_AVAILABLE = True
except ImportError:
    PYDUB_AVAILABLE = False
    logging.warning("pydub未安装，音频格式转换功能将不可用")

from config import env_config

logger = logging.getLogger("ai_chat_service.speech.audio_converter")

class AudioConverter:
    """音频格式转换器"""
    
    def __init__(self):
        """初始化转换器"""
        if not PYDUB_AVAILABLE:
            raise ImportError("pydub未安装，请运行: pip install pydub")
        
        # 设置ffmpeg路径（如果需要）
        self._setup_ffmpeg()
        
        # 支持的音频格式
        self.supported_formats = {
            'webm': ['audio/webm', 'video/webm'],
            'mp3': ['audio/mpeg', 'audio/mp3'],
            'wav': ['audio/wav', 'audio/x-wav'],
            'ogg': ['audio/ogg'],
            'flac': ['audio/flac'],
            'm4a': ['audio/mp4', 'audio/m4a']
        }
        
        logger.info("音频格式转换器初始化完成")
    
    def _setup_ffmpeg(self):
        """设置ffmpeg配置"""
        try:
            # 尝试使用pydub创建一个测试音频来检查ffmpeg
            test_audio = AudioSegment.empty()
            if test_audio:
                logger.info("pydub和ffmpeg配置正常")
        except Exception as e:
            logger.warning(f"ffmpeg配置可能存在问题: {e}")
            # 在Windows上，我们仍然可以尝试使用pydub的基本功能
    
    def webm_to_wav(
        self, 
        input_data: Union[bytes, str], 
        output_path: Optional[str] = None,
        sample_rate: Optional[int] = None,
        channels: Optional[int] = None
    ) -> Tuple[Optional[str], Optional[str]]:
        """
        将WebM格式转换为WAV格式
        
        参数:
            input_data: WebM文件路径或字节数据
            output_path: 输出文件路径，如果为None则生成临时文件
            sample_rate: 目标采样率，如果为None则使用源文件采样率
            channels: 目标声道数，1为单声道，2为立体声，None为保持原声道数
        
        返回:
            (输出文件路径, 错误信息)
        """
        try:
            logger.info("开始WebM到WAV转换")
            
            # 确定输出路径
            if output_path is None:
                fd, temp_path = tempfile.mkstemp(suffix='.wav')
                os.close(fd)
                output_path = temp_path
            else:
                # 确保输出目录存在
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # 如果输入是字节数据，转换为临时文件
            input_file_path = None
            if isinstance(input_data, bytes):
                fd, input_file_path = tempfile.mkstemp(suffix='.webm')
                os.close(fd)
                with open(input_file_path, 'wb') as f:
                    f.write(input_data)
                input_data = input_file_path
            
            logger.info(f"正在转换文件: {input_data}")
            
            # 首先尝试使用pydub直接处理
            try:
                # 读取WebM文件
                audio = AudioSegment.from_file(input_data, format="webm")
                logger.info(f"WebM文件读取成功，原始参数: 采样率={audio.frame_rate}Hz, 声道数={audio.channels}, 时长={len(audio)/1000:.2f}秒")
            except Exception as e:
                # 如果直接webm格式失败，尝试自动检测
                logger.warning(f"使用webm格式读取失败，尝试自动检测格式: {e}")
                try:
                    audio = AudioSegment.from_file(input_data)
                    logger.info(f"自动检测格式成功，原始参数: 采样率={audio.frame_rate}Hz, 声道数={audio.channels}")
                except Exception as e2:
                    raise Exception(f"无法读取音频文件: {e2}")
            
            # 应用音频处理参数
            processed_audio = self._process_audio_for_tts(
                audio, 
                target_sample_rate=sample_rate or env_config.AUDIO_SAMPLE_RATE,
                target_channels=channels or env_config.AUDIO_CHANNELS
            )
            
            # 导出为WAV格式
            processed_audio.export(
                output_path, 
                format="wav",
                parameters=["-acodec", "pcm_s16le"]  # 确保使用标准PCM编码
            )
            
            logger.info(f"WAV文件导出成功: {output_path}")
            logger.info(f"转换后参数: 采样率={processed_audio.frame_rate}Hz, 声道数={processed_audio.channels}, 时长={len(processed_audio)/1000:.2f}秒")
            
            return output_path, None
            
        except Exception as e:
            error = f"WebM到WAV转换失败: {str(e)}"
            logger.error(error)
            logger.exception("转换异常详细信息")
            return None, error
        
        finally:
            # 清理临时输入文件
            if input_file_path and os.path.exists(input_file_path):
                try:
                    os.remove(input_file_path)
                except:
                    pass
    
    def any_to_wav(
        self, 
        input_data: Union[bytes, str], 
        input_format: Optional[str] = None,
        output_path: Optional[str] = None,
        sample_rate: Optional[int] = None,
        channels: Optional[int] = None
    ) -> Tuple[Optional[str], Optional[str]]:
        """
        将任意音频格式转换为WAV格式
        
        参数:
            input_data: 输入音频文件路径或字节数据
            input_format: 输入格式（webm, mp3, wav等），如果为None则自动检测
            output_path: 输出文件路径，如果为None则生成临时文件
            sample_rate: 目标采样率
            channels: 目标声道数
        
        返回:
            (输出文件路径, 错误信息)
        """
        try:
            logger.info(f"开始音频格式转换，源格式: {input_format or '自动检测'}")
            
            # 确定输出路径
            if output_path is None:
                fd, temp_path = tempfile.mkstemp(suffix='.wav')
                os.close(fd)
                output_path = temp_path
            else:
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # 如果输入是字节数据，转换为临时文件
            input_file_path = None
            if isinstance(input_data, bytes):
                # 根据输入格式确定临时文件扩展名
                ext = f".{input_format}" if input_format else ".tmp"
                fd, input_file_path = tempfile.mkstemp(suffix=ext)
                os.close(fd)
                with open(input_file_path, 'wb') as f:
                    f.write(input_data)
                input_data = input_file_path
            
            # 读取音频文件
            try:
                if input_format:
                    logger.info(f"使用指定格式读取: {input_format}")
                    audio = AudioSegment.from_file(input_data, format=input_format)
                else:
                    logger.info("自动检测音频格式")
                    audio = AudioSegment.from_file(input_data)
                
                # 获取音频信息
                info = mediainfo(input_data)
                logger.info(f"音频文件信息: {info}")
                
            except Exception as e:
                raise Exception(f"无法读取音频文件: {str(e)}")
            
            # 应用音频处理参数
            processed_audio = self._process_audio_for_tts(
                audio, 
                target_sample_rate=sample_rate or env_config.AUDIO_SAMPLE_RATE,
                target_channels=channels or env_config.AUDIO_CHANNELS
            )
            
            # 导出为WAV格式
            processed_audio.export(
                output_path, 
                format="wav",
                parameters=["-acodec", "pcm_s16le"]
            )
            
            logger.info(f"音频转换成功: {output_path}")
            return output_path, None
            
        except Exception as e:
            error = f"音频格式转换失败: {str(e)}"
            logger.error(error)
            return None, error
        
        finally:
            # 清理临时文件
            if input_file_path and os.path.exists(input_file_path):
                try:
                    os.remove(input_file_path)
                except:
                    pass
    
    def wav_to_webm(
        self, 
        input_data: Union[bytes, str], 
        output_path: Optional[str] = None,
        quality: str = "medium"
    ) -> Tuple[Optional[str], Optional[str]]:
        """
        将WAV格式转换为WebM格式
        
        参数:
            input_data: WAV文件路径或字节数据
            output_path: 输出文件路径，如果为None则生成临时文件
            quality: 压缩质量 (low, medium, high)
        
        返回:
            (输出文件路径, 错误信息)
        """
        try:
            logger.info("开始WAV到WebM转换")
            
            # 确定输出路径
            if output_path is None:
                fd, temp_path = tempfile.mkstemp(suffix='.webm')
                os.close(fd)
                output_path = temp_path
            else:
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # 如果输入是字节数据，转换为临时文件
            input_file_path = None
            if isinstance(input_data, bytes):
                fd, input_file_path = tempfile.mkstemp(suffix='.wav')
                os.close(fd)
                with open(input_file_path, 'wb') as f:
                    f.write(input_data)
                input_data = input_file_path
            
            # 读取WAV文件
            audio = AudioSegment.from_file(input_data, format="wav")
            logger.info(f"WAV文件读取成功，参数: 采样率={audio.frame_rate}Hz, 声道数={audio.channels}")
            
            # 根据质量设置导出参数
            quality_settings = {
                "low": {"bitrate": "64k"},
                "medium": {"bitrate": "128k"},
                "high": {"bitrate": "192k"}
            }
            
            export_params = quality_settings.get(quality, quality_settings["medium"])
            
            # 导出为WebM格式
            audio.export(
                output_path, 
                format="webm",
                codec="libvorbis",
                bitrate=export_params["bitrate"]
            )
            
            logger.info(f"WebM文件导出成功: {output_path}")
            return output_path, None
            
        except Exception as e:
            error = f"WAV到WebM转换失败: {str(e)}"
            logger.error(error)
            return None, error
        
        finally:
            if input_file_path and os.path.exists(input_file_path):
                try:
                    os.remove(input_file_path)
                except:
                    pass
    
    def _process_audio_for_tts(self, audio: AudioSegment, target_sample_rate: int, target_channels: int) -> AudioSegment:
        """
        处理音频以适合TTS处理
        
        参数:
            audio: 输入音频
            target_sample_rate: 目标采样率
            target_channels: 目标声道数
        
        返回:
            处理后的音频
        """
        try:
            logger.info(f"开始音频预处理，目标参数: 采样率={target_sample_rate}Hz, 声道数={target_channels}")
            
            # 1. 标准化声道数
            if target_channels == 1 and audio.channels > 1:
                audio = audio.set_channels(1)
                logger.info("音频转换为单声道")
            elif target_channels == 2 and audio.channels == 1:
                audio = audio.set_channels(2)
                logger.info("音频转换为立体声")
            
            # 2. 标准化采样率
            if audio.frame_rate != target_sample_rate:
                audio = audio.set_frame_rate(target_sample_rate)
                logger.info(f"采样率转换为 {target_sample_rate}Hz")
            
            # 3. 音量标准化（避免过大或过小的音量）
            # 计算RMS音量
            rms = audio.rms
            if rms == 0:
                logger.warning("音频文件音量过小，可能为空或损坏")
                return audio
            
            # 标准化音量到合适范围
            target_rms = 1000  # 目标RMS音量
            if abs(rms - target_rms) > 300:  # 如果音量差异较大
                volume_change = target_rms - rms
                if volume_change > 0:
                    # 放大音量
                    audio = audio + (volume_change / 1000.0)
                else:
                    # 降低音量
                    audio = audio + (volume_change / 1000.0)
                logger.info(f"音量标准化完成，原始RMS={rms}, 目标RMS={target_rms}")
            
            # 4. 添加轻微的淡入淡出以避免点击声
            fade_duration = min(50, len(audio) // 10)  # 淡入淡出时长（毫秒）
            audio = audio.fade_in(fade_duration).fade_out(fade_duration)
            logger.info(f"添加淡入淡出效果，时长={fade_duration}毫秒")
            
            logger.info("音频预处理完成")
            return audio
            
        except Exception as e:
            logger.warning(f"音频预处理部分失败，返回原始音频: {e}")
            return audio
    
    def convert_bytes_to_wav(
        self, 
        audio_bytes: bytes, 
        original_filename: str,
        output_path: Optional[str] = None,
        sample_rate: Optional[int] = None,
        channels: Optional[int] = None
    ) -> Tuple[Optional[str], Optional[str]]:
        """
        将音频字节数据转换为WAV格式
        
        参数:
            audio_bytes: 音频字节数据
            original_filename: 原始文件名（用于检测格式）
            output_path: 输出文件路径
            sample_rate: 目标采样率
            channels: 目标声道数
        
        返回:
            (输出文件路径, 错误信息)
        """
        try:
            # 根据文件扩展名确定输入格式
            file_ext = Path(original_filename).suffix.lower().lstrip('.')
            format_mapping = {
                'webm': 'webm',
                'mp3': 'mp3', 
                'wav': 'wav',
                'ogg': 'ogg',
                'flac': 'flac',
                'm4a': 'mp4'
            }
            
            input_format = format_mapping.get(file_ext)
            
            # 使用any_to_wav方法转换
            return self.any_to_wav(
                input_data=audio_bytes,
                input_format=input_format,
                output_path=output_path,
                sample_rate=sample_rate,
                channels=channels
            )
            
        except Exception as e:
            error = f"字节数据转换失败: {str(e)}"
            logger.error(error)
            return None, error
    
    def get_audio_info(self, audio_path: str) -> Optional[dict]:
        """
        获取音频文件信息
        
        参数:
            audio_path: 音频文件路径
        
        返回:
            音频信息字典，如果失败则返回None
        """
        try:
            info = mediainfo(audio_path)
            
            # 格式化信息
            formatted_info = {
                'format': info.get('format_name', 'unknown'),
                'duration': float(info.get('duration', 0)),
                'sample_rate': int(info.get('sample_rate', 0)),
                'channels': int(info.get('channels', 0)),
                'bit_rate': info.get('bit_rate', 'unknown'),
                'codec': info.get('codec_name', 'unknown')
            }
            
            logger.info(f"音频文件信息: {formatted_info}")
            return formatted_info
            
        except Exception as e:
            logger.error(f"获取音频信息失败: {e}")
            return None

# 创建全局实例
audio_converter = AudioConverter()