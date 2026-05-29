<template>
  <div class="play-page">
    <!-- 加载中 -->
    <div v-if="loading" class="loading-center">
      <span class="spinner"></span> 加载中...
    </div>

    <template v-else-if="movie">
      <!-- 视频播放区 -->
      <section class="play-video-section">
        <video
          v-if="movie.filename"
          class="movie-player"
          controls
          :poster="posterUrl"
          autoplay
        >
          <source
            :src="`/static/movie_video/${movie.filename}`"
            type="video/mp4"
          />
          您的浏览器不支持视频播放。
        </video>
        <div v-else class="no-video">
          <p>该影片暂无视频资源</p>
        </div>
      </section>

      <!-- 电影信息 -->
      <section class="play-meta container">
        <span class="detail-chip">{{ movie.category || '电影' }}</span>
        <h1>{{ movie.title }}</h1>
        <p class="detail-info">{{ movie.info }}</p>

        <div class="detail-actions">
          <button class="btn btn-outline" @click="router.back()">
            退出播放
          </button>
          <button
            class="btn btn-lg"
            :class="isCollected ? 'btn-warning' : 'btn-outline'"
            @click="handleToggleCollect"
          >
            {{ isCollected ? '⭐ 已收藏（点击取消）' : '☆ 收藏' }}
          </button>
        </div>
      </section>

      <!-- 推荐 -->
      <section v-if="recommends.length > 0" class="play-recommends container">
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
 * 电影播放页面
 * 展示视频播放器、电影信息、相关推荐
 */
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getMovieDetail } from '@/api/movie'
import { toggleCollect } from '@/api/collect'
import type { Movie } from '@/types'
import MovieCard from '@/components/MovieCard.vue'

const route = useRoute()
const router = useRouter()

/* ================== 状态 ================== */

const loading = ref(true)
const movie = ref<Movie | null>(null)
const isCollected = ref(false)
const recommends = ref<Movie[]>([])

const movieId = computed(() => Number(route.params.id))

const posterUrl = computed(() => {
  if (!movie.value?.poster) return ''
  if (movie.value.poster.startsWith('http')) return movie.value.poster
  return `/static/${movie.value.poster}`
})

/* ================== 方法 ================== */

async function loadData() {
  loading.value = true
  try {
    const res = await getMovieDetail(movieId.value)
    if (res.code === 200) {
      movie.value = res.data.movie
      isCollected.value = res.data.is_collected
      recommends.value = res.data.recommends
    }
  } catch (err) {
    console.error('加载播放页失败:', err)
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

onMounted(() => {
  loadData()
})
</script>

<style scoped>
.play-video-section {
  width: 100%;
  background: #000;
  display: flex;
  justify-content: center;
  padding: 20px 0;
}

.movie-player {
  width: 100%;
  max-width: 1080px;
  border-radius: 12px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5);
  outline: none;
}

.no-video {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 340px;
  color: #fff;
  font-size: 18px;
}

.play-meta {
  padding: 32px 0 0;
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

.play-meta h1 {
  font-size: 28px;
  margin-bottom: 8px;
}

.detail-info {
  font-size: 15px;
  color: var(--color-text-muted);
  line-height: 1.7;
  margin-bottom: 20px;
}

.detail-actions {
  display: flex;
  align-items: center;
  gap: 14px;
}

/* 推荐 */
.play-recommends {
  padding: 40px 0;
}

.play-recommends h3 {
  font-size: 20px;
  margin-bottom: 18px;
}

.recommend-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 20px;
}

@media (max-width: 768px) {
  .movie-player {
    border-radius: 0;
  }

  .play-meta h1 {
    font-size: 22px;
  }

  .recommend-grid {
    grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
    gap: 12px;
  }
}
</style>
