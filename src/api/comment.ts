/**
 * 评论相关 API 接口
 */

import apiClient from './client'
import type { ApiResponse, CommentsResponse, Comment } from '@/types'

/**
 * 获取电影评论列表
 */
export function getComments(
  movieId: number,
  params?: { page?: number; per_page?: number }
): Promise<ApiResponse<CommentsResponse>> {
  return apiClient
    .get(`/movies/${movieId}/comments`, { params })
    .then((res) => res.data)
}

/**
 * 创建评论
 */
export function createComment(
  movieId: number,
  content: string
): Promise<ApiResponse<Comment>> {
  return apiClient
    .post(`/movies/${movieId}/comments`, { content })
    .then((res) => res.data)
}

/**
 * 删除评论（作者或管理员）
 */
export function deleteComment(
  commentId: number
): Promise<ApiResponse<null>> {
  return apiClient
    .delete(`/comments/${commentId}`)
    .then((res) => res.data)
}
