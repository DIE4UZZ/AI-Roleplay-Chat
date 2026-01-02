<template>
  <div class="chat-container">
    <!-- 顶部导航 -->
    <header class="chat-header">
      <div class="container">
        <div class="header-content">
          <button class="btn btn-primary" @click="handleBack" style="margin-right: 1rem; padding: 0.75rem 1.5rem; font-weight: 600;">
            ← 返回首页
          </button>
          <router-link to="/" class="logo">
            <div class="logo-icon">🎭</div>
            <div class="logo-text">
              <h1 class="logo-title">角色对话</h1>
            </div>
          </router-link>
        </div>
      </div>
    </header>

    <!-- 错误提示 -->
    <Transition name="fade-up">
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
          <button class="btn btn-primary" @click="resetSearch">重置搜索</button>
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
            <button class="btn btn-primary" @click="changeCharacter">
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
                {{ characterStore.isLoading ? '🔄' : '→' }}
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
/* 全局样式 */
.chat-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: var(--bg-primary);
  color: var(--text-primary);
  overflow-x: hidden;
  position: relative;
}

/* 装饰性背景 */
.chat-container::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-image: 
    radial-gradient(circle at 15% 25%, rgba(99, 102, 241, 0.08) 0%, transparent 30%),
    radial-gradient(circle at 85% 65%, rgba(236, 72, 153, 0.08) 0%, transparent 35%),
    radial-gradient(circle at 50% 50%, rgba(139, 92, 246, 0.05) 0%, transparent 50%);
  pointer-events: none;
  z-index: 0;
}

.container {
  max-width: var(--container-width);
  margin: 0 auto;
  padding: 0 var(--spacing-md);
}

/* 顶部导航 */
.chat-header {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  position: sticky;
  top: 0;
  z-index: 100;
  border-bottom: 1px solid rgba(229, 231, 235, 0.8);
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
}

.chat-header:hover {
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.08), 0 2px 4px -1px rgba(0, 0, 0, 0.05);
}

.header-content {
  height: 72px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.logo {
  display: flex;
  align-items: center;
  gap: 12px;
  text-decoration: none;
  transition: all 0.3s ease;
  padding: 8px 0;
}

.logo:hover {
  transform: translateY(-2px);
}

.logo-icon {
  font-size: 28px;
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.1));
  transition: all 0.3s ease;
}

.logo:hover .logo-icon {
  transform: rotate(10deg) scale(1.1);
}

.logo-title {
  font-size: 20px;
  font-weight: 700;
  margin: 0;
  background: linear-gradient(135deg, var(--primary), var(--secondary));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  letter-spacing: -0.025em;
  transition: all 0.3s ease;
}

/* 主内容区域 */
.chat-main {
  flex: 1;
  max-width: 1200px;
  width: 100%;
  margin: 0 auto;
  padding: 2rem 1.5rem;
  display: flex;
  flex-direction: column;
  position: relative;
  z-index: 1;
}

/* 角色选择面板 */
.character-panel {
  background: var(--bg-primary);
  border: 1px solid var(--border-color);
  border-radius: 16px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
  padding: 2.5rem;
  height: 100%;
  animation: fadeInUp 0.6s ease-out;
  transition: all 0.3s ease;
}

.character-panel:hover {
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
  transform: translateY(-4px);
  border-color: var(--primary-light);
}

.panel-header {
  margin-bottom: 2.5rem;
  text-align: center;
}

.panel-header h2 {
  font-size: 2.5rem;
  color: var(--text-primary);
  margin-bottom: 1rem;
  font-weight: 700;
  background: linear-gradient(135deg, var(--primary), var(--secondary));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  letter-spacing: -0.03em;
}

.search-container {
  display: flex;
  max-width: 600px;
  margin: 0 auto;
  background: var(--bg-primary);
  border: 1px solid var(--border-color);
  border-radius: 9999px;
  overflow: hidden;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
  transition: all 0.3s ease;
}

.search-container:focus-within {
  border-color: var(--primary);
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
}

.search-input {
  flex: 1;
  padding: 1rem 1.5rem;
  border: none;
  background: transparent;
  font-size: 1rem;
  outline: none;
  color: var(--text-primary);
  font-weight: 500;
}

.search-input::placeholder {
  color: var(--text-secondary);
  font-weight: 400;
}

