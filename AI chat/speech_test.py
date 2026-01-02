#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
语音识别简单测试工具
用于测试语音识别功能是否正常工作
"""

import os
import sys
import time
import hashlib
import speech_recognition as sr

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from speech.recognition import speech_recognizer
from speech.audio_utils import audio_utils
from config import env_config
from utils.logger import get_logger

# 创建日志器
logger = get_logger("ai_chat_service.speech_test")

def check_system_info():
    """检查系统信息"""
    print("=== 系统信息检查 ===")
    print(f"识别语言: {speech_recognizer.language}")
    print(f"能量阈值: {speech_recognizer.recognizer.energy_threshold}")
    print(f"动态能量阈值: {speech_recognizer.recognizer.dynamic_energy_threshold}")
    print(f"暂停阈值: {speech_recognizer.recognizer.pause_threshold}")
    print(f"采样率: {env_config.AUDIO_SAMPLE_RATE}")
    print(f"声道数: {env_config.AUDIO_CHANNELS}")
    print()

def test_recognition_multiple_times():
    """测试多次识别是否返回相同结果"""
    print("=== 多次识别测试 ===")
    
    results = []
    audio_hashes = []
    
    for i in range(3):
        print(f"\n--- 第 {i+1} 次测试 ---")
        
        try:
            # 录制音频
            print("开始录制音频（5秒）...")
            audio_bytes, error = audio_utils.record_audio(duration=5)
            
            if error:
                print(f"录音失败: {error}")
                continue
            
            # 计算音频哈希
            audio_hash = hashlib.md5(audio_bytes).hexdigest()
            audio_hashes.append(audio_hash)
            print(f"音频大小: {len(audio_bytes)} 字节")
            print(f"音频哈希: {audio_hash[:8]}...")
            
            # 保存音频文件
            wav_file = f"test_{i+1}.wav"
            success, save_error = audio_utils.save_wav(audio_bytes, wav_file)
            
            if not success:
                print(f"保存音频失败: {save_error}")
                continue
            
            # 识别音频
            print("开始语音识别...")
            text, error = speech_recognizer.recognize_from_audio_file(wav_file)
            
            if error:
                print(f"识别错误: {error}")
                results.append({"text": None, "error": error})
            else:
                print(f"识别结果: '{text}'")
                results.append({"text": text, "error": None})
                
        except Exception as e:
            print(f"测试失败: {str(e)}")
            results.append({"text": None, "error": str(e)})
        
        print("-" * 50)
    
    # 分析结果
    print("\n=== 结果分析 ===")
    
    # 检查音频是否相同
    if len(set(audio_hashes)) == 1:
        print("WARNING: 所有录制的音频内容完全相同！")
        print("这表明录音功能可能有问题")
    else:
        print("GOOD: 录制的音频内容不同")
    
    # 检查识别结果
    successful_results = [r for r in results if r["text"] is not None]
    
    if len(successful_results) == 0:
        print("ERROR: 没有成功的识别结果")
        return False
    elif len(set(r["text"] for r in successful_results)) == 1:
        print("WARNING: 所有识别结果都相同！")
        print("这表明可能存在以下问题:")
        print("1. 麦克风录音异常")
        print("2. 环境噪音干扰")
        print("3. 语音识别服务缓存")
        print("4. 音频处理配置不当")
        return False
    else:
        print("GOOD: 识别结果多样，说明语音识别功能正常")
        return True

def test_microphone():
    """测试麦克风功能"""
    print("\n=== 麦克风测试 ===")
    
    try:
        print("正在初始化麦克风...")
        
        with sr.Microphone() as source:
            print("麦克风初始化成功")
            print("正在调整麦克风以适应环境噪音...")
            speech_recognizer.recognizer.adjust_for_ambient_noise(source, duration=1)
            print(f"当前能量阈值: {speech_recognizer.recognizer.energy_threshold}")
            print("麦克风测试完成")
            return True
            
    except Exception as e:
        print(f"麦克风测试失败: {str(e)}")
        return False

def main():
    """主测试函数"""
    print("语音识别功能测试")
    print("=" * 50)
    
    try:
        # 1. 检查系统信息
        check_system_info()
        
        # 2. 测试麦克风
        mic_ok = test_microphone()
        if not mic_ok:
            print("麦克风测试失败，无法继续")
            return
        
        # 3. 多次识别测试
        recognition_ok = test_recognition_multiple_times()
        
        # 4. 提供建议
        print("\n=== 测试总结 ===")
        if recognition_ok:
            print("SUCCESS: 语音识别功能正常")
        else:
            print("FAILED: 语音识别功能存在问题")
            print("\n建议:")
            print("1. 检查麦克风权限")
            print("2. 在安静环境下测试")
            print("3. 清晰大声说话")
            print("4. 检查网络连接")
            print("5. 重新配置语音识别参数")
        
        # 5. 清理测试文件
        print("\n清理测试文件...")
        for filename in os.listdir('.'):
            if filename.startswith('test_') and filename.endswith('.wav'):
                try:
                    os.remove(filename)
                    print(f"删除: {filename}")
                except:
                    pass
        
    except KeyboardInterrupt:
        print("\n测试被用户中断")
    except Exception as e:
        print(f"测试失败: {str(e)}")

if __name__ == "__main__":
    main()