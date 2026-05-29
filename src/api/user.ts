/**
 * 用户相关 API 接口
 */

import apiClient from './client'
import type {
  ApiResponse,
  User,
  UserProfileResponse,
  CommentsResponse,
} from '@/types'

/**
 * 获取用户主页信息
 */
export function getUserProfile(
  username: string
): Promise<ApiResponse<UserProfileResponse>> {
  return apiClient.get(`/users/${username}`).then((res) => res.data)
}

/**
 * 获取用户评论列表
 */
export function getUserComments(
  username: string,
  params?: { page?: number; per_page?: number }
): Promise<ApiResponse<CommentsResponse>> {
  return apiClient
    .get(`/users/${username}/comments`, { params })
    .then((res) => res.data)
}

/**
 * 更新个人简介
 */
export function updateProfile(bio: string): Promise<ApiResponse<User>> {
  return apiClient
    .put('/users/profile', { bio })
    .then((res) => res.data)
}

/**
 * 修改密码
 */
export function changePassword(data: {
  old_password: string
  new_password: string
  confirm_password: string
}): Promise<ApiResponse<null>> {
  return apiClient
    .put('/users/password', data)
    .then((res) => res.data)
}

/**
 * 上传头像
 */
export function uploadAvatar(
  formData: FormData
): Promise<ApiResponse<{ avatar: string }>> {
  return apiClient
    .post('/upload/avatar', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
    .then((res) => res.data)
}
