<template>
  <div class="chat-container">
    <!-- 顶部导航 -->
    <header class="chat-header">
      <div class="container">
        <div class="header-content">
          <router-link to="/" class="logo">
            <div class="logo-icon">🎭</div>
            <div class="logo-text">
              <h1 class="logo-title">AI 角色扮演</h1>
            </div>
          </router-link>
          <div class="header-actions">
            <button class="btn btn-secondary" @click="handleBack">返回首页</button>
          </div>
        </div>
      </div>
    </header>

    <!-- 错误提示 -->
    <Transition name="slide-up">
      <div v-if="characterStore.error" class="error-banner">
        <span class="error-icon">⚠️</span>
        <span class="error-text">{{ characterStore.error }}</span>
        <button class="error-close" @click="characterStore.setError(null)">×</button>
      </div>
    </Transition>

    <!-- 主内容区域 -->
    <main class="chat-main">
      <!-- 角色选择面板 -->
      <div class="character-panel" v-if="!selectedCharacter">
        <div class="panel-header">
          <h2>选择角色</h2>
          <div class="search-container">
            <input 
              type="text" 
              v-model="searchQuery" 
              placeholder="搜索角色（如：哈利波特、苏格拉底）" 
              class="search-input"
              @input="searchCharacters"
              :disabled="characterStore.isLoading"
            />
            <button class="search-btn" @click="searchCharacters" :disabled="characterStore.isLoading">
              {{ characterStore.isLoading ? '🔄' : '🔍' }}
            </button>
          </div>
        </div>
        
        <div class="character-categories">
          <button 
            v-for="category in categories" 
            :key="category.id"
            :class="['category-btn', { active: selectedCategory === category.id }]"
            @click="selectedCategory = category.id; filterCharacters()"
            :disabled="characterStore.isLoading"
          >
            {{ category.name }}
          </button>
        </div>
        
        <!-- 加载状态 -->
        <div v-if="characterStore.isLoading" class="loading-container">
          <div class="loading-spinner"></div>
          <p>加载角色中...</p>
        </div>
        
        <!-- 空状态 -->
        <div v-else-if="filteredCharacters.length === 0" class="empty-state">
          <div class="empty-icon">🎭</div>
          <h3>未找到角色</h3>
          <p>请尝试使用其他关键词搜索，或选择其他分类</p>
          <button class="btn btn-secondary" @click="resetSearch">重置搜索</button>
        </div>
        
        <!-- 角色列表 -->
        <div v-else class="characters-grid">
          <div 
            v-for="character in filteredCharacters" 
            :key="character.id"
            class="character-card"
            @click="selectCharacter(character)"
          >
            <div class="character-avatar">
              {{ character.avatar }}
            </div>
            <div class="character-info">
              <h3 class="character-name">{{ character.name }}</h3>
              <p class="character-description">{{ character.description }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- 聊天界面 -->
      <div class="chat-interface" v-else>
        <!-- 聊天头部 -->
        <div class="chat-header-info">
          <div class="character-avatar-large">
            {{ selectedCharacter.avatar }}
          </div>
          <div class="character-details">
            <h2>{{ selectedCharacter.name }}</h2>
            <p>{{ selectedCharacter.description }}</p>
          </div>
          <div class="chat-actions">
            <button class="btn btn-secondary" @click="changeCharacter">
              更换角色
            </button>
          </div>
        </div>

        <!-- 聊天记录 -->
        <div class="chat-messages" ref="chatMessages">
          <!-- 欢迎消息 -->
          <div v-if="messages.length === 0" class="welcome-message">
            <p>开始与{{ selectedCharacter.name }}对话吧！</p>
            <p class="welcome-subtext">您可以输入文字或点击麦克风进行语音交流</p>
          </div>
          
          <!-- 消息列表 -->
          <div v-for="message in messages" :key="message.id" :class="['message', message.sender]">
            <div class="message-content">
              {{ message.text }}
            </div>
            <div class="message-time">
              {{ formatTime(message.timestamp) }}
            </div>
          </div>
          
          <!-- AI正在输入 -->
          <div v-if="characterStore.isLoading" class="message ai typing">
            <div class="typing-indicator">
              <span class="typing-dot"></span>
              <span class="typing-dot"></span>
              <span class="typing-dot"></span>
            </div>
          </div>
        </div>

        <!-- 聊天输入 -->
        <div class="chat-input-container">
          <div class="input-wrapper">
            <input 
              type="text" 
              v-model="newMessage" 
              placeholder="输入消息或点击麦克风进行语音对话..." 
              class="message-input"
              @keyup.enter="sendMessage"
              :disabled="characterStore.isLoading"
            />
            <div class="input-actions">
              <button 
                class="voice-btn"
                :class="{ recording: isRecording }"
                @click="toggleRecording"
                :disabled="characterStore.isLoading"
                title="语音输入"
              >
                <span class="voice-icon">{{ isRecording ? '🔴' : '🎤' }}</span>
                <span v-if="isRecording" class="recording-indicator">录音中...</span>
              </button>
              <button 
                class="send-btn"
                @click="sendMessage"
                :disabled="!newMessage.trim() || characterStore.isLoading"
                title="发送消息"
              >
                {{ characterStore.isLoading ? '🔄' : '📤' }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, nextTick, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useCharacterStore } from '../store/character.store';
import type { Character, Message } from '../types/character';

const router = useRouter();
const characterStore = useCharacterStore();

// 组件状态
const searchQuery = ref('');
const selectedCategory = ref('all');
const newMessage = ref('');
const isRecording = ref(false);
const chatMessages = ref<HTMLElement | null>(null);
const voiceSessionId = ref<string>('');

// 角色分类
const categories = [
  { id: 'all', name: '全部' },
  { id: 'historical', name: '历史人物' },
  { id: 'fiction', name: '虚构角色' },
  { id: 'mythology', name: '神话传说' },
];

// 计算属性 - 从store获取数据
const selectedCharacter = computed(() => characterStore.getSelectedCharacter);
const characters = computed(() => characterStore.getAllCharacters);
const messages = computed(() => characterStore.getCurrentMessages);
const isLoading = computed(() => characterStore.isLoadingState);
const error = computed(() => characterStore.getError);

// 过滤后的角色列表
const filteredCharacters = computed(() => {
  let filtered = characters.value;
  
  // 按分类过滤
  if (selectedCategory.value !== 'all') {
    filtered = filtered.filter(character => character.category === selectedCategory.value);
  }
  
  // 按搜索关键词过滤
  if (searchQuery.value.trim()) {
    const query = searchQuery.value.toLowerCase().trim();
    filtered = filtered.filter(character => 
      character.name.toLowerCase().includes(query) || 
      character.description.toLowerCase().includes(query)
    );
  }
  
  return filtered;
});

// 初始化
onMounted(() => {
  loadCharacters();
  
  // 监听消息变化，自动滚动到底部
  const unwatch = characterStore.$subscribe(() => {
    nextTick(() => {
      if (chatMessages.value) {
        chatMessages.value.scrollTop = chatMessages.value.scrollHeight;
      }
    });
  });
  
  // 清理监听器
  return () => unwatch();
});

// 方法
const handleBack = () => {
  router.push('/');
};

const loadCharacters = async () => {
  await characterStore.loadCharacters();
};

const searchCharacters = async () => {
  if (!searchQuery.value.trim()) {
    await loadCharacters();
    return;
  }
  
  await characterStore.searchCharacters(searchQuery.value);
};

const filterCharacters = () => {
  // 过滤逻辑已在computed属性中实现
};

const selectCharacter = async (character: Character) => {
  await characterStore.selectCharacter(character);
};

const changeCharacter = () => {
  characterStore.clearCurrentSession();
};

const sendMessage = async () => {
  if (!newMessage.value.trim() || !selectedCharacter.value) return;
  
  const message = newMessage.value.trim();
  newMessage.value = '';
  
  await characterStore.sendMessage(message);
};

const toggleRecording = async () => {
  if (!selectedCharacter.value) {
    return;
  }
  
  if (isRecording.value) {
    // 停止录制
    try {
      const text = await characterStore.stopVoiceRecognition(voiceSessionId.value);
      newMessage.value = text;
    } catch (error) {
      console.error('语音识别失败:', error);
    } finally {
      isRecording.value = false;
    }
  } else {
    // 开始录制
    try {
      const id = await characterStore.startVoiceRecognition();
      voiceSessionId.value = id;
      isRecording.value = true;
    } catch (error) {
      console.error('开始语音识别失败:', error);
    }
  }
};

const resetSearch = () => {
  searchQuery.value = '';
  selectedCategory.value = 'all';
  loadCharacters();
};

const formatTime = (date: Date) => {
  return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
};
</script>

<style scoped>
:root {
  /* 现代化颜色方案 */
  --primary-color: #6366f1;
  --primary-hover: #4f46e5;
  --secondary-color: #8b5cf6;
  --tertiary-color: #ec4899;
  --text-primary: #1f2937;
  --text-secondary: #6b7280;
  --text-muted: #9ca3af;
  --bg: #f9fafb;
  --card: #ffffff;
  --border: #e5e7eb;
  --radius-sm: 8px;
  --radius-md: 16px;
  --radius-lg: 24px;
  --radius-full: 9999px;
  --shadow: 0 1px 3px rgba(0, 0, 0, 0.1), 0 1px 2px rgba(0, 0, 0, 0.06);
  --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
  --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
  
  /* 动画时长 */
  --transition-fast: 0.2s ease;
  --transition-normal: 0.3s ease;
  --transition-slow: 0.5s ease;
}

.chat-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: var(--bg);
  background-image: 
    radial-gradient(circle at 10% 20%, rgba(99, 102, 241, 0.05) 0%, transparent 20%),
    radial-gradient(circle at 80% 60%, rgba(236, 72, 153, 0.05) 0%, transparent 25%);
}

