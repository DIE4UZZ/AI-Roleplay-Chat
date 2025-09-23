<template>
  <div class="home-container">
    <!-- 顶部导航栏 -->
    <header class="main-header">
      <div class="container">
        <div class="header-content">
          <div class="logo-section">
            <div class="logo">
              <div class="logo-icon">🎭</div>
              <div class="logo-text">
                <h1 class="logo-title">AI 角色扮演</h1>
                <p class="logo-subtitle">探索无限对话世界</p>
              </div>
            </div>
          </div>
          
          <div class="nav-section">
            <nav class="main-nav">
              <ul class="nav-links">
                <li class="nav-item"><a href="#" class="nav-link active">首页</a></li>
                <li class="nav-item"><a href="#features" class="nav-link">功能</a></li>
                <li class="nav-item"><a href="#about" class="nav-link">关于</a></li>
                <li class="nav-item"><a href="#support" class="nav-link">支持</a></li>
              </ul>
            </nav>
            
            <div class="user-section">
              <template v-if="isLoggedIn">
                <div class="user-profile">
                  <div class="avatar" @click="toggleProfileMenu">
                    <img 
                      src="https://api.dicebear.com/7.x/avataaars/svg?seed={{ userSeed }}" 
                      alt="User Avatar"
                    />
                    <span class="dropdown-arrow">▼</span>
                  </div>
                  
                  <!-- 用户菜单 -->
                  <Transition name="dropdown">
                    <div v-if="showProfileMenu" class="profile-menu">
                      <div class="menu-header">
                        <h4>{{ userInfo?.username || '用户' }}</h4>
                        <p>{{ userInfo?.id ? `ID: ${userInfo.id}` : '未设置信息' }}</p>
                      </div>
                      <div class="menu-options">
                        <button class="menu-item">
                          <span class="menu-icon">👤</span>
                          <span>个人资料</span>
                        </button>
                        <button class="menu-item">
                          <span class="menu-icon">📊</span>
                          <span>使用统计</span>
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
                </div>
              </template>
              
              <template v-else>
                <router-link to="/login" class="login-btn">登录 / 注册</router-link>
              </template>
            </div>
          </div>
        </div>
      </div>
    </header>

    <!-- 英雄区域 -->
    <section class="hero-section">
      <div class="container">
        <div class="hero-content">
          <div class="hero-text fade-in">
            <h1 class="hero-title">
              探索无限可能的
              <span class="highlight">AI角色扮演</span>
              世界
            </h1>
            <p class="hero-description">
              与AI驱动的角色进行自然、生动的对话，体验前所未有的沉浸式交流。
              释放创意，探索无限可能。
            </p>
            <div class="hero-cta">
              <button class="primary-btn start-chat-btn">开始对话</button>
              <button class="secondary-btn explore-btn">探索角色</button>
            </div>
          </div>
          
          <div class="hero-image fade-in-delay">
            <div class="hero-illustration">
              <div class="chat-illustration">
                <div class="chat-bubble user">👤 你好，我想和莎士比亚对话</div>
                <div class="chat-bubble ai">🎭 啊，我的朋友！欢迎来到语言与想象的世界...</div>
                <div class="chat-bubble user">👤 能为我创作一首十四行诗吗？</div>
                <div class="chat-bubble ai">🎭 当然可以，我亲爱的朋友...</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 主内容区域 -->
    <main class="main-content">
      <!-- 用户信息或游客提示 -->
      <section class="user-section">
        <div class="container">
          <Transition name="slide-up">
            <div v-if="isLoggedIn" class="user-card">
              <div class="user-avatar">
                <img 
                  src="https://api.dicebear.com/7.x/avataaars/svg?seed={{ userSeed }}" 
                  alt="User Avatar"
                />
              </div>
              <div class="user-details">
                <div class="user-main-info">
                  <h2 class="user-name">{{ userInfo?.username || '用户' }}</h2>
                  <p class="user-id">{{ userInfo?.id ? `用户ID: ${userInfo.id}` : '未设置信息' }}</p>
                </div>
              </div>
              <div class="user-actions">
                <button class="action-btn profile-btn">
                  <span class="btn-icon">👤</span>
                  <span>个人资料</span>
                </button>
              </div>
            </div>

            <div v-else class="guest-notice">
              <div class="notice-icon">💡</div>
              <div class="notice-content">
                <h3>您当前是游客模式</h3>
                <p>以游客身份体验我们的AI聊天服务，您当前有 <strong>{{ trialCount }}</strong> 次试用机会。</p>
                <p class="notice-warning">请注意：游客数据将在会话结束后清除，建议注册账号保存您的聊天记录。</p>
                <button class="register-btn" @click="handleRegisterPrompt">立即注册</button>
              </div>
            </div>
          </Transition>
        </div>
      </section>

      <!-- 功能列表 -->
      <section id="features" class="features-section">
        <div class="container">
          <div class="section-header">
            <h2 class="section-title">核心功能</h2>
            <p class="section-description">探索我们平台提供的强大功能，开启无限可能的对话体验</p>
          </div>
          
          <div class="features-grid">
            <div class="feature-card hover-effect">
              <div class="feature-icon pulse">💬</div>
              <h3 class="feature-title">角色扮演聊天</h3>
              <p class="feature-description">选择或创建您喜欢的角色，进行沉浸式对话体验</p>
            </div>
            
            <div class="feature-card hover-effect">
              <div class="feature-icon pulse">🎙️</div>
              <h3 class="feature-title">语音聊天</h3>
              <p class="feature-description">通过语音与AI角色进行交流，体验更自然的对话</p>
            </div>
            
            <div class="feature-card hover-effect">
              <div class="feature-icon pulse">✨</div>
              <h3 class="feature-title">个性化角色</h3>
              <p class="feature-description">自定义AI角色的性格、背景和对话风格</p>
            </div>
            
            <div class="feature-card hover-effect">
              <div class="feature-icon pulse">📝</div>
              <h3 class="feature-title">对话历史</h3>
              <p class="feature-description">保存和管理您的对话历史，随时回顾之前的交流内容</p>
            </div>
            
            <div class="feature-card hover-effect">
              <div class="feature-icon pulse">🎭</div>
              <h3 class="feature-title">多角色支持</h3>
              <p class="feature-description">从丰富的预设角色库中选择，满足各种对话需求</p>
            </div>
            
            <div class="feature-card hover-effect">
              <div class="feature-icon pulse">🔒</div>
              <h3 class="feature-title">隐私保护</h3>
              <p class="feature-description">严格的数据保护措施，确保您的对话内容安全私密</p>
            </div>
          </div>
        </div>
      </section>

      <!-- 状态信息 -->
      <section class="status-section">
        <div class="container">
          <div class="status-card">
            <div class="status-item">
              <span class="status-label">登录状态:</span>
              <span class="status-value" :class="isLoggedIn ? 'status-online' : 'status-offline'">
                {{ isLoggedIn ? '已登录' : '未登录' }}
              </span>
            </div>
            <div class="status-divider"></div>
            <div class="status-item">
              <span class="status-label">连接状态:</span>
              <span class="status-value status-online">
                <span class="connection-dot"></span>
                已连接
              </span>
            </div>
            <div v-if="isGuest" class="status-divider"></div>
            <div v-if="isGuest" class="status-item">
              <span class="status-label">剩余试用:</span>
              <span class="status-value status-warning">{{ trialCount }} 次</span>
            </div>
          </div>
        </div>
      </section>
    </main>

    <!-- 行动号召 -->
    <section class="cta-section">
      <div class="container">
        <div class="cta-content">
          <h2>准备好开始您的AI角色扮演之旅了吗？</h2>
          <p>加入我们，探索无限可能的对话世界</p>
          <div class="cta-buttons">
            <button class="primary-btn register-cta-btn" @click="handleRegisterPrompt">立即注册</button>
            <button class="secondary-btn login-cta-btn">已有账号，去登录</button>
          </div>
        </div>
      </div>
    </section>

    <!-- 页脚 -->
    <footer class="main-footer">
      <div class="container">
        <div class="footer-content">
          <div class="footer-logo">
            <div class="logo-icon">🎭</div>
            <div class="logo-text">
              <h3>AI 角色扮演</h3>
              <p>探索无限对话世界</p>
            </div>
          </div>
          
          <div class="footer-links">
            <div class="link-group">
              <h4>产品</h4>
              <ul>
                <li><a href="#">功能</a></li>
                <li><a href="#">定价</a></li>
                <li><a href="#">API</a></li>
                <li><a href="#">更新日志</a></li>
              </ul>
            </div>
            
            <div class="link-group">
              <h4>公司</h4>
              <ul>
                <li><a href="#">关于我们</a></li>
                <li><a href="#">联系我们</a></li>
                <li><a href="#">加入团队</a></li>
              </ul>
            </div>
            
            <div class="link-group">
              <h4>资源</h4>
              <ul>
                <li><a href="#">帮助中心</a></li>
                <li><a href="#">使用教程</a></li>
                <li><a href="#">常见问题</a></li>
              </ul>
            </div>
            
            <div class="link-group">
              <h4>法律</h4>
              <ul>
                <li><a href="#">隐私政策</a></li>
                <li><a href="#">服务条款</a></li>
                <li><a href="#">Cookie 政策</a></li>
              </ul>
            </div>
          </div>
        </div>
        
        <div class="footer-bottom">
          <p>© 2023 AI 角色扮演语音聊天. 保留所有权利。</p>
          <div class="social-links">
            <a href="#" class="social-link">Twitter</a>
            <a href="#" class="social-link">Facebook</a>
            <a href="#" class="social-link">Instagram</a>
            <a href="#" class="social-link">GitHub</a>
          </div>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onBeforeUnmount } from 'vue';
