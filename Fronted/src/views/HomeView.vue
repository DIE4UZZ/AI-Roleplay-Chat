<template>
  <div class="home-container">
    <!-- 顶部导航 -->
    <header class="main-header">
      <div class="container">
        <div class="header-content">
          <router-link to="/" class="logo">
            <div class="logo-icon">🎭</div>
            <div class="logo-text">
              <h1 class="logo-title">AI 角色扮演</h1>
            </div>
          </router-link>

          <div class="account-actions">
            <template v-if="isLoggedIn">
              <div class="user-profile" @click="toggleProfileMenu">
                <img
                  :src="`https://api.dicebear.com/7.x/avataaars/svg?seed=${userSeed}`"
                  alt="User Avatar"
                  class="avatar"
                />
                <span class="dropdown-arrow">▼</span>
              </div>

              <Transition name="dropdown">
                <div v-if="showProfileMenu" class="profile-menu">
                  <div class="menu-header">
                    <h4>{{ userInfo?.username || '用户' }}</h4>
                    <p v-if="userInfo?.id" class="user-id">ID: {{ userInfo.id }}</p>
                  </div>
                  <div class="menu-options">
                    <button class="menu-item">
                      <span class="menu-icon">👤</span>
                      <span>个人资料</span>
                    </button>
                    <button class="menu-item">
                      <span class="menu-icon">⚙️</span>
                      <span>设置</span>
                    </button>
                    <button class="menu-item logout" @click="handleLogout">
                      <span class="menu-icon">🚪</span>
                      <span>退出登录</span>
                    </button>
                  </div>
                </div>
              </Transition>
            </template>

            <template v-else>
              <router-link to="/login" class="btn btn-primary">登录 / 注册</router-link>
            </template>
          </div>
        </div>
      </div>
    </header>

    <!-- 英雄区 -->
    <section class="hero-section">
      <div class="container">
        <div class="hero-content">
          <div class="hero-text">
            <h1 class="hero-title">
              更简单、更沉浸的
              <span class="highlight">AI 角色对话</span>
            </h1>
            <p class="hero-description">
              与个性化 AI 角色进行自然交流。开箱即用，轻量直达体验。
            </p>
            <div class="hero-cta">
              <button class="btn btn-primary start-chat-btn" @click="handleStartChat">开始对话</button>
              <button class="btn btn-secondary" @click="handleExploreCharacters">探索角色</button>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 主内容 -->
    <main class="main-content">
      <!-- 用户信息 / 游客提示 -->
      <section class="section">
        <div class="container">
          <Transition name="slide-up">
            <div v-if="isLoggedIn" class="user-card">
              <div class="user-avatar">
                <img
                  :src="`https://api.dicebear.com/7.x/avataaars/svg?seed=${userSeed}`"
                  alt="User Avatar"
                />
              </div>
              <div class="user-details">
                <h2 class="user-name">{{ userInfo?.username || '用户' }}</h2>
                <p v-if="userInfo?.id" class="user-id">用户ID: {{ userInfo.id }}</p>
              </div>
              <div class="user-actions">
                <button class="btn btn-primary" @click="handleStartChat">进入对话</button>
              </div>
            </div>

            <div v-else class="guest-banner">
              <div class="banner-content">
                <h3>游客模式</h3>
                <p>您当前有 <strong>{{ trialCount }}</strong> 次试用机会。</p>
              </div>
              <div class="banner-actions">
                <button class="btn btn-primary" @click="handleRegisterPrompt">立即注册</button>
              </div>
            </div>
          </Transition>
        </div>
      </section>

      <!-- 核心功能 -->
      <section id="features" class="section">
        <div class="container">
          <div class="section-header">
            <h2 class="section-title">核心功能</h2>
          </div>

          <div class="features-grid">
            <div class="feature-card">
              <div class="feature-icon">💬</div>
              <h3 class="feature-title">角色对话</h3>
              <p class="feature-description">选择或创建你的人设，立即开始交流。</p>
            </div>

            <div class="feature-card">
              <div class="feature-icon">✨</div>
              <h3 class="feature-title">个性化</h3>
              <p class="feature-description">自定义背景、语气与话术，贴合你的创作。</p>
            </div>

            <div class="feature-card">
              <div class="feature-icon">🔒</div>
              <h3 class="feature-title">隐私优先</h3>
              <p class="feature-description">本地与云端双重保护，数据更安心。</p>
            </div>
          </div>
        </div>
      </section>
    </main>

    <!-- 页脚 -->
    <footer class="main-footer">
      <div class="container">
        <div class="footer-content">
          <div class="footer-brand">
            <div class="logo-icon">🎭</div>
            <span>AI 角色扮演</span>
          </div>
          <div class="footer-links">
            <a href="#features">功能</a>
            <a href="#">帮助中心</a>
            <a href="#">隐私政策</a>
          </div>
          <div class="footer-copy">© 2025 AI 角色扮演</div>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount } from 'vue';
