<template>
  <div class="profile-page container">
    <!-- 加载中 -->
    <div v-if="loading" class="loading-center">
      <span class="spinner"></span> 加载中...
    </div>

    <template v-else-if="profileUser">
      <div class="profile-layout">
        <!-- 左侧：个人信息 -->
        <aside class="profile-sidebar">
          <!-- 头像 -->
          <div class="card profile-card">
            <div class="avatar-section">
              <div
                class="avatar-wrapper"
                :class="{ 'is-current': isCurrentUser }"
              >
                <img
                  v-if="profileUser.avatar"
                  :src="`/static/avatars/${profileUser.avatar}`"
                  :alt="profileUser.username"
                  class="avatar-img"
                />
                <span v-else class="avatar-fallback">
                  {{ profileUser.username.charAt(0).toUpperCase() }}
                </span>

                <!-- 换头像遮罩（仅自己可见） -->
                <div
                  v-if="isCurrentUser"
                  class="avatar-mask"
                  @click="triggerAvatarUpload"
                >
                  更换头像
                </div>
              </div>

              <!-- 隐藏的上传 input -->
              <input
                v-if="isCurrentUser"
                ref="avatarInput"
                type="file"
                accept="image/*"
                class="hidden-input"
                @change="handleAvatarUpload"
              />

              <h3>{{ profileUser.username }}</h3>
              <p class="bio-text">{{ profileUser.bio || '暂无个人简介，快来添加吧～' }}</p>
            </div>

            <!-- 编辑简介（仅自己可见） -->
            <form
              v-if="isCurrentUser"
              class="bio-form"
              @submit.prevent="handleSaveBio"
            >
              <textarea
                v-model="bioText"
                class="form-control"
                placeholder="写点个人简介..."
                rows="3"
              ></textarea>
              <button type="submit" class="btn btn-primary btn-block btn-sm">
                保存简介
              </button>
            </form>
          </div>

          <!-- 账户安全（仅自己可见） -->
          <div v-if="isCurrentUser" class="card profile-card password-card">
            <h4>🔒 账户安全</h4>

            <!-- 成功提示 -->
            <div v-if="pwdSuccess" class="alert alert-success">
              ✅ 密码修改成功
            </div>

            <form @submit.prevent="handleChangePassword">
              <div class="form-group">
                <label class="form-label">原密码</label>
                <input
                  v-model="pwdForm.old_password"
                  type="password"
                  class="form-control"
                  placeholder="请输入原密码"
                />
              </div>
              <div class="form-group">
                <label class="form-label">新密码</label>
                <input
                  v-model="pwdForm.new_password"
                  type="password"
                  class="form-control"
                  placeholder="请输入新密码"
                />
              </div>
              <div class="form-group">
                <label class="form-label">确认新密码</label>
                <input
                  v-model="pwdForm.confirm_password"
                  type="password"
                  class="form-control"
                  placeholder="请再次输入新密码"
                />
              </div>

              <div v-if="pwdError" class="alert alert-error">{{ pwdError }}</div>

              <button
                type="submit"
                class="btn btn-danger btn-block btn-sm"
                :disabled="pwdSubmitting"
              >
                {{ pwdSubmitting ? '提交中...' : '修改密码' }}
              </button>
            </form>
          </div>
        </aside>

        <!-- 右侧：收藏和评论 -->
        <div class="profile-main">
          <!-- 收藏预览 -->
          <div class="card">
            <div class="section-head">
              <h4>⭐ 我的收藏</h4>
              <div class="section-head-right">
                <span class="count-text">共 {{ collectTotal }} 部</span>
                <router-link
                  :to="`/profile/${profileUser.username}/collects`"
                  class="btn btn-outline btn-sm"
                >
                  查看全部收藏
                </router-link>
              </div>
            </div>

            <!-- 收藏 Tab -->
            <div class="tab-row">
              <button
                v-for="tab in collectTabs"
                :key="tab.key"
                class="tab-btn"
                :class="{ active: activeCollectTab === tab.key }"
                @click="activeCollectTab = tab.key"
              >
                {{ tab.label }}
              </button>
            </div>

            <!-- 收藏内容 -->
            <div class="collect-grid">
              <template v-for="m in collectPreview[activeCollectTab]" :key="m.id">
                <router-link :to="`/movie/${m.id}`" class="collect-item">
                  <img
                    v-if="m.poster"
                    :src="`/static/${m.poster}`"
                    :alt="m.title"
                  />
                  <span v-else class="collect-no-img">?</span>
                  <span class="collect-item-title">{{ m.title }}</span>
                </router-link>
              </template>
              <div v-if="!collectPreview[activeCollectTab]?.length" class="empty-state">
                <p>该分类下暂无收藏电影</p>
              </div>
            </div>
          </div>

          <!-- 评论列表 -->
          <div class="card">
            <h4>💬 我的评论</h4>
            <div v-if="userComments.length > 0" class="comment-list">
              <div v-for="c in userComments" :key="c.id" class="comment-item">
                <router-link :to="`/movie/${c.movie_id}`" class="comment-movie-link">
                  🎬 {{ c.movie_title }}
                </router-link>
                <p class="comment-text" :title="c.content">{{ c.content }}</p>
              </div>
            </div>
            <div v-else class="empty-state">
              <p>暂无评论，快去给喜欢的电影留下你的看法吧～</p>
            </div>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup lang="ts">
