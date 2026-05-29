/**
 * 认证相关 API 接口
 * 包含登录、注册、获取当前用户信息
 */

import apiClient from './client'
import type {
  ApiResponse,
  LoginRequest,
  LoginResponse,
  RegisterRequest,
  User,
} from '@/types'

/**
 * 用户注册
 */
export function register(data: RegisterRequest): Promise<ApiResponse<User>> {
  return apiClient.post('/auth/register', data).then((res) => res.data)
}

/**
 * 用户登录
 */
export function login(data: LoginRequest): Promise<LoginResponse> {
  return apiClient.post('/auth/login', data).then((res) => res.data)
}

/**
 * 获取当前登录用户信息（需要 Token）
 */
export function getCurrentUser(): Promise<ApiResponse<User>> {
  return apiClient.get('/auth/me').then((res) => res.data)
}
