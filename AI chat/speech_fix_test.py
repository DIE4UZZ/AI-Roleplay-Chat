#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
语音识别修复验证测试
快速测试语音识别功能是否正常工作
"""

import os
import sys
import hashlib

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from speech.recognition import speech_recognizer
from speech.audio_utils import audio_utils

def simple_speech_test():
    """简单语音识别测试"""
    print("=== 语音识别修复验证测试 ===")
    
    try:
        # 录制短音频测试
        print("录制3秒测试音频，请清晰说一段话...")
        audio_bytes, error = audio_utils.record_audio(duration=3)
        
        if error:
            print(f"录音失败: {error}")
            return False
        
        print(f"录音成功，音频大小: {len(audio_bytes)} 字节")
        
        # 保存为测试文件
        test_file = "simple_test.wav"
        success, save_error = audio_utils.save_wav(audio_bytes, test_file)
        
        if not success:
            print(f"保存失败: {save_error}")
            return False
        
        print(f"音频保存成功: {test_file}")
        
        # 计算音频哈希，检查内容是否正常
        audio_hash = hashlib.md5(audio_bytes).hexdigest()
        print(f"音频内容哈希: {audio_hash[:12]}...")
        
        # 测试语音识别
        print("开始语音识别...")
        text, error = speech_recognizer.recognize_from_audio_file(test_file)
        
        if error:
            print(f"识别失败: {error}")
            return False
        
        print(f"识别结果: '{text}'")
        
        # 检查结果是否合理
        if text and len(text.strip()) > 0:
            print("SUCCESS: 语音识别功能正常工作")
            
            # 清理测试文件
            try:
                os.remove(test_file)
                print(f"清理测试文件: {test_file}")
            except:
                pass
            
            return True
        else:
            print("WARNING: 识别结果为空")
            return False
            
    except Exception as e:
        print(f"测试失败: {str(e)}")
        return False

def check_recognition_config():
    """检查识别配置"""
    print("\n=== 识别配置检查 ===")
    print(f"识别语言: {speech_recognizer.language}")
    print(f"能量阈值: {speech_recognizer.recognizer.energy_threshold:.1f}")
    print(f"动态能量阈值: {speech_recognizer.recognizer.dynamic_energy_threshold}")
    print(f"暂停阈值: {speech_recognizer.recognizer.pause_threshold}")

def main():
    """主函数"""
    print("语音识别修复验证")
    print("=" * 40)
    
    # 检查配置
    check_recognition_config()
    
    # 运行测试
    success = simple_speech_test()
    
    print("\n=== 测试结果 ===")
    if success:
        print("SUCCESS: 语音识别修复成功，功能正常")
        print("\n建议:")
        print("- 如果还有问题，可能是网络连接或麦克风权限问题")
        print("- 请在安静环境下清晰说话")
    else:
        print("FAILED: 仍存在语音识别问题")
        print("\n请检查:")
        print("1. 麦克风权限设置")
        print("2. 网络连接状态")
        print("3. 语音识别API配置")

if __name__ == "__main__":
    main()