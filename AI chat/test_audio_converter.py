#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
音频转换器测试文件

该文件测试AudioConverter类的各项功能：
1. WebM到WAV转换
2. 多格式到WAV转换
3. WAV到WebM转换
4. 音频预处理功能
5. 错误处理机制
"""

import os
import sys
import tempfile
import logging
from pathlib import Path
from pydub import AudioSegment
from pydub.generators import Sine

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from speech.audio_converter import audio_converter
from config import env_config

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_test_audio(sample_rate=16000, duration=2, frequency=440):
    """创建测试用的音频文件"""
    # 使用pydub生成正弦波
    frames = int(sample_rate * duration)
    sine_wave = Sine(frequency).to_audio_segment(duration=duration * 1000)
    return sine_wave

def test_wav_to_wav():
    """测试WAV到WAV转换（应该是透明处理）"""
    logger.info("=== 测试 WAV 到 WAV 转换 ===")
    
    try:
        # 创建临时WAV文件
        temp_dir = tempfile.mkdtemp()
        wav_path = os.path.join(temp_dir, "test_input.wav")
        
        # 生成测试音频
        audio = create_test_audio()
        audio.export(wav_path, format="wav")
        
        # 转换为WAV
        result_path, error = audio_converter.webm_to_wav(wav_path)
        
        if error:
            logger.error(f"WAV转换失败: {error}")
            return False
        
        # 验证输出文件
        if os.path.exists(result_path):
            logger.info(f"✓ WAV转换成功: {result_path}")
            
            # 检查音频信息
            output_audio = AudioSegment.from_wav(result_path)
            logger.info(f"输出音频信息: 采样率={output_audio.frame_rate}, 声道数={output_audio.channels}")
            
            return True
        else:
            logger.error("转换后的文件不存在")
            return False
            
    except Exception as e:
        logger.error(f"WAV转换测试异常: {str(e)}")
        return False

def test_webm_to_wav():
    """测试WebM到WAV转换"""
    logger.info("=== 测试 WebM 到 WAV 转换 ===")
    
    try:
        temp_dir = tempfile.mkdtemp()
        
        # 创建临时WebM文件
        webm_path = os.path.join(temp_dir, "test_input.webm")
        audio = create_test_audio()
        audio.export(webm_path, format="webm")
        
        # 转换为WAV
        result_path, error = audio_converter.webm_to_wav(webm_path)
        
        if error:
            logger.error(f"WebM转换失败: {error}")
            return False
        
        # 验证输出文件
        if os.path.exists(result_path):
            logger.info(f"✓ WebM转换成功: {result_path}")
            return True
        else:
            logger.error("转换后的文件不存在")
            return False
            
    except Exception as e:
        logger.error(f"WebM转换测试异常: {str(e)}")
        return False

def test_bytes_conversion():
    """测试字节数据转换"""
    logger.info("=== 测试字节数据转换 ===")
    
    try:
        # 生成测试音频字节数据
        audio = create_test_audio()
        wav_bytes = audio.raw_data
        
        # 转换为WAV字节数据
        result_path, error = audio_converter.convert_bytes_to_wav(
            audio_bytes=wav_bytes,
            original_filename="test.wav"
        )
        
        if error:
            logger.error(f"字节转换失败: {error}")
            return False
        
        if os.path.exists(result_path):
            logger.info(f"✓ 字节转换成功: {result_path}")
            return True
        else:
            logger.error("字节转换后的文件不存在")
            return False
            
    except Exception as e:
        logger.error(f"字节转换测试异常: {str(e)}")
        return False

def test_wav_to_webm():
    """测试WAV到WebM转换"""
    logger.info("=== 测试 WAV 到 WebM 转换 ===")
    
    try:
        temp_dir = tempfile.mkdtemp()
        wav_path = os.path.join(temp_dir, "test_input.wav")
        
        # 创建测试WAV文件
        audio = create_test_audio()
        audio.export(wav_path, format="wav")
        
        # 转换为WebM
        result_path, error = audio_converter.wav_to_webm(wav_path, quality="medium")
        
        if error:
            logger.error(f"WAV到WebM转换失败: {error}")
            return False
        
        if os.path.exists(result_path):
            logger.info(f"✓ WAV到WebM转换成功: {result_path}")
            return True
        else:
            logger.error("WAV到WebM转换后的文件不存在")
            return False
            
    except Exception as e:
        logger.error(f"WAV到WebM转换测试异常: {str(e)}")
        return False

def test_audio_preprocessing():
    """测试音频预处理功能"""
    logger.info("=== 测试音频预处理功能 ===")
    
    try:
        temp_dir = tempfile.mkdtemp()
        input_path = os.path.join(temp_dir, "test_input.wav")
        
        # 创建测试音频（立体声，高采样率）
        audio = create_test_audio(sample_rate=44100)
        stereo_audio = audio.set_channels(2)
        stereo_audio.export(input_path, format="wav")
        
        # 预处理为单声道，低采样率
        processed_path, error = audio_converter.webm_to_wav(
            input_path,
            target_sample_rate=16000,
            target_channels=1
        )
        
        if error:
            logger.error(f"音频预处理失败: {error}")
            return False
        
        if os.path.exists(processed_path):
            processed_audio = AudioSegment.from_wav(processed_path)
            
            # 验证预处理结果
            if processed_audio.channels == 1 and processed_audio.frame_rate == 16000:
                logger.info(f"✓ 音频预处理成功: {processed_path}")
                logger.info(f"原始: 立体声, 44100Hz -> 处理后: 单声道, 16000Hz")
                return True
            else:
                logger.error(f"音频预处理参数不正确: 声道数={processed_audio.channels}, 采样率={processed_audio.frame_rate}")
                return False
        else:
            logger.error("预处理后的文件不存在")
            return False
            
    except Exception as e:
        logger.error(f"音频预处理测试异常: {str(e)}")
        return False

def test_error_handling():
    """测试错误处理"""
    logger.info("=== 测试错误处理 ===")
    
    try:
        # 测试不存在的文件
        result_path, error = audio_converter.webm_to_wav("/nonexistent/file.webm")
        
        if error:
            logger.info(f"✓ 正确处理了不存在的文件: {error}")
        else:
            logger.error("应该检测到不存在的文件但没有")
            return False
        
        # 测试无效的音频字节数据
        invalid_bytes = b"this is not audio data"
        result_path, error = audio_converter.convert_bytes_to_wav(
            audio_bytes=invalid_bytes,
            original_filename="invalid.webm"
        )
        
        if error:
            logger.info(f"✓ 正确处理了无效音频数据: {error}")
        else:
            logger.error("应该检测到无效音频数据但没有")
            return False
        
        return True
        
    except Exception as e:
        logger.error(f"错误处理测试异常: {str(e)}")
        return False

def main():
    """主测试函数"""
    logger.info("开始音频转换器测试")
    logger.info(f"当前配置: 采样率={env_config.AUDIO_SAMPLE_RATE}, 声道数={env_config.AUDIO_CHANNELS}")
    
    # 运行所有测试
    tests = [
        ("WAV到WAV转换", test_wav_to_wav),
        ("WebM到WAV转换", test_webm_to_wav),
        ("字节数据转换", test_bytes_conversion),
        ("WAV到WebM转换", test_wav_to_webm),
        ("音频预处理", test_audio_preprocessing),
        ("错误处理", test_error_handling)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        logger.info(f"\n运行测试: {test_name}")
        try:
            if test_func():
                passed += 1
                logger.info(f"✓ {test_name} 测试通过")
            else:
                logger.error(f"✗ {test_name} 测试失败")
        except Exception as e:
            logger.error(f"✗ {test_name} 测试异常: {str(e)}")
    
    # 输出测试结果
    logger.info(f"\n=== 测试结果 ===")
    logger.info(f"通过: {passed}/{total}")
    logger.info(f"成功率: {(passed/total)*100:.1f}%")
    
    if passed == total:
        logger.info("🎉 所有测试通过！音频转换功能正常工作。")
    else:
        logger.warning("⚠️ 部分测试失败，请检查相关功能。")

if __name__ == "__main__":
    main()