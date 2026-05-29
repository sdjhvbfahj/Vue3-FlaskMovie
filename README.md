# 🎬 CQUPT Movie - Vue3 + Flask 电影网站

基于 **Vue 3 + TypeScript + Python Flask + MySQL** 的全栈电影网站，支持用户注册登录、电影浏览搜索、分类筛选、视频播放、评论收藏、个人中心及后台管理等功能。

---

## 📂 项目结构

```
vue3-FlaskMovie/
├── backend/                    # Python Flask 后端
│   ├── app/                    # Flask 应用包
│   │   ├── api/                # API 蓝图路由
│   │   │   ├── __init__.py     # 蓝图注册
│   │   │   ├── auth_routes.py  # 认证相关接口（注册/登录/获取当前用户）
│   │   │   ├── movie_routes.py # 电影相关接口（列表/详情/Banner/首页分类）
│   │   │   ├── comment_routes.py # 评论相关接口
│   │   │   ├── collect_routes.py # 收藏相关接口
│   │   │   ├── user_routes.py  # 用户相关接口（个人主页/资料编辑/修改密码）
│   │   │   ├── upload_routes.py # 文件上传接口
│   │   │   └── admin_routes.py # 管理员接口（统计/用户管理/电影管理/评论管理）
│   │   ├── __init__.py         # Flask 应用工厂函数
│   │   ├── auth.py             # JWT 认证 + bcrypt 密码加密
│   │   ├── config.py           # 应用配置（数据库/密钥/上传目录）
│   │   ├── extensions.py       # SQLAlchemy + Flask-Migrate 扩展
│   │   └── models.py           # 数据模型（User/Movie/Comment/Collect）
│   ├── .env                    # 环境变量配置
│   ├── .gitignore              # Git 忽略文件
│   ├── init_db.py              # 数据库初始化脚本（创建表 + 默认管理员）
│   ├── requirements.txt        # Python 依赖清单
│   └── run.py                  # Flask 应用入口
│
├── public/                     # 前端静态资源
│   └── favicon.svg             # 网站图标
│
├── src/                        # Vue 3 前端源码
│   ├── api/                    # API 请求层（Axios）
│   │   ├── client.ts           # Axios 实例 + 拦截器
│   │   ├── auth.ts             # 认证 API
│   │   ├── movie.ts            # 电影 API
│   │   ├── comment.ts          # 评论 API
│   │   ├── collect.ts          # 收藏 API
│   │   ├── user.ts             # 用户 API
│   │   └── admin.ts            # 管理员 API
│   ├── components/             # 可复用组件
│   │   ├── NavBar.vue          # 顶部导航栏
│   │   └── MovieCard.vue       # 电影卡片组件
│   ├── router/
│   │   └── index.ts            # 路由配置 + 导航守卫
│   ├── stores/
│   │   └── user.ts             # 用户状态管理（Pinia）
│   ├── styles/
│   │   └── global.css          # 全局样式 + CSS 变量
│   ├── types/
│   │   └── index.ts            # TypeScript 类型定义
│   ├── views/                  # 页面视图
│   │   ├── HomeView.vue        # 首页（Banner轮播 + 分类电梯导航）
│   │   ├── MoviesView.vue      # 电影列表（搜索/分类筛选/分页）
│   │   ├── MovieDetailView.vue # 电影详情（评论/收藏/推荐）
│   │   ├── PlayView.vue        # 视频播放页
│   │   ├── LoginView.vue       # 登录页
│   │   ├── RegisterView.vue    # 注册页
│   │   ├── ProfileView.vue     # 个人主页（资料/密码/收藏/评论）
│   │   ├── ProfileCollectsView.vue # 我的收藏
│   │   ├── AdminView.vue       # 后台管理（统计/用户/电影/评论）
│   │   ├── AdminAddMovieView.vue  # 新增电影
│   │   ├── AdminEditMovieView.vue # 编辑电影
│   │   └── NotFoundView.vue    # 404 页面
│   ├── App.vue                 # 根组件
│   └── main.ts                 # 应用入口
│
├── index.html                  # HTML 入口
├── package.json                # Node 依赖 + 脚本
├── tsconfig.json               # TypeScript 配置入口
├── tsconfig.app.json           # TypeScript 应用配置（含路径别名）
├── vite.config.ts              # Vite 构建配置（含开发代理）
└── .gitignore                  # Git 忽略文件
```

