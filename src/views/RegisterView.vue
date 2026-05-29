<template>
  <div class="register-page">
    <div class="register-card">
      <!-- Logo -->
      <div class="register-logo">
        <h1>🎬 注册账号</h1>
        <p>加入 CQUPT Movie，畅享精彩影视</p>
      </div>

      <!-- 错误提示 -->
      <div v-if="errorMsg" class="alert alert-error">
        {{ errorMsg }}
      </div>

      <!-- 成功提示 -->
      <div v-if="successMsg" class="alert alert-success">
        {{ successMsg }}
      </div>

      <!-- 注册表单 -->
      <form @submit.prevent="handleRegister">
        <div class="form-group">
          <label class="form-label" for="username">用户名</label>
          <input
            id="username"
            v-model.trim="form.username"
            type="text"
            class="form-control"
            placeholder="请输入用户名（至少2个字符）"
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
            placeholder="请输入密码（至少6个字符）"
            autocomplete="new-password"
            required
          />
        </div>

        <div class="form-group">
          <label class="form-label" for="confirm_password">确认密码</label>
          <input
            id="confirm_password"
            v-model="form.confirmPassword"
            type="password"
            class="form-control"
            placeholder="请再次输入密码"
            autocomplete="new-password"
            required
          />
        </div>

        <button
          type="submit"
          class="btn btn-primary btn-block btn-lg"
          :disabled="loading"
        >
          <span v-if="loading" class="spinner"></span>
          {{ loading ? '注册中...' : '注 册' }}
        </button>

        <div class="register-footer">
          已有账号？
          <router-link to="/login">立即登录</router-link>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
/**
 * 注册页面
 * 支持用户名和密码注册
 */
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()

/** 表单数据 */
const form = reactive({
  username: '',
  password: '',
  confirmPassword: '',
})

/** 加载状态 */
const loading = ref(false)

/** 错误信息 */
const errorMsg = ref('')

/** 成功信息 */
const successMsg = ref('')

/** 处理注册 */
async function handleRegister() {
  errorMsg.value = ''
  successMsg.value = ''

  // 表单校验
  if (!form.username.trim() || form.username.trim().length < 2) {
    errorMsg.value = '用户名至少需要 2 个字符'
    return
  }
  if (!form.password || form.password.length < 6) {
    errorMsg.value = '密码至少需要 6 个字符'
    return
  }
  if (form.password !== form.confirmPassword) {
    errorMsg.value = '两次密码输入不一致'
    return
  }

  loading.value = true
  try {
    const result = await userStore.register(form.username.trim(), form.password)
    if (result.success) {
      successMsg.value = '注册成功！即将跳转到登录页...'
      setTimeout(() => {
        router.push('/login')
      }, 1500)
    } else {
      errorMsg.value = result.message
    }
  } catch (err: any) {
    errorMsg.value = err?.response?.data?.message || '注册失败，请稍后重试'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.register-page {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
  padding: 20px;
}

.register-card {
  width: 100%;
  max-width: 420px;
  background: #fff;
  border-radius: 16px;
  padding: 40px 36px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}

.register-logo {
  text-align: center;
  margin-bottom: 32px;
}

.register-logo h1 {
  font-size: 26px;
  color: var(--color-dark);
  margin-bottom: 8px;
}

.register-logo p {
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

.alert-success {
  background: #d4edda;
  color: #155724;
  border: 1px solid #c3e6cb;
}

.register-footer {
  text-align: center;
  margin-top: 24px;
  font-size: 14px;
  color: var(--color-text-muted);
}

.register-footer a {
  font-weight: 500;
}
</style>
