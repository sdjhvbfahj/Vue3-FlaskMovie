<template>
  <div class="admin-form-page container">
    <header class="form-header">
      <div>
        <h1>新增电影</h1>
        <p>完善影片信息后即可加入片库，并可设置为首页 Banner。</p>
      </div>
      <router-link to="/admin" class="btn btn-outline">返回后台</router-link>
    </header>

    <div class="card form-card">
      <form @submit.prevent="handleSubmit">
        <!-- 标题 -->
        <div class="form-group">
          <label class="form-label">电影标题 <span class="required">*</span></label>
          <input v-model="form.title" type="text" class="form-control" placeholder="请输入电影标题" required />
        </div>

        <!-- 简介 -->
        <div class="form-group">
          <label class="form-label">电影简介 <span class="required">*</span></label>
          <textarea v-model="form.info" class="form-control" rows="4" placeholder="请输入电影简介" required></textarea>
        </div>

        <!-- 分类和海报 -->
        <div class="form-row">
          <div class="form-group">
            <label class="form-label">类型 <span class="required">*</span></label>
            <input v-model="form.category" type="text" class="form-control" placeholder="例如：动作、喜剧、科幻" required />
          </div>
          <div class="form-group">
            <label class="form-label">电影海报 <span class="required">*</span></label>
            <input
              ref="posterInput"
              type="file"
              class="form-control"
              accept="image/*"
              required
              @change="handlePosterChange"
            />
          </div>
        </div>

        <!-- 视频和展示类型 -->
        <div class="form-row">
          <div class="form-group">
            <label class="form-label">视频文件</label>
            <input
              ref="videoInput"
              type="file"
              class="form-control"
              accept="video/mp4,video/webm,video/ogg"
              @change="handleVideoChange"
            />
          </div>
          <div class="form-group">
            <label class="form-label">展示类型</label>
            <select v-model.number="form.is_banner" class="form-control">
              <option :value="0">普通</option>
              <option :value="1">Banner</option>
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
            placeholder="数字越小越靠前"
            min="0"
          />
        </div>

        <!-- 海报预览 -->
        <div v-if="posterPreview" class="preview-card">
          <p class="preview-title">海报预览</p>
          <img :src="posterPreview" alt="预览" class="preview-img" />
        </div>

        <!-- 操作按钮 -->
        <div class="form-actions">
          <button type="submit" class="btn btn-primary btn-lg" :disabled="submitting">
            {{ submitting ? '添加中...' : '✓ 添加电影' }}
          </button>
          <router-link to="/admin" class="btn btn-outline btn-lg">✕ 取消</router-link>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
/**
 * 新增电影页面（管理员）
 * 支持海报和视频上传，可设置 Banner
 */
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { createMovie } from '@/api/admin'

const router = useRouter()

const form = reactive({
  title: '',
  info: '',
  category: '',
  is_banner: 0,
  banner_order: 0,
})

const posterPreview = ref('')
const posterFile = ref<File | null>(null)
const videoFile = ref<File | null>(null)
const submitting = ref(false)

function handlePosterChange(e: Event) {
  const file = (e.target as HTMLInputElement).files?.[0]
  if (file) {
    posterFile.value = file
    posterPreview.value = URL.createObjectURL(file)
  }
}

function handleVideoChange(e: Event) {
  const file = (e.target as HTMLInputElement).files?.[0]
  if (file) {
    videoFile.value = file
  }
}

async function handleSubmit() {
  if (!form.title.trim() || !form.category.trim()) {
    alert('请填写标题和分类')
    return
  }

  submitting.value = true
  try {
    const formData = new FormData()
    formData.append('title', form.title.trim())
    formData.append('info', form.info.trim())
    formData.append('category', form.category.trim())
    formData.append('is_banner', String(form.is_banner))
    formData.append('banner_order', String(form.banner_order))
    if (posterFile.value) {
      formData.append('poster', posterFile.value)
    }
    if (videoFile.value) {
      formData.append('video', videoFile.value)
    }

    const res = await createMovie(formData)
    if (res.code === 200) {
      router.push('/admin')
    }
  } catch (err: any) {
    alert(err?.response?.data?.message || '添加失败')
  } finally {
    submitting.value = false
  }
}
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

.required {
  color: var(--color-danger);
}

.preview-card {
  margin-top: 16px;
  padding: 16px;
  border: 1px solid #eee;
  border-radius: 8px;
  background: #fafafa;
}

.preview-title {
  font-size: 13px;
  color: var(--color-text-muted);
  margin-bottom: 8px;
}

.preview-img {
  max-width: 200px;
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
