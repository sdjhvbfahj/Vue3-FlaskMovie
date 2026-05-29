<template>
  <div class="movie-card" @click="goToDetail">
    <div class="movie-card__poster">
      <img
        :src="posterUrl"
        :alt="movie.title"
        loading="lazy"
        @error="handleImageError"
      />
      <span v-if="movie.category" class="movie-card__badge">
        {{ movie.category }}
      </span>
    </div>
    <div class="movie-card__body">
      <h3 class="movie-card__title" :title="movie.title">
        {{ movie.title }}
      </h3>
      <p class="movie-card__meta">
        <span class="movie-card__heat">🔥 {{ movie.likes }}</span>
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
/**
 * 电影卡片组件
 * 用于首页、电影列表、收藏列表等页面展示电影信息
 */
import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'
import type { Movie } from '@/types'

const props = defineProps<{
  movie: Movie
}>()

const router = useRouter()

/** 是否图片加载失败 */
const imageError = ref(false)

/** 海报 URL */
const posterUrl = computed(() => {
  if (imageError.value || !props.movie.poster) {
    return ''
  }
  // 如果 poster 已经是完整 URL，直接使用
  if (props.movie.poster.startsWith('http')) {
    return props.movie.poster
  }
  return `/static/${props.movie.poster}`
})

/** 海报加载失败时显示占位 */
function handleImageError() {
  imageError.value = true
}

/** 跳转到电影详情 */
function goToDetail() {
  router.push(`/movie/${props.movie.id}`)
}
</script>

<style scoped>
.movie-card {
  cursor: pointer;
  border-radius: 12px;
  overflow: hidden;
  background: var(--color-card-bg);
  box-shadow: var(--shadow-sm);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.movie-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-md);
}

.movie-card__poster {
  position: relative;
  aspect-ratio: 2 / 3;
  overflow: hidden;
  background: #e9ecef;
}

.movie-card__poster img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.movie-card:hover .movie-card__poster img {
  transform: scale(1.05);
}

.movie-card__badge {
  position: absolute;
  top: 8px;
  left: 8px;
  padding: 2px 8px;
  border-radius: 4px;
  background: rgba(0, 0, 0, 0.65);
  color: #fff;
  font-size: 12px;
}

.movie-card__body {
  padding: 12px;
}

.movie-card__title {
  font-size: 15px;
  font-weight: 600;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  margin-bottom: 4px;
}

.movie-card__meta {
  font-size: 13px;
  color: var(--color-text-muted);
}

.movie-card__heat {
  color: var(--color-danger);
}
</style>
