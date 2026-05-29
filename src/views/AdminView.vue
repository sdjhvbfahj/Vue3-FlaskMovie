<template>
  <div class="admin-page container">
    <!-- 头部统计 -->
    <div class="admin-header">
      <div>
        <h1>后台管理系统</h1>
        <p>统一管理用户、电影与评论内容</p>
      </div>
      <div class="admin-stats">
        <div class="stat-item">
          <span class="stat-label">用户数量</span>
          <span class="stat-value">{{ stats.user_count }}</span>
        </div>
        <div class="stat-item">
          <span class="stat-label">电影数量</span>
          <span class="stat-value">{{ stats.movie_count }}</span>
        </div>
        <div class="stat-item">
          <span class="stat-label">评论数量</span>
          <span class="stat-value">{{ stats.comment_count }}</span>
        </div>
      </div>
    </div>

    <!-- 工具栏 -->
    <div class="admin-toolbar">
      <router-link to="/admin/movies/add" class="btn btn-primary">新增电影</router-link>
      <form class="search-form" @submit.prevent="searchMovies">
        <input
          v-model.trim="movieKeyword"
          type="text"
          class="form-control"
          placeholder="搜索电影名称或简介"
        />
        <button type="submit" class="btn btn-primary btn-sm">搜索</button>
        <button
          v-if="movieKeyword"
          type="button"
          class="btn btn-outline btn-sm"
          @click="clearSearch"
        >
          清空
        </button>
      </form>
    </div>

    <!-- 用户管理 -->
    <div class="card admin-section">
      <h3>用户列表</h3>
      <div class="table-wrap">
        <table class="admin-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>用户名</th>
              <th>状态</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="u in users" :key="u.id">
              <td>{{ u.id }}</td>
              <td>
                {{ u.username }}
                <span v-if="u.is_banned === 1" class="badge badge-danger">已封禁</span>
              </td>
              <td>{{ u.is_banned === 1 ? '封禁中' : '正常' }}</td>
              <td class="action-cell">
                <router-link :to="`/profile/${u.username}`" class="btn btn-sm btn-info">
                  查看主页
                </router-link>
                <button
                  class="btn btn-sm"
                  :class="u.is_banned === 1 ? 'btn-success' : 'btn-danger'"
                  @click="handleToggleBan(u)"
                >
                  {{ u.is_banned === 1 ? '解封' : '封禁' }}
                </button>
              </td>
            </tr>
            <tr v-if="users.length === 0">
              <td colspan="4" class="empty-cell">暂无用户数据</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- 电影管理 -->
    <div class="card admin-section">
      <h3>电影管理</h3>
      <div class="table-wrap">
        <table class="admin-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>标题</th>
              <th>简介</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="m in movies" :key="m.id">
              <td>{{ m.id }}</td>
              <td>
                {{ m.title }}
                <span v-if="m.is_banner === 1" class="badge badge-banner">
                  Banner #{{ m.banner_order }}
                </span>
              </td>
              <td class="ellipsis-cell">{{ m.info }}</td>
              <td class="action-cell">
                <router-link :to="`/admin/movies/${m.id}/edit`" class="btn btn-sm btn-warning">
                  编辑
                </router-link>
                <button class="btn btn-sm btn-danger" @click="handleDeleteMovie(m)">
                  删除
                </button>
              </td>
            </tr>
            <tr v-if="movies.length === 0">
              <td colspan="4" class="empty-cell">暂无电影数据</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- 评论管理 -->
    <div class="card admin-section">
      <h3>评论管理</h3>
      <div class="comment-filter">
        <select v-model="commentMovieId" class="form-control" style="width: auto;" @change="loadComments">
          <option :value="undefined">全部影片</option>
          <option v-for="m in movies" :key="m.id" :value="m.id">{{ m.title }}</option>
        </select>
        <button
          v-if="commentMovieId"
          class="btn btn-outline btn-sm"
          @click="commentMovieId = undefined; loadComments()"
        >
          重置
        </button>
      </div>
      <div class="table-wrap">
        <table class="admin-table">
          <thead>
            <tr>
              <th>影片</th>
              <th>用户</th>
              <th>内容</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="c in adminComments" :key="c.id">
              <td>{{ c.movie_title }}</td>
              <td>{{ c.user }}</td>
              <td class="ellipsis-cell">{{ c.content }}</td>
              <td>
                <button class="btn btn-sm btn-danger" @click="handleDeleteComment(c.id)">
                  删除
                </button>
              </td>
            </tr>
            <tr v-if="adminComments.length === 0">
              <td colspan="4" class="empty-cell">暂无评论数据</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
/**
 * 管理后台首页
 * 提供用户管理、电影管理、评论管理功能
 * 仅 admin 用户可访问
 */
import { ref, reactive, onMounted } from 'vue'
import {
  getAdminStats,
  getAdminUsers,
  getAdminMovies,
  getAdminComments,
  toggleBanUser,
  deleteMovie,
  adminDeleteComment,
} from '@/api/admin'
import type { User, Movie, Comment, AdminStats } from '@/types'

/* ================== 状态 ================== */

