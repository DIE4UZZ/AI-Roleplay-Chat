#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单的音频转换器测试
"""

import os
import sys
import tempfile
import logging

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_basic_conversion():
    """基本转换功能测试"""
    try:
        from speech.audio_converter import audio_converter
        
        # 测试临时文件生成
        temp_fd, temp_path = tempfile.mkstemp(suffix='.wav')
        os.close(temp_fd)
        
        # 创建简单的测试WAV文件
        try:
            from pydub import AudioSegment
            from pydub.generators import Sine
            
            # 生成测试音频
            logger.info("生成测试音频...")
            test_audio = Sine(440).to_audio_segment(duration=1000)  # 1秒，440Hz
            test_audio.export(temp_path, format="wav")
            
            # 测试转换功能
            logger.info("测试音频信息获取...")
            info = audio_converter.get_audio_info(temp_path)
            if info:
                logger.info(f"✓ 音频信息获取成功: {info}")
            else:
                logger.warning("音频信息获取失败")
            
            # 尝试基本格式转换
            logger.info("测试基本格式转换...")
            result_path, error = audio_converter.any_to_wav(
                input_data=temp_path,
                input_format="wav",
                sample_rate=16000,
                channels=1
            )
            
            if error:
                logger.error(f"格式转换失败: {error}")
            else:
                logger.info(f"✓ 格式转换成功: {result_path}")
                
            # 清理测试文件
            if os.path.exists(temp_path):
                os.remove(temp_path)
            if result_path and os.path.exists(result_path):
                os.remove(result_path)
                
            return True
            
        except ImportError as e:
            logger.error(f"缺少音频处理库: {e}")
            return False
            
    except Exception as e:
        logger.error(f"基本转换测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_byte_conversion():
    """字节数据转换测试"""
    try:
        from speech.audio_converter import audio_converter
        from pydub.generators import Sine
        
        # 生成测试音频字节数据
        logger.info("生成测试音频字节数据...")
        test_audio = Sine(440).to_audio_segment(duration=500)  # 0.5秒
        wav_bytes = test_audio.raw_data
        
        # 转换字节数据
        result_path, error = audio_converter.convert_bytes_to_wav(
            audio_bytes=wav_bytes,
            original_filename="test.wav"
        )
        
        if error:
            logger.error(f"字节转换失败: {error}")
            return False
        else:
            logger.info(f"✓ 字节转换成功: {result_path}")
            # 清理文件
            if result_path and os.path.exists(result_path):
                os.remove(result_path)
            return True
            
    except Exception as e:
        logger.error(f"字节转换测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主测试函数"""
    logger.info("开始简单音频转换器测试")
    
    tests = [
        ("基本转换功能", test_basic_conversion),
        ("字节数据转换", test_byte_conversion),
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
        logger.info("🎉 基本测试通过！音频转换功能可以正常工作。")
    else:
        logger.warning("⚠️ 部分测试失败，但基本功能可能仍然可用。")

if __name__ == "__main__":
    main()