.search-btn {
  padding: 0 1.5rem;
  background: linear-gradient(135deg, var(--primary), var(--primary-dark));
  color: white;
  border: none;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 1.2rem;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
}

.search-btn:hover:not(:disabled) {
  background: linear-gradient(135deg, var(--primary-dark), var(--primary-darker));
  transform: scale(1.05);
  box-shadow: 0 8px 25px rgba(99, 102, 241, 0.4);
}

.search-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.character-categories {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
  justify-content: center;
  margin-bottom: 2rem;
}

.category-btn {
  padding: 0.75rem 1.5rem;
  background: var(--bg-primary);
  border: 1px solid var(--border-color);
  border-radius: 9999px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--text-primary);
}

.category-btn:hover:not(:disabled) {
  background: var(--bg-secondary);
  transform: translateY(-2px);
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
}

.category-btn.active {
  background: linear-gradient(135deg, var(--primary), var(--primary-dark));
  color: white;
  border-color: var(--primary);
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
}

.category-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.characters-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 1.5rem;
  max-height: calc(100vh - 400px);
  overflow-y: auto;
  padding: 1rem 0;
}

/* 角色卡片 */
.character-card {
  background: var(--bg-primary);
  border: 1px solid var(--border-color);
  border-radius: 16px;
  padding: 1.75rem;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 1.25rem;
  position: relative;
  overflow: hidden;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
}

.character-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(99, 102, 241, 0.1), transparent);
  transition: left 0.5s ease;
}

.character-card:hover {
  transform: translateY(-4px) scale(1.02);
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
  border-color: var(--primary-light);
}

.character-card:hover::before {
  left: 100%;
}

.character-avatar {
  font-size: 3rem;
  background: linear-gradient(135deg, var(--primary), var(--secondary));
  width: 70px;
  height: 70px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  transition: all 0.3s ease;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
  color: white;
}

.character-card:hover .character-avatar {
  transform: scale(1.15) rotate(8deg);
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
}

.character-info {
  flex: 1;
}

.character-name {
  font-size: 1.375rem;
  color: var(--text-primary);
  margin: 0 0 0.5rem 0;
  font-weight: 700;
  letter-spacing: -0.025em;
}

.character-description {
  font-size: 0.9375rem;
  color: var(--text-secondary);
  margin: 0;
  line-height: 1.5;
  font-weight: 400;
}

/* 聊天界面 */
.chat-interface {
  display: flex;
  flex-direction: column;
  height: calc(100vh - 120px);
  background: var(--bg-primary);
  border: 1px solid var(--border-color);
  border-radius: 16px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
  overflow: hidden;
  animation: fadeInUp 0.6s ease-out;
  transition: all 0.3s ease;
}

.chat-interface:hover {
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
  border-color: var(--primary-light);
}

/* 聊天头部 */
.chat-header-info {
  background: linear-gradient(135deg, var(--bg-primary) 0%, var(--bg-secondary) 100%);
  padding: 2rem;
  display: flex;
  align-items: center;
  gap: 1.5rem;
  border-bottom: 1px solid var(--border-color);
  transition: all 0.3s ease;
}

.character-avatar-large {
  font-size: 3.5rem;
  background: linear-gradient(135deg, var(--primary), var(--secondary));
  width: 80px;
  height: 80px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
  color: white;
  animation: float 3s ease-in-out infinite;
}

.character-details h2 {
  font-size: 1.75rem;
  color: var(--text-primary);
  margin: 0 0 0.5rem 0;
  font-weight: 700;
  letter-spacing: -0.025em;
}

.character-details p {
  font-size: 1rem;
  color: var(--text-secondary);
  margin: 0;
  line-height: 1.5;
}

.chat-actions {
  margin-left: auto;
  display: flex;
  flex-shrink: 0;
}

/* 聊天消息 */
.chat-messages {
  flex: 1;
  background: var(--bg-secondary);
  padding: 2rem;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
  transition: all 0.3s ease;
}

/* 消息样式 */
.message {
  max-width: 75%;
  padding: 1rem 1.25rem;
  border-radius: 16px;
  position: relative;
  animation: fadeInUp 0.4s ease-out;
  word-wrap: break-word;
  line-height: 1.6;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 1px solid var(--border-color);
}

.message.user {
  align-self: flex-end;
  background: linear-gradient(135deg, var(--primary), var(--primary-dark));
  color: white;
  border-radius: 1rem 0.5rem 1rem 1rem;
  font-weight: 500;
}

