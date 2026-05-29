<template>
  <div class="movies-page container">
    <!-- 顶部 Hero -->
    <section class="movies-hero">
      <div class="movies-hero__content">
        <p class="movies-hero__tag">影片库</p>
        <h1>{{ currentCategory || '全部电影' }}</h1>
        <p class="movies-hero__meta">
          共 {{ pagination.total }} 部影片 ·
          第 {{ pagination.page }} / {{ Math.max(pagination.pages, 1) }} 页
        </p>
        <p v-if="keyword" class="movies-hero__meta">
          搜索关键词：{{ keyword }}
        </p>
      </div>
    </section>

    <!-- 搜索和筛选 -->
    <section class="movies-filter">
      <div class="movies-filter__head">
        <h2>分类选择</h2>
        <form class="search-form" @submit.prevent="doSearch">
          <input
            v-model.trim="searchKeyword"
            type="text"
            class="form-control search-input"
            placeholder="搜索电影名或简介"
          />
          <button type="submit" class="btn btn-primary btn-sm">搜索</button>
          <button
            v-if="keyword"
            type="button"
            class="btn btn-outline btn-sm"
            @click="clearSearch"
          >
            清空
          </button>
        </form>
      </div>

      <!-- 分类标签 -->
      <div class="chip-row">
        <button
          class="chip"
          :class="{ active: !currentCategory }"
          @click="selectCategory('')"
        >
          全部
        </button>
        <button
          v-for="cat in categories"
          :key="cat"
          class="chip"
          :class="{ active: cat === currentCategory }"
          @click="selectCategory(cat)"
        >
          {{ cat }}
        </button>
      </div>
    </section>

    <!-- 电影网格 -->
    <section class="movies-grid-wrap">
      <div v-if="movies.length > 0" class="movie-grid">
        <MovieCard
          v-for="movie in movies"
          :key="movie.id"
          :movie="movie"
        >
          <template #extra>
            <p class="movie-heat">热度 {{ movie.likes }}</p>
          </template>
        </MovieCard>
      </div>

      <!-- 空状态 -->
      <div v-else-if="!loading" class="empty-state">
        <h3>暂无影片数据</h3>
        <p>当前分类没有可展示内容，试试切换到全部电影。</p>
        <button class="btn btn-primary" @click="selectCategory('')">
          返回全部电影
        </button>
      </div>

      <!-- 加载中 -->
      <div v-if="loading" class="loading-center">
        <span class="spinner"></span>
        加载中...
      </div>
    </section>

    <!-- 分页 -->
    <div v-if="pagination.pages > 1" class="pagination">
      <button
        class="page-btn"
        :disabled="!pagination.has_prev"
        @click="goToPage(pagination.page - 1)"
      >
        上一页
      </button>

      <template v-for="p in pageNumbers" :key="p">
        <button
          v-if="p > 0 && p <= pagination.pages"
          class="page-btn"
          :class="{ active: p === pagination.page }"
          @click="goToPage(p)"
        >
          {{ p }}
        </button>
      </template>

      <button
        class="page-btn"
        :disabled="!pagination.has_next"
        @click="goToPage(pagination.page + 1)"
      >
        下一页
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
/**
 * 电影列表页面
 * 支持分类筛选、关键词搜索、分页浏览
 */
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getMovies } from '@/api/movie'
import type { Movie, Pagination } from '@/types'
import MovieCard from '@/components/MovieCard.vue'

const route = useRoute()
const router = useRouter()

/* ================== 状态 ================== */

const loading = ref(true)
const movies = ref<Movie[]>([])
const categories = ref<string[]>([])
const pagination = ref<Pagination>({
  page: 1, per_page: 28, total: 0, pages: 0,
  has_prev: false, has_next: false,
})

const currentCategory = ref('')
const keyword = ref('')
const searchKeyword = ref('')
const currentPage = ref(1)

/* ================== 计算属性 ================== */