import { useRouter } from 'vue-router';
import authService from '../services/auth.service';
import { useAuthStore } from '../store/auth.store';
import type { UserInfo } from '../types/user';

const router = useRouter();
const authStore = useAuthStore();

const showProfileMenu = ref(false);

const userInfo = ref<UserInfo | null>(null);
const isLoggedIn = ref(false);
const isGuest = ref(false);
const trialCount = ref(0);
const userSeed = ref('');

// 生成用户头像种子
const generateUserSeed = (username: string) => {
  return username || Math.random().toString(36).substring(2, 15);
};

// 初始化
const initializeData = () => {
  userInfo.value = authService.getCurrentUser();
  isLoggedIn.value = authService.isLoggedIn();
  isGuest.value = authService.isGuest();
  trialCount.value = authService.getTrialCount();
  userSeed.value = generateUserSeed(userInfo.value?.username || 'guest');
};

const handleLogout = () => {
  authService.logout();
  authStore.clearUserState();
  router.push('/login');
  showProfileMenu.value = false;
};

const handleRegisterPrompt = () => {
  authService.logout();
  authStore.clearUserState();
  router.push('/login');
};

const handleStartChat = () => {
  // 直接导航到聊天页面
  router.push('/chat');
};

const handleExploreCharacters = () => {
  // 同样导航到聊天页面，用户可以在那里浏览角色
  router.push('/chat');
};

const toggleProfileMenu = () => {
  showProfileMenu.value = !showProfileMenu.value;
};

const handleClickOutside = (event: MouseEvent) => {
  const profileElement = document.querySelector('.user-profile');
  if (profileElement && !profileElement.contains(event.target as Node)) {
    showProfileMenu.value = false;
  }
};

onMounted(() => {
  initializeData();
  document.addEventListener('click', handleClickOutside);
});

onBeforeUnmount(() => {
  document.removeEventListener('click', handleClickOutside);
});
</script>

<style scoped>
:root {
  /* 现代配色方案 */
  --primary-color: #4f46e5;
  --primary-hover: #4338ca;
  --secondary-color: #6366f1;
  --text-primary: #1f2937;
  --text-secondary: #6b7280;
  --bg: #f9fafb;
  --card: #ffffff;
  --border: #e5e7eb;
  --radius-sm: 8px;
  --radius-md: 12px;
  --radius-lg: 16px;
  --shadow: 0 1px 3px rgba(0, 0, 0, 0.1), 0 1px 2px rgba(0, 0, 0, 0.06);
  --shadow-md: 0 4px 6px rgba(0, 0, 0, 0.1), 0 1px 3px rgba(0, 0, 0, 0.08);
  --shadow-lg: 0 10px 15px rgba(0, 0, 0, 0.1), 0 4px 6px rgba(0, 0, 0, 0.05);
  --transition: 0.3s ease;
}

* {
  box-sizing: border-box;
}

body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

.container {
  max-width: 1140px;
  margin: 0 auto;
  padding: 0 20px;
}

.home-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: var(--bg);
  color: var(--text-primary);
}

/* 顶部导航 */
.main-header {
  background: rgba(255, 255, 255, 0.95);
  position: sticky;
  top: 0;
  z-index: 100;
  backdrop-filter: blur(8px);
  border-bottom: 1px solid var(--border);
  transition: all var(--transition);
}

