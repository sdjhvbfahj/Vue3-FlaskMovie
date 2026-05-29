<template>
  <div class="detail-page">
    <!-- 加载中 -->
    <div v-if="loading" class="loading-center">
      <span class="spinner"></span> 加载中...
    </div>

    <template v-else-if="movie">
      <!-- Hero 区 -->
      <section class="detail-hero">
        <div
          class="detail-hero__bg"
          :style="{ backgroundImage: `url(${posterUrl})` }"
        ></div>
        <div class="detail-hero__overlay"></div>

        <div class="detail-hero__content container">
          <div class="detail-poster">
            <img :src="posterUrl" :alt="movie.title" />
          </div>
          <div class="detail-meta">
            <span class="detail-chip">{{ movie.category || '电影' }}</span>
            <h1>{{ movie.title }}</h1>
            <p class="detail-info">{{ movie.info }}</p>

            <div class="detail-actions">
              <router-link
                :to="`/play/${movie.id}`"
                class="btn btn-primary btn-lg"
              >
                ▶ 播放
              </router-link>
              <button
                class="btn btn-lg"
                :class="isCollected ? 'btn-warning' : 'btn-outline'"
                @click="handleToggleCollect"
              >
                {{ isCollected ? '⭐ 已收藏（点击取消）' : '☆ 收藏' }}
              </button>
              <span class="detail-likes">⭐ {{ movie.likes }}</span>
            </div>
          </div>
        </div>
      </section>

      <!-- 评论区 -->
      <section class="detail-comments container">
        <div class="card">
          <div class="comments-head">
            <h3>💬 评论区</h3>
            <span>{{ pagination.total }} 条评论</span>
          </div>

          <!-- 发表评论 -->
          <form class="comment-form" @submit.prevent="handleSubmitComment">
            <textarea
              v-model="commentText"
              class="form-control"
              placeholder="写下你的想法..."
              rows="3"
              required
            ></textarea>
            <button type="submit" class="btn btn-primary" :disabled="submitting">
              {{ submitting ? '发布中...' : '发布评论' }}
            </button>
          </form>

          <!-- 评论列表 -->
          <div class="comment-list">
            <article
              v-for="c in comments"
              :key="c.id"
              class="comment-item"
            >
              <div class="comment-item__head">
                <div class="comment-user-time">
                  <strong>{{ c.user || '匿名用户' }}</strong>
                  <span class="comment-time">{{ c.created_at }}</span>
                </div>
                <button
                  v-if="canDeleteComment(c.user)"
                  class="btn btn-sm btn-danger"
                  @click="handleDeleteComment(c.id)"
                >
                  删除
                </button>
              </div>
              <p class="comment-content">{{ c.content }}</p>
            </article>

            <div v-if="comments.length === 0" class="empty-state">
              <p>暂无评论，抢个沙发吧。</p>
            </div>
          </div>
        </div>
      </section>

      <!-- 推荐 -->
      <section v-if="recommends.length > 0" class="detail-recommends container">
        <h3>相关推荐</h3>
        <div class="recommend-grid">
          <MovieCard
            v-for="rec in recommends"
            :key="rec.id"
            :movie="rec"
          />
        </div>
      </section>
    </template>
  </div>
</template>

<script setup lang="ts">
/**
 * 电影详情页面
 * 展示电影信息、收藏按钮、评论区、相关推荐
 */
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { getMovieDetail } from '@/api/movie'
import { getComments, createComment, deleteComment } from '@/api/comment'
import { toggleCollect } from '@/api/collect'
import type { Movie, Comment, Pagination } from '@/types'
import MovieCard from '@/components/MovieCard.vue'

const route = useRoute()
const userStore = useUserStore()

/* ================== 状态 ================== */

const loading = ref(true)
const movie = ref<Movie | null>(null)
const isCollected = ref(false)
const recommends = ref<Movie[]>([])
const comments = ref<Comment[]>([])
const pagination = ref<Pagination>({
  page: 1, per_page: 20, total: 0, pages: 0,
  has_prev: false, has_next: false,
})
const commentText = ref('')
const submitting = ref(false)

/* ================== 计算属性 ================== */

const movieId = computed(() => Number(route.params.id))

const posterUrl = computed(() => {
  if (!movie.value?.poster) return ''
  if (movie.value.poster.startsWith('http')) return movie.value.poster
  return `/static/${movie.value.poster}`
})

/* ================== 方法 ================== */

function canDeleteComment(commentUser: string): boolean {
  return (
    commentUser === userStore.username || userStore.isAdmin
  )
}

