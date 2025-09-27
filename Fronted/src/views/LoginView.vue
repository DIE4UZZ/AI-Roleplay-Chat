<template>
  <div class="login-container">
    <!-- 装饰性背景元素 -->
    <div class="bg-shapes">
      <div class="shape shape-1"></div>
      <div class="shape shape-2"></div>
      <div class="shape shape-3"></div>
    </div>
    
    <div class="login-content">
      <div class="login-card fade-in">
        <!-- 品牌标志 -->
        <div class="brand-logo">
          <div class="logo-icon">🎭</div>
          <div class="login-header">
            <h1>AI 角色扮演语音聊天</h1>
            <p>探索无限可能的对话世界</p>
          </div>
        </div>

        <!-- 标签页切换 -->
        <div class="tabs">
          <button 
            class="tab-btn" 
            :class="{ active: activeTab === 'login' }" 
            @click="switchTab('login')"
          >
            登录
          </button>
          <button 
            class="tab-btn" 
            :class="{ active: activeTab === 'register' }" 
            @click="switchTab('register')"
          >
            注册
          </button>
          <button 
            class="tab-btn" 
            :class="{ active: activeTab === 'guest' }" 
            @click="switchTab('guest')"
          >
            游客体验
          </button>
        </div>

        <!-- 登录表单 -->
        <Transition name="tab-fade" mode="out-in">
          <div v-if="activeTab === 'login'" key="login" class="form-container">
            <form @submit.prevent="handleLogin">
              <div class="form-group">
                <label for="login-username" class="form-label">用户名</label>
                <div class="input-wrapper">
                  <span class="input-icon">👤</span>
                  <input
                    id="login-username"
                    v-model="loginForm.username"
                    type="text"
                    placeholder="请输入用户名"
                    required
                    class="form-input"
                  />
                </div>
              </div>
              <div class="form-group">
                <label for="login-password" class="form-label">密码</label>
                <div class="input-wrapper">
                  <span class="input-icon">🔒</span>
                  <input
                    id="login-password"
                    v-model="loginForm.password"
                    type="password"
                    placeholder="请输入密码"
                    required
                    class="form-input"
                  />
                </div>
              </div>
              <button type="submit" class="submit-btn" :disabled="loading">
                <span v-if="loading" class="loading-spinner"></span>
                {{ loading ? '登录中...' : '登录' }}
              </button>
            </form>
          </div>

          <!-- 注册表单 -->
          <div v-else-if="activeTab === 'register'" key="register" class="form-container">
            <form @submit.prevent="handleRegister">
              <div class="form-group">
                <label for="register-username" class="form-label">用户名</label>
                <div class="input-wrapper">
                  <span class="input-icon">👤</span>
                  <input
                    id="register-username"
                    v-model="registerForm.username"
                    type="text"
                    placeholder="请设置用户名（3-20位字母、数字或下划线）"
                    required
                    class="form-input"
                    @input="handleUsernameInput"
                    :class="{ 'error': registerErrors.username }"
                  />
                </div>
                <div v-if="registerErrors.username" class="error-tip">
                  {{ registerErrors.username }}
                </div>
                <div v-else-if="registerForm.username && !registerErrors.username" class="success-tip">
                  用户名格式正确
                </div>
              </div>
              <div class="form-group">
                <label for="register-email" class="form-label">邮箱</label>
                <div class="input-wrapper">
                  <span class="input-icon">📧</span>
                  <input
                    id="register-email"
                    v-model="registerForm.email"
                    type="email"
                    placeholder="请输入邮箱"
                    required
                    class="form-input"
                  />
                </div>
              </div>
              <div class="form-group">
                <label for="register-password" class="form-label">密码</label>
                <div class="input-wrapper">
                  <span class="input-icon">🔒</span>
                  <input
                    id="register-password"
                    v-model="registerForm.password"
                    type="password"
                    placeholder="请设置密码（至少6位）"
                    required
                    class="form-input"
                    @input="handlePasswordInput"
                    :class="{ 'error': registerErrors.password }"
                  />
                </div>
                <div v-if="registerErrors.password" class="error-tip">
                  {{ registerErrors.password }}
                </div>
                <div v-else-if="registerForm.password && !registerErrors.password" class="success-tip">
                  密码格式正确
                </div>
              </div>
              <button type="submit" class="submit-btn" :disabled="loading || !isRegisterFormValid">
                <span v-if="loading" class="loading-spinner"></span>
                {{ loading ? '注册中...' : '注册' }}
              </button>
            </form>
          </div>

          <!-- 游客登录 -->
          <div v-else-if="activeTab === 'guest'" key="guest" class="form-container guest-container">
            <div class="guest-info">
              <div class="guest-icon">✨</div>
              <h3>游客体验</h3>
              <p class="guest-description">以游客身份体验我们的AI聊天服务，您将获得有限次数的免费试用。</p>
              <p class="warning-text">请注意：游客数据将在会话结束后清除，建议注册账号保存您的聊天记录。</p>
            </div>
            <button class="submit-btn guest-btn" :disabled="loading" @click="handleGuestLogin">
              <span v-if="loading" class="loading-spinner"></span>
              {{ loading ? '登录中...' : '开始游客体验' }}
            </button>
          </div>
        </Transition>

        <!-- 错误提示 -->
        <Transition name="slide-up">
          <div v-if="error" class="error-message">
            <span class="error-icon">⚠️</span>
            {{ error }}
          </div>
        </Transition>
      </div>
      
      <!-- 页脚信息 -->
      <div class="login-footer">
        <p>© 2023 AI 角色扮演语音聊天 | 探索无限可能</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import authService from '../services/auth.service';