import { useRouter } from 'vue-router';
import authService from '../services/auth.service';
import { useAuthStore } from '../store/auth.store';
import type { UserInfo } from '../types/user';

// 路由实例
const router = useRouter();
// 认证store
const authStore = useAuthStore();

// 用户菜单状态
const showProfileMenu = ref(false);

// 用户信息
const userInfo = ref<UserInfo | null>(null);
const isLoggedIn = ref(false);
const isGuest = ref(false);
const trialCount = ref(0);
const userSeed = ref('');

// 生成用户头像种子
const generateUserSeed = (username: string) => {
  return username || Math.random().toString(36).substring(2, 15);
};

// 初始化页面数据
const initializeData = () => {
  userInfo.value = authService.getCurrentUser();
  isLoggedIn.value = authService.isLoggedIn();
  isGuest.value = authService.isGuest();
  trialCount.value = authService.getTrialCount();
  userSeed.value = generateUserSeed(userInfo.value?.username || 'guest');
};

// 处理退出登录
const handleLogout = () => {
  authService.logout();
  authStore.clearUserState();
  router.push('/login');
  showProfileMenu.value = false;
};

// 处理注册提示
const handleRegisterPrompt = () => {
  // 先退出游客登录
  authService.logout();
  authStore.clearUserState();
  // 跳转到注册页面
  router.push('/login');
};

