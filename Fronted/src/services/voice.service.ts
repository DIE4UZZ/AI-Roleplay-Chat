import api from '../utils/api';

/**
 * 语音服务 - 处理麦克风录音和音频上传
 */
class VoiceService {
  private mediaRecorder: MediaRecorder | null = null;
  private audioChunks: Blob[] = [];
  private stream: MediaStream | null = null;
  private recorderInitialized = false;

  /**
   * 初始化麦克风权限和MediaRecorder
   * @returns Promise<boolean> 是否初始化成功
   */
  private async initializeRecorder(): Promise<boolean> {
    try {
      // 检查浏览器支持
      if (!('mediaDevices' in navigator) || !('getUserMedia' in navigator.mediaDevices)) {
        throw new Error('您的浏览器不支持麦克风录音功能');
      }

      // 请求麦克风权限
      this.stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      
      // 创建MediaRecorder实例
      const options = {
        mimeType: 'audio/webm;codecs=opus',
      };

      // 如果浏览器不支持webm格式，尝试其他格式
      if (!MediaRecorder.isTypeSupported(options.mimeType)) {
        const supportedMimeTypes = [
          'audio/webm',
          'audio/ogg;codecs=opus',
          'audio/wav',
          'audio/mpeg'
        ];
        
        let supportedType = '';
        for (const type of supportedMimeTypes) {
          if (MediaRecorder.isTypeSupported(type)) {
            supportedType = type;
            break;
          }
        }
        
        if (!supportedType) {
          throw new Error('您的浏览器不支持任何可用的音频录制格式');
        }
        
        options.mimeType = supportedType;
      }

      this.mediaRecorder = new MediaRecorder(this.stream, options);
      this.mediaRecorder.addEventListener('dataavailable', (event) => {
        if (event.data.size > 0) {
          this.audioChunks.push(event.data);
        }
      });

      this.recorderInitialized = true;
      return true;
    } catch (error) {
      console.error('初始化麦克风失败:', error);
      // 清理资源
      this.cleanup();
      throw error;
    }
  }

  /**
   * 开始录音
   * @returns Promise<string> 会话ID
   */
  async startRecording(): Promise<string> {
    try {
      // 确保初始化完成
      if (!this.recorderInitialized) {
        await this.initializeRecorder();
      }

      // 重置录音数据
      this.audioChunks = [];

      // 开始录音
      if (this.mediaRecorder && this.mediaRecorder.state !== 'recording') {
        this.mediaRecorder.start(1000); // 每1000ms发送一个数据块
      }

      // 调用后端API创建会话
      const sessionResponse = await api.post('/voice/start');
      
      console.log('录音已开始，会话ID:', sessionResponse.id);
      return sessionResponse.id;
    } catch (error) {
      console.error('开始录音失败:', error);
      throw error;
    }
  }

  /**
   * 停止录音并发送到后端进行识别
   * @param sessionId 会话ID
   * @returns Promise<string> 识别的文本
   */
  async stopRecording(sessionId: string): Promise<string> {
    try {
      if (!this.mediaRecorder || this.mediaRecorder.state === 'inactive') {
        throw new Error('没有正在进行的录音会话');
      }

      // 停止录音
      this.mediaRecorder.stop();

      // 创建Promise等待录音完成
      return new Promise((resolve, reject) => {
        if (!this.mediaRecorder) {
          reject(new Error('MediaRecorder未初始化'));
          return;
        }

        // 监听录音结束事件
        this.mediaRecorder.addEventListener('stop', async () => {
          try {
            // 合并音频数据
            const audioBlob = new Blob(this.audioChunks, { type: this.mediaRecorder?.mimeType || 'audio/webm' });
            
            // 创建FormData上传文件
            const formData = new FormData();
            formData.append('file', audioBlob, `recording_${Date.now()}.webm`);
            formData.append('language', 'zh-CN');
            formData.append('sample_rate', '16000');

            // 调用后端语音识别API
            const recognitionResponse = await api.post('/speech/recognize', formData, {
              headers: {
                'Content-Type': 'multipart/form-data'
              }
            });

            console.log('语音识别结果:', recognitionResponse.text);
            resolve(recognitionResponse.text);
          } catch (error) {
            console.error('语音识别失败:', error);
            reject(error);
          } finally {
            // 清理资源
            this.cleanup();
          }
        }, { once: true });
      });
    } catch (error) {
      console.error('停止录音失败:', error);
      // 确保清理资源
      this.cleanup();
      throw error;
    }
  }

  /**
   * 清理录音相关资源
   */
  private cleanup(): void {
    // 停止所有轨道
    if (this.stream) {
      this.stream.getTracks().forEach(track => track.stop());
      this.stream = null;
    }

    this.mediaRecorder = null;
    this.audioChunks = [];
    this.recorderInitialized = false;
  }

  /**
   * 检查录音权限
   * @returns Promise<boolean> 是否有权限
   */
  async checkPermission(): Promise<boolean> {
    try {
      if (!navigator.permissions || !navigator.mediaDevices) {
        return false;
      }

      const permission = await navigator.permissions.query({ name: 'microphone' as PermissionName });
      return permission.state === 'granted';
    } catch (error) {
      console.error('检查麦克风权限失败:', error);
      return false;
    }
  }

  /**
   * 请求录音权限
   * @returns Promise<boolean> 是否获取权限
   */
  async requestPermission(): Promise<boolean> {
    try {
      if (!navigator.mediaDevices) {
        throw new Error('浏览器不支持媒体设备API');
      }

      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      stream.getTracks().forEach(track => track.stop());
      return true;
    } catch (error) {
      console.error('请求麦克风权限失败:', error);
      return false;
    }
  }
}

export default new VoiceService();