async function loadData() {
  loading.value = true
  try {
    const [detailRes, commentsRes] = await Promise.all([
      getMovieDetail(movieId.value),
      getComments(movieId.value),
    ])

    if (detailRes.code === 200) {
      movie.value = detailRes.data.movie
      isCollected.value = detailRes.data.is_collected
      recommends.value = detailRes.data.recommends
    }

    if (commentsRes.code === 200) {
      comments.value = commentsRes.data.comments
      pagination.value = commentsRes.data.pagination
    }
  } catch (err) {
    console.error('加载电影详情失败:', err)
  } finally {
    loading.value = false
  }
}

async function handleToggleCollect() {
  try {
    const res = await toggleCollect(movieId.value)
    if (res.code === 200) {
      isCollected.value = res.data.is_collected
      if (movie.value) {
        movie.value.likes = res.data.likes
      }
    }
  } catch (err) {
    console.error('收藏操作失败:', err)
  }
}

async function handleSubmitComment() {
  if (!commentText.value.trim()) return
  submitting.value = true
  try {
    const res = await createComment(movieId.value, commentText.value.trim())
    if (res.code === 200) {
      commentText.value = ''
      // 重新加载评论
      const commentsRes = await getComments(movieId.value)
      if (commentsRes.code === 200) {
        comments.value = commentsRes.data.comments
        pagination.value = commentsRes.data.pagination
      }
    }
  } catch (err) {
    console.error('评论失败:', err)
  } finally {
    submitting.value = false
  }
}

async function handleDeleteComment(commentId: number) {
  if (!confirm('确定删除这条评论吗？')) return
  try {
    const res = await deleteComment(commentId)
    if (res.code === 200) {
      // 重新加载评论
      const commentsRes = await getComments(movieId.value)
      if (commentsRes.code === 200) {
        comments.value = commentsRes.data.comments
        pagination.value = commentsRes.data.pagination
      }
    }
  } catch (err) {
    console.error('删除评论失败:', err)
  }
}

onMounted(() => {
  loadData()
})
</script>

<style scoped>
/* Hero */
.detail-hero {
  position: relative;
  min-height: 400px;
  overflow: hidden;
}

.detail-hero__bg {
  position: absolute;
  inset: 0;
  background-size: cover;
  background-position: center;
  filter: blur(20px) brightness(0.3);
  transform: scale(1.1);
}

.detail-hero__overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(180deg, rgba(0,0,0,0.2), rgba(0,0,0,0.7));
}

.detail-hero__content {
  position: relative;
  z-index: 2;
  display: flex;
  gap: 36px;
  padding: 48px 20px;
  align-items: center;
}

.detail-poster {
  flex-shrink: 0;
  width: 240px;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
}

.detail-poster img {
  width: 100%;
  aspect-ratio: 2/3;
  object-fit: cover;
}

.detail-meta {
  flex: 1;
  color: #fff;
}

.detail-chip {
  display: inline-block;
  padding: 2px 10px;
  border-radius: 4px;
  background: var(--color-primary);
  color: #fff;
  font-size: 12px;
  margin-bottom: 8px;
}

.detail-meta h1 {
  font-size: 30px;
  margin-bottom: 8px;
}

.detail-info {
  font-size: 15px;
  opacity: 0.85;
  line-height: 1.7;
  margin-bottom: 24px;
}

.detail-actions {
  display: flex;
  align-items: center;
  gap: 14px;
  flex-wrap: wrap;
}

.detail-likes {
  font-size: 18px;
  color: var(--color-warning);
}

/* 评论区 */
.detail-comments {
  padding: 40px 0;
}

.comments-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
}

.comments-head h3 {
  font-size: 20px;
}

.comments-head span {
  font-size: 14px;
  color: var(--color-text-muted);
}

.comment-form {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 24px;
}

.comment-form textarea {
  resize: vertical;
}

.comment-form button {
  align-self: flex-end;
}

.comment-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.comment-item {
  padding: 16px;
  border-radius: var(--border-radius);
  background: #f8f9fa;
}

.comment-item__head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 8px;
}

.comment-user-time {
  display: flex;
  align-items: center;
  gap: 12px;
}

.comment-time {
  font-size: 12px;
  color: var(--color-text-muted);
}

.comment-content {
  font-size: 14px;
  line-height: 1.6;
  color: var(--color-text);
}

/* 推荐 */
.detail-recommends {
  padding: 0 0 48px;
}

.detail-recommends h3 {
  font-size: 20px;
  margin-bottom: 18px;
}

.recommend-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 20px;
}

@media (max-width: 768px) {
  .detail-hero__content {
    flex-direction: column;
    align-items: flex-start;
    padding: 32px 16px;
  }

  .detail-poster {
    width: 160px;
  }

  .detail-meta h1 {
    font-size: 24px;
  }

  .recommend-grid {
    grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
    gap: 12px;
  }
}
</style>
