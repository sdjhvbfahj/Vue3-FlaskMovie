/**
 * 管理后台相关 API 接口
 * 仅管理员可访问
 */

import apiClient from './client'
import type {
  ApiResponse,
  AdminStats,
  User,
  Movie,
  Comment,
} from '@/types'

/**
 * 获取后台统计数据
 */
export function getAdminStats(): Promise<ApiResponse<AdminStats>> {
  return apiClient.get('/admin/stats').then((res) => res.data)
}

/**
 * 获取所有用户列表
 */
export function getAdminUsers(): Promise<ApiResponse<{ users: User[] }>> {
  return apiClient.get('/admin/users').then((res) => res.data)
}

/**
 * 封禁/解封用户
 */
export function toggleBanUser(
  userId: number
): Promise<ApiResponse<{ is_banned: number }>> {
  return apiClient
    .post(`/admin/users/${userId}/toggle_ban`)
    .then((res) => res.data)
}

/**
 * 获取所有电影（后台管理）
 */
export function getAdminMovies(params?: {
  keyword?: string
}): Promise<ApiResponse<{ movies: Movie[] }>> {
  return apiClient.get('/admin/movies', { params }).then((res) => res.data)
}

/**
 * 新增电影
 */
export function createMovie(formData: FormData): Promise<ApiResponse<Movie>> {
  return apiClient
    .post('/admin/movies', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
    .then((res) => res.data)
}

/**
 * 编辑电影
 */
export function updateMovie(
  movieId: number,
  formData: FormData
): Promise<ApiResponse<Movie>> {
  return apiClient
    .put(`/admin/movies/${movieId}`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
    .then((res) => res.data)
}

/**
 * 删除电影
 */
export function deleteMovie(movieId: number): Promise<ApiResponse<null>> {
  return apiClient
    .delete(`/admin/movies/${movieId}`)
    .then((res) => res.data)
}

/**
 * 获取所有评论（后台管理）
 */
export function getAdminComments(params?: {
  movie_id?: number
  keyword?: string
}): Promise<ApiResponse<{ comments: Comment[] }>> {
  return apiClient
    .get('/admin/comments', { params })
    .then((res) => res.data)
}

/**
 * 管理员删除评论
 */
export function adminDeleteComment(
  commentId: number
): Promise<ApiResponse<null>> {
  return apiClient
    .delete(`/admin/comments/${commentId}`)
    .then((res) => res.data)
}
