import { defineStore } from 'pinia';
import type { UserInfo } from '../types/user';

// 定义用户认证状态store
interface AuthState {
  userInfo: UserInfo | null;
  isLoggedIn: boolean;
  isGuest: boolean;
  trialCount: number;
  loading: boolean;
  error: string | null;
}

export const useAuthStore = defineStore('auth', {
  state: (): AuthState => ({
    userInfo: null,
    isLoggedIn: false,
    isGuest: false,
    trialCount: 0,
    loading: false,
    error: null,
  }),

  getters: {
    // 获取当前用户信息
    currentUser(): UserInfo | null {
      return this.userInfo;
    },
    // 检查是否为登录状态
    isAuthenticated(): boolean {
      return this.isLoggedIn;
    },
    // 检查是否为游客模式
    isGuestMode(): boolean {
      return this.isGuest;
    },
  },

  actions: {
    // 设置用户信息
    setUserInfo(userInfo: UserInfo | null): void {
      this.userInfo = userInfo;
    },
    // 设置登录状态
    setLoggedIn(loggedIn: boolean): void {
      this.isLoggedIn = loggedIn;
    },
    // 设置游客模式
    setGuest(guest: boolean): void {
      this.isGuest = guest;
    },
    // 设置试用次数
    setTrialCount(count: number): void {
      this.trialCount = count;
    },
    // 设置加载状态
    setLoading(loading: boolean): void {
      this.loading = loading;
    },
    // 设置错误信息
    setError(error: string | null): void {
      this.error = error;
    },
    // 初始化用户状态
    initializeUserState(): void {
      const token = localStorage.getItem('token');
      const userInfoStr = localStorage.getItem('userInfo');
      const isGuest = localStorage.getItem('isGuest') === 'true';
      const trialCountStr = localStorage.getItem('trialCount');

      this.isLoggedIn = !!token;
      this.isGuest = isGuest;
      this.trialCount = trialCountStr ? parseInt(trialCountStr, 10) : 0;
      this.userInfo = userInfoStr ? JSON.parse(userInfoStr) : null;
    },
    // 清除用户状态
    clearUserState(): void {
      this.userInfo = null;
      this.isLoggedIn = false;
      this.isGuest = false;
      this.trialCount = 0;
      this.error = null;
    },
  },
});