import type { LoginFormData, RegisterFormData } from '../types/user';

// 路由实例
const router = useRouter();

// 状态管理
const activeTab = ref<'login' | 'register' | 'guest'>('login');
const loading = ref(false);
const error = ref('');

// 表单数据
const loginForm = ref<LoginFormData>({
  username: '',
  password: '',
});

const registerForm = ref<RegisterFormData>({
  username: '',
  password: '',
  email: '',
});

// 表单验证状态
const registerErrors = ref({
  username: '',
  password: '',
});

// 用户名特殊字符正则表达式（只允许字母、数字、下划线）
const usernameRegex = /^[a-zA-Z0-9_]{3,20}$/;

// 检查用户名是否有效
const validateUsername = (username: string): string => {
  if (!username) {
    return '请输入用户名';
  }
  if (!usernameRegex.test(username)) {
    return '用户名只能包含字母、数字和下划线，长度3-20位';
  }
  return '';
};

// 检查密码是否有效
const validatePassword = (password: string): string => {
  if (!password) {
    return '请输入密码';
  }
  if (password.length < 6) {
    return '密码长度至少为6位';
  }
  return '';
};

// 实时验证用户名
const handleUsernameInput = () => {
  registerErrors.value.username = validateUsername(registerForm.value.username);
};

// 实时验证密码
const handlePasswordInput = () => {
  registerErrors.value.password = validatePassword(registerForm.value.password);
};

// 计算表单是否有效
const isRegisterFormValid = computed(() => {
  return !registerErrors.value.username && 
         !registerErrors.value.password && 
         registerForm.value.username && 
         registerForm.value.password;
});

// 切换标签页
const switchTab = (tab: 'login' | 'register' | 'guest') => {
  activeTab.value = tab;
  error.value = ''; // 切换标签时清除错误信息
};

// 处理登录
const handleLogin = async () => {
  loading.value = true;
  error.value = '';

  try {
    const response = await authService.login(loginForm.value);
    if (response.success) {
      // 登录成功，跳转到首页
      router.push('/home');
    } else {
      error.value = '登录失败，请检查用户名和密码';
    }
  } catch (err) {
    error.value = '登录失败，请稍后重试';
    console.error('登录错误:', err);
  } finally {
    loading.value = false;
  }
};

// 处理注册
const handleRegister = async () => {
  // 再次验证表单
  registerErrors.value.username = validateUsername(registerForm.value.username);
  registerErrors.value.password = validatePassword(registerForm.value.password);
  
  if (!isRegisterFormValid.value) {
    return;
  }

  loading.value = true;
  error.value = '';

  try {
    const response = await authService.register(registerForm.value);
    if (response.success) {
      // 注册成功，跳转到首页
      router.push('/home');
    } else {
      // 处理后端返回的错误，特别是用户名已存在的错误
      error.value = response.message || '注册失败，请稍后重试';
      if (error.value.includes('用户名已存在')) {
        registerErrors.value.username = error.value;
      }
    }
  } catch (err) {
    // 捕获网络请求错误
    const errorObj = err as any;
    if (errorObj.response?.data?.message?.includes('用户名已存在')) {
      error.value = '用户名已存在，请更换其他用户名';
      registerErrors.value.username = error.value;
    } else {
      error.value = '注册失败，请稍后重试';
    }
    console.error('注册错误:', err);
  } finally {
    loading.value = false;
  }
};

