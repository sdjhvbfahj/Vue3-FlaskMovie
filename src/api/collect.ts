/**
 * 收藏相关 API 接口
 */

import apiClient from './client'
import type { ApiResponse, CollectsResponse } from '@/types'

/**
 * 切换收藏状态
 */
export function toggleCollect(movieId: number): Promise<
  ApiResponse<{ is_collected: boolean; likes: number }>
> {
  return apiClient
    .post(`/collects/toggle/${movieId}`)
    .then((res) => res.data)
}

/**
 * 获取收藏列表
 */
export function getCollects(params?: {
  page?: number
  per_page?: number
  category?: string
}): Promise<ApiResponse<CollectsResponse>> {
  return apiClient.get('/collects', { params }).then((res) => res.data)
}

/**
 * 取消收藏（通过收藏 ID）
 */
export function deleteCollect(collectId: number): Promise<ApiResponse<null>> {
  return apiClient.delete(`/collects/${collectId}`).then((res) => res.data)
}