// 切换用户菜单显示状态
const toggleProfileMenu = () => {
  showProfileMenu.value = !showProfileMenu.value;
};

// 点击外部关闭用户菜单
const handleClickOutside = (event: MouseEvent) => {
  const profileElement = document.querySelector('.user-profile');
  if (profileElement && !profileElement.contains(event.target as Node)) {
    showProfileMenu.value = false;
  }
};

// 组件挂载时初始化数据
onMounted(() => {
  initializeData();
  
  // 添加点击外部关闭菜单的事件监听
  document.addEventListener('click', handleClickOutside);
  
  // 为导航链接添加平滑滚动
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
      e.preventDefault();
      const targetId = this.getAttribute('href');
      if (targetId && targetId !== '#') {
        const targetElement = document.querySelector(targetId);
        if (targetElement) {
          targetElement.scrollIntoView({ behavior: 'smooth' });
        }
      }
    });
  });
});

// 组件卸载时清理
onBeforeUnmount(() => {
  document.removeEventListener('click', handleClickOutside);
});
</script>

<style scoped>
/* CSS变量定义 */
:root {
  --primary-color: #4361ee;
  --secondary-color: #3a0ca3;
  --accent-color: #f72585;
  --text-primary: #1e293b;
  --text-secondary: #64748b;
  --background-color: #f8fafc;
  --card-bg: #ffffff;
  --border-color: #e2e8f0;
  --success-color: #10b981;
  --warning-color: #f59e0b;
  --error-color: #ef4444;
  --shadow-light: 0 1px 3px rgba(0, 0, 0, 0.1);
  --shadow-medium: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  --shadow-heavy: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
  --border-radius-sm: 0.375rem;
  --border-radius-md: 0.5rem;
  --border-radius-lg: 1rem;
  --transition-fast: 0.2s ease;
  --transition-normal: 0.3s ease;
}

/* 通用容器 */
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1.5rem;
}