/**
 * 个人主页
 * 展示用户信息、收藏预览、评论列表
 * 支持编辑简介、修改密码、上传头像（仅本人可见）
 */
import { ref, reactive, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { getUserProfile, getUserComments, updateProfile, changePassword, uploadAvatar } from '@/api/user'
import { getCollects } from '@/api/collect'
import type { User, Comment, CollectItem } from '@/types'

const route = useRoute()
const userStore = useUserStore()

/* ================== 状态 ================== */

const loading = ref(true)
const profileUser = ref<User | null>(null)
const commentCount = ref(0)
const collectTotal = ref(0)

const bioText = ref('')
const userComments = ref<Comment[]>([])
const collectPreview = ref<Record<string, CollectItem[]>>({})
const activeCollectTab = ref('全部')
const collectTabs = [
  { key: '全部', label: '全部' },
  { key: '动作', label: '动作' },
  { key: '科幻', label: '科幻' },
  { key: '动画', label: '动画' },
  { key: '战争', label: '战争' },
]

// 头像上传
const avatarInput = ref<HTMLInputElement | null>(null)

// 密码修改
const pwdForm = reactive({ old_password: '', new_password: '', confirm_password: '' })
const pwdError = ref('')
const pwdSuccess = ref(false)
const pwdSubmitting = ref(false)

/* ================== 计算属性 ================== */

const username = computed(() => route.params.username as string)
const isCurrentUser = computed(() => username.value === userStore.username)

/* ================== 方法 ================== */

async function loadData() {
  loading.value = true
  try {
    const [profileRes, commentsRes, collectsRes] = await Promise.all([
      getUserProfile(username.value),
      getUserComments(username.value),
      getCollects({ per_page: 8 }),
    ])

    if (profileRes.code === 200) {
      profileUser.value = profileRes.data.user
      commentCount.value = profileRes.data.comment_count
      collectTotal.value = profileRes.data.collect_count
      bioText.value = profileRes.data.user.bio || ''
    }

    if (commentsRes.code === 200) {
      userComments.value = commentsRes.data.comments
    }

    if (collectsRes.code === 200) {
      // 构建分类分组预览
      const all = collectsRes.data.collects
      const groups: Record<string, CollectItem[]> = { 全部: all.slice(0, 8) }
      for (const tab of collectTabs) {
        if (tab.key === '全部') continue
        groups[tab.key] = all.filter((c) => c.category === tab.key).slice(0, 8)
      }
      collectPreview.value = groups
    }
  } catch (err) {
    console.error('加载个人主页失败:', err)
  } finally {
    loading.value = false
  }
}

function triggerAvatarUpload() {
  avatarInput.value?.click()
}

async function handleAvatarUpload(event: Event) {
  const file = (event.target as HTMLInputElement).files?.[0]
  if (!file) return

  const formData = new FormData()
  formData.append('avatar', file)

  try {
    const res = await uploadAvatar(formData)
    if (res.code === 200) {
      // 刷新页面显示新头像
      window.location.reload()
    }
  } catch (err) {
    console.error('头像上传失败:', err)
  }
}

async function handleSaveBio() {
  try {
    const res = await updateProfile(bioText.value)
    if (res.code === 200 && profileUser.value) {
      profileUser.value.bio = bioText.value
    }
  } catch (err) {
    console.error('保存简介失败:', err)
  }
}

async function handleChangePassword() {
  pwdError.value = ''
  pwdSuccess.value = false

  if (!pwdForm.old_password) {
    pwdError.value = '原密码不能为空'
    return
  }
  if (!pwdForm.new_password) {
    pwdError.value = '新密码不能为空'
    return
  }
  if (!pwdForm.confirm_password) {
    pwdError.value = '确认密码不能为空'
    return
  }

  pwdSubmitting.value = true
  try {
    const res = await changePassword({
      old_password: pwdForm.old_password,
      new_password: pwdForm.new_password,
      confirm_password: pwdForm.confirm_password,
    })
    if (res.code === 200) {
      pwdSuccess.value = true
      pwdForm.old_password = ''
      pwdForm.new_password = ''
      pwdForm.confirm_password = ''
    }
  } catch (err: any) {
    pwdError.value = err?.response?.data?.message || '密码修改失败'
  } finally {
    pwdSubmitting.value = false
  }
}

onMounted(() => {
  loadData()
})
</script>

<style scoped>
.profile-page {
  padding: 32px 0;
}

.profile-layout {
  display: grid;
  grid-template-columns: 320px 1fr;
  gap: 24px;
}

/* 侧边栏 */
.profile-sidebar {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.profile-card {
  padding: 24px;
}

.avatar-section {
  text-align: center;
  margin-bottom: 16px;
}

.avatar-wrapper {
  position: relative;
  display: inline-block;
  width: 100px;
  height: 100px;
  border-radius: 50%;
  overflow: hidden;
  margin-bottom: 12px;
}

.avatar-wrapper.is-current {
  cursor: pointer;
}

.avatar-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.avatar-fallback {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
  background: var(--color-primary);
  color: #fff;
  font-size: 36px;
  font-weight: 700;
}

.avatar-mask {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(0, 0, 0, 0.5);
  color: #fff;
  font-size: 13px;
  opacity: 0;
  transition: opacity 0.2s;
}

.avatar-wrapper:hover .avatar-mask {
  opacity: 1;
}

.bio-text {
  font-size: 14px;
  color: var(--color-text-muted);
  margin-top: 8px;
}

.hidden-input {
  display: none;
}

.bio-form {
  margin-top: 16px;
}

.bio-form textarea {
  margin-bottom: 8px;
}

.password-card h4 {
  margin-bottom: 16px;
  font-size: 16px;
}

/* 主区域 */
.profile-main {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.section-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
  flex-wrap: wrap;
  gap: 8px;
}

.section-head h4 {
  font-size: 18px;
}

.section-head-right {
  display: flex;
  align-items: center;
  gap: 10px;
}

.count-text {
  font-size: 14px;
  color: var(--color-text-muted);
}

.tab-row {
  display: flex;
  gap: 6px;
  margin-bottom: 18px;
  flex-wrap: wrap;
}

.tab-btn {
  padding: 6px 14px;
  border-radius: 6px;
  background: #f0f0f0;
  font-size: 13px;
  color: var(--color-text);
  transition: var(--transition);
}

.tab-btn:hover {
  background: #e0e0e0;
}

.tab-btn.active {
  background: var(--color-primary);
  color: #fff;
}

.collect-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(110px, 1fr));
  gap: 12px;
}

