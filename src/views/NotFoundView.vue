<template>
  <div class="not-found-page">
    <div class="not-found-content">
      <h1>404</h1>
      <h2>页面不存在</h2>
      <p>你访问的页面可能已被移动或删除。</p>
      <router-link to="/" class="btn btn-primary">返回首页</router-link>
    </div>
  </div>
</template>

<script setup lang="ts">
/**
 * 404 页面不存在
 */
</script>

<style scoped>
.not-found-page {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 60vh;
  text-align: center;
}

.not-found-content h1 {
  font-size: 96px;
  font-weight: 800;
  color: var(--color-primary);
  line-height: 1;
  margin-bottom: 8px;
}

.not-found-content h2 {
  font-size: 24px;
  margin-bottom: 12px;
}

.not-found-content p {
  color: var(--color-text-muted);
  margin-bottom: 24px;
}
</style>