/* 主容器 */
.home-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: var(--background-color);
}

/* 主标题栏 */
.main-header {
  background-color: var(--card-bg);
  box-shadow: var(--shadow-light);
  position: sticky;
  top: 0;
  z-index: 100;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 6rem;
}

.logo-section .logo {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.logo-icon {
  font-size: 2rem;
  line-height: 1;
}

.logo-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0;
}

.logo-subtitle {
  font-size: 0.875rem;
  color: var(--text-secondary);
  margin: 0;
}

/* 导航菜单 */
.nav-section {
  display: flex;
  align-items: center;
  gap: 2rem;
}

.main-nav .nav-links {
  display: flex;
  gap: 1.5rem;
  list-style: none;
  margin: 0;
  padding: 0;
}

.nav-link {
  color: var(--text-secondary);
  text-decoration: none;
  font-weight: 500;
  padding: 0.5rem 0;
  position: relative;
  transition: color var(--transition-fast);
}

.nav-link:hover, .nav-link.active {
  color: var(--primary-color);
}

.nav-link.active::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 2px;
  background-color: var(--primary-color);
  border-radius: 2px;
}

/* 用户区域 */
.user-section {
  display: flex;
  align-items: center;
}

.login-btn {
  background-color: var(--primary-color);
  color: white;
  border: none;
  padding: 0.625rem 1.25rem;
  border-radius: var(--border-radius-md);
  cursor: pointer;
  font-weight: 500;
  transition: background-color var(--transition-fast);
}

.login-btn:hover {
  background-color: var(--secondary-color);
}

/* 用户资料区域 */
.user-profile {
  position: relative;
}

.avatar {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  padding: 0.25rem;
  border-radius: 50%;
  transition: background-color var(--transition-fast);
}

.avatar:hover {
  background-color: var(--border-color);
}

.avatar img {
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid var(--border-color);
}

.dropdown-arrow {
  font-size: 0.75rem;
  transition: transform var(--transition-fast);
}

.profile-menu {
  position: absolute;
  top: 100%;
  right: 0;
  margin-top: 0.5rem;
  background-color: var(--card-bg);
  border-radius: var(--border-radius-md);
  box-shadow: var(--shadow-heavy);
  width: 18rem;
  overflow: hidden;
  z-index: 1000;
}

.menu-header {
  padding: 1rem;
  border-bottom: 1px solid var(--border-color);
}

.menu-header h4 {
  margin: 0;
  font-size: 1rem;
  font-weight: 600;
  color: var(--text-primary);
}

.menu-header p {
  margin: 0.25rem 0 0;
  font-size: 0.875rem;
  color: var(--text-secondary);
}

.menu-options {
  padding: 0.5rem 0;
}

.menu-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  width: 100%;
  text-align: left;
  padding: 0.75rem 1rem;
  border: none;
  background: none;
  cursor: pointer;
  font-size: 0.875rem;
  color: var(--text-primary);
  transition: background-color var(--transition-fast);
}

.menu-item:hover {
  background-color: var(--background-color);
}

.menu-item.logout {
  color: var(--error-color);
  margin-top: 0.5rem;
}

.menu-item.logout:hover {
  background-color: #fee2e2;
}

.menu-icon {
  font-size: 1rem;
}

/* 英雄区域 */
.hero-section {
  background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
  color: white;
  padding: 6rem 0;
  position: relative;
  overflow: hidden;
}

.hero-section::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-image: url("data:image/svg+xml,%3Csvg width='100' height='100' viewBox='0 0 100 100' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M11 18c3.866 0 7-3.134 7-7s-3.134-7-7-7-7 3.134-7 7 3.134 7 7 7zm48 25c3.866 0 7-3.134 7-7s-3.134-7-7-7-7 3.134-7 7 3.134 7 7 7zm-43-7c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zm63 31c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zM34 90c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zm56-76c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zM12 86c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm28-65c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm23-11c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm-6 60c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm29 22c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zM32 63c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm57-13c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm-9-21c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM60 91c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM35 41c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM12 60c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2z' fill='%23ffffff' fill-opacity='0.05' fill-rule='evenodd'/%3E%3C/svg%3E");
  opacity: 0.3;
}

.hero-content {
  display: flex;
  align-items: center;
  gap: 4rem;
  position: relative;
}

.hero-text {
  flex: 1;
}