// 处理游客登录
const handleGuestLogin = async () => {
  loading.value = true;
  error.value = '';

  try {
    const response = await authService.guestLogin();
    if (response.success) {
      // 游客登录成功，跳转到首页
      router.push('/home');
    } else {
      error.value = '游客登录失败，请稍后重试';
    }
  } catch (err) {
    error.value = '游客登录失败，请稍后重试';
    console.error('游客登录错误:', err);
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
/* CSS Variables */
:root {
  --primary-color: #667eea;
  --secondary-color: #764ba2;
  --accent-color: #f093fb;
  --text-primary: #333;
  --text-secondary: #666;
  --text-muted: #999;
  --card-bg: white;
  --bg-primary: #f8f9fa;
  --bg-secondary: #f0f2f5;
  --input-bg: #ffffff;
  --border-color: #e0e0e0;
  --error-bg: #ffebee;
  --error-color: #c62828;
  --error-border: #ffcdd2;
  --warning-color: #ff6b6b;
  --success-color: #4caf50;
  --bg-gradient-primary: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  --btn-gradient-primary: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  --btn-gradient-secondary: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  --card-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  --btn-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
}

/* 主容器样式 */
.login-container {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: var(--bg-gradient-primary);
  padding: 20px;
  position: relative;
  overflow: hidden;
}

/* 装饰性背景元素 */
.bg-shapes {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 0;
}

.shape {
  position: absolute;
  border-radius: 50%;
  filter: blur(60px);
  opacity: 0.4;
  animation: float 8s infinite ease-in-out;
}

.shape-1 {
  top: 10%;
  left: 10%;
  width: 300px;
  height: 300px;
  background: var(--primary-color);
  animation-delay: 0s;
}

.shape-2 {
  bottom: 15%;
  right: 15%;
  width: 400px;
  height: 400px;
  background: var(--secondary-color);
  animation-delay: 2s;
}

.shape-3 {
  top: 40%;
  right: 20%;
  width: 250px;
  height: 250px;
  background: var(--accent-color);
  animation-delay: 4s;
}

/* 登录内容容器 */
.login-content {
  position: relative;
  z-index: 1;
  width: 100%;
  max-width: 500px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
}

/* 登录卡片样式 */
.login-card {
  background: var(--card-bg);
  border-radius: 20px;
  padding: 40px;
  width: 100%;
  box-shadow: var(--card-shadow);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

/* 品牌标志 */
.brand-logo {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 15px;
  margin-bottom: 30px;
}

.logo-icon {
  font-size: 3rem;
  animation: pulse 2s infinite;
}

/* 标题样式 */
.login-header h1 {
  color: var(--text-primary);
  margin-bottom: 8px;
  font-size: 2rem;
  font-weight: 700;
  text-align: center;
}

.login-header p {
  color: var(--text-secondary);
  margin-bottom: 0;
  font-size: 1rem;
  text-align: center;
  opacity: 0.9;
}

/* 标签页样式 */
.tabs {
  display: flex;
  margin-bottom: 30px;
  border-radius: 12px;
  overflow: hidden;
  background: var(--bg-secondary);
  padding: 4px;
}

.tab-btn {
  flex: 1;
  padding: 12px 16px;
  border: none;
  background: transparent;
  cursor: pointer;
  font-size: 1rem;
  color: var(--text-secondary);
  font-weight: 500;
  border-radius: 8px;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.tab-btn:hover {
  color: var(--primary-color);
  background: rgba(102, 126, 234, 0.1);
}

.tab-btn.active {
  color: white;
  background: var(--primary-color);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

/* 表单容器 */
.form-container {
  width: 100%;
}

/* 表单组样式 */
.form-group {
  margin-bottom: 20px;
}

.form-label {
  display: block;
  margin-bottom: 8px;
  color: var(--text-primary);
  font-weight: 500;
  font-size: 0.9rem;
}

.input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.input-icon {
  position: absolute;
  left: 12px;
  font-size: 1.1rem;
  color: var(--text-secondary);
  z-index: 1;
}

.form-input {
  width: 100%;
  padding: 12px 16px 12px 40px;
  border: 1px solid var(--border-color);
  border-radius: 12px;
  font-size: 1rem;
  background: var(--input-bg);
  color: var(--text-primary);
  transition: all 0.3s ease;
}

.form-input:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
  transform: translateY(-1px);
}

.form-input::placeholder {
  color: var(--text-muted);
}

/* 按钮样式 */
.submit-btn {
  width: 100%;
  padding: 14px;
  background: var(--btn-gradient-primary);
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  position: relative;
  overflow: hidden;
}

.submit-btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
  transition: left 0.6s ease;
}

.submit-btn:hover:not(:disabled)::before {
  left: 100%;
}

.submit-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: var(--btn-shadow);
}

.submit-btn:active:not(:disabled) {
  transform: translateY(0);
}

.submit-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
  transform: none;
}

.guest-btn {
  background: var(--btn-gradient-secondary);
}

/* 游客登录容器 */
.guest-container {
  text-align: center;
}

.guest-info {
  margin-bottom: 30px;
  padding: 20px;
  background: var(--bg-secondary);
  border-radius: 12px;
  border: 1px solid var(--border-color);
}

.guest-icon {
  font-size: 3rem;
  margin-bottom: 15px;
  animation: pulse 2s infinite;
}

.guest-info h3 {
  color: var(--text-primary);
  margin-bottom: 15px;
  font-size: 1.4rem;
}

.guest-description {
  color: var(--text-secondary);
  line-height: 1.6;
  margin-bottom: 15px;
  font-size: 0.95rem;
}

.warning-text {
  color: var(--warning-color);
  font-weight: 500;
  font-size: 0.9rem;
  padding: 10px;
  background: rgba(255, 107, 107, 0.1);
  border-radius: 8px;
  display: inline-block;
}

/* 错误提示样式 */
.error-message {
  background: var(--error-bg);
  color: var(--error-color);
  padding: 12px 16px;
  border-radius: 12px;
  margin-top: 20px;
  text-align: center;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  font-size: 0.95rem;
  border: 1px solid var(--error-border);
}

/* 输入错误状态 */
.form-input.error {
  border-color: var(--error-color);
  box-shadow: 0 0 0 3px rgba(198, 40, 40, 0.1);
}

/* 输入框提示信息 */
.error-tip {
  color: var(--error-color);
  font-size: 0.85rem;
  margin-top: 6px;
  display: flex;
  align-items: center;
  gap: 4px;
}

.success-tip {
  color: var(--success-color);
  font-size: 0.85rem;
  margin-top: 6px;
  display: flex;
  align-items: center;
  gap: 4px;
}

.error-icon {
  font-size: 1.1rem;
}

/* 页脚样式 */
.login-footer {
  text-align: center;
  padding: 10px;
}

.login-footer p {
  color: rgba(255, 255, 255, 0.8);
  font-size: 0.85rem;
  margin: 0;
}

/* 加载动画 */
.loading-spinner {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top-color: white;
  animation: spin 1s ease-in-out infinite;
}

/* 动画定义 */
@keyframes spin {
  to { transform: rotate(360deg); }
}

@keyframes float {
  0%, 100% { transform: translateY(0) rotate(0deg); }
  50% { transform: translateY(-20px) rotate(5deg); }
}

@keyframes pulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.1); }
}

