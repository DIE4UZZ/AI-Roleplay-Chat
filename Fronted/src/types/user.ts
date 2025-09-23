// 用户相关类型定义

export interface UserInfo {
  id: number;
  username: string;
}

export interface LoginResponse {
  success: boolean;
  token: string;
  userInfo: UserInfo;
}

export interface RegisterResponse {
  success: boolean;
  message: string;
  token: string;
}

export interface GuestResponse {
  success: boolean;
  token: string;
  trialCount: number;
}

export interface LoginFormData {
  username: string;
  password: string;
}

export interface RegisterFormData {
  username: string;
  password: string;
  email: string;
}