.chat-header {
  background: linear-gradient(135deg, var(--primary-color), var(--tertiary-color));
  color: white;
  padding: 1rem 0;
  box-shadow: var(--shadow-md);
  position: relative;
  overflow: hidden;
}

.chat-header::before {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
  animation: floating 8s ease-in-out infinite;
}

@keyframes floating {
  0%, 100% {
    transform: translate(0, 0) rotate(0deg);
  }
  25% {
    transform: translate(5%, 5%) rotate(5deg);
  }
  50% {
    transform: translate(0, 10%) rotate(0deg);
  }
  75% {
    transform: translate(-5%, 5%) rotate(-5deg);
  }
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1.5rem;
}

.logo {
  display: flex;
  align-items: center;
  color: white;
  text-decoration: none;
}

.logo-icon {
  font-size: 2rem;
  margin-right: 0.75rem;
}

.logo-title {
  font-size: 1.5rem;
  font-weight: 600;
  margin: 0;
}

.header-actions {
  display: flex;
  gap: 1rem;
}

.btn {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: var(--radius-full);
  font-weight: 500;
  cursor: pointer;
  transition: all var(--transition-normal);
  font-size: 0.875rem;
  position: relative;
  overflow: hidden;
  z-index: 1;
}

.btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(45deg, transparent 0%, rgba(255,255,255,0.1) 50%, transparent 100%);
  transform: translateX(-100%);
  transition: transform var(--transition-fast);
  z-index: -1;
}

