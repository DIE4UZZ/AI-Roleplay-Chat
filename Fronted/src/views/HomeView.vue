<template>
  <div class="home-container">
    <!-- 顶部导航 -->
    <header class="main-header">
      <div class="container">
        <div class="header-content">
          <router-link to="/" class="logo">
            <div class="logo-icon">🎭</div>
            <div class="logo-text">
              <h1 class="logo-title">角色对话</h1>
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
              探索无限可能的
              <span class="highlight">角色世界</span>
            </h1>
            <p class="hero-description">
              与你喜爱的角色进行自然流畅的对话，创造属于你的独特故事体验。
            </p>
            <div class="hero-cta">
              <button class="btn btn-primary start-chat-btn" @click="handleStartChat">
                <span>开始对话</span>
                <span class="btn-icon">→</span>
              </button>
              <button class="btn btn-secondary" @click="handleExploreCharacters">
                <span>探索角色</span>
              </button>
            </div>
          </div>
          <div class="hero-visual">
            <div class="floating-card">
              <div class="card-icon">💬</div>
              <div class="card-text">自然对话</div>
            </div>
            <div class="floating-card">
              <div class="card-icon">🎨</div>
              <div class="card-text">个性化角色</div>
            </div>
            <div class="floating-card">
              <div class="card-icon">✨</div>
              <div class="card-text">沉浸体验</div>
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
          <Transition name="fade-up">
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
                <button class="btn btn-primary" @click="handleStartChat">
                  <span>进入对话</span>
                  <span class="btn-icon">→</span>
                </button>
              </div>
            </div>

            <div v-else class="guest-banner">
              <div class="banner-content">
                <h3>欢迎体验</h3>
                <p>您当前有 <strong>{{ trialCount }}</strong> 次试用机会，注册后享受更多功能。</p>
              </div>
              <div class="banner-actions">
                <button class="btn btn-primary" @click="handleRegisterPrompt">
                  <span>立即注册</span>
                  <span class="btn-icon">→</span>
                </button>
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
            <p class="section-subtitle">体验更加智能、流畅的角色对话</p>
          </div>

          <div class="features-grid">
            <div class="feature-card">
              <div class="feature-icon">💬</div>
              <h3 class="feature-title">自然对话</h3>
              <p class="feature-description">与AI角色进行流畅自然的交流，享受沉浸式对话体验。</p>
            </div>

            <div class="feature-card">
              <div class="feature-icon">🎨</div>
              <h3 class="feature-title">个性化角色</h3>
              <p class="feature-description">创建或选择你喜爱的角色，自定义对话风格和背景故事。</p>
            </div>

            <div class="feature-card">
              <div class="feature-icon">🔒</div>
              <h3 class="feature-title">隐私保护</h3>
              <p class="feature-description">严格的隐私政策，确保你的对话内容安全可靠。</p>
            </div>

            <div class="feature-card">
              <div class="feature-icon">📱</div>
              <h3 class="feature-title">多端同步</h3>
              <p class="feature-description">支持多设备同步，随时随地继续你的对话。</p>
            </div>

            <div class="feature-card">
              <div class="feature-icon">🎭</div>
              <h3 class="feature-title">丰富角色库</h3>
              <p class="feature-description">提供多种类型的角色，满足不同场景的对话需求。</p>
            </div>

            <div class="feature-card">
              <div class="feature-icon">✨</div>
              <h3 class="feature-title">智能回复</h3>
              <p class="feature-description">AI智能理解上下文，提供更加精准的回复内容。</p>
            </div>
          </div>
        </div>
      </section>

      <!-- 体验优势 -->
      <section class="section advantage-section">
        <div class="container">
          <div class="advantage-content">
            <div class="advantage-text">
              <h2 class="advantage-title">为什么选择我们？</h2>
              <p class="advantage-description">
                我们致力于提供最优质的角色对话体验，让你与AI角色的交流更加自然、流畅、有趣。
              </p>
              <ul class="advantage-list">
                <li class="advantage-item">
                  <span class="advantage-check">✓</span>
                  <span>先进的AI技术，提供自然流畅的对话体验</span>
                </li>
                <li class="advantage-item">
                  <span class="advantage-check">✓</span>
                  <span>丰富的角色库，满足不同场景的对话需求</span>
                </li>
                <li class="advantage-item">
                  <span class="advantage-check">✓</span>
                  <span>严格的隐私保护，确保你的对话内容安全</span>
                </li>
                <li class="advantage-item">
                  <span class="advantage-check">✓</span>
                  <span>多端同步，随时随地继续你的对话</span>
                </li>
              </ul>
              <button class="btn btn-primary mt-6" @click="handleStartChat">
                <span>立即体验</span>
                <span class="btn-icon">→</span>
              </button>
            </div>
            <div class="advantage-visual">
              <div class="visual-card">
                <div class="visual-icon">🎯</div>
                <div class="visual-title">精准理解</div>
                <div class="visual-description">AI智能理解上下文，提供精准回复</div>
              </div>
              <div class="visual-card">
                <div class="visual-icon">⚡</div>
                <div class="visual-title">快速响应</div>
                <div class="visual-description">毫秒级响应，流畅对话体验</div>
              </div>
              <div class="visual-card">
                <div class="visual-icon">🌟</div>
                <div class="visual-title">优质服务</div>
                <div class="visual-description">24/7在线，随时为你服务</div>
              </div>
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
            <span>角色对话</span>
          </div>
          <div class="footer-links">
            <a href="#features">功能</a>
            <a href="#">帮助中心</a>
            <a href="#">隐私政策</a>
            <a href="#">服务条款</a>
          </div>
          <div class="footer-social">
            <a href="#" class="social-icon">📧</a>
            <a href="#" class="social-icon">🐦</a>
            <a href="#" class="social-icon">📱</a>
          </div>
        </div>
        <div class="footer-copy">© 2025 角色对话. 保留所有权利.</div>
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
/* 全局样式 */
.home-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: var(--bg-primary);
  color: var(--text-primary);
  overflow-x: hidden;
}

