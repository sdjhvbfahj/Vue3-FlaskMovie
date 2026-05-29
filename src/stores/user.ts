/**
 * 用户状态管理 Store（Pinia）
 *
 * 管理用户登录状态、用户信息，提供登录/登出/注册等操作
 */

import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { User } from '@/types'
import * as authApi from '@/api/auth'

export const useUserStore = defineStore('user', () => {
  /* ================== 状态 ================== */

  /** 当前用户信息（null 表示未登录） */
  const user = ref<User | null>(null)

  /** JWT Token */
  const token = ref<string>('')

  /** 是否正在加载用户信息 */
  const loading = ref(false)

  /* ================== 计算属性 ================== */

  /** 是否已登录 */
  const isLoggedIn = computed(() => !!token.value && !!user.value)

  /** 当前用户名 */
  const username = computed(() => user.value?.username || '')

  /** 是否为管理员 */
  const isAdmin = computed(() => user.value?.username === 'admin')

  /* ================== 方法 ================== */

  /**
   * 从 localStorage 恢复登录状态
   * 在应用启动时调用
   */
  function restoreFromStorage() {
    const savedToken = localStorage.getItem('token')
    const savedUser = localStorage.getItem('user')

    if (savedToken) {
      token.value = savedToken
    }

    if (savedUser) {
      try {
        user.value = JSON.parse(savedUser)
      } catch {
        // JSON 解析失败，清除无效数据
        clearAuth()
      }
    }
  }

  /**
   * 保存登录状态到 localStorage
   */
  function persistAuth(authToken: string, authUser: User) {
    token.value = authToken
    user.value = authUser
    localStorage.setItem('token', authToken)
    localStorage.setItem('user', JSON.stringify(authUser))
  }

  /**
   * 清除登录状态
   */
  function clearAuth() {
    token.value = ''
    user.value = null
    localStorage.removeItem('token')
    localStorage.removeItem('user')
  }

  /**
   * 登录
   */
  async function login(username: string, password: string): Promise<boolean> {
    loading.value = true
    try {
      const res = await authApi.login({ username, password })
      if (res.code === 200) {
        persistAuth(res.data.token, res.data.user)
        return true
      }
      return false
    } finally {
      loading.value = false
    }
  }

  /**
   * 注册
   */
  async function register(
    username: string,
    password: string
  ): Promise<{ success: boolean; message: string }> {
    loading.value = true
    try {
      const res = await authApi.register({ username, password })
      if (res.code === 200) {
        return { success: true, message: res.message || '注册成功' }
      }
      return { success: false, message: res.message || '注册失败' }
    } finally {
      loading.value = false
    }
  }

  /**
   * 登出
   */
  function logout() {
    clearAuth()
  }

  /**
   * 刷新用户信息（从服务器获取最新数据）
   */
  async function refreshUser(): Promise<void> {
    if (!token.value) return
    try {
      const res = await authApi.getCurrentUser()
      if (res.code === 200) {
        user.value = res.data
        localStorage.setItem('user', JSON.stringify(res.data))
      }
    } catch {
      // token 失效
      clearAuth()
    }
  }

  return {
    // 状态
    user,
    token,
    loading,
    // 计算属性
    isLoggedIn,
    username,
    isAdmin,
    // 方法
    restoreFromStorage,
    login,
    register,
    logout,
    refreshUser,
  }
})
