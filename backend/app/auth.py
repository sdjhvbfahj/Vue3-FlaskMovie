"""
认证工具模块
提供 JWT Token 生成与验证、密码加密与校验等功能

使用方式：
  - hash_password(plain) -> str: 加密密码
  - check_password(plain, hashed) -> bool: 验证密码
  - generate_token(user_id, username) -> str: 生成 JWT Token
  - verify_token(token) -> dict | None: 验证并解析 Token
"""

import jwt
import bcrypt
from datetime import datetime, timezone, timedelta
from functools import wraps
from typing import Optional

from flask import request, jsonify, current_app, g

# 北京时间时区
CHINA_TZ = timezone(timedelta(hours=8))


# ================== 密码工具 ==================

def hash_password(password: str) -> str:
    """
    对明文密码进行 bcrypt 加密

    Args:
        password: 明文密码

    Returns:
        加密后的密码字符串
    """
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")


def check_password(password: str, hashed: str) -> bool:
    """
    验证明文密码是否与加密密码匹配

    Args:
        password: 用户输入的明文密码
        hashed: 数据库中存储的加密密码

    Returns:
        匹配返回 True，否则返回 False
    """
    return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))


# ================== JWT Token 工具 ==================

def generate_token(user_id: int, username: str) -> str:
    """
    生成 JWT Token

    Args:
        user_id: 用户 ID
        username: 用户名

    Returns:
        JWT Token 字符串
    """
    expiration_hours = current_app.config.get("JWT_EXPIRATION_HOURS", 168)
    payload = {
        "user_id": user_id,
        "username": username,
        "exp": datetime.now(tz=CHINA_TZ) + timedelta(hours=expiration_hours),
        "iat": datetime.now(tz=CHINA_TZ),
    }
    secret = current_app.config["JWT_SECRET_KEY"]
    return jwt.encode(payload, secret, algorithm="HS256")


def verify_token(token: str) -> Optional[dict]:
    """
    验证并解析 JWT Token

    Args:
        token: JWT Token 字符串

    Returns:
        解析成功返回 payload 字典，失败返回 None
    """
    try:
        secret = current_app.config["JWT_SECRET_KEY"]
        payload = jwt.decode(token, secret, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return None  # Token 已过期
    except jwt.InvalidTokenError:
        return None  # Token 无效


# ================== 登录验证装饰器 ==================

def login_required(f):
    """
    登录验证装饰器

    用于保护需要用户登录的 API 接口。
    从请求头 Authorization 中提取 Bearer Token 并验证。
    验证通过后，将用户信息注入 Flask g 对象。

    使用方式：
      @login_required
      def some_api():
          current_user = g.current_user
          ...
    """

    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        # 从 Authorization 头获取 Token（格式: Bearer <token>）
        auth_header = request.headers.get("Authorization", "")
        if auth_header.startswith("Bearer "):
            token = auth_header[7:]

        if not token:
            return jsonify({"code": 401, "message": "请先登录"}), 401

        # 验证 Token
        payload = verify_token(token)
        if payload is None:
            return jsonify({"code": 401, "message": "登录已过期，请重新登录"}), 401

        # 将用户信息存入 g 对象，方便后续使用
        g.current_user_id = payload["user_id"]
        g.current_username = payload["username"]

        return f(*args, **kwargs)

    return decorated


def admin_required(f):
    """
    管理员权限验证装饰器

    在 login_required 基础上，额外验证用户是否为管理员（username == "admin"）

    使用方式：
      @admin_required
      def admin_api():
          ...
    """

    @wraps(f)
    @login_required
    def decorated(*args, **kwargs):
        if g.current_username != "admin":
            return jsonify({"code": 403, "message": "无权限访问"}), 403
        return f(*args, **kwargs)

    return decorated