.container {
  max-width: var(--container-width);
  margin: 0 auto;
  padding: 0 var(--spacing-md);
}

/* 顶部导航 */
.main-header {
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

.main-header:hover {
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
  gap: 8px;
  padding: 6px 12px;
  border-radius: 9999px;
  transition: all 0.3s ease;
  border: 2px solid transparent;
  background: var(--bg-secondary);
}

.user-profile:hover {
  background: var(--bg-tertiary);
  transform: translateY(-2px);
  border-color: var(--primary-light);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid var(--bg-primary);
  transition: all 0.3s ease;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.user-profile:hover .avatar {
  border-color: var(--primary);
  transform: scale(1.1);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.dropdown-arrow {
  font-size: 12px;
  color: var(--text-secondary);
  transition: all 0.3s ease;
}

.user-profile:hover .dropdown-arrow {
  transform: rotate(180deg) scale(1.1);
  color: var(--primary);
}

/* 下拉菜单 */
.profile-menu {
  position: absolute;
  top: 100%;
  right: 0;
  margin-top: 8px;
  background: var(--bg-primary);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
  width: 280px;
  overflow: hidden;
  transform: translateY(4px);
  opacity: 0;
  visibility: hidden;
  transition: all 0.3s ease;
  z-index: 1000;
}

.dropdown-enter-active {
  transform: translateY(0);
  opacity: 1;
  visibility: visible;
}

.dropdown-leave-active {
  transform: translateY(4px);
  opacity: 0;
  visibility: hidden;
}

.menu-header {
  padding: 20px;
  border-bottom: 1px solid var(--border-color);
  background: linear-gradient(135deg, var(--bg-primary) 0%, var(--bg-secondary) 100%);
}

.menu-header h4 {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
}

.user-id {
  margin: 4px 0 0;
  font-size: 12px;
  color: var(--text-secondary);
  font-family: monospace;
}

.menu-options {
  padding: 8px;
}

.menu-item {
  width: 100%;
  background: transparent;
  border: 0;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.2s ease;
  text-align: left;
  position: relative;
  overflow: hidden;
  color: var(--text-primary);
}

.menu-item::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  height: 100%;
  width: 3px;
  background: linear-gradient(to bottom, var(--primary), var(--secondary));
  transform: scaleY(0);
  transition: transform 0.2s ease;
}

.menu-item:hover {
  background: var(--bg-secondary);
  transform: translateX(4px);
  color: var(--primary);
}

.menu-item:hover::before {
  transform: scaleY(1);
}

.menu-item .menu-icon {
  font-size: 16px;
  transition: transform 0.2s ease;
}

.menu-item:hover .menu-icon {
  transform: scale(1.2) rotate(5deg);
}

.menu-item.logout {
  color: var(--error);
}

.menu-item.logout:hover {
  background: var(--error-bg);
  color: var(--error);
}

.menu-item.logout::before {
  background: var(--error);
}

/* 英雄区 */
.hero-section {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 120px 0 80px;
  position: relative;
  overflow: hidden;
}

/* 装饰性元素 */
.hero-section::before {
  content: '';
  position: absolute;
  top: -50%;
  right: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle, rgba(255, 255, 255, 0.15) 0%, transparent 70%);
  animation: rotate 20s linear infinite;
  z-index: 0;
}

.hero-section::after {
  content: '';
  position: absolute;
  bottom: -50px;
  left: -50px;
  width: 300px;
  height: 300px;
  background: radial-gradient(circle, rgba(255, 255, 255, 0.1) 0%, transparent 70%);
  border-radius: 50%;
  z-index: 0;
}

@keyframes rotate {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.hero-content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 60px;
  align-items: center;
  justify-content: center;
  position: relative;
  z-index: 1;
  max-width: 1200px;
  margin: 0 auto;
}

.hero-text {
  animation: fadeInUp 0.8s ease-out forwards;
  opacity: 0;
}

.hero-title {
  font-size: clamp(2.5rem, 8vw, 4rem);
  line-height: 1.1;
  margin: 0 0 24px;
  font-weight: 800;
  letter-spacing: -0.03em;
  text-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  background: linear-gradient(135deg, #ffffff, rgba(255, 255, 255, 0.8));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.highlight {
  position: relative;
  display: inline-block;
}

.highlight::after {
  content: '';
  position: absolute;
  bottom: -4px;
  left: 0;
  width: 100%;
  height: 6px;
  background: rgba(255, 255, 255, 0.3);
  border-radius: 9999px;
  transform: skewX(-15deg);
  animation: highlightPulse 2s infinite alternate;
}

@keyframes highlightPulse {
  from { transform: skewX(-15deg) scaleX(1); }
  to { transform: skewX(-15deg) scaleX(1.05); }
}

.hero-description {
  margin: 0 0 32px;
  color: rgba(255, 255, 255, 0.9);
  font-size: clamp(1.125rem, 3vw, 1.5rem);
  line-height: 1.7;
  max-width: 600px;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.hero-cta {
  display: flex;
  gap: 20px;
  flex-wrap: wrap;
}

/* 英雄区浮动卡片 */
.hero-visual {
  position: relative;
  height: 400px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.floating-card {
  position: absolute;
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  animation: float 3s ease-in-out infinite;
  transition: all 0.3s ease;
  max-width: 200px;
}

.floating-card:hover {
  transform: translateY(-10px) scale(1.05);
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
}

.floating-card:nth-child(1) {
  top: 20%;
  left: 20%;
  animation-delay: 0s;
}

.floating-card:nth-child(2) {
  top: 50%;
  right: 20%;
  animation-delay: 1s;
}

.floating-card:nth-child(3) {
  bottom: 20%;
  left: 30%;
  animation-delay: 2s;
}

.floating-card .card-icon {
  font-size: 32px;
  margin-bottom: 12px;
  text-align: center;
}

.floating-card .card-text {
  font-size: 16px;
  font-weight: 500;
  text-align: center;
  color: white;
}

@keyframes float {
  0%, 100% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-20px);
  }
}

/* 按钮样式 */
.btn {
  border: 2px solid transparent;
  padding: 14px 28px;
  border-radius: 9999px;
  font-weight: 600;
  font-size: 16px;
  transition: all 0.3s ease;
  cursor: pointer;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
  min-width: 140px;
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

.btn-icon {
  font-size: 18px;
  transition: all 0.3s ease;
}

.btn:hover .btn-icon {
  transform: translateX(4px);
}

/* 主按钮 */
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

/* 次按钮 */
.btn-secondary {
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border-color: rgba(255, 255, 255, 0.3);
  color: white;
  font-weight: 600;
}

.btn-secondary:hover {
  background: rgba(255, 255, 255, 0.25);
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
  border-color: rgba(255, 255, 255, 0.5);
}

.btn-secondary:active {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

/* 主内容 */
.main-content {
  flex: 1;
  padding: 80px 0 40px;
  position: relative;
}

.section {
  margin-bottom: 120px;
}

/* 用户信息 / 游客提示 */
.user-card, .guest-banner {
  background: var(--bg-primary);
  border: 1px solid var(--border-color);
  border-radius: 16px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
  padding: 32px;
  display: flex;
  align-items: center;
  gap: 24px;
  justify-content: space-between;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.user-card::before, .guest-banner::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 4px;
  height: 100%;
  background: linear-gradient(to bottom, var(--primary), var(--secondary));
}

.user-card:hover, .guest-banner:hover {
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
  transform: translateY(-4px);
  border-color: var(--primary-light);
}

.user-card {
  flex-wrap: wrap;
}

.user-avatar {
  position: relative;
}

.user-avatar::after {
  content: '';
  position: absolute;
  top: -4px;
  left: -4px;
  right: -4px;
  bottom: -4px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--primary), var(--secondary));
  z-index: -1;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.user-card:hover .user-avatar::after {
  opacity: 1;
}

.user-avatar img {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  object-fit: cover;
  border: 3px solid var(--bg-tertiary);
  transition: all 0.3s ease;
}

.user-card:hover .user-avatar img {
  transform: scale(1.05);
  border-color: white;
}

.user-details {
  min-width: 200px;
  flex: 1;
}

.user-name {
  margin: 0 0 8px;
  font-size: 24px;
  font-weight: 700;
  color: var(--text-primary);
  letter-spacing: -0.02em;
}

.user-id {
  margin: 0;
  color: var(--text-secondary);
  font-size: 14px;
  font-family: monospace;
}

.user-actions {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
  justify-content: flex-end;
}

.guest-banner {
  flex-wrap: wrap;
  background: linear-gradient(135deg, var(--bg-primary) 0%, var(--bg-secondary) 100%);
}

.guest-banner::before {
  background: linear-gradient(to bottom, var(--secondary), var(--primary));
}

.banner-content {
  flex: 1;
  min-width: 200px;
}

.banner-content h3 {
  margin: 0 0 8px;
  font-size: 20px;
  font-weight: 700;
  color: var(--text-primary);
}

.banner-content p {
  margin: 0;
  color: var(--text-secondary);
  font-size: 16px;
  line-height: 1.6;
}

.banner-content strong {
  color: var(--primary);
  font-weight: 700;
}

.banner-actions {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
}

/* 功能区块 */
.section-header {
  text-align: center;
  margin-bottom: 60px;
  position: relative;
}

.section-title {
  margin: 0 0 16px;
  font-size: 36px;
  font-weight: 700;
  color: var(--text-primary);
  letter-spacing: -0.03em;
  position: relative;
  display: inline-block;
}

.section-title::after {
  content: '';
  position: absolute;
  bottom: -12px;
  left: 50%;
  transform: translateX(-50%);
  width: 80px;
  height: 4px;
  background: linear-gradient(90deg, var(--primary), var(--secondary));
  border-radius: 2px;
}

.section-subtitle {
  margin: 0 auto;
  color: var(--text-secondary);
  font-size: 18px;
  line-height: 1.6;
  max-width: 600px;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 32px;
  margin-top: 60px;
}

.feature-card {
  background: var(--bg-primary);
  border: 1px solid var(--border-color);
  border-radius: 16px;
  padding: 40px 32px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  min-height: 280px;
  position: relative;
  overflow: hidden;
  transform: translateY(0);
}

/* 卡片悬停效果增强 */
.feature-card:hover {
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
  transform: translateY(-10px);
  border-color: var(--primary-light);
}

/* 卡片顶部装饰条 */
.feature-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 4px;
  background: linear-gradient(90deg, var(--primary), var(--secondary));
  transform: translateY(-4px);
  transition: transform 0.3s ease;
}

.feature-card:hover::before {
  transform: translateY(0);
}

.feature-icon {
  margin-bottom: 24px;
  width: 80px;
  height: 80px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  background: rgba(59, 130, 246, 0.1);
  color: var(--primary);
  font-size: 40px;
  margin-left: auto;
  margin-right: auto;
  transition: all 0.3s ease;
  position: relative;
  z-index: 1;
}

.feature-icon::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  border-radius: 50%;
  background: var(--primary);
  transform: scale(0);
  transition: transform 0.3s ease;
  z-index: -1;
}

.feature-card:hover .feature-icon {
  color: white;
  transform: scale(1.1);
}

.feature-card:hover .feature-icon::after {
  transform: scale(1);
}

.feature-title {
  margin: 0 0 18px;
  font-size: 24px;
  font-weight: 600;
  color: var(--text-primary);
  transition: color 0.3s ease;
}

.feature-card:hover .feature-title {
  color: var(--primary);
}

.feature-description {
  margin: 0;
  color: var(--text-secondary);
  font-size: 16px;
  line-height: 1.7;
  transition: all 0.3s ease;
}

/* 体验优势 */
.advantage-section {
  background: linear-gradient(135deg, var(--bg-secondary) 0%, var(--bg-primary) 100%);
  border-radius: 24px;
  padding: 80px 0;
  margin: 80px 0;
}

.advantage-content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 80px;
  align-items: center;
}

