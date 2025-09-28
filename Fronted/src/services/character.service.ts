import api from '../utils/api';
import type { Character, Message } from '../types/character';

// 角色服务
class CharacterService {
  // 获取角色列表
  async getCharacters(): Promise<Character[]> {
    try {
      const data = await api.get('/characters');
      return data || [];
    } catch (error) {
      console.error('获取角色列表失败:', error);
      // 在API不可用的情况下返回模拟数据
      return [
        { id: 1, name: '哈利波特', avatar: '🧙‍♂️', description: '魔法世界的传奇巫师', category: 'fiction' },
        { id: 2, name: '苏格拉底', avatar: '👨‍🏫', description: '古希腊著名哲学家', category: 'historical' },
        { id: 3, name: '爱因斯坦', avatar: '🧠', description: '著名物理学家，相对论提出者', category: 'historical' },
        { id: 4, name: '林黛玉', avatar: '💃', description: '《红楼梦》中的经典人物', category: 'fiction' },
        { id: 5, name: '莎士比亚', avatar: '📝', description: '英国著名剧作家和诗人', category: 'historical' },
        { id: 6, name: '哪吒', avatar: '👶', description: '中国古代神话中的神童', category: 'mythology' },
        { id: 7, name: '牛顿', avatar: '🍎', description: '万有引力定律的发现者', category: 'historical' },
        { id: 8, name: '孙悟空', avatar: '🐒', description: '《西游记》中的齐天大圣', category: 'mythology' },
      ];
    }
  }

  // 搜索角色
  async searchCharacters(query: string): Promise<Character[]> {
    try {
      const data = await api.get(`/characters/search?q=${encodeURIComponent(query)}`);
      return data || [];
    } catch (error) {
      console.error('搜索角色失败:', error);
      // 在API不可用的情况下使用本地过滤
      const characters = await this.getCharacters();
      return characters.filter(character => 
        character.name.toLowerCase().includes(query.toLowerCase()) ||
        character.description.toLowerCase().includes(query.toLowerCase())
      );
    }
  }

  // 获取角色详情
  async getCharacterById(id: number): Promise<Character | null> {
    try {
      const data = await api.get(`/characters/${id}`);
      return data || null;
    } catch (error) {
      console.error('获取角色详情失败:', error);
      // 在API不可用的情况下从模拟数据中查找
      const characters = await this.getCharacters();
      return characters.find(char => char.id === id) || null;
    }
  }

  // 发送聊天消息
  async sendMessage(characterId: number, message: string): Promise<string> {
    try {
      // 调用专门处理前端格式的接口
      const data = await api.post('/chat/character/send', {
        characterId,
        message
      });
      return data.reply || '抱歉，我无法回答这个问题。';
    } catch (error) {
      console.error('发送消息失败:', error);
      // 在API不可用的情况下返回模拟回复
      const aiResponses = [
        `这是一个有趣的话题！关于${message}，我认为...`,
        `你提出了一个很好的问题。根据我的理解，${message}...`,
        `我很高兴你提到了${message}。让我详细解释一下...`,
        `${message}确实值得深入探讨。从多个角度来看...`,
        `感谢分享你的想法。关于${message}，我的看法是...`,
      ];
      return aiResponses[Math.floor(Math.random() * aiResponses.length)];
    }
  }

  // 获取聊天历史
  async getChatHistory(characterId: number): Promise<Message[]> {
    try {
      const data = await api.get(`/chat/history/${characterId}`);
      return data || [];
    } catch (error) {
      console.error('获取聊天历史失败:', error);
      return [];
    }
  }

  // 开始语音识别
  async startVoiceRecognition(): Promise<{id: string}> {
    try {
      const data = await api.post('/voice/start');
      return data;
    } catch (error) {
      console.error('开始语音识别失败:', error);
      // 在API不可用的情况下返回模拟ID
      return { id: `voice_${Date.now()}` };
    }
  }

  // 结束语音识别
  async stopVoiceRecognition(sessionId: string): Promise<{text: string}> {
    try {
      const data = await api.post('/voice/stop', { sessionId });
      return data;
    } catch (error) {
      console.error('结束语音识别失败:', error);
      // 在API不可用的情况下返回模拟文本
      return { text: '这是一段模拟的语音输入内容' };
    }
  }
}

export default new CharacterService();