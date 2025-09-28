import os
import sys
from speech.tts import TextToSpeech
from config import env_config

# 测试TTS功能
def test_tts():
    print("开始测试TTS功能...")
    
    try:
        # 创建TTS实例
        tts = TextToSpeech()
        
        print(f"成功创建TTS实例")
        print(f"使用的引擎: {tts.tts_engine}")
        print(f"TTS API密钥配置: {tts.api_key is not None}")
        
        # 测试简单的文本转语音
        text = "你好，这是一个TTS测试。"
        print(f"\n测试文本: {text}")
        
        # 保存为文件测试
        print("正在将文本转换为语音文件...")
        temp_file = os.path.join(os.path.dirname(__file__), "test_tts_output.mp3")
        file_path, error = tts.text_to_speech(text, temp_file)
        
        if file_path:
            print(f"语音文件保存成功: {file_path}")
            print(f"文件大小: {os.path.getsize(file_path)} 字节")
        else:
            print(f"语音文件保存失败: {error}")
        
        # 测试字节数据输出
        print("\n正在测试文本转语音字节数据...")
        audio_bytes, error = tts.text_to_speech_bytes(text)
        
        if audio_bytes:
            print(f"语音字节数据生成成功")
            print(f"数据大小: {len(audio_bytes)} 字节")
        else:
            print(f"语音字节数据生成失败: {error}")
        
        # 测试播放功能（可选）
        print("\n测试语音播放功能（按Enter继续，或按Ctrl+C跳过）")
        try:
            input()
            success, error = tts.speak(text)
            if success:
                print("语音播放成功")
            else:
                print(f"语音播放失败: {error}")
        except KeyboardInterrupt:
            print("跳过语音播放测试")
            
        print("\nTTS功能测试完成！")
        return True
        
    except Exception as e:
        print(f"\nTTS功能测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        # 清理临时文件
        if 'temp_file' in locals() and os.path.exists(temp_file):
            try:
                os.remove(temp_file)
                print(f"已清理临时文件: {temp_file}")
            except:
                pass

if __name__ == "__main__":
    # 显示当前TTS配置
    print(f"当前TTS引擎: {env_config.TTS_ENGINE}")
    print(f"TTS API密钥配置: {env_config.TTS_API_KEY is not None}")
    print(f"TTS模型: {env_config.TTS_MODEL}")
    
    # 运行测试
    success = test_tts()
    
    # 根据测试结果设置退出码
    sys.exit(0 if success else 1)