.advantage-text {
  animation: fadeInLeft 0.8s ease-out forwards;
  opacity: 0;
}

.advantage-title {
  margin: 0 0 24px;
  font-size: 36px;
  font-weight: 700;
  color: var(--text-primary);
  letter-spacing: -0.03em;
}

.advantage-description {
  margin: 0 0 32px;
  color: var(--text-secondary);
  font-size: 18px;
  line-height: 1.7;
}

.advantage-list {
  list-style: none;
  padding: 0;
  margin: 0 0 32px;
}

.advantage-item {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  margin-bottom: 20px;
  padding-left: 8px;
  position: relative;
}

.advantage-item::before {
  content: '';
  position: absolute;
  left: 0;
  top: 8px;
  width: 4px;
  height: 4px;
  background: var(--primary);
  border-radius: 50%;
}

.advantage-check {
  color: var(--success);
  font-weight: 700;
  font-size: 20px;
  line-height: 1;
  margin-top: -2px;
}

.advantage-item span:last-child {
  color: var(--text-secondary);
  line-height: 1.6;
}

.advantage-visual {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 24px;
  animation: fadeInRight 0.8s ease-out forwards;
  opacity: 0;
}

.visual-card {
  background: var(--bg-primary);
  border: 1px solid var(--border-color);
  border-radius: 16px;
  padding: 32px 24px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
  transition: all 0.3s ease;
  text-align: center;
}

