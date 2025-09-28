import { defineStore } from 'pinia';
import type { Character, Message, ChatSession } from '../types/character';
import characterService from '../services/character.service';

// 定义角色和聊天状态store
interface CharacterState {
  characters: Character[];
  selectedCharacter: Character | null;
  messages: Message[];
  chatSessions: ChatSession[];
  isLoading: boolean;
  error: string | null;
}

export const useCharacterStore = defineStore('character', {
  state: (): CharacterState => ({
    characters: [],
    selectedCharacter: null,
    messages: [],
    chatSessions: [],
    isLoading: false,
    error: null,
  }),

  getters: {
    // 获取所有角色
    getAllCharacters(): Character[] {
      return this.characters;
    },
    
    // 获取当前选中的角色
    getSelectedCharacter(): Character | null {
      return this.selectedCharacter;
    },
    
    // 获取当前会话的消息
    getCurrentMessages(): Message[] {
      return this.messages;
    },
    
    // 检查是否正在加载
    isLoadingState(): boolean {
      return this.isLoading;
    },
    
    // 获取错误信息
    getError(): string | null {
      return this.error;
    },
  },

  actions: {
    // 加载角色列表
    async loadCharacters(): Promise<void> {
      this.isLoading = true;
      this.error = null;
      try {
        this.characters = await characterService.getCharacters();
      } catch (error) {
        console.error('加载角色失败:', error);
        this.error = '加载角色失败，请稍后再试';
      } finally {
        this.isLoading = false;
      }
    },

    // 搜索角色
    async searchCharacters(query: string): Promise<void> {
      this.isLoading = true;
      this.error = null;
      try {
        this.characters = await characterService.searchCharacters(query);
      } catch (error) {
        console.error('搜索角色失败:', error);
        this.error = '搜索角色失败，请稍后再试';
      } finally {
        this.isLoading = false;
      }
    },

    // 选择角色
    async selectCharacter(character: Character): Promise<void> {
      this.selectedCharacter = character;
      this.messages = [];
      
      // 添加欢迎消息
      this.addMessage(`你好！我是${character.name}，很高兴与你交流。`, 'ai');
      
      // 可以在这里加载历史聊天记录
      try {
        const history = await characterService.getChatHistory(character.id);
        if (history.length > 0) {
          this.messages = history;
        }
      } catch (error) {
        console.error('加载聊天历史失败:', error);
      }
    },

    // 发送消息
    async sendMessage(message: string): Promise<void> {
      if (!this.selectedCharacter) {
        this.error = '请先选择一个角色';
        return;
      }
      
      // 添加用户消息
      this.addMessage(message, 'user');
      
      // 发送消息并获取回复
      this.isLoading = true;
      try {
        const reply = await characterService.sendMessage(this.selectedCharacter.id, message);
        this.addMessage(reply, 'ai');
      } catch (error) {
        console.error('发送消息失败:', error);
        this.error = '发送消息失败，请稍后再试';
      } finally {
        this.isLoading = false;
      }
    },

    // 添加消息到消息列表
    addMessage(text: string, sender: 'user' | 'ai'): void {
      this.messages.push({
        id: Date.now(),
        text,
        sender,
        timestamp: new Date(),
      });
    },

    // 清除当前会话
    clearCurrentSession(): void {
      this.selectedCharacter = null;
      this.messages = [];
    },

    // 设置错误信息
    setError(error: string | null): void {
      this.error = error;
    },

    // 开始语音识别
    async startVoiceRecognition(): Promise<string> {
      try {
        const result = await characterService.startVoiceRecognition();
        return result.id;
      } catch (error) {
        console.error('开始语音识别失败:', error);
        this.error = '开始语音识别失败，请稍后再试';
        throw error;
      }
    },

    // 停止语音识别
    async stopVoiceRecognition(sessionId: string): Promise<string> {
      try {
        const result = await characterService.stopVoiceRecognition(sessionId);
        return result.text;
      } catch (error) {
        console.error('结束语音识别失败:', error);
        this.error = '语音识别失败，请稍后再试';
        throw error;
      }
    },
  },
});