---

## 🚀 快速开始

### 环境要求

| 工具 | 版本要求 |
|------|----------|
| Node.js | ≥ 18.x |
| Python | ≥ 3.10 |
| MySQL | ≥ 8.0 |

### 1. 克隆项目

```bash
git clone <repository-url>
cd vue3-FlaskMovie
```

### 2. 安装后端依赖

```bash
cd backend

# 创建虚拟环境（推荐）
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# macOS / Linux:
source venv/bin/activate

# 安装 Python 依赖
pip install -r requirements.txt
```

### 3. 配置数据库

编辑 [`backend/.env`](backend/.env) 文件，修改数据库连接信息：

```env
# MySQL 数据库连接
DATABASE_URL=mysql+pymysql://root:your_password@localhost:3306/cqupt_movie

# 密钥（请修改为随机字符串）
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here
```

> 确保 MySQL 服务已启动，并创建了 `cqupt_movie` 数据库：
>
> ```sql
> CREATE DATABASE cqupt_movie CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
> ```

### 4. 初始化数据库

```bash
# 在 backend 目录下执行
python init_db.py
```

该脚本将创建所有表并自动创建一个默认管理员账号：

| 字段 | 值 |
|------|-----|
| 用户名 | `admin` |
| 密码 | `admin123` |
| 昵称 | 管理员 |

> ⚠️ **安全提示**：部署到生产环境前，务必修改默认管理员密码。

### 5. 启动后端服务

```bash
# 开发环境（在 backend 目录下）
python run.py
```

Flask API 服务将运行在 `http://localhost:5000`。

### 6. 安装前端依赖并启动

```bash
# 回到项目根目录
cd ..

# 安装 Node.js 依赖
npm install

# 启动前端开发服务器
npm run dev
```

前端开发服务器将运行在 `http://localhost:3000`，并自动代理 API 请求到 Flask 后端。

---

## 🔧 技术栈

### 前端

