<template>
  <div class="collects-page container">
    <!-- Hero -->
    <section class="collects-hero">
      <p class="collects-hero__tag">个人主页</p>
      <h1>{{ username }} 的收藏电影</h1>
      <p>支持分类筛选与分页浏览，方便快速找回看过的电影。</p>
      <router-link :to="`/profile/${username}`" class="btn btn-outline">
        返回个人主页
      </router-link>
    </section>

    <!-- 分类筛选 -->
    <section class="collects-filter">
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
    </section>

    <!-- 收藏网格 -->
    <section class="collects-grid-wrap">
      <div v-if="collects.length > 0" class="collects-grid">
        <router-link
          v-for="item in collects"
          :key="item.id"
          :to="`/movie/${item.id}`"
          class="collect-card"
        >
          <img
            v-if="item.poster"
            :src="`/static/${item.poster}`"
            :alt="item.title"
          />
          <span v-else class="collect-no-img">?</span>
          <div class="collect-card__body">
            <span class="collect-card__title">{{ item.title }}</span>
            <span class="collect-card__meta">{{ item.category || '电影' }}</span>
          </div>
        </router-link>
      </div>
      <div v-else-if="!loading" class="empty-state">
        <h3>暂无收藏电影</h3>
        <p>先去首页挑几部喜欢的电影收藏起来吧。</p>
        <router-link to="/" class="btn btn-primary">去首页看看</router-link>
      </div>
      <div v-if="loading" class="loading-center">
        <span class="spinner"></span> 加载中...
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
 * 用户收藏列表页面
 * 支持分类筛选和分页浏览
 */
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { getCollects } from '@/api/collect'
import type { CollectItem, Pagination } from '@/types'

const route = useRoute()
const username = computed(() => route.params.username as string)

const loading = ref(true)
const collects = ref<CollectItem[]>([])
const categories = ref<string[]>([])
const currentCategory = ref('')
const pagination = ref<Pagination>({
  page: 1, per_page: 24, total: 0, pages: 0,
  has_prev: false, has_next: false,
})
const currentPage = ref(1)

const pageNumbers = computed(() => {
  const p = pagination.value.page
  const pages = pagination.value.pages
  const nums: number[] = []
  for (let i = p - 2; i <= p + 2; i++) {
    if (i > 0 && i <= pages) nums.push(i)
  }
  return nums
})

function selectCategory(cat: string) {
  currentCategory.value = cat
  currentPage.value = 1
  fetchCollects()
}

function goToPage(page: number) {
  currentPage.value = page
  fetchCollects()
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

async function fetchCollects() {
  loading.value = true
  try {
    const res = await getCollects({
      page: currentPage.value,
      per_page: 24,
      category: currentCategory.value || undefined,
    })
    if (res.code === 200) {
      collects.value = res.data.collects
      categories.value = res.data.categories
      pagination.value = res.data.pagination
    }
  } catch (err) {
    console.error('加载收藏列表失败:', err)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchCollects()
})
</script>

<style scoped>
.collects-page {
  padding-bottom: 40px;
}

.collects-hero {
  padding: 32px 0 20px;
}

.collects-hero__tag {
  display: inline-block;
  padding: 2px 10px;
  border-radius: 4px;
  background: var(--color-primary);
  color: #fff;
  font-size: 12px;
  margin-bottom: 8px;
}

.collects-hero h1 {
  font-size: 28px;
  margin-bottom: 6px;
}

.collects-hero p {
  font-size: 14px;
  color: var(--color-text-muted);
  margin-bottom: 14px;
}

.collects-filter {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 24px;
}

.chip {
  padding: 6px 16px;
  border-radius: 20px;
  background: #fff;
  border: 1px solid #ddd;
  font-size: 13px;
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

.collects-grid-wrap {
  min-height: 200px;
}

.collects-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(170px, 1fr));
  gap: 20px;
}

.collect-card {
  text-decoration: none;
  color: var(--color-text);
  border-radius: 10px;
  overflow: hidden;
  background: #fff;
  box-shadow: var(--shadow-sm);
  transition: transform 0.2s, box-shadow 0.2s;
}

.collect-card:hover {
  transform: translateY(-3px);
  box-shadow: var(--shadow-md);
}

.collect-card img {
  width: 100%;
  aspect-ratio: 2/3;
  object-fit: cover;
}

.collect-no-img {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  aspect-ratio: 2/3;
  background: #e9ecef;
  font-size: 28px;
  color: #aaa;
}

.collect-card__body {
  padding: 10px 12px;
}

.collect-card__title {
  display: block;
  font-size: 14px;
  font-weight: 500;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.collect-card__meta {
  font-size: 12px;
  color: var(--color-text-muted);
}
</style>
