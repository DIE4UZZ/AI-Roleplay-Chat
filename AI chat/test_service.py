#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
AI角色聊天服务测试脚本

这个脚本用于测试AI服务的基本功能，包括LLM模型交互、语音识别和TTS功能。
"""

import os
import sys
import time

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 导入服务组件
from llm.openai_llm import OpenAILLM
from speech.recognition import speech_recognizer
from speech.tts import tts_engine
from speech.audio_utils import audio_utils
from config import env_config
from utils.logger import get_logger

# 创建日志器
logger = get_logger("ai_chat_service.test")

def test_llm():
    """测试LLM模型功能"""
    logger.info("=== 开始测试LLM模型功能 ===")
    
    try:
        # 创建角色上下文
        character_context = {
            "name": "测试助手",
            "description": "你是一个友好的AI助手，总是用简洁的语言回答问题。"
        }
        
        # 创建模型实例
        if env_config.DEFAULT_LLM_PROVIDER == 'openai':
            llm = OpenAILLM()
            prompt = "你好，能介绍一下你自己吗？"
            
            logger.info(f"向{env_config.DEFAULT_LLM_PROVIDER}模型发送请求: {prompt}")
            
            # 生成响应
            response = llm.generate_response(
                prompt=prompt,
                character_context=character_context
            )
            
            logger.info(f"模型响应: {response}")
            return True
        else:
            logger.warning(f"跳过测试: 默认模型提供商 {env_config.DEFAULT_LLM_PROVIDER} 未配置或不支持")
            return False
            
    except Exception as e:
        logger.error(f"LLM模型测试失败: {str(e)}")
        return False
    
    finally:
        logger.info("=== LLM模型功能测试结束 ===\n")

def test_speech_recognition():
    """测试语音识别功能"""
    logger.info("=== 开始测试语音识别功能 ===")
    
    try:
        logger.info("请对着麦克风说话（5秒内）...")
        
        # 录制5秒音频
        audio_bytes, error = audio_utils.record_audio(duration=5)
        
        if error:
            logger.error(f"音频录制失败: {error}")
            return False
        
        logger.info("音频录制成功，开始识别...")
        
        # 语音识别
        text, error = speech_recognizer.recognize_from_audio_bytes(audio_bytes)
        
        if error:
            logger.error(f"语音识别失败: {error}")
            return False
        
        logger.info(f"语音识别结果: {text}")
        return True
        
    except Exception as e:
        logger.error(f"语音识别测试失败: {str(e)}")
        return False
    
    finally:
        logger.info("=== 语音识别功能测试结束 ===\n")

def test_tts():
    """测试文本转语音功能"""
    logger.info("=== 开始测试文本转语音功能 ===")
    
    try:
        text = "这是一段用于测试文本转语音功能的示例文本。"
        logger.info(f"要转换的文本: {text}")
        
        # 文本转语音
        success, error = tts_engine.speak(text)
        
        if error:
            logger.error(f"文本转语音失败: {error}")
            return False
        
        logger.info("文本转语音成功，已播放语音")
        return True
        
    except Exception as e:
        logger.error(f"文本转语音测试失败: {str(e)}")
        return False
    
    finally:
        logger.info("=== 文本转语音功能测试结束 ===\n")

def main():
    """主测试函数"""
    logger.info("开始AI角色聊天服务测试...")
    
    # 记录测试开始时间
    start_time = time.time()
    
    # 运行各个测试
    results = {
        "LLM模型": test_llm(),
        "语音识别": test_speech_recognition(),
        "文本转语音": test_tts()
    }
    
    # 统计测试结果
    success_count = sum(results.values())
    total_count = len(results)
    
    # 计算测试用时
    elapsed_time = time.time() - start_time
    
    # 输出测试摘要
    logger.info("\n=== 测试摘要 ===")
    for test_name, passed in results.items():
        logger.info(f"{test_name}: {'通过' if passed else '失败'}")
    
    logger.info(f"测试结果: {success_count}/{total_count} 项通过")
    logger.info(f"总用时: {elapsed_time:.2f} 秒")
    
    # 根据测试结果返回不同的退出码
    sys.exit(0 if success_count == total_count else 1)

if __name__ == "__main__":
    main()