.header-content {
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.logo {
  display: flex;
  align-items: center;
  gap: 12px;
  text-decoration: none;
  transition: transform var(--transition);
}

.logo:hover {
  transform: translateY(-1px);
}

.logo-icon {
  font-size: 24px;
}

.logo-title {
  font-size: 18px;
  font-weight: 700;
  margin: 0;
  color: var(--text-primary);
}

.account-actions {
  display: flex;
  align-items: center;
  gap: 16px;
}

/* 用户头像和菜单 */
.user-profile {
  position: relative;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 4px 8px;
  border-radius: 9999px;
  transition: background-color var(--transition);
}

.user-profile:hover {
  background-color: #f3f4f6;
}

.avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid transparent;
  transition: border-color var(--transition);
}

.user-profile:hover .avatar {
  border-color: var(--primary-color);
}

.dropdown-arrow {
  font-size: 10px;
  color: var(--text-secondary);
  transition: transform var(--transition);
}

.user-profile:hover .dropdown-arrow {
  transform: rotate(180deg);
}

/* 下拉菜单 */
.profile-menu {
  position: absolute;
  top: 100%;
  right: 0;
  margin-top: 8px;
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-lg);
  width: 240px;
  overflow: hidden;
  transform: translateY(4px);
  opacity: 0;
  visibility: hidden;
  transition: all var(--transition);
}

.dropdown-enter-active {
  transform: translateY(0);
  opacity: 1;
  visibility: visible;
}

.menu-header {
  padding: 16px;
  border-bottom: 1px solid var(--border);
  background-color: #f9fafb;
}

.menu-header h4 {
  margin: 0;
  font-size: 14px;
  font-weight: 600;
}

.user-id {
  margin: 4px 0 0;
  font-size: 12px;
  color: var(--text-secondary);
}

.menu-options {
  padding: 4px;
}

.menu-item {
  width: 100%;
  background: transparent;
  border: 0;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 16px;
  border-radius: var(--radius-sm);
  font-size: 14px;
  transition: all var(--transition);
  text-align: left;
}

.menu-item:hover {
  background-color: #f3f4f6;
  transform: translateX(2px);
}

.menu-item.logout {
  color: #ef4444;
}

.menu-item.logout:hover {
  background-color: #fee2e2;
}

/* 英雄区 */
.hero-section {
  background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
  border-bottom: 1px solid var(--border);
  padding: 80px 0;
}

.hero-content {
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  max-width: 800px;
  margin: 0 auto;
}

.hero-text {
  animation: fadeInUp 0.6s ease-out;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.hero-title {
  font-size: 42px;
  line-height: 1.1;
  margin: 0 0 24px;
  font-weight: 800;
  letter-spacing: -0.025em;
}

.highlight {
  color: var(--primary-color);
  position: relative;
}

.highlight::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 4px;
  background-color: var(--primary-color);
  opacity: 0.2;
  border-radius: 4px;
}

.hero-description {
  margin: 0 auto 32px;
  color: var(--text-secondary);
  font-size: 18px;
  line-height: 1.6;
}

.hero-cta {
  display: flex;
  gap: 16px;
  justify-content: center;
  flex-wrap: wrap;
}

/* 按钮样式 */
.btn {
  border: 1px solid transparent;
  padding: 12px 24px;
  border-radius: var(--radius-md);
  font-weight: 600;
  font-size: 16px;
  transition: all var(--transition);
  cursor: pointer;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
}

.btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
  transition: all 0.6s ease;
}

.btn:hover::before {
  left: 100%;
}

.btn-primary {
  background: var(--primary-color);
  color: #fff;
  box-shadow: var(--shadow-md);
}

.btn-primary:hover {
  background: var(--primary-hover);
  transform: translateY(-2px);
  box-shadow: var(--shadow-lg);
}

.btn-secondary {
  background: transparent;
  border-color: var(--secondary-color);
  color: var(--secondary-color);
}

.btn-secondary:hover {
  background: var(--secondary-color);
  color: #fff;
  transform: translateY(-2px);
}

/* 主内容 */
.main-content {
  flex: 1;
  padding: 60px 0 40px;
}

.section {
  margin-bottom: 60px;
}

/* 用户卡片 / 游客提示 */
.user-card, .guest-banner {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow);
  padding: 24px;
  display: flex;
  align-items: center;
  gap: 20px;
  justify-content: space-between;
  transition: all var(--transition);
}

.user-card:hover, .guest-banner:hover {
  box-shadow: var(--shadow-md);
  transform: translateY(-2px);
}

.user-card {
  flex-wrap: wrap;
}