.message.ai {
  align-self: flex-start;
  background: var(--bg-primary);
  color: var(--text-primary);
  border-radius: 0.5rem 1rem 1rem 1rem;
}

.message-content {
  font-size: 1rem;
  line-height: 1.5;
  margin-bottom: 0.5rem;
}

.message-time {
  font-size: 0.75rem;
  opacity: 0.7;
  text-align: right;
  font-weight: 500;
  letter-spacing: 0.5px;
}

/* 欢迎消息 */
.welcome-message {
  text-align: center;
  padding: 3rem 1rem;
  color: var(--text-secondary);
  animation: fadeInUp 0.6s ease-out;
}

.welcome-message p {
  font-size: 1.125rem;
  margin-bottom: 0.5rem;
  color: var(--text-primary);
  font-weight: 500;
}

.welcome-subtext {
  font-size: 0.875rem;
  opacity: 0.8;
  color: var(--text-secondary);
  font-weight: 400;
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
  align-items: center;
  gap: 0.375rem;
  padding: 1rem 1.25rem;
  background: var(--bg-primary);
  border: 1px solid var(--border-color);
  border-radius: 16px;
  margin-right: auto;
  animation: fadeInUp 0.4s ease-out;
  border-radius: 0.5rem 1rem 1rem 1rem;
}

.typing-dot {
  width: 8px;
  height: 8px;
  background: linear-gradient(135deg, var(--primary), var(--primary-light));
  border-radius: 50%;
  animation: typing 1.4s infinite ease-in-out;
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

/* 聊天输入 */
.chat-input-container {
  background: var(--bg-primary);
  padding: 1.5rem 2rem;
  border-top: 1px solid var(--border-color);
  display: flex;
  gap: 1rem;
  align-items: flex-end;
  transition: all 0.3s ease;
}

.input-wrapper {
  display: flex;
  gap: 0.5rem;
  align-items: center;
  max-width: 100%;
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  border-radius: 9999px;
  padding: 0.25rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
  transition: all 0.3s ease;
  flex: 1;
}

.input-wrapper:focus-within {
  border-color: var(--primary);
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
}

.message-input {
  flex: 1;
  background: var(--bg-primary);
  border: 1px solid var(--border-color);
  border-radius: 9999px;
  padding: 1rem 1.25rem;
  color: var(--text-primary);
  font-size: 1rem;
  resize: none;
  min-height: 3rem;
  max-height: 10rem;
  outline: none;
  transition: all 0.3s ease;
  font-weight: 500;
}

.message-input:focus {
  border-color: var(--primary);
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
}

.message-input::placeholder {
  color: var(--text-secondary);
  font-weight: 400;
}

.input-actions {
  display: flex;
  gap: 0.5rem;
}

.voice-btn, .send-btn {
  width: 44px;
  height: 44px;
  border: 1px solid var(--border-color);
  border-radius: 50%;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.25rem;
  flex-shrink: 0;
  position: relative;
  overflow: hidden;
  background: var(--bg-primary);
  color: var(--text-primary);
  font-weight: 600;
}

.voice-btn:hover:not(:disabled) {
  background: var(--bg-secondary);
  transform: scale(1.05);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
}

.voice-btn.recording {
  background: var(--error);
  color: white;
  border-color: var(--error);
  animation: pulse 1.5s ease-in-out infinite;
}

.send-btn {
  background: linear-gradient(135deg, var(--primary), var(--primary-dark));
  color: white;
  border: none;
}

.send-btn:hover:not(:disabled) {
  background: linear-gradient(135deg, var(--primary-dark), var(--primary-darker));
  transform: translateY(-2px) scale(1.05);
  box-shadow: 0 8px 25px rgba(99, 102, 241, 0.4);
}

.send-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
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

/* 错误提示 */
.error-banner {
  background: var(--error-bg);
  color: var(--error);
  padding: 0.75rem 1.5rem;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 0.875rem;
  border-bottom: 1px solid var(--error-border);
  position: relative;
  z-index: 100;
  animation: slideIn 0.4s ease-out;
  font-weight: 500;
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
  color: var(--error);
  padding: 0;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: all 0.3s ease;
}

.error-close:hover {
  background: var(--error);
  color: white;
  transform: scale(1.1);
}

/* 加载状态 */
.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 1rem;
  text-align: center;
  animation: fadeInUp 0.6s ease-out;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 3px solid var(--border-color);
  border-top: 3px solid var(--primary);
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 1rem;
}

