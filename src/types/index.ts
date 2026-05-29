/**
 * 项目全局 TypeScript 类型定义
 * 定义前后端交互中的核心数据结构
 */

/* ================== 用户相关 ================== */

/** 用户信息 */
export interface User {
  id: number
  username: string
  bio: string
  avatar: string
  is_banned: number
  created_at: string
}

/** 登录请求 */
export interface LoginRequest {
  username: string
  password: string
}

/** 注册请求 */
export interface RegisterRequest {
  username: string
  password: string
}

/** 登录响应 */
export interface LoginResponse {
  code: number
  message: string
  data: {
    user: User
    token: string
  }
}

/* ================== 电影相关 ================== */

/** 电影信息 */
export interface Movie {
  id: number
  title: string
  info: string
  poster: string
  category: string
  filename: string
  is_banner: number
  banner_order: number
  likes: number
  created_at: string
}

/* ================== 评论相关 ================== */

/** 评论信息 */
export interface Comment {
  id: number
  content: string
  user: string
  movie_id: number
  movie_title: string
  created_at: string
}

/* ================== 收藏相关 ================== */

/** 收藏信息（简化的电影信息） */
export interface CollectItem {
  id: number
  title: string
  poster: string
  category: string
  likes: number
}

/* ================== 分页相关 ================== */

/** 分页信息 */
export interface Pagination {
  page: number
  per_page: number
  total: number
  pages: number
  has_prev: boolean
  has_next: boolean
  prev_num?: number
  next_num?: number
}

/* ================== 通用 API 响应 ================== */

/** API 统一响应格式 */
export interface ApiResponse<T = unknown> {
  code: number
  message?: string
  data: T
}

/** 电影列表响应 */
export interface MoviesResponse {
  movies: Movie[]
  pagination: Pagination
  categories: string[]
}

/** 首页电影数据 */
export interface HomeMoviesResponse {
  categories: string[]
  movies_by_category: Record<string, Movie[]>
}

/** 电影详情响应 */
export interface MovieDetailResponse {
  movie: Movie
  is_collected: boolean
  recommends: Movie[]
}

/** 评论列表响应 */
export interface CommentsResponse {
  comments: Comment[]
  pagination: Pagination
}

/** 收藏列表响应 */
export interface CollectsResponse {
  collects: CollectItem[]
  pagination: Pagination
  categories: string[]
}

/** 管理员统计 */
export interface AdminStats {
  user_count: number
  movie_count: number
  comment_count: number
}

/** Banner 响应 */
export interface BannersResponse {
  banners: Movie[]
}

/** 用户主页响应 */
export interface UserProfileResponse {
  user: User
  comment_count: number
  collect_count: number
}