.btn:hover::before {
  transform: translateX(100%);
}

.btn-primary {
  background-color: var(--primary-color);
  color: white;
}

.btn-primary:hover {
  background-color: var(--primary-hover);
  transform: translateY(-1px);
  box-shadow: var(--shadow-md);
}

.btn-secondary {
  background-color: rgba(255, 255, 255, 0.2);
  color: white;
  backdrop-filter: blur(4px);
  border: 1px solid rgba(255, 255, 255, 0.3);
}

.btn-secondary:hover {
  background-color: rgba(255, 255, 255, 0.3);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.chat-main {
  flex: 1;
  max-width: 1200px;
  width: 100%;
  margin: 0 auto;
  padding: 2rem 1.5rem;
  display: flex;
  flex-direction: column;
}

/* 角色选择面板 */
.character-panel {
  background-color: var(--card);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-md);
  padding: 2rem;
  height: 100%;
  backdrop-filter: blur(8px);
  background: rgba(255, 255, 255, 0.95);
  border: 1px solid rgba(229, 231, 235, 0.5);
}

.panel-header {
  margin-bottom: 2rem;
}

.panel-header h2 {
  font-size: 1.75rem;
  color: var(--text-primary);
  margin-bottom: 1.5rem;
  text-align: center;
}

.search-container {
  display: flex;
  max-width: 500px;
  margin: 0 auto;
}

