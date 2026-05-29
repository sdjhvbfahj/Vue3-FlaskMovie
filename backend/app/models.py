"""
数据库模型定义
定义应用的所有数据表结构，与 MySQL 数据库映射

表结构：
  - User: 用户表（用户名、密码、头像、简介、封禁状态）
  - Movie: 电影表（标题、简介、海报、分类、视频、Banner、热度）
  - Comment: 评论表（内容、时间、关联用户和电影）
  - Collect: 收藏表（关联用户和电影）
"""

from datetime import datetime, timezone, timedelta

from .extensions import db

# 北京时间时区
CHINA_TZ = timezone(timedelta(hours=8))


# ================== 用户表 ==================
class User(db.Model):
    """用户模型"""

    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False, comment="用户名")
    password = db.Column(db.String(255), nullable=False, comment="密码（bcrypt 加密）")
    bio = db.Column(db.String(255), default="这个人很懒，还没写简介...", comment="个人简介")
    avatar = db.Column(db.String(100), nullable=True, comment="头像文件名")
    is_banned = db.Column(db.Integer, default=0, comment="封禁状态：0=正常，1=封禁")
    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(CHINA_TZ),
        comment="创建时间",
    )

    def to_dict(self) -> dict:
        """转换为字典（不包含密码）"""
        return {
            "id": self.id,
            "username": self.username,
            "bio": self.bio or "",
            "avatar": self.avatar or "",
            "is_banned": self.is_banned,
            "created_at": (
                self.created_at.strftime("%Y-%m-%d %H:%M:%S")
                if self.created_at
                else ""
            ),
        }

    def __repr__(self) -> str:
        return f"<User {self.username}>"


# ================== 电影表 ==================
class Movie(db.Model):
    """电影模型"""

    __tablename__ = "movie"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False, comment="电影标题")
    info = db.Column(db.Text, nullable=True, comment="电影简介")
    poster = db.Column(db.String(255), nullable=True, comment="海报图片路径")
    category = db.Column(db.String(50), nullable=True, comment="电影分类")
    filename = db.Column(db.String(200), nullable=True, comment="视频文件名")
    is_banner = db.Column(db.Integer, default=0, comment="是否为 Banner: 0=否, 1=是")
    banner_order = db.Column(db.Integer, default=0, comment="Banner 排序（越小越靠前）")
    likes = db.Column(db.Integer, default=0, comment="收藏/点赞数量")
    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(CHINA_TZ),
        comment="创建时间",
    )

    # 关联评论（一对多）
    comments = db.relationship(
        "Comment", backref="movie", lazy="dynamic", cascade="all, delete-orphan"
    )

    # 关联收藏（一对多）
    collects = db.relationship(
        "Collect", backref="movie", lazy="dynamic", cascade="all, delete-orphan"
    )

    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            "id": self.id,
            "title": self.title,
            "info": self.info or "",
            "poster": self.poster or "",
            "category": self.category or "",
            "filename": self.filename or "",
            "is_banner": self.is_banner,
            "banner_order": self.banner_order,
            "likes": self.likes,
            "created_at": (
                self.created_at.strftime("%Y-%m-%d %H:%M:%S")
                if self.created_at
                else ""
            ),
        }

    def __repr__(self) -> str:
        return f"<Movie {self.title}>"


# ================== 评论表 ==================
class Comment(db.Model):
    """评论模型"""

    __tablename__ = "comment"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False, comment="评论内容")
    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(CHINA_TZ),
        comment="评论时间",
    )

    # 评论用户（关联用户名）
    user = db.Column(db.String(50), nullable=False, comment="评论用户名")

    # 所属电影（外键关联）
    movie_id = db.Column(
        db.Integer, db.ForeignKey("movie.id"), nullable=False, comment="所属电影 ID"
    )

    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            "id": self.id,
            "content": self.content,
            "user": self.user,
            "movie_id": self.movie_id,
            "movie_title": self.movie.title if self.movie else "",
            "created_at": (
                self.created_at.strftime("%Y-%m-%d %H:%M:%S")
                if self.created_at
                else ""
            ),
        }

    def __repr__(self) -> str:
        return f"<Comment {self.content[:10]}>"


# ================== 收藏表 ==================
class Collect(db.Model):
    """收藏模型"""

    __tablename__ = "collect"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user = db.Column(db.String(50), nullable=False, comment="收藏用户名")
    movie_id = db.Column(
        db.Integer, db.ForeignKey("movie.id"), nullable=False, comment="收藏的电影 ID"
    )
    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(CHINA_TZ),
        comment="收藏时间",
    )

    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            "id": self.id,
            "user": self.user,
            "movie_id": self.movie_id,
            "movie_title": self.movie.title if self.movie else "",
            "movie_poster": self.movie.poster if self.movie else "",
            "movie_category": self.movie.category if self.movie else "",
            "created_at": (
                self.created_at.strftime("%Y-%m-%d %H:%M:%S")
                if self.created_at
                else ""
            ),
        }

    def __repr__(self) -> str:
        return f"<Collect {self.user} - {self.movie_id}>"
