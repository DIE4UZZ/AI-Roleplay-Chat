#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
语音识别调试工具
用于诊断和测试语音识别功能，解决识别结果重复的问题
"""

import os
import sys
import time
import hashlib
import tempfile
from typing import Optional, Tuple

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from speech.recognition import speech_recognizer
from speech.audio_utils import audio_utils
from speech.audio_converter import audio_converter
from config import env_config
from utils.logger import get_logger

# 创建日志器
logger = get_logger("ai_chat_service.speech_debug")

def generate_test_audio_files():
    """生成测试音频文件"""
    logger.info("=== 生成测试音频文件 ===")
    
    test_files = {}
    
    try:
        # 录制3个不同的音频文件
        for i in range(1, 4):
            logger.info(f"开始录制测试音频 {i}，请说出不同的内容...")
            
            # 录制5秒音频
            audio_bytes, error = audio_utils.record_audio(duration=5)
            
            if error:
                logger.error(f"录制音频 {i} 失败: {error}")
                continue
            
            # 保存为WAV文件
            wav_file = f"test_audio_{i}.wav"
            success, save_error = audio_utils.save_wav(audio_bytes, wav_file)
            
            if success:
                # 计算音频内容的哈希值
                audio_hash = hashlib.md5(audio_bytes).hexdigest()
                test_files[wav_file] = {
                    'hash': audio_hash,
                    'size': len(audio_bytes)
                }
                logger.info(f"测试音频 {i} 保存成功: {wav_file} (哈希: {audio_hash[:8]}..., 大小: {len(audio_bytes)} 字节)")
            else:
                logger.error(f"保存音频 {i} 失败: {save_error}")
        
        return test_files
        
    except Exception as e:
        logger.error(f"生成测试音频失败: {str(e)}")
        return {}

def test_recognition_consistency(test_files: dict):
    """测试识别一致性"""
    logger.info("=== 测试识别一致性 ===")
    
    results = {}
    
    for filename, file_info in test_files.items():
        logger.info(f"\n--- 测试文件: {filename} ---")
        
        try:
            # 测试文件识别
            text, error = speech_recognizer.recognize_from_audio_file(filename)
            
            if error:
                logger.error(f"识别错误: {error}")
                results[filename] = {
                    'text': None,
                    'error': error,
                    'hash': file_info['hash'],
                    'size': file_info['size']
                }
            else:
                logger.info(f"识别结果: {text}")
                results[filename] = {
                    'text': text,
                    'error': None,
                    'hash': file_info['hash'],
                    'size': file_info['size']
                }
                
        except Exception as e:
            logger.error(f"处理文件 {filename} 时出错: {str(e)}")
            results[filename] = {
                'text': None,
                'error': str(e),
                'hash': file_info['hash'],
                'size': file_info['size']
            }
    
    return results

def analyze_results(test_results: dict):
    """分析测试结果"""
    logger.info("=== 分析测试结果 ===")
    
    # 检查是否所有识别结果都相同
    recognized_texts = []
    errors = []
    
    for filename, result in test_results.items():
        if result['error']:
            errors.append((filename, result['error']))
        else:
            recognized_texts.append(result['text'])
    
    # 分析结果
    if len(recognized_texts) == 0:
        logger.warning("没有成功的识别结果")
        return
    elif len(set(recognized_texts)) == 1:
        logger.warning(f"⚠️  所有识别结果都相同: '{recognized_texts[0]}'")
        logger.warning("这可能表明:")
        logger.warning("1. 麦克风录音有问题")
        logger.warning("2. 环境噪音干扰")
        logger.warning("3. 语音识别服务缓存问题")
        logger.warning("4. 音频处理配置不当")
    elif len(set(recognized_texts)) < len(recognized_texts):
        logger.warning("⚠️  识别结果有重复")
        for i, text in enumerate(recognized_texts):
            count = recognized_texts.count(text)
            if count > 1:
                logger.warning(f"  '{text}' 出现了 {count} 次")
    else:
        logger.info("✅ 识别结果多样，语音识别功能正常")
    
    # 输出详细信息
    logger.info("\n--- 详细结果 ---")
    for filename, result in test_results.items():
        logger.info(f"文件: {filename}")
        logger.info(f"  哈希: {result['hash'][:8]}...")
        logger.info(f"  大小: {result['size']} 字节")
        if result['error']:
            logger.info(f"  错误: {result['error']}")
        else:
            logger.info(f"  识别: '{result['text']}'")
        logger.info("")

def test_audio_conversion():
    """测试音频转换功能"""
    logger.info("=== 测试音频转换功能 ===")
    
    try:
        # 生成一个测试WebM文件
        from pydub import AudioSegment
        from pydub.generators import Sine
        
        # 生成500Hz的正弦波，持续2秒
        audio = Sine(500).to_audio_segment(duration=2000)
        
        # 导出为WebM格式
        webm_file = "test_audio.webm"
        audio.export(webm_file, format="webm")
        logger.info(f"生成测试WebM文件: {webm_file}")
        
        # 测试转换为WAV
        wav_file, error = audio_converter.webm_to_wav(webm_file)
        
        if error:
            logger.error(f"WebM到WAV转换失败: {error}")
            return False
        else:
            logger.info(f"WebM到WAV转换成功: {wav_file}")
            return True
            
    except Exception as e:
        logger.error(f"音频转换测试失败: {str(e)}")
        return False

def check_system_configuration():
    """检查系统配置"""
    logger.info("=== 检查系统配置 ===")
    
    # 检查语音识别配置
    logger.info(f"识别语言: {speech_recognizer.language}")
    logger.info(f"能量阈值: {speech_recognizer.recognizer.energy_threshold}")
    logger.info(f"动态能量阈值: {speech_recognizer.recognizer.dynamic_energy_threshold}")
    logger.info(f"暂停阈值: {speech_recognizer.recognizer.pause_threshold}")
    
    # 检查音频配置
    logger.info(f"采样率: {env_config.AUDIO_SAMPLE_RATE}")
    logger.info(f"声道数: {env_config.AUDIO_CHANNELS}")
    
    # 检查依赖库
    try:
        import speech_recognition as sr
        logger.info("✅ speech_recognition 库正常")
    except ImportError:
        logger.error("❌ speech_recognition 库未安装")
    
    try:
        import pyaudio
        logger.info("✅ pyaudio 库正常")
    except ImportError:
        logger.error("❌ pyaudio 库未安装")
    
    try:
        import pydub
        logger.info("✅ pydub 库正常")
    except ImportError:
        logger.error("❌ pydub 库未安装")

def main():
    """主测试函数"""
    logger.info("开始语音识别调试测试...")
    
    try:
        # 1. 检查系统配置
        check_system_configuration()
        
        # 2. 测试音频转换功能
        logger.info("\n")
        audio_conversion_ok = test_audio_conversion()
        
        # 3. 生成测试音频文件
        logger.info("\n")
        test_files = generate_test_audio_files()
        
        if not test_files:
            logger.error("无法生成测试音频文件")
            return
        
        # 等待用户确认
        input("\n按回车键开始识别测试...")
        
        # 4. 测试识别一致性
        logger.info("\n")
        results = test_recognition_consistency(test_files)
        
        # 5. 分析结果
        logger.info("\n")
        analyze_results(results)
        
        # 6. 提供建议
        logger.info("=== 调试建议 ===")
        logger.info("如果识别结果仍然重复，建议:")
        logger.info("1. 检查麦克风是否正常工作")
        logger.info("2. 在安静环境下测试")
        logger.info("3. 清晰大声说话")
        logger.info("4. 检查网络连接（Google识别需要网络）")
        logger.info("5. 重启应用程序")
        
    except KeyboardInterrupt:
        logger.info("测试被用户中断")
    except Exception as e:
        logger.error(f"调试测试失败: {str(e)}")
    finally:
        # 清理测试文件
        for filename in os.listdir('.'):
            if filename.startswith('test_audio') and filename.endswith('.wav'):
                try:
                    os.remove(filename)
                    logger.info(f"清理测试文件: {filename}")
                except:
                    pass

if __name__ == "__main__":
    main()