.visual-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
  border-color: var(--primary-light);
}

.visual-icon {
  font-size: 48px;
  margin-bottom: 16px;
  background: linear-gradient(135deg, var(--primary), var(--secondary));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.visual-title {
  margin: 0 0 8px;
  font-size: 20px;
  font-weight: 600;
  color: var(--text-primary);
}

.visual-description {
  margin: 0;
  color: var(--text-secondary);
  font-size: 14px;
  line-height: 1.6;
}

/* 页脚 */
.main-footer {
  background: linear-gradient(135deg, var(--bg-secondary) 0%, var(--bg-primary) 100%);
  border-top: 1px solid var(--border-color);
  padding: 60px 0 30px;
  margin-top: 80px;
  position: relative;
  overflow: hidden;
}

/* 页脚装饰背景 */
.main-footer::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: 
    radial-gradient(circle at 10% 20%, rgba(59, 130, 246, 0.05) 0%, rgba(59, 130, 246, 0) 20%),
    radial-gradient(circle at 80% 60%, rgba(167, 139, 250, 0.05) 0%, rgba(167, 139, 250, 0) 20%);
  z-index: 0;
}

.footer-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 50px;
  flex-wrap: wrap;
  position: relative;
  z-index: 1;
  margin-bottom: 30px;
}

