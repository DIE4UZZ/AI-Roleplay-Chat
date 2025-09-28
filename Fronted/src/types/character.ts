// 角色相关类型定义

export interface Character {
  id: number;
  name: string;
  avatar: string;
  description: string;
  category: string;
}

export interface CharacterCategory {
  id: string;
  name: string;
}

export interface Message {
  id: number;
  text: string;
  sender: 'user' | 'ai';
  timestamp: Date;
}

export interface ChatSession {
  id: number;
  characterId: number;
  startTime: Date;
  endTime?: Date;
  messageCount: number;
}