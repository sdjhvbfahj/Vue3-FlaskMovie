<template>
  <nav class="navbar">
    <div class="navbar__inner container">
      <!-- Logo -->
      <div class="navbar__logo">
        <router-link to="/" class="navbar__brand">
          🎬 CQUPT Movie
        </router-link>
      </div>

      <!-- 导航链接 -->
      <div class="navbar__links">
        <router-link to="/" class="navbar__link" active-class="navbar__link--active">
          首页
        </router-link>
        <router-link to="/movies" class="navbar__link" active-class="navbar__link--active">
          电影库
        </router-link>
        <router-link
          v-if="userStore.isAdmin"
          to="/admin"
          class="navbar__link navbar__link--admin"
          active-class="navbar__link--active"
        >
          ⚙ 后台
        </router-link>
      </div>

      <!-- 用户区域 -->
      <div class="navbar__user">
        <router-link
          :to="`/profile/${userStore.username}`"
          class="navbar__user-link"
        >
          <span class="navbar__avatar">
            {{ userStore.username.charAt(0).toUpperCase() }}
          </span>
          <span class="navbar__username">{{ userStore.username }}</span>
        </router-link>
        <button class="btn btn-sm btn-danger" @click="handleLogout">
          退出
        </button>
      </div>
    </div>
  </nav>
</template>

<script setup lang="ts">
/**
 * 顶部导航栏组件
 * 显示 Logo、导航链接、用户信息和退出按钮
 */
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()

/** 退出登录 */
function handleLogout() {
  userStore.logout()
  router.push('/login')
}
</script>

<style scoped>
.navbar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: var(--nav-height, 56px);
  background: var(--color-dark);
  color: #fff;
  z-index: 1000;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

.navbar__inner {
  display: flex;
  align-items: center;
  height: 100%;
  gap: 24px;
}

.navbar__logo {
  flex-shrink: 0;
}

.navbar__brand {
  font-size: 18px;
  font-weight: 700;
  color: #fff;
  letter-spacing: 0.5px;
}

.navbar__brand:hover {
  color: var(--color-warning);
}

.navbar__links {
  display: flex;
  align-items: center;
  gap: 8px;
  flex: 1;
}

.navbar__link {
  padding: 6px 14px;
  border-radius: 6px;
  font-size: 14px;
  color: rgba(255, 255, 255, 0.8);
  transition: var(--transition);
}

.navbar__link:hover {
  color: #fff;
  background: rgba(255, 255, 255, 0.1);
}

.navbar__link--active {
  color: var(--color-warning) !important;
  background: rgba(255, 193, 7, 0.1);
}

.navbar__link--admin {
  color: var(--color-info) !important;
}

.navbar__user {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-shrink: 0;
}

.navbar__user-link {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #fff;
  padding: 4px 8px;
  border-radius: 6px;
  transition: var(--transition);
}

.navbar__user-link:hover {
  background: rgba(255, 255, 255, 0.1);
  color: #fff;
}

.navbar__avatar {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: var(--color-primary);
  color: #fff;
  font-size: 14px;
  font-weight: 600;
}

.navbar__username {
  font-size: 14px;
  max-width: 100px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

@media (max-width: 768px) {
  .navbar__links {
    gap: 2px;
  }

  .navbar__link {
    padding: 4px 8px;
    font-size: 13px;
  }

  .navbar__username {
    display: none;
  }
}
</style>