.loading-container p {
  color: var(--text-secondary);
  font-size: 0.875rem;
  font-weight: 500;
}

/* 空状态 */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 1rem;
  text-align: center;
  animation: fadeInUp 0.6s ease-out;
}

.empty-icon {
  font-size: 4rem;
  margin-bottom: 1.5rem;
  opacity: 0.5;
  background: linear-gradient(135deg, var(--primary), var(--secondary));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.empty-state h3 {
  font-size: 1.25rem;
  color: var(--text-primary);
  margin-bottom: 0.5rem;
  font-weight: 700;
  letter-spacing: -0.025em;
}

.empty-state p {
  color: var(--text-secondary);
  font-size: 0.875rem;
  margin-bottom: 1.5rem;
  max-width: 300px;
  line-height: 1.5;
}

/* 按钮样式 */
.btn {
  border: 2px solid transparent;
  padding: 0.75rem 1.5rem;
  border-radius: 9999px;
  font-weight: 600;
  font-size: 0.875rem;
  transition: all 0.3s ease;
  cursor: pointer;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
  min-width: 120px;
  gap: 8px;
  letter-spacing: 0.025em;
  z-index: 1;
}

.btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
  transition: all 0.5s ease;
  z-index: -1;
}

.btn:hover::before {
  left: 100%;
}

.btn span {
  position: relative;
  z-index: 1;
}

.btn-primary {
  background: linear-gradient(135deg, var(--primary), var(--primary-dark));
  color: white;
  box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
  border-color: var(--primary-light);
}

.btn-primary:hover {
  background: linear-gradient(135deg, var(--primary-dark), var(--primary-darker));
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(99, 102, 241, 0.4);
  border-color: var(--primary);
}

.btn-primary:active {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
}

.btn-secondary {
  background: var(--bg-primary);
  color: var(--text-primary);
  border-color: var(--border-color);
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
}

.btn-secondary:hover {
  background: var(--bg-secondary);
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
  border-color: var(--primary-light);
}