.user-avatar img {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  object-fit: cover;
  border: 3px solid #f3f4f6;
}

.user-details {
  min-width: 200px;
}

.user-name {
  margin: 0 0 6px;
  font-size: 20px;
  font-weight: 700;
}

.user-id {
  margin: 0;
  color: var(--text-secondary);
  font-size: 14px;
}

.user-actions {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.guest-banner {
  flex-wrap: wrap;
}

.banner-content h3 {
  margin: 0 0 8px;
  font-size: 18px;
  font-weight: 700;
}

.banner-content p {
  margin: 0;
  color: var(--text-secondary);
  font-size: 16px;
}

.banner-actions {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

/* 功能区块 */
.section-header {
  text-align: center;
  margin-bottom: 40px;
}

.section-title {
  margin: 0;
  font-size: 30px;
  font-weight: 800;
  letter-spacing: -0.025em;
  position: relative;
  display: inline-block;
}

.section-title::after {
  content: '';
  position: absolute;
  bottom: -12px;
  left: 50%;
  transform: translateX(-50%);
  width: 60px;
  height: 4px;
  background-color: var(--primary-color);
  border-radius: 4px;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
}

.feature-card {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 24px;
  box-shadow: var(--shadow);
  transition: all var(--transition);
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  min-height: 220px;
}

.feature-card:hover {
  transform: translateY(-5px);
  box-shadow: var(--shadow-lg);
  border-color: var(--primary-color);
}

.feature-icon {
  font-size: 36px;
  margin-bottom: 16px;
  color: var(--primary-color);
}

.feature-title {
  margin: 0 0 12px;
  font-size: 18px;
  font-weight: 700;
}

.feature-description {
  margin: 0;
  color: var(--text-secondary);
  font-size: 14px;
  line-height: 1.6;
}

/* 页脚 */
.main-footer {
  border-top: 1px solid var(--border);
  background: #ffffff;
  padding: 40px 0;
  margin-top: auto;
}

.footer-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 24px;
  flex-wrap: wrap;
}

.footer-brand {
  display: flex;
  align-items: center;
  gap: 10px;
  color: var(--text-primary);
  font-weight: 700;
  font-size: 16px;
}

.footer-links {
  display: flex;
  gap: 24px;
  flex-wrap: wrap;
}

.footer-links a {
  color: var(--text-secondary);
  text-decoration: none;
  font-size: 14px;
  transition: all var(--transition);
  position: relative;
}

.footer-links a::after {
  content: '';
  position: absolute;
  bottom: -4px;
  left: 0;
  width: 0;
  height: 2px;
  background-color: var(--primary-color);
  transition: width var(--transition);
}

.footer-links a:hover {
  color: var(--primary-color);
}

.footer-links a:hover::after {
  width: 100%;
}

.footer-copy {
  color: var(--text-secondary);
  font-size: 14px;
}

/* 过渡动画 */
.slide-up-enter-active, .slide-up-leave-active {
  transition: all 0.4s cubic-bezier(0.25, 0.1, 0.25, 1);
}

.slide-up-enter-from, .slide-up-leave-to {
  opacity: 0;
  transform: translateY(20px);
}

/* 响应式设计 */
@media (max-width: 992px) {
  .features-grid {
    grid-template-columns: 1fr 1fr;
  }
  
  .hero-title {
    font-size: 36px;
  }
}

@media (max-width: 768px) {
  .header-content {
    height: auto;
    padding: 12px 0;
  }
  
  .hero-section {
    padding: 60px 0;
  }
  
  .hero-title {
    font-size: 30px;
  }
  
  .hero-description {
    font-size: 16px;
  }
  
  .main-content {
    padding: 40px 0 30px;
  }
  
  .section {
    margin-bottom: 40px;
  }
  
  .footer-content {
    flex-direction: column;
    align-items: center;
    text-align: center;
  }
  
  .footer-links {
    justify-content: center;
  }
}

@media (max-width: 576px) {
  .features-grid {
    grid-template-columns: 1fr;
  }
  
  .hero-title {
    font-size: 26px;
  }
  
  .user-card, .guest-banner {
    flex-direction: column;
    text-align: center;
  }
  
  .user-details {
    min-width: auto;
  }
  
  .hero-cta {
    flex-direction: column;
  }
  
  .btn {
    width: 100%;
  }
}
</style>