.footer-brand {
  display: flex;
  align-items: center;
  gap: 16px;
  color: var(--text-primary);
  font-weight: 700;
  font-size: 24px;
  transition: all 0.3s ease;
}

.footer-brand:hover {
  transform: translateX(8px);
}

.footer-brand .logo-icon {
  font-size: 32px;
  transition: all 0.3s ease;
}

.footer-brand:hover .logo-icon {
  transform: rotate(10deg) scale(1.1);
}

.footer-brand span {
  background: linear-gradient(90deg, var(--primary), var(--secondary));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  letter-spacing: -0.02em;
}

.footer-links {
  display: flex;
  gap: 30px;
  flex-wrap: wrap;
}

.footer-links a {
  color: var(--text-secondary);
  text-decoration: none;
  font-size: 16px;
  transition: all 0.3s ease;
  position: relative;
  padding-left: 0;
  display: inline-block;
}

.footer-links a::before {
  content: '→';
  position: absolute;
  left: -20px;
  opacity: 0;
  transition: all 0.3s ease;
  color: var(--primary);
}

.footer-links a:hover {
  color: var(--primary);
  padding-left: 10px;
}

.footer-links a:hover::before {
  left: -12px;
  opacity: 1;
}

.footer-links a::after {
  content: '';
  position: absolute;
  bottom: -4px;
  left: 0;
  width: 0;
  height: 2px;
  background: var(--primary);
  transition: width 0.3s ease;
}

