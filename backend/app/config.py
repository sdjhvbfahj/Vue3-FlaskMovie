"""
应用配置文件
从环境变量或 .env 文件中读取配置，提供合理的默认值
"""

import os
from dotenv import load_dotenv

# 加载 .env 文件中的环境变量
load_dotenv()

# 项目根目录
BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


class Config:
    """Flask 应用配置类"""

    # 数据库配置
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "mysql+pymysql://root:danyue050617@localhost:3306/movie_website"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 安全密钥
    SECRET_KEY = os.environ.get("SECRET_KEY", "danyue050617")
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "movie_website_jwt_secret_2025")

    # JWT Token 过期时间（7 天）
    JWT_EXPIRATION_HOURS = 168

    # 文件上传配置
    UPLOAD_FOLDER = os.environ.get("UPLOAD_FOLDER", os.path.join(BASE_DIR, "static/uploads"))
    AVATAR_FOLDER = os.environ.get("AVATAR_FOLDER", os.path.join(BASE_DIR, "static/avatars"))
    ALLOWED_EXTENSIONS = set(
        os.environ.get("ALLOWED_EXTENSIONS", "png,jpg,jpeg,gif,webp").split(",")
    )

    # 分页默认每页数量
    MOVIES_PER_PAGE = 28
    COMMENTS_PER_PAGE = 20
