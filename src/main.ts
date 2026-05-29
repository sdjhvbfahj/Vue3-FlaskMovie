/**
 * 应用入口文件
 * 初始化 Vue 应用、路由、状态管理
 */

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
import { useUserStore } from './stores/user'

// 全局样式
import './styles/global.css'

const app = createApp(App)

// 状态管理（Pinia）
const pinia = createPinia()
app.use(pinia)

// 路由
app.use(router)

// 挂载前恢复登录状态
const userStore = useUserStore()
userStore.restoreFromStorage()

app.mount('#app')
