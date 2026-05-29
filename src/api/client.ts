/**
 * Axios HTTP 客户端配置
 * 封装 API 请求，统一处理 Token 注入和错误响应
 */

import axios, { type AxiosInstance, type AxiosResponse } from 'axios'
import type { ApiResponse } from '@/types'

/**
 * 创建 Axios 实例
 *
 * baseURL 默认指向后端 Flask API 服务地址
 * 开发环境通常为 http://localhost:5000/api
 */
const apiClient: AxiosInstance = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000/api',
  timeout: 15000,
  headers: {
    'Content-Type': 'application/json',
  },
})

/**
 * 请求拦截器：自动注入 Authorization Token
 */
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error)
)

/**
 * 响应拦截器：统一处理错误
 * - 401: Token 过期或无效，清除登录状态
 * - 403: 无权限访问
 * - 其他错误透传
 */
apiClient.interceptors.response.use(
  (response: AxiosResponse<ApiResponse>) => {
    return response
  },
  (error) => {
    if (error.response) {
      const { status } = error.response

      if (status === 401) {
        // Token 过期，清除本地存储的登录信息
        localStorage.removeItem('token')
        localStorage.removeItem('user')
        // 跳转到登录页（避免在登录页重复跳转）
        if (window.location.pathname !== '/login') {
          window.location.href = '/login'
        }
      }
    }
    return Promise.reject(error)
  }
)

export default apiClient