.hero-title {
  font-size: 3rem;
  font-weight: 800;
  line-height: 1.1;
  margin: 0 0 1.5rem;
}

.highlight {
  color: #4cc9f0;
  position: relative;
}

.highlight::after {
  content: '';
  position: absolute;
  bottom: -0.5rem;
  left: 0;
  width: 100%;
  height: 0.5rem;
  background-color: rgba(76, 201, 240, 0.3);
  border-radius: 0.25rem;
}

.hero-description {
  font-size: 1.125rem;
  line-height: 1.6;
  margin: 0 0 2.5rem;
  opacity: 0.9;
}

.hero-cta {
  display: flex;
  gap: 1rem;
}

.primary-btn {
  background-color: white;
  color: var(--primary-color);
  border: none;
  padding: 0.875rem 1.75rem;
  border-radius: var(--border-radius-md);
  cursor: pointer;
  font-size: 1rem;
  font-weight: 600;
  transition: all var(--transition-fast);
}

.primary-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
}

.secondary-btn {
  background-color: transparent;
  color: white;
  border: 2px solid rgba(255, 255, 255, 0.3);
  padding: 0.875rem 1.75rem;
  border-radius: var(--border-radius-md);
  cursor: pointer;
  font-size: 1rem;
  font-weight: 600;
  transition: all var(--transition-fast);
}

.secondary-btn:hover {
  background-color: rgba(255, 255, 255, 0.1);
  border-color: white;
}

.hero-image {
  flex: 1;
  display: flex;
  justify-content: center;
}

.hero-illustration {
  background-color: rgba(255, 255, 255, 0.95);
  border-radius: var(--border-radius-lg);
  padding: 2rem;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
  max-width: 350px;
}

.chat-illustration {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.chat-bubble {
  padding: 1rem;
  border-radius: var(--border-radius-md);
  max-width: 90%;
  box-shadow: var(--shadow-light);
  position: relative;
  font-size: 0.9rem;
}

.chat-bubble.user {
  background-color: #f0f9ff;
  border-top-left-radius: 0;
  align-self: flex-end;
  color: var(--text-primary);
}

.chat-bubble.ai {
  background-color: #f0fdf4;
  border-top-right-radius: 0;
  align-self: flex-start;
  color: var(--text-primary);
}

/* 主内容区域 */
.main-content {
  flex: 1;
  padding: 4rem 0;
}

/* 用户区域 */
.user-section {
  margin-bottom: 4rem;
}

.user-card {
  background-color: var(--card-bg);
  border-radius: var(--border-radius-lg);
  box-shadow: var(--shadow-medium);
  padding: 2rem;
  display: flex;
  align-items: center;
  gap: 2rem;
}

.user-avatar img {
  width: 8rem;
  height: 8rem;
  border-radius: 50%;
  object-fit: cover;
  border: 3px solid var(--border-color);
  box-shadow: var(--shadow-light);
}

.user-details {
  flex: 1;
}

.user-name {
  font-size: 1.75rem;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0 0 0.5rem;
}

.user-id {
  font-size: 1rem;
  color: var(--text-secondary);
  margin: 0;
}

.user-actions {
  display: flex;
  gap: 1rem;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.25rem;
  border-radius: var(--border-radius-md);
  font-weight: 500;
  transition: all var(--transition-fast);
  cursor: pointer;
}

.profile-btn {
  background-color: var(--primary-color);
  color: white;
  border: none;
}

.profile-btn:hover {
  background-color: var(--secondary-color);
}

.guest-notice {
  background-color: var(--card-bg);
  border-radius: var(--border-radius-lg);
  box-shadow: var(--shadow-medium);
  padding: 2rem;
  display: flex;
  align-items: flex-start;
  gap: 1.5rem;
  border-left: 4px solid var(--warning-color);
}

.notice-icon {
  font-size: 2rem;
  flex-shrink: 0;
  margin-top: 0.25rem;
}

.notice-content h3 {
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 0.75rem;
}

.notice-content p {
  color: var(--text-secondary);
  line-height: 1.6;
  margin: 0 0 0.75rem;
}

.notice-warning {
  color: var(--warning-color) !important;
  font-weight: 500;
}

.register-btn {
  background-color: var(--primary-color);
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: var(--border-radius-md);
  cursor: pointer;
  font-weight: 500;
  transition: background-color var(--transition-fast);
}

.register-btn:hover {
  background-color: var(--secondary-color);
}

/* 功能区域 */
.features-section {
  margin-bottom: 4rem;
}

.section-header {
  text-align: center;
  margin-bottom: 3rem;
}

.section-title {
  font-size: 2rem;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0 0 1rem;
}

.section-description {
  font-size: 1.125rem;
  color: var(--text-secondary);
  max-width: 700px;
  margin: 0 auto;
  line-height: 1.6;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 2rem;
}

.feature-card {
  background-color: var(--card-bg);
  border-radius: var(--border-radius-lg);
  padding: 2rem;
  text-align: center;
  box-shadow: var(--shadow-light);
  transition: all var(--transition-normal);
  border: 1px solid var(--border-color);
}

.feature-card:hover {
  transform: translateY(-5px);
  box-shadow: var(--shadow-medium);
}

.feature-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
  display: inline-block;
}