/* 标签页切换过渡 */
.tab-fade-enter-active,
.tab-fade-leave-active {
  transition: all 0.3s ease;
}

.tab-fade-enter-from {
  opacity: 0;
  transform: translateX(20px);
}

.tab-fade-leave-to {
  opacity: 0;
  transform: translateX(-20px);
}

/* 错误提示过渡 */
.slide-up-enter-active,
.slide-up-leave-active {
  transition: all 0.3s ease;
}

.slide-up-enter-from {
  opacity: 0;
  transform: translateY(10px);
}

.slide-up-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

/* 淡入动画 */
.fade-in {
  animation: fadeIn 0.5s ease-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 响应式设计 */
@media (max-width: 768px) {
  .login-card {
    padding: 25px;
  }

  .brand-logo {
    flex-direction: column;
    gap: 10px;
  }

  .login-header h1 {
    font-size: 1.6rem;
  }

  .tabs {
    padding: 3px;
  }

  .tab-btn {
    padding: 10px 8px;
    font-size: 0.9rem;
  }

  .form-input {
    padding: 12px 14px 12px 36px;
  }

  .submit-btn {
    padding: 13px;
    font-size: 1rem;
  }

  .shape {
    transform: scale(0.7);
  }
}

@media (max-width: 480px) {
  .login-container {
    padding: 15px;
  }

  .login-card {
    padding: 20px;
    border-radius: 16px;
  }

  .login-header h1 {
    font-size: 1.4rem;
  }

  .form-group {
    margin-bottom: 16px;
  }

  .guest-info {
    padding: 16px;
  }
}
</style>