<template>
  <div class="login-page">
    <div class="login-card">
      <!-- Logo -->
      <div class="login-logo">
        <h1>🎬 CQUPT Movie</h1>
        <p>登录你的账号，发现精彩电影</p>
      </div>

      <!-- 错误提示 -->
      <div v-if="errorMsg" class="alert alert-error">
        {{ errorMsg }}
      </div>

      <!-- 登录表单 -->
      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label class="form-label" for="username">用户名</label>
          <input
            id="username"
            v-model.trim="form.username"
            type="text"
            class="form-control"
            placeholder="请输入用户名"
            autocomplete="username"
            required
          />
        </div>

        <div class="form-group">
          <label class="form-label" for="password">密码</label>
          <input
            id="password"
            v-model="form.password"
            type="password"
            class="form-control"
            placeholder="请输入密码"
            autocomplete="current-password"
            required
          />
        </div>

        <button
          type="submit"
          class="btn btn-primary btn-block btn-lg"
          :disabled="loading"
        >
          <span v-if="loading" class="spinner"></span>
          {{ loading ? '登录中...' : '登 录' }}
        </button>

        <div class="login-footer">
          还没有账号？
          <router-link to="/register">立即注册</router-link>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
/**
 * 登录页面
 * 支持用户名和密码登录，登录成功后重定向
 */
import { ref, reactive } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()

/** 表单数据 */
const form = reactive({
  username: '',
  password: '',
})

/** 加载状态 */
const loading = ref(false)

/** 错误信息 */
const errorMsg = ref('')

/** 处理登录 */
async function handleLogin() {
  // 清空之前的错误
  errorMsg.value = ''

  // 表单校验
  if (!form.username.trim()) {
    errorMsg.value = '请输入用户名'
    return
  }
  if (!form.password) {
    errorMsg.value = '请输入密码'
    return
  }

  loading.value = true
  try {
    await userStore.login(form.username.trim(), form.password)

    // 登录成功后检查是否有重定向参数
    const redirect = (route.query.redirect as string) || '/'
    router.push(redirect)
  } catch (err: any) {
    const msg = err?.response?.data?.message || '登录失败，请检查用户名和密码'
    errorMsg.value = msg
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-page {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
  padding: 20px;
}

.login-card {
  width: 100%;
  max-width: 400px;
  background: #fff;
  border-radius: 16px;
  padding: 40px 36px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}

.login-logo {
  text-align: center;
  margin-bottom: 32px;
}

.login-logo h1 {
  font-size: 26px;
  color: var(--color-dark);
  margin-bottom: 8px;
}

.login-logo p {
  color: var(--color-text-muted);
  font-size: 14px;
}

.alert {
  padding: 10px 14px;
  border-radius: var(--border-radius);
  font-size: 14px;
  margin-bottom: 16px;
}

.alert-error {
  background: #ffe0e0;
  color: #c0392b;
  border: 1px solid #f5c6cb;
}

.login-footer {
  text-align: center;
  margin-top: 24px;
  font-size: 14px;
  color: var(--color-text-muted);
}

.login-footer a {
  font-weight: 500;
}
</style>
