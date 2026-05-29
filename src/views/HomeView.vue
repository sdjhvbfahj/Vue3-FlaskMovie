<template>
  <div class="home-page">
    <!-- Banner 轮播 -->
    <section class="banner-section" v-if="banners.length > 0">
      <div class="banner-carousel">
        <div
          v-for="(banner, index) in banners"
          :key="banner.id"
          class="banner-slide"
          :class="{ active: currentBannerIndex === index }"
          @click="goToDetail(banner.id)"
        >
          <img
            :src="getBannerImage(banner)"
            :alt="banner.title"
            class="banner-img"
          />
          <div class="banner-caption">
            <span class="banner-tag">热播推荐</span>
            <h2>{{ banner.title }}</h2>
            <p>{{ banner.info }}</p>
          </div>
        </div>
      </div>

      <!-- 轮播控制 -->
      <button class="carousel-btn carousel-btn--prev" @click="prevBanner">◀</button>
      <button class="carousel-btn carousel-btn--next" @click="nextBanner">▶</button>

      <!-- 指示器 -->
      <div class="banner-dots">
        <span
          v-for="(_, idx) in banners"
          :key="idx"
          class="banner-dot"
          :class="{ active: currentBannerIndex === idx }"
          @click="currentBannerIndex = idx"
        ></span>
      </div>
    </section>

    <!-- 分类导航 -->
    <aside class="elevator-nav" v-if="categories.length > 0">
      <button
        v-for="(cat, idx) in categories"
        :key="cat"
        class="elevator-item"
        :class="{ active: activeCategoryIdx === idx }"
        @click="scrollToCategory(idx)"
      >
        {{ cat }}
      </button>
      <button class="elevator-item elevator-top" @click="scrollToTop">
        ↑ 顶部
      </button>
    </aside>

    <!-- 分类电影区块 -->
    <section
      v-for="(cat, idx) in categories"
      :key="cat"
      :id="`cat-section-${idx}`"
      class="category-section container"
    >
      <header class="category-header">
        <h2>{{ cat }}</h2>
        <router-link
          :to="cat === '全部' ? '/movies' : `/movies?category=${encodeURIComponent(cat)}`"
          class="category-more"
        >
          查看更多 →
        </router-link>
      </header>

      <!-- 电影卡片网格 -->
      <div class="movie-grid" v-if="moviesByCategory[cat]?.length">
        <MovieCard
          v-for="movie in moviesByCategory[cat]"
          :key="movie.id"
          :movie="movie"
        />
      </div>

      <!-- 空状态 -->
      <div v-else class="empty-state">
        <p>该分类暂无电影</p>
      </div>
    </section>

    <!-- 加载中 -->
    <div v-if="loading" class="loading-center">
      <span class="spinner"></span>
      加载中...
    </div>
  </div>
</template>

<script setup lang="ts">
/**
 * 首页
 * 展示 Banner 轮播、分类电梯导航和各分类的电影列表
 */
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { getBanners, getHomeMovies } from '@/api/movie'
import type { Movie } from '@/types'
import MovieCard from '@/components/MovieCard.vue'

const router = useRouter()

/* ================== 状态 ================== */

/** 加载状态 */
const loading = ref(true)

/** Banner 列表 */
const banners = ref<Movie[]>([])

/** 当前 Banner 索引 */
const currentBannerIndex = ref(0)

/** 分类列表 */
const categories = ref<string[]>([])

/** 各分类下的电影 */
const moviesByCategory = ref<Record<string, Movie[]>>({})

/** 当前激活的分类索引 */
const activeCategoryIdx = ref(0)

/** Banner 自动轮播定时器 */
let bannerTimer: ReturnType<typeof setInterval> | null = null

/* ================== 方法 ================== */

/** 获取 Banner 图片 URL */
function getBannerImage(banner: Movie): string {
  if (!banner.poster) return ''
  if (banner.poster.startsWith('http')) return banner.poster
  return `/static/${banner.poster}`
}

/** 上一张 Banner */
function prevBanner() {
  if (banners.value.length === 0) return
  currentBannerIndex.value =
    (currentBannerIndex.value - 1 + banners.value.length) % banners.value.length
}

/** 下一张 Banner */
function nextBanner() {
  if (banners.value.length === 0) return
  currentBannerIndex.value =
    (currentBannerIndex.value + 1) % banners.value.length
}

/** 跳转到电影详情 */
function goToDetail(id: number) {
  router.push(`/movie/${id}`)
}

/** 滚动到指定分类 */
function scrollToCategory(idx: number) {
  activeCategoryIdx.value = idx
  const el = document.getElementById(`cat-section-${idx}`)
  if (el) {
    const navHeight = 56 + 10
    const y = el.getBoundingClientRect().top + window.scrollY - navHeight
    window.scrollTo({ top: y, behavior: 'smooth' })
  }
}