.btn-secondary:active {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

/* 动画效果 */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes fadeInLeft {
  from {
    opacity: 0;
    transform: translateX(-30px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

@keyframes fadeInRight {
  from {
    opacity: 0;
    transform: translateX(30px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

@keyframes float {
  0%, 100% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-20px);
  }
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

@keyframes typing {
  0%, 60%, 100% {
    opacity: 0.4;
    transform: scale(1);
  }
  30% {
    opacity: 1;
    transform: scale(1.2);
  }
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
    transform: scale(1);
    box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.4);
  }
  50% {
    opacity: 0.8;
    transform: scale(1.05);
    box-shadow: 0 0 0 10px rgba(239, 68, 68, 0);
  }
}

@keyframes blink {
  0%, 50% {
    opacity: 1;
  }
  51%, 100% {
    opacity: 0;
  }
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 过渡动画 */
.fade-up-enter-active, .fade-up-leave-active {
  transition: all 0.6s cubic-bezier(0.25, 0.1, 0.25, 1);
}

.fade-up-enter-from, .fade-up-leave-to {
  opacity: 0;
  transform: translateY(30px);
}

/* 滚动条样式 */
.characters-grid::-webkit-scrollbar,
.chat-messages::-webkit-scrollbar {
  width: 8px;
}

.characters-grid::-webkit-scrollbar-track,
.chat-messages::-webkit-scrollbar-track {
  background: var(--bg-secondary);
  border-radius: 4px;
}

.characters-grid::-webkit-scrollbar-thumb,
.chat-messages::-webkit-scrollbar-thumb {
  background: linear-gradient(135deg, var(--primary), var(--primary-light));
  border-radius: 4px;
  border: 2px solid var(--bg-secondary);
}

.characters-grid::-webkit-scrollbar-thumb:hover,
.chat-messages::-webkit-scrollbar-thumb:hover {
  background: linear-gradient(135deg, var(--primary-dark), var(--primary));
}

/* 响应式设计 */
@media (max-width: 1024px) {
  .character-panel {
    padding: 1.5rem;
  }
  
  .panel-header h2 {
    font-size: 2rem;
  }
  
  .characters-grid {
    grid-template-columns: 1fr 1fr;
  }
  
  .search-container {
    width: 90%;
  }
}

@media (max-width: 768px) {
  .chat-main {
    padding: 1rem;
  }
  
  .character-panel {
    padding: 1rem;
  }
  
  .panel-header h2 {
    font-size: 1.5rem;
    margin-bottom: 1rem;
  }
  
  .characters-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
  
  .character-card {
    padding: 1.25rem;
  }
  
  .character-name {
    font-size: 1.25rem;
  }
  
  .character-description {
    font-size: 0.875rem;
  }
  
  .message {
    max-width: 85%;
    padding: 0.75rem 1rem;
  }
  
  .message-content {
    font-size: 0.875rem;
  }
  
  .chat-input-container {
    padding: 1rem;
  }
  
  .message-input {
    padding: 0.75rem 1rem;
    font-size: 0.875rem;
  }
  
  .chat-header-info {
    padding: 1.5rem;
    gap: 1rem;
  }
  
  .character-avatar-large {
    font-size: 2.5rem;
    width: 60px;
    height: 60px;
  }
  
  .character-details h2 {
    font-size: 1.5rem;
  }
  
  .character-details p {
    font-size: 0.875rem;
  }
  
  .search-container {
    flex-direction: column;
    border-radius: 16px;
    overflow: hidden;
  }
  
  .search-input {
    border-radius: 0;
    border-bottom: 1px solid var(--border-color);
  }
  
  .search-btn {
    border-radius: 0;
  }
}

@media (max-width: 576px) {
  .chat-main {
    padding: 0.5rem;
  }
  
  .character-panel {
    padding: 0.75rem;
    border-radius: 12px;
  }
  
  .panel-header h2 {
    font-size: 1.25rem;
  }
  
  .character-categories {
    gap: 0.25rem;
  }
  
  .category-btn {
    padding: 0.5rem 1rem;
    font-size: 0.75rem;
  }
  
  .character-card {
    padding: 1rem;
    flex-direction: column;
    text-align: center;
    gap: 1rem;
  }
  
  .character-avatar {
    font-size: 2.5rem;
    width: 60px;
    height: 60px;
  }
  
  .message {
    max-width: 90%;
    padding: 0.625rem 0.875rem;
  }
  
  .message-content {
    font-size: 0.875rem;
  }
  
  .message-time {
    font-size: 0.75rem;
  }
  
  .chat-input-container {
    padding: 0.75rem;
  }
  
  .input-wrapper {
    padding: 0.125rem;
  }
  
  .message-input {
    padding: 0.625rem 0.875rem;
    font-size: 0.875rem;
  }
  
  .voice-btn, .send-btn {
    width: 40px;
    height: 40px;
    font-size: 1rem;
  }
  
  .chat-header-info {
    flex-direction: column;
    text-align: center;
    padding: 1rem;
  }
  
  .chat-actions {
    margin-left: 0;
    width: 100%;
    justify-content: center;
  }
  
  .btn {
    padding: 0.625rem 1.25rem;
    font-size: 0.75rem;
    min-width: 100px;
  }
}

/* 深色模式支持 */
@media (prefers-color-scheme: dark) {
  .character-panel,
  .chat-interface,
  .message.ai,
  .chat-header-info,
  .chat-input-container,
  .input-wrapper,
  .message-input {
    background: var(--bg-primary);
    border-color: var(--border-color);
    color: var(--text-primary);
  }
  
  .character-card {
    background: var(--bg-primary);
    border-color: var(--border-color);
  }
  
  .character-card:hover {
    border-color: var(--primary-light);
  }
  
  .message-input::placeholder {
    color: var(--text-secondary);
  }
  
  .search-input {
    background: var(--bg-primary);
    color: var(--text-primary);
    border-color: var(--border-color);
  }
  
  .search-input::placeholder {
    color: var(--text-secondary);
  }
  
  .voice-btn {
    background: var(--bg-primary);
    border-color: var(--border-color);
    color: var(--text-primary);
  }
  
  .voice-btn:hover {
    background: var(--bg-secondary);
  }
  
  .category-btn {
    background: var(--bg-primary);
    border-color: var(--border-color);
    color: var(--text-primary);
  }
  
  .category-btn:hover {
    background: var(--bg-secondary);
  }
}
</style>