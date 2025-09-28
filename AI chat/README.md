# AI角色聊天服务

这是AI-Roleplay-Chat项目的Python后端服务，负责处理大模型交互、语音识别和文本转语音(TTS)功能。

## 项目结构

```
AI chat/
├── main.py            # 主入口文件，启动FastAPI服务
├── config.py          # 配置文件，存储API密钥等
├── requirements.txt   # 项目依赖
├── llm/               # 大模型相关功能
│   ├── __init__.py
│   ├── base.py        # 基础LLM接口
│   ├── openai_llm.py  # OpenAI模型实现
│   └── ...            # 其他模型实现
├── speech/            # 语音处理功能
│   ├── __init__.py
│   ├── recognition.py # 语音识别
│   ├── tts.py         # 文本转语音
│   └── audio_utils.py # 音频处理工具
├── api/               # API接口
│   ├── __init__.py
│   ├── chat_routes.py # 聊天相关路由
│   ├── speech_routes.py # 语音相关路由
│   └── models.py      # API数据模型
└── utils/             # 工具函数
    ├── __init__.py
    └── logger.py      # 日志工具
```

## 功能说明

1. **大模型交互**：支持多种LLM模型，如OpenAI的GPT系列、Ollama本地模型等
2. **语音识别**：将用户的语音输入转换为文本
3. **文本转语音**：将AI的回复转换为语音输出
4. **API服务**：提供RESTful API供前端调用

## 环境配置

1. 安装Python 3.8+（推荐3.10）
2. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```
3. 创建`.env`文件，配置必要的API密钥：
   ```
   # OpenAI API配置（如使用）
   OPENAI_API_KEY=your_openai_api_key
   
   # 其他模型配置
   # OLLAMA_BASE_URL=http://localhost:11434
   # ANTHROPIC_API_KEY=your_anthropic_api_key
   
   # 服务器配置
   HOST=0.0.0.0
   PORT=8000
   ```

## 运行服务

```bash
python main.py
```

服务将在 http://localhost:8000 启动

## API文档

启动服务后，可以访问 http://localhost:8000/docs 查看API文档

## 注意事项

1. 请确保安装了所有必要的依赖，特别是pyaudio可能需要额外的系统依赖
2. 根据实际需求选择并配置适当的LLM模型
3. 语音识别和TTS功能可能需要网络连接（如使用在线服务）