/** 分页数字数组 */
const pageNumbers = computed(() => {
  const page = pagination.value.page
  const pages = pagination.value.pages
  const nums: number[] = []
  for (let p = page - 2; p <= page + 2; p++) {
    if (p > 0 && p <= pages) {
      nums.push(p)
    }
  }
  return nums
})

/* ================== 方法 ================== */

/** 加载电影数据 */
async function fetchMovies() {
  loading.value = true
  try {
    const res = await getMovies({
      page: currentPage.value,
      per_page: 28,
      category: currentCategory.value || undefined,
      keyword: keyword.value || undefined,
    })

    if (res.code === 200) {
      movies.value = res.data.movies
      pagination.value = res.data.pagination
      categories.value = res.data.categories
    }
  } catch (err) {
    console.error('加载电影列表失败:', err)
  } finally {
    loading.value = false
  }
}

/** 选择分类 */
function selectCategory(cat: string) {
  currentCategory.value = cat
  currentPage.value = 1
  updateURL()
  fetchMovies()
}

/** 执行搜索 */
function doSearch() {
  keyword.value = searchKeyword.value.trim()
  currentPage.value = 1
  updateURL()
  fetchMovies()
}

/** 清空搜索 */
function clearSearch() {
  searchKeyword.value = ''
  keyword.value = ''
  currentPage.value = 1
  updateURL()
  fetchMovies()
}

/** 跳转页面 */
function goToPage(page: number) {
  currentPage.value = page
  updateURL()
  fetchMovies()
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

/** 更新 URL 参数 */
function updateURL() {
  const query: Record<string, string> = {}
  if (currentCategory.value) query.category = currentCategory.value
  if (keyword.value) query.keyword = keyword.value
  if (currentPage.value > 1) query.page = String(currentPage.value)
  router.replace({ query })
}

/* ================== 生命周期 ================== */

onMounted(() => {
  // 从 URL 获取初始参数
  currentCategory.value = (route.query.category as string) || ''
  keyword.value = (route.query.keyword as string) || ''
  searchKeyword.value = keyword.value
  currentPage.value = parseInt(route.query.page as string) || 1

  fetchMovies()
})
</script>

<style scoped>
.movies-page {
  padding-bottom: 40px;
}

/* Hero */
.movies-hero {
  padding: 32px 0 20px;
}

.movies-hero__tag {
  display: inline-block;
  padding: 2px 10px;
  border-radius: 4px;
  background: var(--color-primary);
  color: #fff;
  font-size: 12px;
  margin-bottom: 8px;
}

.movies-hero h1 {
  font-size: 28px;
  margin-bottom: 4px;
}

.movies-hero__meta {
  font-size: 14px;
  color: var(--color-text-muted);
}

/* 筛选区 */
.movies-filter {
  margin-bottom: 24px;
}

.movies-filter__head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 14px;
  flex-wrap: wrap;
  gap: 12px;
}

.movies-filter__head h2 {
  font-size: 18px;
}

.search-form {
  display: flex;
  gap: 8px;
  align-items: center;
}

.search-input {
  width: 240px !important;
}

/* 分类标签 */
.chip-row {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.chip {
  padding: 6px 16px;
  border-radius: 20px;
  background: #fff;
  border: 1px solid #ddd;
  font-size: 13px;
  color: var(--color-text);
  cursor: pointer;
  transition: var(--transition);
}

.chip:hover {
  border-color: var(--color-primary);
  color: var(--color-primary);
}

.chip.active {
  background: var(--color-primary);
  border-color: var(--color-primary);
  color: #fff;
}

/* 电影网格 */
.movies-grid-wrap {
  min-height: 300px;
}

.movie-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 20px;
}

.movie-heat {
  font-size: 12px;
  color: var(--color-danger);
  margin-top: 2px;
}

@media (max-width: 768px) {
  .search-input {
    width: 160px !important;
  }

  .movie-grid {
    grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
    gap: 12px;
  }
}
</style>