.feature-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 0.75rem;
}

.feature-description {
  color: var(--text-secondary);
  line-height: 1.6;
  margin: 0;
}

/* 状态区域 */
.status-section {
  margin-bottom: 4rem;
}

.status-card {
  background-color: var(--card-bg);
  border-radius: var(--border-radius-lg);
  box-shadow: var(--shadow-medium);
  padding: 1.5rem 2rem;
  display: flex;
  align-items: center;
  justify-content: space-around;
  flex-wrap: wrap;
  gap: 1.5rem;
}

.status-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.status-label {
  font-size: 0.9rem;
  color: var(--text-secondary);
}

.status-value {
  font-size: 1rem;
  font-weight: 600;
}

.status-online {
  color: var(--success-color);
}

.status-offline {
  color: var(--error-color);
}

.status-warning {
  color: var(--warning-color);
}

.connection-dot {
  display: inline-block;
  width: 0.5rem;
  height: 0.5rem;
  border-radius: 50%;
  background-color: var(--success-color);
  margin-right: 0.5rem;
  animation: pulse 2s infinite;
}

.status-divider {
  width: 1px;
  height: 2rem;
  background-color: var(--border-color);
  display: none;
}

/* CTA区域 */
.cta-section {
  background: linear-gradient(135deg, var(--accent-color) 0%, var(--primary-color) 100%);
  color: white;
  padding: 4rem 0;
  border-radius: var(--border-radius-lg);
  margin: 0 1.5rem 4rem;
  position: relative;
  overflow: hidden;
}

.cta-section::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-image: url("data:image/svg+xml,%3Csvg width='100' height='100' viewBox='0 0 100 100' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M11 18c3.866 0 7-3.134 7-7s-3.134-7-7-7-7 3.134-7 7 3.134 7 7 7zm48 25c3.866 0 7-3.134 7-7s-3.134-7-7-7-7 3.134-7 7 3.134 7 7 7zm-43-7c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zm63 31c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zM34 90c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zm56-76c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zM12 86c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm28-65c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm23-11c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm-6 60c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm29 22c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zM32 63c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm57-13c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm-9-21c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM60 91c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM35 41c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM12 60c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2z' fill='%23ffffff' fill-opacity='0.05' fill-rule='evenodd'/%3E%3C/svg%3E");
  opacity: 0.3;
}

.cta-content {
  text-align: center;
  position: relative;
}

.cta-content h2 {
  font-size: 2rem;
  font-weight: 700;
  margin: 0 0 1rem;
}

.cta-content p {
  font-size: 1.125rem;
  margin: 0 0 2rem;
  opacity: 0.9;
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
}

.cta-buttons {
  display: flex;
  justify-content: center;
  gap: 1rem;
  flex-wrap: wrap;
}

.register-cta-btn {
  background-color: white;
  color: var(--primary-color);
}

.login-cta-btn {
  background-color: transparent;
  color: white;
  border: 2px solid rgba(255, 255, 255, 0.3);
}

.login-cta-btn:hover {
  background-color: rgba(255, 255, 255, 0.1);
  border-color: white;
}

/* 页脚 */
.main-footer {
  background-color: #1e293b;
  color: white;
  padding: 4rem 0 2rem;
}

.footer-content {
  display: flex;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 2rem;
  margin-bottom: 3rem;
}

.footer-logo {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  min-width: 200px;
}

.footer-logo .logo-icon {
  font-size: 2rem;
}

.footer-logo h3 {
  font-size: 1.25rem;
  font-weight: 700;
  margin: 0;
}

