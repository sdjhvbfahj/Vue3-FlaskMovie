/**
 * Vite 构建配置
 * 配置路径别名、开发代理、构建选项等
 */

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { resolve } from 'path'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],

  // 路径别名：@ 指向 src 目录
  resolve: {
    alias: {
      '@': resolve(__dirname, 'src'),
    },
  },

  // 开发服务器配置
  server: {
    port: 3000,
    // API 代理：将 /api 请求转发到 Flask 后端
    proxy: {
      '/api': {
        target: 'http://localhost:5000',
        changeOrigin: true,
      },
      // 静态资源代理（图片、视频等）
      '/static': {
        target: 'http://localhost:5000',
        changeOrigin: true,
      },
    },
  },

  // 构建输出
  build: {
    outDir: 'dist',
    assetsDir: 'assets',
    sourcemap: false,
  },
})
