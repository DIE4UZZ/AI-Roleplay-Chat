import api from '../utils/api';
import type { LoginFormData, RegisterFormData, LoginResponse, RegisterResponse, GuestResponse } from '../types/user';

// 认证服务
class AuthService {
  // 用户登录
  async login(credentials: LoginFormData): Promise<LoginResponse> {
    try {
      const response = await api.post<LoginResponse>('/auth/login', credentials);
      if (response.success) {
        // 存储token
        localStorage.setItem('token', response.token);
        // 存储用户信息
        localStorage.setItem('userInfo', JSON.stringify(response.userInfo));
      }
      return response;
    } catch (error) {
      console.error('登录失败:', error);
      throw error;
    }
  }

  // 用户注册
  async register(userData: RegisterFormData): Promise<RegisterResponse> {
    try {
      const response = await api.post<RegisterResponse>('/auth/register', userData);
      if (response.success && response.token) {
        // 注册成功后自动登录
        localStorage.setItem('token', response.token);
      }
      return response;
    } catch (error) {
      console.error('注册失败:', error);
      throw error;
    }
  }

  // 游客登录
  async guestLogin(): Promise<GuestResponse> {
    try {
      const response = await api.post<GuestResponse>('/auth/guest');
      if (response.success) {
        // 存储token
        localStorage.setItem('token', response.token);
        // 存储游客信息
        localStorage.setItem('isGuest', 'true');
        localStorage.setItem('trialCount', String(response.trialCount));
      }
      return response;
    } catch (error) {
      console.error('游客登录失败:', error);
      throw error;
    }
  }

  // 退出登录
  logout(): void {
    localStorage.removeItem('token');
    localStorage.removeItem('userInfo');
    localStorage.removeItem('isGuest');
    localStorage.removeItem('trialCount');
  }

  // 检查用户是否已登录
  isLoggedIn(): boolean {
    return !!localStorage.getItem('token');
  }

  // 获取当前用户信息
  getCurrentUser(): any {
    const userInfo = localStorage.getItem('userInfo');
    return userInfo ? JSON.parse(userInfo) : null;
  }

  // 检查是否为游客模式
  isGuest(): boolean {
    return localStorage.getItem('isGuest') === 'true';
  }

  // 获取剩余试用次数
  getTrialCount(): number {
    const trialCount = localStorage.getItem('trialCount');
    return trialCount ? parseInt(trialCount, 10) : 0;
  }
}

export default new AuthService();