| 技术 | 用途 |
|------|------|
| [Vue 3](https://vuejs.org/) | 渐进式 JavaScript 框架 |
| [TypeScript](https://www.typescriptlang.org/) | 类型安全的 JavaScript 超集 |
| [Vite](https://vitejs.dev/) | 极速前端构建工具 |
| [Vue Router](https://router.vuejs.org/) | SPA 页面路由 |
| [Pinia](https://pinia.vuejs.org/) | 轻量级状态管理 |
| [Axios](https://axios-http.com/) | HTTP 客户端（请求/响应拦截） |

### 后端

| 技术 | 用途 |
|------|------|
| [Flask](https://flask.palletsprojects.com/) | 轻量级 Python Web 框架 |
| [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/) | ORM 数据库操作 |
| [Flask-CORS](https://flask-cors.readthedocs.io/) | 跨域资源共享 |
| [Flask-Migrate](https://flask-migrate.readthedocs.io/) | 数据库迁移管理 |
| [PyMySQL](https://pymysql.readthedocs.io/) | MySQL 数据库驱动 |
| [PyJWT](https://pyjwt.readthedocs.io/) | JSON Web Token 认证 |
| [bcrypt](https://pypi.org/project/bcrypt/) | 密码哈希加密 |

---

## 📡 API 接口概览

### 认证相关 (`/api/auth`)

| 方法 | 路径 | 说明 | 认证 |
|------|------|------|------|
| POST | `/api/auth/register` | 用户注册 | 否 |
| POST | `/api/auth/login` | 用户登录 | 否 |
| GET | `/api/auth/me` | 获取当前用户信息 | 是 |

### 电影相关 (`/api/movies`)

| 方法 | 路径 | 说明 | 认证 |
|------|------|------|------|
| GET | `/api/movies` | 电影列表（分页/搜索/分类） | 是 |
| GET | `/api/movies/banners` | 获取 Banner 轮播图 | 是 |
| GET | `/api/movies/home` | 首页分类电影数据 | 是 |
| GET | `/api/movies/<id>` | 电影详情 + 推荐 + 收藏状态 | 是 |

### 评论相关 (`/api/movies/<id>/comments`)

| 方法 | 路径 | 说明 | 认证 |
|------|------|------|------|
| GET | `/api/movies/<id>/comments` | 获取电影评论 | 是 |
| POST | `/api/movies/<id>/comments` | 发表评论 | 是 |
| DELETE | `/api/comments/<id>` | 删除评论 | 是 |

### 收藏相关 (`/api/collects`)

| 方法 | 路径 | 说明 | 认证 |
|------|------|------|------|
| POST | `/api/collects/toggle/<movie_id>` | 切换收藏状态 | 是 |
| GET | `/api/collects` | 获取收藏列表（分页/分类） | 是 |
| DELETE | `/api/collects/<id>` | 取消收藏 | 是 |

### 用户相关 (`/api/users`)

| 方法 | 路径 | 说明 | 认证 |
|------|------|------|------|
| GET | `/api/users/<username>` | 用户主页信息 | 是 |
| GET | `/api/users/<username>/comments` | 用户的评论列表 | 是 |
| PUT | `/api/users/profile` | 修改个人资料 | 是 |
| PUT | `/api/users/password` | 修改密码 | 是 |
| POST | `/api/upload/avatar` | 上传头像 | 是 |

### 管理员接口 (`/api/admin`)

| 方法 | 路径 | 说明 | 认证 |
|------|------|------|------|
| GET | `/api/admin/stats` | 管理统计（用户/电影/评论数） | 管理员 |
| GET | `/api/admin/users` | 用户列表 | 管理员 |
| POST | `/api/admin/users/<id>/toggle_ban` | 封禁/解封用户 | 管理员 |
| GET | `/api/admin/movies` | 电影列表（管理用） | 管理员 |
| POST | `/api/admin/movies` | 新增电影 | 管理员 |
| PUT | `/api/admin/movies/<id>` | 编辑电影 | 管理员 |
| DELETE | `/api/admin/movies/<id>` | 删除电影 | 管理员 |
| GET | `/api/admin/comments` | 评论列表（管理用） | 管理员 |
| DELETE | `/api/admin/comments/<id>` | 删除评论（管理） | 管理员 |

---

## 🏗️ 构建部署

### 前端生产构建

```bash
npm run build
```

构建产物输出到 `dist/` 目录，可直接部署到 Nginx 等 Web 服务器。

### 后端生产部署

```bash
# 使用 Gunicorn 部署（Linux/macOS）
cd backend
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

---

## 📝 功能清单

- ✅ 用户注册/登录/登出（JWT 认证）
- ✅ BCrypt 密码加密存储
- ✅ 首页 Banner 轮播图
- ✅ 首页分类电梯导航（动作/科幻/动画/战争）
- ✅ 电影列表（搜索 + 分页 + 分类筛选）
- ✅ 电影详情（信息/海报/评论/推荐）
- ✅ 视频播放页
- ✅ 评论系统（发表/删除）
- ✅ 收藏功能（收藏/取消收藏）
- ✅ 个人主页（头像/资料/密码/收藏/评论）
- ✅ 后台管理面板（统计 + 用户管理 + 电影管理 + 评论管理）
- ✅ 文件上传（头像/海报/视频）
- ✅ 路由守卫（登录验证 + 管理员权限）
- ✅ 404 错误页面
- ✅ 响应式布局

---

## ⚙️ 环境变量说明

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `DATABASE_URL` | MySQL 数据库连接字符串 | `mysql+pymysql://root:mysql_2006@localhost:3306/cqupt_movie` |
| `SECRET_KEY` | Flask 应用密钥 | `dev-secret-key-change-in-production` |
| `JWT_SECRET_KEY` | JWT 签名密钥 | `jwt-secret-key-change-in-production` |
| `JWT_EXPIRATION_HOURS` | JWT 令牌过期时间（小时） | `24` |
| `UPLOAD_FOLDER` | 文件上传根目录 | `static` |
| `FLASK_RUN_HOST` | Flask 监听地址 | `0.0.0.0` |
| `FLASK_RUN_PORT` | Flask 监听端口 | `5000` |
| `FLASK_DEBUG` | 调试模式 | `True` |

---

## 📄 许可证

MIT License
