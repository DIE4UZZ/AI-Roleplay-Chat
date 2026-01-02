# 音频格式转换功能实现

## 功能概述

为AI-Roleplay-Chat项目添加了WebM到WAV的音频格式转换功能，以解决TTS（文本转语音）功能因音频格式不兼容导致的错误问题。

## 实现的功能

### 1. 核心转换功能

- **WebM到WAV转换** (`speech/audio_converter.py`)
  - 支持文件路径和字节数据输入
  - 可配置采样率和声道数
  - 自动检测音频格式
  - 适合TTS处理的音频优化

- **多格式转换支持**
  - MP3 → WAV
  - OGG → WAV  
  - FLAC → WAV
  - M4A → WAV
  - 任意格式 → WAV

### 2. 音频预处理

- **声道标准化**：自动转换为单声道或立体声
- **采样率调整**：支持自定义采样率（推荐16000Hz用于TTS）
- **音量标准化**：避免音频过大或过小
- **淡入淡出**：添加轻微效果避免点击声

### 3. API接口

新增音频转换API接口：`/api/speech/convert-audio`

**请求参数：**
- `file`: 上传的音频文件
- `target_format`: 目标格式（支持：wav, webm, mp3）
- `sample_rate`: 目标采样率（可选）
- `channels`: 目标声道数（可选）

**响应：**
- 转换后的音频文件
- 支持WAV、WebM、MP3格式输出

### 4. 集成点

- **TTS模块集成** (`speech/tts.py`)
  - 新增 `convert_audio_for_tts` 和 `convert_audio_bytes_for_tts` 方法
  - 支持在TTS处理前自动转换音频格式

- **语音识别模块集成** (`speech/recognition.py`)
  - 修改识别方法支持音频格式自动转换
  - 增强对WebM等格式的兼容性

## 文件结构

```
AI chat/
├── speech/
│   ├── audio_converter.py     # 音频转换核心类
│   ├── tts.py                 # TTS模块（已集成转换功能）
│   └── recognition.py         # 语音识别模块（已集成转换功能）
├── api/
│   └── speech_routes.py       # API路由（新增转换接口）
├── test_audio_converter.py    # 完整测试文件
└── test_simple_converter.py   # 简化测试文件
```

## 使用方法

### 1. 直接使用转换器

```python
from speech.audio_converter import audio_converter

# 文件转换
wav_path, error = audio_converter.webm_to_wav("input.webm", sample_rate=16000)

# 字节数据转换
wav_path, error = audio_converter.convert_bytes_to_wav(
    audio_bytes=webm_data,
    original_filename="test.webm"
)
```

### 2. 在TTS中使用

```python
from speech.tts import tts_engine

# 自动转换音频用于TTS
tts_engine.convert_audio_for_tts("input.webm")
tts_engine.convert_audio_bytes_for_tts(audio_bytes)
```

### 3. API调用

```bash
curl -X POST "http://localhost:8000/api/speech/convert-audio" \
  -F "file=@audio.webm" \
  -F "target_format=wav" \
  -F "sample_rate=16000" \
  -F "channels=1"
```

## 配置

在 `config.py` 中的音频配置：

```python
AUDIO_SAMPLE_RATE = 16000    # 音频采样率
AUDIO_CHANNELS = 1           # 音频声道数（1=单声道）
```

## 错误处理

- **文件不存在**：返回明确错误信息
- **格式不支持**：提供支持的格式列表
- **转换失败**：详细记录错误日志
- **临时文件清理**：自动清理转换过程中的临时文件

## 依赖库

已在 `requirements.txt` 中包含：
- `pydub>=0.25.1` - 音频处理核心库
- `ffmpeg-python>=0.2.0` - FFmpeg Python接口

## 测试

运行测试验证功能：

```bash
# 基本功能测试
python test_simple_converter.py

# 完整功能测试
python test_audio_converter.py
```

## 注意事项

1. **FFmpeg依赖**：虽然pydub基本功能可用，但建议安装FFmpeg以获得最佳性能和格式支持
2. **格式兼容性**：WebM格式在某些环境下可能需要FFmpeg支持
3. **内存使用**：大文件转换时会创建临时文件，请确保有足够磁盘空间
4. **错误恢复**：如果转换失败，系统会尝试多种转换方法

## 故障排除

### 常见问题

1. **"FFmpeg未找到"警告**
   - 这是正常警告，不影响基本功能
   - 可安装FFmpeg提升兼容性：`conda install ffmpeg` 或下载Windows版本

2. **WebM转换失败**
   - 确保输入文件是有效的WebM格式
   - 检查文件是否损坏

3. **采样率设置无效**
   - 某些格式可能有最小采样率限制
   - 系统会使用最接近的可用采样率

### 调试

启用详细日志：
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 性能优化建议

1. **小文件处理**：文件小于1MB时直接加载到内存
2. **批量转换**：可考虑添加批量转换功能
3. **缓存机制**：对相同文件的重复转换进行缓存

## 未来扩展

- 支持更多音频格式（FLAC、AAC等）
- 添加音频质量参数控制
- 实现流式转换支持大文件
- 添加音频合并和分割功能