const stats = reactive<AdminStats>({ user_count: 0, movie_count: 0, comment_count: 0 })
const users = ref<User[]>([])
const movies = ref<Movie[]>([])
const adminComments = ref<Comment[]>([])
const movieKeyword = ref('')
const commentMovieId = ref<number | undefined>(undefined)

/* ================== 方法 ================== */

async function loadAll() {
  try {
    const [statsRes, usersRes, moviesRes, commentsRes] = await Promise.all([
      getAdminStats(),
      getAdminUsers(),
      getAdminMovies(),
      getAdminComments(),
    ])

    if (statsRes.code === 200) {
      Object.assign(stats, statsRes.data)
    }
    if (usersRes.code === 200) {
      users.value = usersRes.data.users
    }
    if (moviesRes.code === 200) {
      movies.value = moviesRes.data.movies
    }
    if (commentsRes.code === 200) {
      adminComments.value = commentsRes.data.comments
    }
  } catch (err) {
    console.error('加载后台数据失败:', err)
  }
}

async function searchMovies() {
  try {
    const res = await getAdminMovies({ keyword: movieKeyword.value || undefined })
    if (res.code === 200) {
      movies.value = res.data.movies
    }
  } catch (err) {
    console.error('搜索电影失败:', err)
  }
}

function clearSearch() {
  movieKeyword.value = ''
  loadAll()
}

async function loadComments() {
  try {
    const res = await getAdminComments({ movie_id: commentMovieId.value })
    if (res.code === 200) {
      adminComments.value = res.data.comments
    }
  } catch (err) {
    console.error('加载评论失败:', err)
  }
}

async function handleToggleBan(user: User) {
  if (user.username === 'admin') {
    alert('不能封禁管理员账号')
    return
  }
  if (!confirm(`确定${user.is_banned === 1 ? '解封' : '封禁'}用户「${user.username}」吗？`)) return

  try {
    const res = await toggleBanUser(user.id)
    if (res.code === 200) {
      user.is_banned = res.data.is_banned
    }
  } catch (err) {
    console.error('封禁操作失败:', err)
  }
}

async function handleDeleteMovie(movie: Movie) {
  if (!confirm(`确定删除电影「${movie.title}」吗？此操作不可恢复。`)) return
  try {
    const res = await deleteMovie(movie.id)
    if (res.code === 200) {
      loadAll()
    }
  } catch (err) {
    console.error('删除电影失败:', err)
  }
}

async function handleDeleteComment(commentId: number) {
  if (!confirm('确定删除该评论吗？')) return
  try {
    const res = await adminDeleteComment(commentId)
    if (res.code === 200) {
      adminComments.value = adminComments.value.filter((c) => c.id !== commentId)
    }
  } catch (err) {
    console.error('删除评论失败:', err)
  }
}

onMounted(() => {
  loadAll()
})
</script>

<style scoped>
.admin-page {
  padding: 32px 0;
}

.admin-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 24px;
  flex-wrap: wrap;
  gap: 16px;
}

.admin-header h1 {
  font-size: 26px;
}

.admin-header p {
  font-size: 14px;
  color: var(--color-text-muted);
}

.admin-stats {
  display: flex;
  gap: 16px;
}

.stat-item {
  text-align: center;
  padding: 12px 24px;
  background: #fff;
  border-radius: 10px;
  box-shadow: var(--shadow-sm);
}

.stat-label {
  display: block;
  font-size: 12px;
  color: var(--color-text-muted);
  margin-bottom: 4px;
}

.stat-value {
  font-size: 24px;
  font-weight: 700;
  color: var(--color-primary);
}

.admin-toolbar {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 20px;
  flex-wrap: wrap;
}

.admin-toolbar .search-form {
  display: flex;
  gap: 8px;
}

.admin-toolbar .search-form .form-control {
  width: 240px;
}

.admin-section {
  margin-bottom: 24px;
  padding: 24px;
}

.admin-section h3 {
  font-size: 18px;
  margin-bottom: 16px;
  padding-bottom: 12px;
  border-bottom: 2px solid #eee;
}

.table-wrap {
  overflow-x: auto;
}

.admin-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 14px;
}

.admin-table th,
.admin-table td {
  padding: 10px 12px;
  text-align: left;
  border-bottom: 1px solid #eee;
}

.admin-table th {
  font-weight: 600;
  background: #f8f9fa;
}

.action-cell {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
}

.ellipsis-cell {
  max-width: 260px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.empty-cell {
  text-align: center;
  color: var(--color-text-muted);
  padding: 32px !important;
}

.badge {
  display: inline-block;
  padding: 1px 8px;
  border-radius: 4px;
  font-size: 11px;
  margin-left: 6px;
}

.badge-danger {
  background: #f8d7da;
  color: #721c24;
}

.badge-banner {
  background: #fff3cd;
  color: #856404;
}

.comment-filter {
  display: flex;
  gap: 8px;
  margin-bottom: 12px;
}

.btn-info {
  background: var(--color-info);
  color: #fff;
}

@media (max-width: 768px) {
  .admin-stats {
    flex-wrap: wrap;
  }

  .stat-item {
    padding: 8px 16px;
  }

  .admin-toolbar .search-form .form-control {
    width: 160px;
  }
}
</style>
