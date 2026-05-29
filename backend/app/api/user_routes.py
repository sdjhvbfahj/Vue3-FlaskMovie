"""
用户相关 API 路由
处理个人信息查看、编辑、密码修改等操作
"""

from flask import request, jsonify, g

from .. import db
from ..models import User, Comment, Collect, Movie
from ..auth import login_required, check_password, hash_password
from . import api_bp


@api_bp.route("/users/<username>", methods=["GET"])
def get_user_profile(username: str):
    """
    获取用户个人主页信息

    Path Parameters:
        username: str   - 用户名

    Response:
        { code: 200, data: { user: { ... }, comment_count: int, collect_count: int } }
    """
    user = User.query.filter_by(username=username).first()

    if not user:
        return jsonify({"code": 404, "message": "用户不存在"}), 404

    # 统计评论和收藏数量
    comment_count = Comment.query.filter_by(user=username).count()
    collect_count = Collect.query.filter_by(user=username).count()

    return jsonify({
        "code": 200,
        "data": {
            "user": user.to_dict(),
            "comment_count": comment_count,
            "collect_count": collect_count,
        },
    })


@api_bp.route("/users/<username>/comments", methods=["GET"])
def get_user_comments(username: str):
    """
    获取用户的评论列表

    Path Parameters:
        username: str   - 用户名

    Query Parameters:
        page: int        - 页码（默认 1）
        per_page: int    - 每页数量（默认 10）

    Response:
        { code: 200, data: { comments: [...], pagination: { ... } } }
    """
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)

    pagination = (
        Comment.query
        .filter_by(user=username)
        .order_by(Comment.created_at.desc(), Comment.id.desc())
        .paginate(page=page, per_page=per_page, error_out=False)
    )

    return jsonify({
        "code": 200,
        "data": {
            "comments": [c.to_dict() for c in pagination.items],
            "pagination": {
                "page": pagination.page,
                "per_page": pagination.per_page,
                "total": pagination.total,
                "pages": pagination.pages,
            },
        },
    })


@api_bp.route("/users/profile", methods=["PUT"])
@login_required
def update_profile():
    """
    更新个人简介

    Request Body (JSON):
        bio: str        - 个人简介

    Response:
        { code: 200, message: "修改成功", data: { ... } }
    """
    data = request.get_json()
    bio = (data.get("bio") or "").strip() if data else ""

    user = User.query.filter_by(username=g.current_username).first()
    if not user:
        return jsonify({"code": 404, "message": "用户不存在"}), 404

    user.bio = bio or "这个人很懒，还没写简介..."
    db.session.commit()

    return jsonify({
        "code": 200,
        "message": "修改成功",
        "data": user.to_dict(),
    })


@api_bp.route("/users/password", methods=["PUT"])
@login_required
def change_password():
    """
    修改密码

    Request Body (JSON):
        old_password: str       - 原密码
        new_password: str       - 新密码
        confirm_password: str   - 确认新密码

    Response:
        { code: 200, message: "密码修改成功" }
        { code: 400, message: "错误信息" }
    """
    data = request.get_json()
    if not data:
        return jsonify({"code": 400, "message": "请提供密码信息"}), 400

    old_password = (data.get("old_password") or "").strip()
    new_password = (data.get("new_password") or "").strip()
    confirm_password = (data.get("confirm_password") or "").strip()

    # 表单校验
    if not old_password:
        return jsonify({"code": 400, "message": "原密码不能为空"}), 400
    if not new_password:
        return jsonify({"code": 400, "message": "新密码不能为空"}), 400
    if not confirm_password:
        return jsonify({"code": 400, "message": "确认密码不能为空"}), 400
    if new_password != confirm_password:
        return jsonify({"code": 400, "message": "两次密码输入不一致"}), 400
    if len(new_password) < 6:
        return jsonify({"code": 400, "message": "新密码至少需要 6 个字符"}), 400

    user = User.query.filter_by(username=g.current_username).first()
    if not user:
        return jsonify({"code": 404, "message": "用户不存在"}), 404

    # 验证原密码
    if not check_password(old_password, user.password):
        return jsonify({"code": 400, "message": "原密码不正确"}), 400

    # 检查新旧密码是否相同
    if old_password == new_password:
        return jsonify({"code": 400, "message": "新密码不能与原密码相同"}), 400

    # 更新密码
    user.password = hash_password(new_password)
    db.session.commit()

    return jsonify({"code": 200, "message": "密码修改成功"})