.search-input {
  flex: 1;
  padding: 0.75rem 1rem;
  border: 1px solid var(--border);
  border-radius: var(--radius-md) 0 0 var(--radius-md);
  font-size: 1rem;
  outline: none;
  transition: border-color 0.3s ease;
}

.search-input:focus {
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1);
}

.search-btn {
  padding: 0 1.25rem;
  background-color: var(--primary-color);
  color: white;
  border: none;
  border-radius: 0 var(--radius-md) var(--radius-md) 0;
  cursor: pointer;
  transition: background-color 0.3s ease;
  font-size: 1.25rem;
}

.search-btn:hover {
  background-color: var(--primary-hover);
}

.character-categories {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
  justify-content: center;
  margin-bottom: 2rem;
}

.category-btn {
  padding: 0.5rem 1rem;
  background-color: var(--bg);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 0.875rem;
}

.category-btn:hover {
  background-color: var(--border);
}

.category-btn.active {
  background-color: var(--primary-color);
  color: white;
  border-color: var(--primary-color);
}

.characters-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
  max-height: calc(100vh - 350px);
  overflow-y: auto;
}

.character-card {
  background-color: var(--bg);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  padding: 1.5rem;
  cursor: pointer;
  transition: all var(--transition-normal);
  display: flex;
  align-items: center;
  gap: 1rem;
  position: relative;
  overflow: hidden;
}

.character-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(99, 102, 241, 0.1), transparent);
  transition: left var(--transition-slow);
}

.character-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
  border-color: var(--primary-color);
}

.character-card:hover::before {
  left: 100%;
}

.character-avatar {
  font-size: 3rem;
  background: linear-gradient(135deg, rgba(99, 102, 241, 0.1), rgba(236, 72, 153, 0.1));
  width: 60px;
  height: 60px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  transition: transform var(--transition-normal);
}

.character-card:hover .character-avatar {
  transform: scale(1.1) rotate(5deg);
}

.character-info {
  flex: 1;
}

.character-name {
  font-size: 1.25rem;
  color: var(--text-primary);
  margin: 0 0 0.5rem 0;
}

.character-description {
  font-size: 0.875rem;
  color: var(--text-secondary);
  margin: 0;
}

/* 聊天界面 */
.chat-interface {
  display: flex;
  flex-direction: column;
  height: calc(100vh - 120px);
}

.chat-header-info {
  background-color: var(--card);
  border-radius: var(--radius-lg) var(--radius-lg) 0 0;
  box-shadow: var(--shadow);
  padding: 1.5rem;
  display: flex;
  align-items: center;
  gap: 1.5rem;
  border-bottom: 1px solid var(--border);
}