.footer-logo p {
  font-size: 0.875rem;
  color: rgba(255, 255, 255, 0.7);
  margin: 0;
}

.footer-links {
  display: flex;
  gap: 3rem;
  flex-wrap: wrap;
}

.link-group h4 {
  font-size: 1rem;
  font-weight: 600;
  margin: 0 0 1rem;
  color: white;
}

.link-group ul {
  list-style: none;
  margin: 0;
  padding: 0;
}

.link-group li {
  margin-bottom: 0.5rem;
}

.link-group a {
  color: rgba(255, 255, 255, 0.7);
  text-decoration: none;
  font-size: 0.875rem;
  transition: color var(--transition-fast);
}

.link-group a:hover {
  color: white;
}

.footer-bottom {
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  padding-top: 1.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 1rem;
}

.footer-bottom p {
  margin: 0;
  font-size: 0.875rem;
  color: rgba(255, 255, 255, 0.7);
}

.social-links {
  display: flex;
  gap: 1rem;
}

.social-link {
  color: rgba(255, 255, 255, 0.7);
  text-decoration: none;
  font-size: 0.875rem;
  transition: color var(--transition-fast);
}

.social-link:hover {
  color: white;
}

/* 动画效果 */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes fadeInDelay {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes pulse {
  0% {
    box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.4);
  }
  70% {
    box-shadow: 0 0 0 10px rgba(16, 185, 129, 0);
  }
  100% {
    box-shadow: 0 0 0 0 rgba(16, 185, 129, 0);
  }
}

.fade-in {
  animation: fadeIn 0.8s ease forwards;
}

.fade-in-delay {
  animation: fadeInDelay 0.8s ease 0.3s forwards;
  opacity: 0;
}

.slide-up {
  animation: slideUp 0.6s ease forwards;
}

.pulse {
  animation: pulse 2s infinite;
}

.hover-effect:hover {
  transform: translateY(-5px);
}

/* 过渡动画 */
.dropdown-enter-active,
.dropdown-leave-active {
  transition: all var(--transition-fast);
}

.dropdown-enter-from,
.dropdown-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

/* 响应式设计 */
@media (max-width: 1024px) {
  .hero-content {
    gap: 2rem;
  }
  
  .hero-title {
    font-size: 2.5rem;
  }
  
  .footer-links {
    gap: 2rem;
  }
}

@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    height: auto;
    padding: 1rem 0;
    gap: 1rem;
  }
  
  .nav-section {
    flex-direction: column;
    gap: 1rem;
    width: 100%;
  }
  
  .main-nav .nav-links {
    justify-content: center;
    gap: 1rem;
    flex-wrap: wrap;
  }
  
  .hero-content {
    flex-direction: column;
    text-align: center;
  }
  
  .hero-title {
    font-size: 2rem;
  }
  
  .hero-cta {
    justify-content: center;
    flex-wrap: wrap;
  }
  
  .user-card {
    flex-direction: column;
    text-align: center;
  }
  
  .user-actions {
    justify-content: center;
  }
  
  .guest-notice {
    flex-direction: column;
    text-align: center;
  }
  
  .status-card {
    flex-direction: column;
    text-align: center;
    gap: 1rem;
  }
  
  .status-divider {
    display: none;
  }
  
  .features-grid {
    grid-template-columns: 1fr;
    max-width: 400px;
    margin: 0 auto;
  }
  
  .footer-content {
    flex-direction: column;
    align-items: center;
    text-align: center;
  }
  
  .footer-links {
    justify-content: center;
  }
  
  .footer-bottom {
    flex-direction: column;
  }
  
  .cta-buttons {
    flex-direction: column;
    align-items: center;
  }
  
  .primary-btn, .secondary-btn {
    width: 100%;
    max-width: 300px;
  }
}

@media (max-width: 480px) {
  .container {
    padding: 0 1rem;
  }
  
  .hero-section {
    padding: 4rem 0;
  }
  
  .hero-title {
    font-size: 1.75rem;
  }
  
  .hero-illustration {
    padding: 1.5rem;
  }
  
  .chat-bubble {
    font-size: 0.8rem;
    padding: 0.75rem;
  }
  
  .user-avatar img {
    width: 6rem;
    height: 6rem;
  }
  
  .user-name {
    font-size: 1.5rem;
  }
  
  .cta-section {
    margin: 0 1rem 3rem;
    padding: 3rem 1rem;
  }
}
</style>