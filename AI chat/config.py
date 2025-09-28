import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class Config:
    # 服务器配置
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', '8000'))
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    
    # OpenAI 配置
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo')
    OPENAI_TEMPERATURE = float(os.getenv('OPENAI_TEMPERATURE', '0.7'))
    
    # Ollama 配置（本地模型）
    OLLAMA_BASE_URL = os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')
    OLLAMA_MODEL = os.getenv('OLLAMA_MODEL', 'llama2')
    
    # Anthropic 配置
    ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
    ANTHROPIC_MODEL = os.getenv('ANTHROPIC_MODEL', 'claude-3-opus-20240229')
    
    # DeepSeek 配置
    DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
    DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL", "https://openai.qiniu.com/v1")
    DEEPSEEK_BACKUP_BASE_URL = os.getenv("DEEPSEEK_BACKUP_BASE_URL", "https://api.qnaigc.com/v1")
    DEEPSEEK_MODEL = os.getenv("DEEPSEEK_MODEL", "deepseek/deepseek-v3.1-terminus")
    DEEPSEEK_TEMPERATURE = float(os.getenv("DEEPSEEK_TEMPERATURE", "0.7"))
    
    # TTS 配置
    TTS_ENGINE = os.getenv("TTS_ENGINE", "gtts")
    TTS_API_KEY = os.getenv("TTS_API_KEY")
    TTS_BASE_URL = os.getenv("TTS_BASE_URL", "https://openai.qiniu.com/v1")
    TTS_BACKUP_BASE_URL = os.getenv("TTS_BACKUP_BASE_URL", "https://api.qnaigc.com/v1")
    TTS_MODEL = os.getenv("TTS_MODEL", "tts")
    TTS_LANG = os.getenv("TTS_LANG", "zh-CN")
    TTS_SLOW = os.getenv("TTS_SLOW", "False").lower() == "true"
    
    # 语音识别配置
    SPEECH_RECOGNITION_LANGUAGE = os.getenv('SPEECH_RECOGNITION_LANGUAGE', 'zh-CN')
    
    # TTS配置
    TTS_LANG = os.getenv('TTS_LANG', 'zh-cn')
    TTS_SLOW = os.getenv('TTS_SLOW', 'False').lower() == 'true'
    
    # 默认模型选择
    DEFAULT_LLM_PROVIDER = os.getenv('DEFAULT_LLM_PROVIDER', 'openai')  # openai, ollama, anthropic, deepseek
    
    # 音频设置
    AUDIO_SAMPLE_RATE = 16000
    AUDIO_CHANNELS = 1
    AUDIO_CHUNK_SIZE = 1024

# 创建配置实例
env_config = Config()

# 验证必要的配置
if env_config.DEFAULT_LLM_PROVIDER == 'openai' and not env_config.OPENAI_API_KEY:
    print("警告: OpenAI API密钥未设置")
    # 可以选择默认使用其他模型或提示用户设置
    env_config.DEFAULT_LLM_PROVIDER = 'ollama'
    
if env_config.DEFAULT_LLM_PROVIDER == 'anthropic' and not env_config.ANTHROPIC_API_KEY:
    print("警告: Anthropic API密钥未设置")
    env_config.DEFAULT_LLM_PROVIDER = 'ollama'
    
if env_config.DEFAULT_LLM_PROVIDER == 'deepseek' and not env_config.DEEPSEEK_API_KEY:
    print("警告: DeepSeek API密钥未设置")
    env_config.DEFAULT_LLM_PROVIDER = 'ollama'