.character-avatar-large {
  font-size: 4rem;
  background-color: rgba(79, 70, 229, 0.1);
  width: 80px;
  height: 80px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.character-details h2 {
  font-size: 1.5rem;
  color: var(--text-primary);
  margin: 0 0 0.5rem 0;
}

.character-details p {
  font-size: 0.875rem;
  color: var(--text-secondary);
  margin: 0;
}

.chat-actions {
  margin-left: auto;
}

.chat-messages {
  flex: 1;
  background-color: var(--card);
  padding: 1.5rem;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.message {
  max-width: 70%;
  padding: 0.75rem 1rem;
  border-radius: var(--radius-md);
  position: relative;
  animation: slideIn 0.3s ease;
  word-wrap: break-word;
  line-height: 1.5;
  box-shadow: var(--shadow);
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.message.user {
  align-self: flex-end;
  background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
  color: white;
  border-radius: var(--radius-md) 4px var(--radius-md) var(--radius-md);
}

.message.ai {
  align-self: flex-start;
  background-color: var(--bg);
  color: var(--text-primary);
  border: 1px solid var(--border);
  border-radius: 4px var(--radius-md) var(--radius-md) var(--radius-md);
}

.message-content {
  font-size: 1rem;
  line-height: 1.5;
}

.message-time {
  font-size: 0.75rem;
  opacity: 0.7;
  margin-top: 0.25rem;
  text-align: right;
  font-weight: 500;
  letter-spacing: 0.5px;
}

.chat-input-container {
  background-color: var(--card);
  border-radius: 0 0 var(--radius-lg) var(--radius-lg);
  box-shadow: 0 -4px 12px rgba(0, 0, 0, 0.05);
  padding: 1.5rem;
  border-top: 1px solid var(--border);
  position: relative;
}

.chat-input-container::before {
  content: '';
  position: absolute;
  top: -10px;
  left: 50%;
  transform: translateX(-50%);
  width: 80%;
  height: 10px;
  background: linear-gradient(to bottom, transparent, rgba(0, 0, 0, 0.02));
  border-radius: 50%;
}

.input-wrapper {
  display: flex;
  gap: 0.5rem;
  align-items: center;
  max-width: 100%;
  background: var(--bg);
  border: 1px solid var(--border);
  border-radius: var(--radius-full);
  padding: 0.25rem;
  box-shadow: var(--shadow);
  transition: all var(--transition-normal);
}

.input-wrapper:focus-within {
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
}

.message-input {
  flex: 1;
  padding: 0.75rem 1rem;
  border: none;
  border-radius: var(--radius-full);
  font-size: 1rem;
  outline: none;
  background: transparent;
  min-width: 0;
}

.message-input:focus {
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1);
}

.input-actions {
  display: flex;
  gap: 0.5rem;
}

.voice-btn, .send-btn {
  width: 44px;
  height: 44px;
  border: none;
  border-radius: 50%;
  cursor: pointer;
  transition: all var(--transition-normal);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.25rem;
  flex-shrink: 0;
  position: relative;
  overflow: hidden;
}

.voice-btn::before, .send-btn::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 0;
  height: 0;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.3);
  transform: translate(-50%, -50%);
  transition: width var(--transition-slow), height var(--transition-slow);
}

.voice-btn:hover::before, .send-btn:hover::before {
  width: 80px;
  height: 80px;
}

.voice-btn {
  background-color: var(--bg);
  border: 1px solid var(--border);
  color: var(--text-primary);
}

.voice-btn:hover {
  background-color: var(--border);
  transform: scale(1.05);
}

.voice-btn.recording {
  background-color: #ef4444;
  color: white;
  border-color: #ef4444;
  animation: pulse 1.5s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% {
    transform: scale(1);
    box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.4);
  }
  50% {
    transform: scale(1.05);
    box-shadow: 0 0 0 10px rgba(239, 68, 68, 0);
  }
}

.send-btn {
  background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
  color: white;
}

.send-btn:hover:not(:disabled) {
  background: linear-gradient(135deg, var(--primary-hover), var(--secondary-color));
  transform: translateY(-1px) scale(1.05);
  box-shadow: var(--shadow-md);
}

.send-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* 过渡动画 */
.slide-up-enter-active,
.slide-up-leave-active {
  transition: transform 0.3s ease, opacity 0.3s ease;
}

.slide-up-enter-from,
.slide-up-leave-to {
  transform: translateY(-20px);
  opacity: 0;
}

/* 错误提示 */
.error-banner {
  background-color: #fecaca;
  color: #991b1b;
  padding: 0.75rem 1.5rem;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 0.875rem;
  border-bottom: 1px solid #fca5a5;
  position: relative;
  z-index: 100;
}

.error-icon {
  font-size: 1.25rem;
}

.error-close {
  margin-left: auto;
  background: none;
  border: none;
  font-size: 1.25rem;
  cursor: pointer;
  color: #991b1b;
  padding: 0;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* 加载状态 */
.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 1rem;
  text-align: center;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 3px solid var(--border);
  border-top: 3px solid var(--primary-color);
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.loading-container p {
  color: var(--text-secondary);
  font-size: 0.875rem;
}

/* 空状态 */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 1rem;
  text-align: center;
}

.empty-icon {
  font-size: 4rem;
  margin-bottom: 1.5rem;
  opacity: 0.5;
}

.empty-state h3 {
  font-size: 1.25rem;
  color: var(--text-primary);
  margin-bottom: 0.5rem;
}

