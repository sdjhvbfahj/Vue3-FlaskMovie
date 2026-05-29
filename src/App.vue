<template>
  <div id="app-root">
    <!-- 顶部导航栏：登录后显示 -->
    <NavBar v-if="userStore.isLoggedIn" />

    <!-- 主内容区域 -->
    <main class="app-main">
      <router-view />
    </main>
  </div>
</template>

<script setup lang="ts">
/**
 * 根组件
 * 根据登录状态显示/隐藏顶部导航栏
 */
import { useUserStore } from '@/stores/user'
import NavBar from '@/components/NavBar.vue'

const userStore = useUserStore()
</script>

<style scoped>
.app-main {
  min-height: calc(100vh - 56px);
  padding-top: 56px;
}
</style>
