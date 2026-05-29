<template>
  <div class="admin-form-page container">
    <header class="form-header">
      <div>
        <h1>编辑电影</h1>
        <p>更新影片信息、海报与 Banner 配置。</p>
      </div>
      <router-link to="/admin" class="btn btn-outline">返回后台</router-link>
    </header>

    <!-- 加载中 -->
    <div v-if="loading" class="loading-center">
      <span class="spinner"></span> 加载中...
    </div>

    <div v-else class="card form-card">
      <form @submit.prevent="handleSubmit">
        <!-- 标题 -->
        <div class="form-group">
          <label class="form-label">电影标题</label>
          <input v-model="form.title" type="text" class="form-control" required />
        </div>

        <!-- 简介 -->
        <div class="form-group">
          <label class="form-label">电影简介</label>
          <textarea v-model="form.info" class="form-control" rows="4" required></textarea>
        </div>

        <!-- 分类和海报 -->
        <div class="form-row">
          <div class="form-group">
            <label class="form-label">电影类型</label>
            <input v-model="form.category" type="text" class="form-control" required />
          </div>
          <div class="form-group">
            <label class="form-label">更换海报（可选）</label>
            <input
              type="file"
              class="form-control"
              accept="image/*"
              @change="handlePosterChange"
            />
          </div>
        </div>

        <!-- 视频和展示类型 -->
        <div class="form-row">
          <div class="form-group">
            <label class="form-label">更换视频（可选）</label>
            <input
              type="file"
              class="form-control"
              accept="video/mp4,video/webm,video/ogg"
              @change="handleVideoChange"
            />
          </div>
          <div class="form-group">
            <label class="form-label">是否设为 Banner</label>
            <select v-model.number="form.is_banner" class="form-control">
              <option :value="0">否</option>
              <option :value="1">是</option>
            </select>
          </div>
        </div>

        <!-- Banner 排序 -->
        <div class="form-group" v-if="form.is_banner === 1">
          <label class="form-label">Banner 排序</label>
          <input
            v-model.number="form.banner_order"
            type="number"
            class="form-control"
            min="0"
          />
        </div>

        <!-- 海报对比 -->
        <div class="poster-compare">
          <div class="poster-block">
            <p class="poster-block-title">当前海报</p>
            <img
              v-if="movie?.poster"
              :src="`/static/${movie.poster}`"
              :alt="movie.title"
              class="poster-img"
            />
            <span v-else>无海报</span>
          </div>
          <div class="poster-block" v-if="newPosterPreview">
            <p class="poster-block-title">新海报预览</p>
            <img :src="newPosterPreview" alt="预览" class="poster-img" />
          </div>
        </div>

        <!-- 操作按钮 -->
        <div class="form-actions">
          <button type="submit" class="btn btn-primary btn-lg" :disabled="submitting">
            {{ submitting ? '保存中...' : '✓ 保存修改' }}
          </button>
          <router-link to="/admin" class="btn btn-outline btn-lg">✕ 取消</router-link>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
/**
 * 编辑电影页面（管理员）
 */
import { ref, reactive, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getMovieDetail } from '@/api/movie'
import { updateMovie } from '@/api/admin'
import type { Movie } from '@/types'

const route = useRoute()
const router = useRouter()
const movieId = Number(route.params.id)

const loading = ref(true)
const submitting = ref(false)
const movie = ref<Movie | null>(null)

const form = reactive({
  title: '',
  info: '',
  category: '',
  is_banner: 0,
  banner_order: 0,
})

const newPosterPreview = ref('')
const newPosterFile = ref<File | null>(null)
const newVideoFile = ref<File | null>(null)

function handlePosterChange(e: Event) {
  const file = (e.target as HTMLInputElement).files?.[0]
  if (file) {
    newPosterFile.value = file
    newPosterPreview.value = URL.createObjectURL(file)
  }
}

function handleVideoChange(e: Event) {
  const file = (e.target as HTMLInputElement).files?.[0]
  if (file) {
    newVideoFile.value = file
  }
}

async function handleSubmit() {
  submitting.value = true
  try {
    const formData = new FormData()
    formData.append('title', form.title.trim())
    formData.append('info', form.info.trim())
    formData.append('category', form.category.trim())
    formData.append('is_banner', String(form.is_banner))
    formData.append('banner_order', String(form.banner_order))
    if (newPosterFile.value) {
      formData.append('poster', newPosterFile.value)
    }
    if (newVideoFile.value) {
      formData.append('video', newVideoFile.value)
    }

    const res = await updateMovie(movieId, formData)
    if (res.code === 200) {
      router.push('/admin')
    }
  } catch (err: any) {
    alert(err?.response?.data?.message || '修改失败')
  } finally {
    submitting.value = false
  }
}

onMounted(async () => {
  try {
    const res = await getMovieDetail(movieId)
    if (res.code === 200) {
      movie.value = res.data.movie
      form.title = res.data.movie.title
      form.info = res.data.movie.info
      form.category = res.data.movie.category
      form.is_banner = res.data.movie.is_banner
      form.banner_order = res.data.movie.banner_order
    }
  } catch (err) {
    console.error('加载电影数据失败:', err)
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.admin-form-page {
  max-width: 800px;
  padding: 32px 0;
}

.form-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 24px;
  flex-wrap: wrap;
  gap: 12px;
}

.form-header h1 {
  font-size: 24px;
}

.form-header p {
  font-size: 14px;
  color: var(--color-text-muted);
}

.form-card {
  padding: 32px;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.poster-compare {
  display: flex;
  gap: 24px;
  margin-top: 16px;
  padding: 16px;
  border: 1px solid #eee;
  border-radius: 8px;
  background: #fafafa;
}

.poster-block-title {
  font-size: 13px;
  color: var(--color-text-muted);
  margin-bottom: 8px;
}

.poster-img {
  max-width: 160px;
  border-radius: 8px;
}

.form-actions {
  display: flex;
  gap: 12px;
  margin-top: 28px;
  padding-top: 20px;
  border-top: 1px solid #eee;
}

@media (max-width: 768px) {
  .form-row {
    grid-template-columns: 1fr;
  }
}
</style>