.collect-item {
  text-decoration: none;
  color: var(--color-text);
}

.collect-item img {
  width: 100%;
  aspect-ratio: 2/3;
  object-fit: cover;
  border-radius: 8px;
  box-shadow: var(--shadow-sm);
  transition: transform 0.2s;
}

.collect-item:hover img {
  transform: scale(1.04);
}

.collect-no-img {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  aspect-ratio: 2/3;
  background: #e9ecef;
  border-radius: 8px;
  font-size: 24px;
  color: #aaa;
}

.collect-item-title {
  display: block;
  font-size: 13px;
  margin-top: 4px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.comment-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.comment-item {
  padding: 12px;
  border-radius: 8px;
  background: #f8f9fa;
}

.comment-movie-link {
  font-size: 14px;
  font-weight: 500;
  display: block;
  margin-bottom: 6px;
}

.comment-text {
  font-size: 14px;
  color: var(--color-text);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.alert {
  padding: 8px 12px;
  border-radius: 6px;
  font-size: 13px;
  margin-bottom: 12px;
}

.alert-error {
  background: #ffe0e0;
  color: #c0392b;
}

.alert-success {
  background: #d4edda;
  color: #155724;
}

.profile-main .card {
  padding: 24px;
}

@media (max-width: 768px) {
  .profile-layout {
    grid-template-columns: 1fr;
  }

  .collect-grid {
    grid-template-columns: repeat(auto-fill, minmax(90px, 1fr));
  }
}
</style>
