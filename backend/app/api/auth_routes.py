"""
认证相关 API 路由
处理用户登录、注册、登出等操作
"""

from flask import request, jsonify, g

from .. import db
from ..models import User
from ..auth import hash_password, check_password, generate_token, login_required
from . import api_bp


@api_bp.route("/auth/register", methods=["POST"])
def register():
    """
    用户注册

    Request Body (JSON):
        username: str   - 用户名
        password: str   - 密码

    Response:
        { code: 200, message: "注册成功", data: { ... } }
        { code: 400, message: "错误信息" }
    """
    data = request.get_json()

    if not data:
        return jsonify({"code": 400, "message": "请提供注册信息"}), 400

    username = (data.get("username") or "").strip()
    password = (data.get("password") or "").strip()

    # 表单校验
    if not username or len(username) < 2:
        return jsonify({"code": 400, "message": "用户名至少需要 2 个字符"}), 400

    if not password or len(password) < 6:
        return jsonify({"code": 400, "message": "密码至少需要 6 个字符"}), 400

    # 检查用户名是否已存在
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({"code": 400, "message": "该用户名已被注册"}), 400

    # 创建用户
    user = User(
        username=username,
        password=hash_password(password),
    )
    db.session.add(user)
    db.session.commit()

    return jsonify({
        "code": 200,
        "message": "注册成功",
        "data": user.to_dict(),
    })


@api_bp.route("/auth/login", methods=["POST"])
def login():
    """
    用户登录

    Request Body (JSON):
        username: str   - 用户名
        password: str   - 密码

    Response:
        { code: 200, message: "登录成功", data: { user: { ... }, token: "..." } }
        { code: 400/403, message: "错误信息" }
    """
    data = request.get_json()

    if not data:
        return jsonify({"code": 400, "message": "请提供登录信息"}), 400

    username = (data.get("username") or "").strip()
    password = (data.get("password") or "").strip()

    if not username or not password:
        return jsonify({"code": 400, "message": "用户名和密码不能为空"}), 400

    # 查找用户
    user = User.query.filter_by(username=username).first()

    if not user:
        return jsonify({"code": 400, "message": "用户名或密码错误"}), 400

    # 检查是否被封禁
    if user.is_banned == 1:
        return jsonify({"code": 403, "message": "您的账号已被封禁，请联系管理员"}), 403

    # 验证密码
    if not check_password(password, user.password):
        return jsonify({"code": 400, "message": "用户名或密码错误"}), 400

    # 生成 Token
    token = generate_token(user.id, user.username)

    return jsonify({
        "code": 200,
        "message": "登录成功",
        "data": {
            "user": user.to_dict(),
            "token": token,
        },
    })


@api_bp.route("/auth/me", methods=["GET"])
@login_required
def get_current_user():
    """
    获取当前登录用户信息

    Headers:
        Authorization: Bearer <token>

    Response:
        { code: 200, data: { user: { ... } } }
    """
    user = User.query.filter_by(username=g.current_username).first()

    if not user or user.is_banned == 1:
        return jsonify({"code": 401, "message": "用户不存在或已被封禁"}), 401

    return jsonify({
        "code": 200,
        "data": user.to_dict(),
    })