.footer-links a:hover::after {
  width: 100%;
}

.footer-social {
  display: flex;
  gap: 16px;
}

.social-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: var(--bg-tertiary);
  color: var(--text-secondary);
  text-decoration: none;
  transition: all 0.3s ease;
  font-size: 18px;
}

.social-icon:hover {
  background: linear-gradient(135deg, var(--primary), var(--secondary));
  color: white;
  transform: translateY(-3px);
  box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
}

.footer-copy {
  color: var(--text-secondary);
  font-size: 14px;
  text-align: center;
  position: relative;
  z-index: 1;
  padding-top: 30px;
  border-top: 1px solid var(--border-color);
}

/* 过渡动画 */
.fade-up-enter-active, .fade-up-leave-active {
  transition: all 0.6s cubic-bezier(0.25, 0.1, 0.25, 1);
}

.fade-up-enter-from, .fade-up-leave-to {
  opacity: 0;
  transform: translateY(30px);
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

/* 响应式调整 */
@media (max-width: 1024px) {
  .advantage-content {
    grid-template-columns: 1fr;
    gap: 60px;
    text-align: center;
  }
  
  .advantage-visual {
    justify-items: center;
  }
}

@media (max-width: 992px) {
  .hero-content {
    grid-template-columns: 1fr;
    gap: 60px;
    text-align: center;
  }
  
  .hero-visual {
    height: 300px;
  }
  
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
    padding: 80px 0 60px;
  }
  
  .hero-title {
    font-size: 30px;
  }
  
  .hero-description {
    font-size: 16px;
  }
  
  .main-content {
    padding: 60px 0 30px;
  }
  
  .section {
    margin-bottom: 60px;
  }
  
  .section-title {
    font-size: 28px;
  }
  
  .features-grid {
    grid-template-columns: 1fr;
    gap: 24px;
  }
  
  .feature-card {
    padding: 32px 24px;
  }
  
  .footer-content {
    flex-direction: column;
    align-items: center;
    text-align: center;
    gap: 30px;
  }
  
  .footer-links {
    justify-content: center;
    gap: 20px;
  }
  
  .advantage-section {
    padding: 60px 0;
    margin: 60px 0;
  }
  
  .advantage-title {
    font-size: 28px;
  }
}

@media (max-width: 576px) {
  .hero-cta {
    flex-direction: column;
    align-items: center;
  }
  
  .btn {
    width: 100%;
    max-width: 280px;
  }
  
  .user-card, .guest-banner {
    flex-direction: column;
    text-align: center;
  }
  
  .user-details {
    min-width: auto;
  }
  
  .user-actions, .banner-actions {
    justify-content: center;
  }
  
  .advantage-item {
    text-align: left;
  }
}
</style>