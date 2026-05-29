/**
 * 电影相关 API 接口
 * 包含电影列表、Banner、详情、首页分类数据等
 */

import apiClient from './client'
import type {
  ApiResponse,
  MoviesResponse,
  BannersResponse,
  HomeMoviesResponse,
  MovieDetailResponse,
  Movie,
} from '@/types'

/**
 * 获取电影列表（分页 + 分类筛选 + 搜索）
 */
export function getMovies(params: {
  page?: number
  per_page?: number
  category?: string
  keyword?: string
}): Promise<ApiResponse<MoviesResponse>> {
  return apiClient.get('/movies', { params }).then((res) => res.data)
}

/**
 * 获取 Banner 列表
 */
export function getBanners(): Promise<ApiResponse<BannersResponse>> {
  return apiClient.get('/movies/banners').then((res) => res.data)
}

/**
 * 获取首页分类电影数据
 */
export function getHomeMovies(): Promise<ApiResponse<HomeMoviesResponse>> {
  return apiClient.get('/movies/home').then((res) => res.data)
}

/**
 * 获取电影详情
 */
export function getMovieDetail(
  movieId: number
): Promise<ApiResponse<MovieDetailResponse>> {
  return apiClient.get(`/movies/${movieId}`).then((res) => res.data)
}