/** 滚动到顶部 */
function scrollToTop() {
  window.scrollTo({ top: 0, behavior: 'smooth' })
  activeCategoryIdx.value = 0
}

/** 监听滚动，更新激活分类 */
function onScroll() {
  const sections = document.querySelectorAll('.category-section')
  const offset = 56 + 30

  for (let i = sections.length - 1; i >= 0; i--) {
    const rect = sections[i].getBoundingClientRect()
    if (rect.top <= offset) {
      activeCategoryIdx.value = i
      return
    }
  }
  activeCategoryIdx.value = 0
}

/** 启动 Banner 自动轮播 */
function startBannerAutoPlay() {
  if (banners.value.length <= 1) return
  bannerTimer = setInterval(() => {
    nextBanner()
  }, 4000)
}

/** 停止 Banner 自动轮播 */
function stopBannerAutoPlay() {
  if (bannerTimer) {
    clearInterval(bannerTimer)
    bannerTimer = null
  }
}

/* ================== 生命周期 ================== */

onMounted(async () => {
  try {
    // 并行请求 Banner 和首页数据
    const [bannersRes, homeRes] = await Promise.all([
      getBanners(),
      getHomeMovies(),
    ])

    if (bannersRes.code === 200) {
      banners.value = bannersRes.data.banners
    }

    if (homeRes.code === 200) {
      categories.value = homeRes.data.categories
      moviesByCategory.value = homeRes.data.movies_by_category
    }

    startBannerAutoPlay()
    window.addEventListener('scroll', onScroll, { passive: true })
  } catch (err) {
    console.error('首页数据加载失败:', err)
  } finally {
    loading.value = false
  }
})

onUnmounted(() => {
  stopBannerAutoPlay()
  window.removeEventListener('scroll', onScroll)
})
</script>

<style scoped>
/* Banner */
.banner-section {
  position: relative;
  width: 100%;
  height: 420px;
  overflow: hidden;
  background: #000;
}

.banner-carousel {
  position: relative;
  width: 100%;
  height: 100%;
}

.banner-slide {
  position: absolute;
  inset: 0;
  opacity: 0;
  transition: opacity 0.6s ease;
  cursor: pointer;
}

.banner-slide.active {
  opacity: 1;
}

.banner-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.banner-caption {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 40px 60px;
  background: linear-gradient(transparent, rgba(0, 0, 0, 0.8));
  color: #fff;
}

.banner-tag {
  display: inline-block;
  padding: 2px 12px;
  border-radius: 4px;
  background: var(--color-danger);
  font-size: 12px;
  margin-bottom: 8px;
}

.banner-caption h2 {
  font-size: 28px;
  margin-bottom: 6px;
}

.banner-caption p {
  font-size: 14px;
  opacity: 0.85;
  max-width: 600px;
}

.carousel-btn {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  width: 44px;
  height: 44px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.2);
  color: #fff;
  font-size: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: background 0.2s;
  z-index: 10;
}

.carousel-btn:hover {
  background: rgba(255, 255, 255, 0.4);
}

.carousel-btn--prev {
  left: 16px;
}

.carousel-btn--next {
  right: 16px;
}

.banner-dots {
  position: absolute;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 8px;
}

.banner-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.4);
  cursor: pointer;
  transition: background 0.2s;
}

.banner-dot.active {
  background: #fff;
}

/* 电梯导航 */
.elevator-nav {
  position: fixed;
  right: 20px;
  top: 50%;
  transform: translateY(-50%);
  display: flex;
  flex-direction: column;
  gap: 4px;
  z-index: 100;
}

.elevator-item {
  padding: 6px 14px;
  border-radius: 6px;
  background: var(--color-card-bg);
  box-shadow: var(--shadow-sm);
  font-size: 13px;
  color: var(--color-text);
  transition: var(--transition);
  text-align: center;
  white-space: nowrap;
}

.elevator-item:hover,
.elevator-item.active {
  background: var(--color-primary);
  color: #fff;
}

.elevator-top {
  margin-top: 8px;
  border-top: 1px solid #eee;
  padding-top: 10px;
}

/* 分类区块 */
.category-section {
  padding: 48px 20px;
}

.category-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
}

.category-header h2 {
  font-size: 22px;
  font-weight: 700;
}

.category-more {
  font-size: 14px;
  color: var(--color-text-muted);
  transition: var(--transition);
}

.category-more:hover {
  color: var(--color-primary);
}

/* 电影网格 */
.movie-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 20px;
}

@media (max-width: 768px) {
  .banner-section {
    height: 240px;
  }

  .banner-caption {
    padding: 20px;
  }

  .banner-caption h2 {
    font-size: 20px;
  }

  .elevator-nav {
    right: 8px;
    gap: 2px;
  }

  .elevator-item {
    padding: 4px 8px;
    font-size: 11px;
  }

  .movie-grid {
    grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
    gap: 12px;
  }

  .category-section {
    padding: 32px 12px;
  }
}
</style>