.empty-state p {
  color: var(--text-secondary);
  font-size: 0.875rem;
  margin-bottom: 1.5rem;
  max-width: 300px;
}

/* 欢迎消息 */
.welcome-message {
  text-align: center;
  padding: 3rem 1rem;
  color: var(--text-secondary);
}

.welcome-message p {
  font-size: 1.125rem;
  margin-bottom: 0.5rem;
}

.welcome-subtext {
  font-size: 0.875rem;
  opacity: 0.8;
}

/* 输入中指示器 */
.message.typing {
  min-height: 40px;
  display: flex;
  align-items: center;
  padding: 0.75rem 1rem;
}

.typing-indicator {
  display: flex;
  gap: 6px;
  align-items: center;
  padding: 0.5rem 0;
}

.typing-dot {
  width: 8px;
  height: 8px;
  background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
  border-radius: 50%;
  animation: typing 1.4s infinite ease-in-out both;
  box-shadow: 0 0 8px rgba(99, 102, 241, 0.5);
}

.typing-dot:nth-child(1) {
  animation-delay: 0s;
}

.typing-dot:nth-child(2) {
  animation-delay: 0.2s;
}

.typing-dot:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes typing {
  0%, 80%, 100% {
    transform: scale(0);
    opacity: 0.3;
  }
  40% {
    transform: scale(1);
    opacity: 1;
  }
}

/* 录音指示器 */
  .recording-indicator {
  display: none;
  font-size: 0.75rem;
  margin-left: 0.25rem;
  animation: blink 1s infinite;
  font-weight: 500;
}

.voice-btn.recording .recording-indicator {
  display: inline;
}

@keyframes blink {
  0%, 50% {
    opacity: 1;
  }
  51%, 100% {
    opacity: 0;
  }
}

/* 禁用状态样式 */
:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .header-content {
    padding: 0 1rem;
  }
  
  .chat-main {
    padding: 1rem;
  }
  
  .characters-grid {
    grid-template-columns: 1fr;
  }
  
  .message {
    max-width: 85%;
  }
  
  .chat-header-info {
    flex-direction: column;
    text-align: center;
    gap: 1rem;
  }
  
  .chat-actions {
    margin-left: 0;
    width: 100%;
  }
  
  .error-banner {
    padding: 0.5rem 1rem;
    font-size: 0.75rem;
  }
  
  .input-wrapper {
    padding: 0.2rem;
  }
  
  .voice-btn, .send-btn {
    width: 40px;
    height: 40px;
    font-size: 1.1rem;
  }
}

/* 深色模式支持 */
@media (prefers-color-scheme: dark) {
  :root {
    --bg: #1a1a2e;
    --card: #16213e;
    --border: #0f3460;
    --text-primary: #f5f5f5;
    --text-secondary: #b0b0b0;
  }
  
  .character-card {
    background-color: rgba(22, 33, 62, 0.7);
    border-color: var(--border);
  }
  
  .message.ai {
    background-color: rgba(22, 33, 62, 0.7);
  }
  
  .chat-input-container {
    background-color: var(--card);
    border-top-color: var(--border);
  }
  
  .input-wrapper {
    background-color: rgba(22, 33, 62, 0.7);
    border-color: var(--border);
  }
  
  .voice-btn {
    background-color: rgba(22, 33, 62, 0.7);
    border-color: var(--border);
    color: var(--text-primary);
  }
  
  .voice-btn:hover {
    background-color: var(--border);
  }
  
  .search-input {
    background-color: rgba(22, 33, 62, 0.7);
    border-color: var(--border);
    color: var(--text-primary);
  }
  
  .search-input::placeholder {
    color: var(--text-muted);
  }
  
  .message-input {
    color: var(--text-primary);
  }
  
  .message-input::placeholder {
    color: var(--text-muted);
  }
  
  .category-btn {
    background-color: rgba(22, 33, 62, 0.7);
    border-color: var(--border);
    color: var(--text-primary);
  }
  
  .category-btn:hover {
    background-color: var(--border);
  }
  
  .typing-dot {
    background: linear-gradient(135deg, var(--tertiary-color), var(--secondary-color));
  }
}
</style>